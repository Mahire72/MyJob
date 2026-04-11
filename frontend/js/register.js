/**
 * Fonction pour créer un compte
 * @param {string} email - L'email de l'utilisateur
 * @param {string} password - Le mot de passe de l'utilisateur
 */

function register() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!email || !password) {
    alert("Veuillez remplir l'email et le mot de passe.");
    return;
  }

  // TODO: Ajouter le nom de l'utilisateur
  // const nom = document.getElementById("nom").value;

  fetch("https://myjob.2in013projet.info/api/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
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
        const msg = (data && (data.detail || data.message)) || text || "Erreur lors de l'inscription.";
        throw new Error(msg);
      }
      return data;
    })
    .then((data) => {
      if (!data || !data.user || !data.user.id || !data.access_token) {
        alert("Erreur lors de l'inscription.");
        return;
      }
      localStorage.setItem("user_id", data.user.id);
      localStorage.setItem("email", email);
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("token_type", data.token_type || "bearer");
      alert("Compte créé avec succès !");
      window.location.href = "se_connecter.html";
    })
    .catch((err) => {
      console.error(err);
      alert(err && err.message ? err.message : "Impossible de contacter le serveur.");
    });
}

