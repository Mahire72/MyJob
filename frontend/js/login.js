/**
 * Fonction pour se connecter
 * @param {string} email - L'email de l'utilisateur
 * @param {string} password - Le mot de passe de l'utilisateur
 */
// Meme que register.js mais avec la route /login

function login() {
  console.log("login clicked");
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!email || !password) {
    alert("Veuillez remplir l'email et le mot de passe.");
    return;
  }

  fetch("https://myjob.2in013projet.info/api/login", {
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
        const msg =
          (data && (data.detail || data.message)) ||
          text ||
          "Erreur lors de la connexion.";
        throw new Error(msg);
      }
      return data;
    })
    .then((data) => {
      if (!data || !data.user || !data.user.id || !data.access_token) {
        alert("Email ou mot de passe incorrect !");
        return;
      }
      localStorage.setItem("user_id", data.user.id);
      localStorage.setItem("email", email);
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("token_type", data.token_type || "bearer");
      window.location.href = "dashboard.html";
    })
    .catch((err) => {
      console.error(err);
      alert(err && err.message ? err.message : "Impossible de contacter le serveur.");
    });
}
