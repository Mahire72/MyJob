/**
 * Fonction pour initialiser le profile
 * @param {string} email - L'email de l'utilisateur
 * @param {string} password - Le mot de passe de l'utilisateur
 * @param {string} nom - Le nom de l'utilisateur
 * @param {string} prenom - Le prénom de l'utilisateur
 * @param {string} code_postal - Le code postal de l'utilisateur
 * @param {string} distance_max - La distance maximale de l'utilisateur
 * @param {string} salaire_min - Le salaire minimum de l'utilisateur
 * @param {string} type_contrat - Le type de contrat de l'utilisateur
 * @param {string} mots_cles - Les mots-clés de l'utilisateur
 */

document.addEventListener("DOMContentLoaded", init);

// a ajouter dans env si joublie pas lol
const API_BASE = "http://127.0.0.1:8000";

// Fonction pour initialiser le profile
function init() {
  const form = document.getElementById("profileForm");
  form.addEventListener("submit", handleSubmit);

  const updateBtn = document.getElementById("updateBtn");
  if (updateBtn) {
    updateBtn.addEventListener("click", () => form.requestSubmit());
  }

  const email = localStorage.getItem("email");
  if (email) document.getElementById("email").value = email;

  loadProfile();
}

// Fonction pour récupérer l'ID de l'utilisateur
function getUserId() {
  return localStorage.getItem("user_id");
}

// Fonction pour charger le profile
function loadProfile() {
  const userId = getUserId();
  if (!userId) return;
  // On récupère le profile du serveur
  fetch(`${API_BASE}/profile?user_id=${encodeURIComponent(userId)}`)
    .then((res) => res.json())
    .then((data) => {
      if (!data || !data.profile) return;
      applyProfileToForm(data.profile);
    })
    .catch((err) => console.error(err));
}

// Fonction pour appliquer le profile au formulaire
function applyProfileToForm(profile) {
  if (profile.mots_cles != null) document.getElementById("Competences").value = profile.mots_cles;
  if (profile.code_postal != null) document.getElementById("code_postal").value = profile.code_postal;
  if (profile.type_contrat != null) document.getElementById("contrat").value = profile.type_contrat;
  if (profile.distance_max != null) document.getElementById("distance_max").value = profile.distance_max;
  if (profile.salaire_min != null) document.getElementById("salaire_min").value = profile.salaire_min;
}

// Fonction pour gérer le submit du formulaire
function handleSubmit(e) {
  e.preventDefault();
   // On récupère l'ID de l'utilisateur
  const userId = getUserId();
  if (!userId) {
    alert("Vous devez être connecté (user_id manquant).");
    return;
  }
  // On récupère le payload du profile
  const payload = getProfilePayload();
  if (!payload.mots_cles || !payload.code_postal) {
    alert("Veuillez renseigner au minimum mots-clés et code postal.");
    return;
  }

  // On envoie le payload au serveur
  fetch(`${API_BASE}/profile?user_id=${encodeURIComponent(userId)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then(async (res) => {
      const text = await res.text();
      let data = null;
      try {
        data = text ? JSON.parse(text) : null;
      } catch {
        data = null;
      }
      if (!res.ok) {
        const msg = (data && (data.detail || data.message)) || text || "Erreur lors de l'enregistrement du profil.";
        throw new Error(msg);
      }
      return data;
    })
    .then(() => {
      alert("Profil mis à jour !");
    })
    .catch((err) => {
      console.error(err);
      alert(err && err.message ? err.message : "Impossible de contacter le serveur.");
    });
}

// Fonction pour récupérer le payload du profile
// Le payload est l'objet JSON que l'on envoie au serveur
// On récupère les valeurs des champs du formulaire
// On les transforme en objet JSON
// On retourne l'objet JSON
function getProfilePayload() {
  const mots_cles = (document.getElementById("Competences").value || "").trim();
  const code_postal = (document.getElementById("code_postal").value || "").trim();
  const type_contrat = document.getElementById("contrat").value || null;

  const distanceRaw = document.getElementById("distance_max").value;
  const salaireRaw = document.getElementById("salaire_min").value;

  const distance_max = distanceRaw === "" ? null : Number(distanceRaw);
  const salaire_min = salaireRaw === "" ? null : Number(salaireRaw);

  return { mots_cles, code_postal, type_contrat, distance_max, salaire_min };
}