# Calen.IO

Calen.IO est une application web innovante conçue pour gérer efficacement vos événements et rendez-vous. 📅 Elle offre une interface utilisateur intuitive et des fonctionnalités avancées pour améliorer votre productivité. 🚀

## Table des matières 📚

- [Aperçu](#aperçu) 👀
- [Fonctionnalités](#fonctionnalités) ✨
- [Installation](#installation) 🛠️
- [Configuration](#configuration) ⚙️
- [Utilisation](#utilisation) 📖
- [Structure du projet](#structure-du-projet) 🗂️
- [Technologies utilisées](#technologies-utilisées) 💻
- [Contribuer](#contribuer) 🤝
- [Licence](#licence) 📜

## Aperçu

Calen.IO est conçu pour simplifier la gestion de votre emploi du temps. Avec une interface moderne et des outils puissants, il vous permet de suivre vos évènements et vos tâches, de planifier des rendez-vous. 🔔

## Fonctionnalités

- Gestion des événements et des tâches 📋
- Création et modification facile des événements ✏️
- Vue calendrier mensuelle, hebdomadaire et quotidienne 📆
- Interface utilisateur moderne et réactive 💡

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/calen-io.git
   cd calen-io
   ```

2. Installez les dépendances pour le front-end :

   ```bash
   cd front
   npm install
   ```

3. Installez les dépendances pour le back-end :
   ```bash
   cd ../back
   pip install -r requirements.txt
   ```

## Utilisation

1. Démarrez le serveur back-end :

   ```bash
   cd back/backend
   python manage.py runserver
   ```

2. Démarrez le serveur front-end :

   ```bash
   cd front
   npm run dev
   ```

3. Ouvrez votre navigateur et accédez à l'application à l'adresse indiquée par le serveur de développement. 🌐

## Structure du projet 🗂️

Voici une structure détaillée du projet :

```
calen-io/
│
├── front/                          # Code source du front-end
│   ├── src/                        # Fichiers source Vue.js
│   │   ├── assets/                 # Fichiers d'assets (images, styles)
│   │   ├── components/             # Composants Vue.js
│   │   ├── views/                  # Vues de l'application
│   │   ├── router/                 # Configuration du routeur
│   │   │   └── index.js            # Fichier de configuration des routes
│   │   ├── store/                  # Gestion de l'état (Vuex)
│   │   │   └── index.js            # Fichier de configuration du store
│   │   ├── App.vue                 # Composant racine
│   │   └── main.js                 # Point d'entrée de l'application
│   │
│   ├── public/                     # Fichiers statiques
│   │   ├── index.html              # Fichier HTML principal
│   │   └── favicon.ico             # Icône du site
│   │
│   ├── package.json                # Fichier de configuration npm
│   ├── tailwind.config.js          # Configuration de Tailwind CSS
│   └── vue.config.js               # Configuration de Vue.js
│
├── back/                           # Code source du back-end
│   ├── backend/                    # Application Django
│   │   ├── settings.py             # Configuration de l'application
│   │   ├── urls.py                 # Configuration des routes
│   │   ├── wsgi.py                 # Point d'entrée WSGI
│   │   ├── asgi.py                 # Point d'entrée ASGI
│   │   ├── manage.py               # Script de gestion de Django
│   │   └── apps/                   # Applications Django spécifiques
│   │       ├── events/             # Application pour la gestion des événements
│   │       │   ├── migrations/     # Fichiers de migration
│   │       │   ├── models.py       # Modèles de données
│   │       │   ├── views.py        # Logique de vue
│   │       │   ├── serializers.py  # Sérialiseurs pour l'API
│   │       │   ├── urls.py         # Routes spécifiques à l'application
│   │       │   └── tests.py        # Tests unitaires
│   │       └── users/              # Application pour la gestion des utilisateurs
│   │           ├── migrations/     # Fichiers de migration
│   │           ├── models.py       # Modèles de données
│   │           ├── views.py        # Logique de vue
│   │           ├── serializers.py  # Sérialiseurs pour l'API
│   │           ├── urls.py         # Routes spécifiques à l'application
│   │           └── tests.py        # Tests unitaires
│   │
│   ├── migrations/                 # Fichiers de migration de la base de données
│   └── requirements.txt            # Dépendances Python
│
└── README.md                       # Documentation du projet
```

Cette section fournit une vue d'ensemble complète de la structure du projet, ce qui peut être très utile pour les nouveaux contributeurs ou pour la documentation interne. Assurez-vous d'adapter cette structure si votre projet a des particularités spécifiques.

## Technologies utilisées

- **HTML/CSS/JavaScript** : Technologies de base pour le développement web. 🌐
- **Vue.js** : Framework JavaScript pour construire l'interface utilisateur. 🖥️
- **Tailwind CSS** : Framework CSS pour styliser l'application de manière moderne et réactive. 🎨
- **FullCalendar JS** : Bibliothèque JavaScript pour afficher des calendriers interactifs. 📅
- **Python/Django** : Utilisé pour le back-end. 🐍
- **PostgreSQL** : Base de données pour stocker les données des utilisateurs. 🗄️

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter. 🙌

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails. 📄
