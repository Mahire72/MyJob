/*
Ce fichier contient les fonctions pour la page dashboard.
Il contient les fonctions pour afficher les offres d'emploi, les recommandations, etc.
Je vais pas trop ajouter de commentaires car chaque fonction est assez simple et claire. (je pense xd)
*/

// encore l'url de l'API -> je vais le mettre dans un fichier .env plus tard (cette fois je vais pas oublier)
const API_BASE = "http://127.0.0.1:8000";

const list = document.getElementById("jobList");
const detailsBody = document.getElementById("jobDetailsBody");
const welcomeNameEl = document.getElementById("welcomeName");

let _offres = [];

// Fonction pour récupérer l'id de l'utilisateur
// Necessaire pour les requêtes à l'API à partir du profil de l'utilisateur
function getUserId() {
  return localStorage.getItem("user_id");
}

//le petit "Bon retour, [nom] [prenom]"
function setWelcomeName(profile) {
  if (!welcomeNameEl) return;
  const nom = (profile && profile.nom ? String(profile.nom) : "").trim();
  const prenom = (profile && profile.prenom ? String(profile.prenom) : "").trim();
  const full = `${prenom} ${nom}`.trim();
  welcomeNameEl.textContent = full || "____";
}

function loadProfileForWelcome() {
  const userId = getUserId();
  if (!userId) return;
  fetch(`${API_BASE}/profile?user_id=${encodeURIComponent(userId)}`)
    .then((res) => res.json())
    .then((data) => {
      if (!data || !data.profile) return;
      setWelcomeName(data.profile);
    })
    .catch((err) => console.error(err));
}

function renderJobs(offres) {
  list.innerHTML = "";
  if (!Array.isArray(offres) || offres.length === 0) {
    const empty = document.createElement("div");
    empty.className = "job";
    empty.textContent = "Aucune offre trouvée.";
    list.appendChild(empty);
    return;
  }

  // On affiche les offres dans la liste
  //A modifier plus tard pour afficher les offres avec un design plus moderne et sexy, et plus d'infos :)
  offres.forEach((job, idx) => {
    const div = document.createElement("div");
    div.className = "job";

    const titre = job.titre || "Offre";
    const lieu = job.lieu ? ` - ${job.lieu}` : "";
    const entreprise = job.entreprise ? ` (${job.entreprise})` : "";

    div.textContent = `${titre}${entreprise}${lieu}`;
    div.addEventListener("click", () => renderDetails(idx));
    list.appendChild(div);
  });
}

function renderDetails(index) {
  if (!detailsBody) return;
  const job = _offres[index];
  if (!job) {
    detailsBody.innerHTML = "";
    return;
  }

  // Pour l'instant on affiche les info simplement, je stylise plus tard
  const rows = [
    ["Titre", job.titre],
    ["Entreprise", job.entreprise],
    ["Lieu", job.lieu],
    ["Code postal", job.code_postal],
    ["Type contrat", job.type_contrat],
    ["Salaire", job.salaire],
    ["Créé le", job.date_creation],
    ["Mis à jour", job.date_actualisation],
    ["URL", job.url],
    ["Description", job.description],
  ];

  detailsBody.innerHTML = rows
    .filter(([, v]) => v !== null && v !== undefined && String(v).trim() !== "")
    .map(([k, v]) => {
      if (k === "URL") {
        const safe = String(v);
        return `<div><strong>${k}:</strong> <a href="${safe}" target="_blank" rel="noreferrer">${safe}</a></div>`;
      }
      return `<div><strong>${k}:</strong> ${String(v)}</div>`;
    })
    .join("");
}


// Cette fonction est appelée lorsque l'utilisateur charge la page dashboard
// Elle récupère les offres recommandées pour l'utilisateur
//et les affiches
function loadRecommended() {
  const userId = getUserId();
  if (!userId) {
    renderJobs([]);
    return;
  }

  fetch(`${API_BASE}/jobs/recommended?user_id=${encodeURIComponent(userId)}`)
    .then((res) => res.json())
    .then((data) => {
      const offres = data && data.offres ? data.offres : [];
      _offres = offres;
      renderJobs(offres);
      renderDetails(0);
    })
    .catch((err) => {
      console.error(err);
      renderJobs([]);
    });
}

loadProfileForWelcome();
loadRecommended();


function goToProfile(){
    window.location.href = "profile.html"
}