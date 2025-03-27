# Explorateur de Fichiers

**Explorateur de Fichiers** est une application graphique développée en Python utilisant `customtkinter`. Cette application permet aux utilisateurs de naviguer, gérer et manipuler leurs fichiers et répertoires via une interface conviviale. Elle inclut des fonctionnalités pour copier, déplacer, renommer, supprimer, et gérer des favoris ainsi que l'historique de navigation.

## Fonctionnalités principales

- **Navigation des fichiers** : Exploration de l'arborescence des répertoires et affichage des fichiers et dossiers dans un `Treeview` interactif.
- **Gestion des favoris** : Ajouter des répertoires aux favoris pour y accéder rapidement.
- **Historique de navigation** : Permet de revenir à un répertoire précédemment visité via la barre d'adresse.
- **Opérations CRUD** :
  - Créer un fichier ou un dossier.
  - Supprimer un fichier ou un dossier.
  - Renommer un fichier ou un dossier.
  - Copier et déplacer des fichiers et des répertoires.
- **Gestion des Permissions et des Erreurs** : Capturer les erreurs liées aux permissions d'accès et afficher des messages d'erreur explicites via des boîtes de dialogue centrées sur l'écran.  
  - En cas d'accès refusé, l'utilisateur peut être invité à réessayer l'opération.
- **Menus contextuels** : Menus contextuels accessibles par clic droit pour effectuer diverses actions sur les fichiers.
- **Affichage fluide** : Gestion de l'affichage des répertoires et des fichiers avec une barre de défilement pour une navigation fluide, même avec un grand nombre d'éléments.
- **Nettoyage des noms** : Retrait des emojis indésirables (comme "📁" et "📄") et des espaces superflus lors de la récupération des noms de fichiers.

## Structure des modules

L'application est divisée en plusieurs modules :

| Module                    | Rôle |
|---------------------------|------|
| `favoris.py`              | Gère les favoris et l'historique de navigation. |
| `operations_fichiers.py`  | Contient les fonctions pour créer, supprimer, renommer, copier et déplacer les fichiers. |
| `affichage_fichiers.py`   | Affiche le contenu des répertoires dans un `Treeview` et gère l'affichage des fichiers/dossiers. |
| `barre_chemin.py`         | Gère la barre d'adresse de navigation et l'historique des répertoires visités. |
| `menus_contextuels.py`    | Crée des menus contextuels pour effectuer des actions sur les fichiers via clic droit. |

## Fonctionnalités détaillées

### 1. Gestion des Favoris (`favoris.py`)

- **`ajouter_favori(chemin)`**  
  - **Rôle** : Ajoute un répertoire aux favoris.
  - **Défi** : Éviter les doublons.
  - **Solution** : Utilisation d'un `set` pour garantir l'unicité (persistance à envisager via JSON ou une base de données).

- **`parcours(direction)`**  
  - **Rôle** : Naviguer dans l'historique des répertoires visités.
  - **Défi** : Gestion des dépassements d'index.
  - **Solution** : Validation de l'index avant la navigation.

### 2. Opérations CRUD (`operations_fichiers.py`)

- **`creer_fichier(dir)`**  
  - **Rôle** : Créer un fichier dans un répertoire spécifié.
  - **Défi** : Gérer les erreurs (accès refusé, nom invalide).
  - **Solution** : Capture des exceptions (`OSError`) avec gestion de l'accès refusé et possibilité de réessayer.

- **`creer_dossier(dir)`**  
  - **Rôle** : Créer un dossier dans un répertoire donné.
  - **Défi** : Problèmes de permissions et d'existence du dossier.
  - **Solution** : Utilisation de `os.makedirs()` avec gestion appropriée des erreurs.

- **`coller_element()`**  
  - **Rôle** : Coller un fichier ou un dossier copié/coupé dans une destination.
  - **Défi** : Gérer les erreurs liées aux permissions et aux destinations invalides.
  - **Solution** : Vérification de la destination et affichage de messages d'erreur clairs avec réessai possible.

- **`supprimer_element(nom, dir)`**  
  - **Rôle** : Supprimer un fichier ou un dossier après confirmation.
  - **Défi** : Prévenir la perte de données et gérer les erreurs de suppression.
  - **Solution** : Demande de confirmation et capture des erreurs lors de la suppression.

- **`renommer_element(nom, dir)`**  
  - **Rôle** : Renommer un fichier ou un dossier.
  - **Défi** : Assurer que le nouveau nom est valide et gérer les erreurs de permission.
  - **Solution** : Capture des exceptions avec messages explicites et possibilité de réessayer.

### 3. Affichage des Fichiers (`affichage_fichiers.py`)

- **`afficher_contenu()`**  
  - **Rôle** : Afficher le contenu d'un répertoire dans un `Treeview` avec informations (type, taille, date de création).
  - **Défi** : Gérer l'affichage des répertoires volumineux sans ralentir l'application.
  - **Solution** : Limiter l'affichage et utiliser une barre de défilement.

- **`trier_par_colonne(colonne)`**  
  - **Rôle** : Trier les fichiers affichés par nom, taille ou date de création.
  - **Défi** : Trier correctement des données non numériques.
  - **Solution** : Utiliser des fonctions de tri personnalisées pour une conversion correcte des données.

- **Nettoyage des noms**  
  - Retrait des emojis "📁" et "📄" et des espaces superflus pour éviter les erreurs lors de la manipulation des chemins et des noms de fichiers.

### 4. Barre de Navigation (`barre_chemin.py`)

- **`valider_chemin()`**  
  - **Rôle** : Valider le chemin d'un répertoire saisi par l'utilisateur.
  - **Défi** : Empêcher la saisie de chemins invalides.
  - **Solution** : Vérification avec `os.path.exists()` avant affichage.

### 5. Menus Contextuels (`menus_contextuels.py`)

- **`ouvrir()`**  
  - **Rôle** : Ouvrir un fichier ou un dossier en fonction de son type.
  - **Défi** : Gérer l'ouverture sécurisée d'exécutables ou de fichiers spéciaux.
  - **Solution** : Utilisation de `subprocess.Popen` pour une ouverture sécurisée.

### 6. Gestion des erreurs et permissions

- **Boîtes de dialogue centrées** :  
  Les boîtes de dialogue (erreur, information, confirmation) apparaissent au centre de l'écran pour une meilleure visibilité, grâce à une fonction de centrage.
- **Réessai en cas d'accès refusé** :  
  Pour les opérations sensibles, si une erreur de type "accès refusé" survient, l'utilisateur est invité à réessayer. En cas d'échec à nouveau, un message d'erreur définitif est affiché et l'opération est abandonnée.

## Défis rencontrés et solutions apportées

| Problème                                | Solution |
|-----------------------------------------|----------|
| **Problèmes de performance avec des répertoires volumineux** | Limiter l'affichage à un nombre raisonnable d'éléments et utiliser une barre de défilement. |
| **Erreurs liées aux permissions d'accès** | Capture des exceptions (notamment `OSError` avec `errno == 13`) et affichage de messages d'erreur explicites, avec possibilité de réessayer l'opération. |
| **Gestion de l'historique et des favoris** | Utilisation d'un `set` pour éviter les doublons et réinitialisation de l'index en cas d'ajout. |
| **Affichage des boîtes de dialogue** | Centrage des boîtes de dialogue pour une meilleure visibilité. |

## Améliorations futures

1. **Persistance des favoris et de l'historique** : Sauvegarder les données dans un fichier JSON ou une base de données SQLite pour conserver les informations après fermeture de l'application.
2. **Recherche avancée** : Ajouter des options de recherche par nom, type, taille ou date pour filtrer plus efficacement les fichiers.
3. **Multithreading** : Implémenter le multithreading pour effectuer des opérations longues sans bloquer l'interface utilisateur.
4. **Aperçu des fichiers** : Permettre la prévisualisation de certains types de fichiers (images, PDF, etc.) directement dans l'application.

## Installation

Pour installer et lancer l'application :

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/explorateur-fichiers.git

2. Accédez au répertoire du projet :
   ```bash
   cd explorateur-fichiers
  
3. Installez les dépendances nécessaires :
    ```bash
   pip install -r requirements.txt
  
4. Lancez l'application :
   ```bash
   python main.py