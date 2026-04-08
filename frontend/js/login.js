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

  fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (!data || !data.user || !data.user.id) {
        alert("Email ou mot de passe incorrect !");
        return;
      }
      localStorage.setItem("user_id", data.user.id);
      localStorage.setItem("email", email);
      window.location.href = "dashboard.html";
    })
    .catch((err) => {
      console.error(err);
      alert("Impossible de contacter le serveur.");
    });
}
