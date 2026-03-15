Nous avons développé une application web de recherche d'emploi en utilisant l’API de France Travail API.


L’objectif du projet est de construire une application from scratch avec une stack technique simple et l’utilisation d’une API publique.

Architecture du projet
L’application est composée de trois parties principales :
1. Frontend
    Une interface web développée en HTML, CSS et JavaScript qui permet à l’utilisateur de rechercher des offres d’emploi.

2. Backend
    Un serveur développé avec FastAPI qui gère les requêtes et communique avec l’API France Travail.

3. API externe
    L’application utilise l’API de France Travail pour récupérer les données des offres d’emploi.


Fonctionnement de l'application
Le fonctionnement de l’application est le suivant :

    1. L’utilisateur saisit un métier (keyword) et éventuellement une ville dans le formulaire de recherche.

    2. Le frontend envoie une requête au backend via l’endpoint /jobs.

    3. Le backend récupère un token d’authentification auprès du serveur OAuth de France Travail.

    4. Le backend appelle l’API France Travail pour rechercher les offres correspondantes.

    5. Les résultats sont renvoyés au frontend sous forme de JSON.

    6. Les offres sont affichées sur la page sous forme de cartes (job cards).

Fonctionnalités implémentées
Nous avons implémenté les fonctionnalités suivantes :
    Recherche d'offres d'emploi par mot-clé (métier)
    Filtre par ville
    Affichage des résultats sous forme de cartes d’offres d’emploi
    Communication entre le frontend et le backend
    Utilisation d’un token OAuth pour accéder à l’API

Structure du projet
project
│
├── backend
│   ├── main.py
│   └── src
│       ├── token_manager.py
│       └── requete_api.py
│
└── frontend
    ├── index.html
    ├── stylesheet.css
    └── topnav.js

Flux de l'application
    Utilisateur
        ↓
    Frontend (HTML / JS)
        ↓
    Backend FastAPI
        ↓
    API France Travail
        ↓
    Résultats des offres d'emploi
        ↓
    Affichage sur la page web