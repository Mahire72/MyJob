/*
Ce fichier contient les fonctions pour la page dashboard.
Il contient les fonctions pour afficher les offres d'emploi, les recommandations, etc.
Je vais pas trop ajouter de commentaires car chaque fonction est assez simple et claire. (je pense xd)
*/

const API_BASE = "https://myjob.2in013projet.info/api";

const list = document.getElementById("jobList");
const detailsBody = document.getElementById("jobDetailsBody");
const welcomeNameEl = document.getElementById("welcomeName");
const jobDetailsTitle = document.getElementById("jobDetailsTitle");
const jobDetailsHint = document.getElementById("jobDetailsHint");

let _offres = [];

// Fonction pour récupérer l'id de l'utilisateur
// Necessaire pour les requêtes à l'API à partir du profil de l'utilisateur
function getUserId() {
  return localStorage.getItem("user_id");
}

function getAccessToken() {
  return localStorage.getItem("access_token");
}

function ensureConnected() {
  const token = getAccessToken();
  if (!token) {
    window.location.href = "se_connecter.html";
    return false;
  }
  return true;
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
  if (!ensureConnected()) return;
  const token = getAccessToken();
  fetch(`${API_BASE}/profile`, {
    headers: { Authorization: `Bearer ${token}` },
  })
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
    if (jobDetailsTitle) jobDetailsTitle.style.display = "";
    if (jobDetailsHint) jobDetailsHint.style.display = "";
    return;
  }

  if (jobDetailsTitle) jobDetailsTitle.style.display = "none";
  if (jobDetailsHint) jobDetailsHint.style.display = "none";
  // on affiche les détails de l'offre
  //v2 avec un meilleur design
  const titre = job.titre || "Offre";
  const entreprise = job.entreprise || "";
  const lieu = job.lieu || "";
  const codePostal = job.code_postal || "";
  const typeContrat = job.type_contrat || "";
  const salaire = job.salaire || "";
  const dateCreation = job.date_creation || "";
  const dateMaj = job.date_actualisation || "";
  const url = job.url || "";
  const description = job.description || "";

  const chips = [
    typeContrat && { label: typeContrat },
    salaire && { label: salaire },
    (lieu || codePostal) && { label: [lieu, codePostal].filter(Boolean).join(" • ") },
  ].filter(Boolean);

  detailsBody.innerHTML = `
    <div class="job-detail">
      <div class="job-detail-title">${escapeHtml(titre)}</div>
      ${entreprise ? `<div class="job-detail-company">${escapeHtml(entreprise)}</div>` : ""}

      ${chips.length ? `
        <div class="job-detail-chips">
          ${chips.map(c => `<span class="chip">${escapeHtml(c.label)}</span>`).join("")}
        </div>
      ` : ""}

      ${url ? `
        <div class="job-detail-actions">
          <a class="btn-link" href="${escapeAttr(url)}" target="_blank" rel="noreferrer">Voir l'offre</a>
        </div>
      ` : ""}

      ${(dateCreation || dateMaj) ? `
        <div class="job-detail-meta">
          ${dateCreation ? `<div><strong>Créé le</strong> ${escapeHtml(dateCreation)}</div>` : ""}
          ${dateMaj ? `<div><strong>Mis à jour</strong> ${escapeHtml(dateMaj)}</div>` : ""}
        </div>
      ` : ""}

      ${description ? `
        <div class="job-detail-section">
          <div class="job-detail-section-title">Description</div>
          <div class="job-detail-description">${escapeHtml(description)}</div>
        </div>
      ` : ""}
    </div>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
  // href -> pour les liens
  return escapeHtml(value);
}


// Cette fonction est appelée lorsque l'utilisateur charge la page dashboard
// Elle récupère les offres recommandées pour l'utilisateur
//et les affiches
function loadRecommended() {
  if (!ensureConnected()) return;
  const token = getAccessToken();
  fetch(`${API_BASE}/jobs/recommended`, {
    headers: { Authorization: `Bearer ${token}` },
  })
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

function logout() {
  localStorage.removeItem("user_id");
  localStorage.removeItem("email");
  localStorage.removeItem("access_token");
  localStorage.removeItem("token_type");
  window.location.href = "se_connecter.html";
}