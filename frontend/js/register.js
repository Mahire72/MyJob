/**
 * Fonction pour créer un compte
 * @param {string} email - L'email de l'utilisateur
 * @param {string} password - Le mot de passe de l'utilisateur
 */

function register() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  // TODO: Ajouter le nom de l'utilisateur
  // const nom = document.getElementById("nom").value;

  fetch("http://127.0.0.1:8000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (!data || !data.user || !data.user.id) {
        alert("Erreur lors de l'inscription.");
        return;
      }
      localStorage.setItem("user_id", data.user.id);
      localStorage.setItem("email", email);
      alert("Compte créé avec succès !");
      window.location.href = "se_connecter.html";
    })
    .catch((err) => {
      console.error(err);
      alert("Impossible de contacter le serveur.");
    });
}

