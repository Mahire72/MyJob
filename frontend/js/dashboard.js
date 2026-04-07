const jobs = [
    {
        title: "Développeur Web",
        city: "Paris",
        lat: 48.8566,
        lon: 2.3522,
        desc: "Créer des sites web et applications"
    },
    {
        title: "Designer UI/UX",
        city: "Lyon",
        lat: 45.7640,
        lon: 4.8357,
        desc: "Concevoir des interfaces utilisateur"
    },
    {
        title: "Data Analyst",
        city: "Marseille",
        lat: 43.2965,
        lon: 5.3698,
        desc: "Analyser les données pour les entreprises"
    }
];


// obtenir l'element de la liste
const list = document.getElementById("jobList");


//
jobs.forEach(job => {

    const div = document.createElement("div");
    div.className = "job";
    div.textContent = job.title + " - " + job.city;

    list.appendChild(div);

    // creer map marker
    const marker = L.marker([job.lat, job.lon]).addTo(map);

    marker.bindPopup(`
        <b>${job.title}</b><br>
        📍 ${job.city}<br>
        ${job.desc}
    `);

    // click gauche, ouvrir description + move map
    div.onclick = () => {
        map.setView([job.lat, job.lon], 10);
        marker.openPopup();
    };

});

function goToProfile(){
    window.location.href = "profile.html"
}