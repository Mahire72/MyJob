document.addEventListener("DOMContentLoaded", init);

function init() {
    const form = document.getElementById("profileForm");
    form.addEventListener("submit", handleSubmit);
}

function handleSubmit(e) {
    e.preventDefault();

    const data = getFormData();

    console.log(data);

    alert("Profil envoyé avec succès !");
}

function getFormData() {
    return {
        nom: document.getElementById("nom").value,
        prenom: document.getElementById("prenom").value,
        email: document.getElementById("email").value,
        ville: document.getElementById("ville").value,
        salaire: document.getElementById("salaire").value,
        contrat: document.getElementById("contrat").value,
        competences: document.getElementById("Competences").value
    };
}