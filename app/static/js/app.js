const form = document.getElementById("cvForm");
const submitBtn = document.getElementById("submitBtn");
const resetBtn = document.getElementById("resetBtn");

const fileInput = document.getElementById("cvFile");
const dropzone = document.getElementById("dropzone");
const dzFileName = document.getElementById("dzFileName");
const loadingText = document.getElementById("loadingText");

const scoreNum = document.getElementById("scoreNum");
const scoreBar = document.getElementById("scoreBar");
const skillsDetectadas = document.getElementById("skillsDetectadas");
const skillsFaltantes = document.getElementById("skillsFaltantes");
const recomendaciones = document.getElementById("recomendaciones");
const errorMsg = document.getElementById("errorMsg");

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

        scoreNum.textContent = `${data.score}%`;

        scoreBar.className = "meter-fill";

        if (data.score < 40) {
            scoreBar.classList.add("score-low");
        } else if (data.score < 70) {
            scoreBar.classList.add("score-medium");
        } else {
            scoreBar.classList.add("score-high");
        }

        renderChips(skillsDetectadas, data.skills_detectadas, "detected");
        renderChips(skillsFaltantes, data.skills_faltantes, "missing");

        recomendaciones.innerHTML =
            data.recomendaciones.map(item => `<li>${item}</li>`).join("");

        showState("result");

        requestAnimationFrame(() => {
            scoreBar.style.width = `${data.score}%`;
        });

    } catch (error) {
        errorMsg.textContent = error.message;
        showState("error");
    } finally {
        clearInterval(msgInterval);
        submitBtn.disabled = false;
        submitBtn.textContent = "Generar análisis";
    }
});

resetBtn.addEventListener("click", () => {
    form.reset();

    dropzone.classList.remove("has-file", "drag-over");
    dzFileName.textContent = "Seleccionar o arrastrar archivo";

    showState("empty");

    scoreNum.textContent = "0%";
    scoreBar.className = "meter-fill";
    scoreBar.style.width = "0%";

    skillsDetectadas.innerHTML = "";
    skillsFaltantes.innerHTML = "";
    recomendaciones.innerHTML = "";
    errorMsg.textContent = "";
});