const form = document.getElementById("cvForm");
const submitBtn = document.getElementById("submitBtn");
const fileInput = document.getElementById("cvFile");
const dropzone = document.getElementById("dropzone");
const dzFileName = document.getElementById("dzFileName");
const loadingText = document.getElementById("loadingText");

const states = {
    empty: document.getElementById("stateEmpty"),
    loading: document.getElementById("stateLoading"),
    result: document.getElementById("stateResult"),
    error: document.getElementById("stateError"),
};

function showState(name) {
    Object.values(states).forEach(el => el.classList.remove("active"));
    states[name].classList.add("active");
}

function setFile(file) {
    if (!file) return;
    if (file.type !== "application/pdf") {
        dzFileName.textContent = "Solo se aceptan archivos PDF";
        dropzone.classList.remove("has-file");
        return;
    }
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    dzFileName.textContent = file.name;
    dropzone.classList.add("has-file");
}

fileInput.addEventListener("change", () => {
    setFile(fileInput.files[0]);
});

// El label nativo ya abre el selector de archivos; aquí solo se maneja drag & drop
["dragenter", "dragover"].forEach(evt =>
    dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.add("drag-over");
    })
);

["dragleave", "drop"].forEach(evt =>
    dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.remove("drag-over");
    })
);

dropzone.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files[0];
    setFile(file);
});

function renderChips(container, items, type) {
    container.innerHTML = items.length
        ? items.map(s => `<span class="chip ${type}">${s}</span>`).join("")
        : `<span class="chip ${type}">Sin coincidencias</span>`;
}

const loadingMessages = [
    "Procesando currículum…",
    "Comparando contra la vacante…",
    "Construyendo el dictamen…"
];

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    const jobDescription = document.getElementById("jobDescription").value;

    if (!file) {
        dzFileName.textContent = "Selecciona un archivo PDF";
        return;
    }

    const formData = new FormData();
    formData.append("cv_file", file);
    formData.append("job_description", jobDescription);

    submitBtn.disabled = true;
    submitBtn.textContent = "Analizando…";
    showState("loading");

    let msgIndex = 0;
    const msgInterval = setInterval(() => {
        msgIndex = (msgIndex + 1) % loadingMessages.length;
        loadingText.textContent = loadingMessages[msgIndex];
    }, 1400);

    try {
        const response = await fetch("/api/cv/analyze-pdf", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Error al analizar el CV");
        }

        document.getElementById("scoreNum").textContent = `${data.score}%`;
        renderChips(document.getElementById("skillsDetectadas"), data.skills_detectadas, "detected");
        renderChips(document.getElementById("skillsFaltantes"), data.skills_faltantes, "missing");
        document.getElementById("recomendaciones").innerHTML =
            data.recomendaciones.map(item => `<li>${item}</li>`).join("");

        showState("result");
        requestAnimationFrame(() => {
            document.getElementById("scoreBar").style.width = `${data.score}%`;
        });

    } catch (error) {
        document.getElementById("errorMsg").textContent = error.message;
        showState("error");
    } finally {
        clearInterval(msgInterval);
        submitBtn.disabled = false;
        submitBtn.textContent = "Generar análisis";
    }
});