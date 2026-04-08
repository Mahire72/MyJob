/*
Ce fichier contient les fonctions pour la page dashboard.
Il contient les fonctions pour afficher les offres d'emploi, les recommandations, etc.
*/

const API_BASE = "http://127.0.0.1:8000";

const list = document.getElementById("jobList");

function renderJobs(offres) {
  list.innerHTML = "";
  if (!Array.isArray(offres) || offres.length === 0) {
    const empty = document.createElement("div");
    empty.className = "job";
    empty.textContent = "Aucune offre trouvée.";
    list.appendChild(empty);
    return;
  }

  offres.forEach((job) => {
    const div = document.createElement("div");
    div.className = "job";

    const titre = job.titre || "Offre";
    const lieu = job.lieu ? ` - ${job.lieu}` : "";
    const entreprise = job.entreprise ? ` (${job.entreprise})` : "";

    div.textContent = `${titre}${entreprise}${lieu}`;
    list.appendChild(div);
  });
}

function loadRecommended() {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    renderJobs([]);
    return;
  }

  fetch(`${API_BASE}/jobs/recommended?user_id=${encodeURIComponent(userId)}`)
    .then((res) => res.json())
    .then((data) => {
      const offres = data && data.offres ? data.offres : [];
      renderJobs(offres);
    })
    .catch((err) => {
      console.error(err);
      renderJobs([]);
    });
}

loadRecommended();


function goToProfile(){
    window.location.href = "profile.html"
}