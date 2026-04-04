// se_connecter
function login()
{
        console.log("login clicked");
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        // pour obtenir les saved data
        const savedEmail = localStorage.getItem("email");
        const savedPassword = localStorage.getItem("password");

        if (email === savedEmail && password === savedPassword)
        {
            window.location.href = "dashboard.html";
        }
        else 
        {
            alert("Email ou mot de passe incorrect !");
        }
}
