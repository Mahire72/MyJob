function topNav(){
    var x = document.getElementById("Topnav");
    if(x.className == "topnav"){
        x.className +=" responsive";
    } else {
        x.className = "topnav";
    }
}

// creer_compte
function register() {
    const nom = document.getElementById("nom").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (nom === "" || email === "" || password === "") {
        alert("Tous les champs sont obligatoires !");
    } else {
        localStorage.setItem("email", email);
        localStorage.setItem("password", password);
        
        alert("Compte créé !");
        window.location.href = "se_connecter.html";
    }
}

//dashboard
function searchJobs() {

    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "";
    map.eachLayer(layer => {
        if (layer instanceof L.Marker) map.removeLayer(layer);
    });

    //pour l'insatnt 
    const jobs = [
        { title: "Développeur", city: "Paris", lat: 48.8566, lon: 2.3522 },
        { title: "Data Analyst", city: "Lyon", lat: 45.7640, lon: 4.8357 },
        { title: "Designer", city: "Marseille", lat: 43.2965, lon: 5.3698 }
    ];

    jobs.forEach(job => {
        resultsDiv.innerHTML += `
            <div class="card">
                💼 ${job.title}<br>
                📍 ${job.city}
            </div>
        `;
        L.marker([job.lat, job.lon])
            .addTo(map)
            .bindPopup(`${job.title} - ${job.city}`);
    });
}
