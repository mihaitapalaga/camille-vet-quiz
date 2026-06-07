# Camille Vet Quiz

Petite application de révision vétérinaire pour Camille.

## Application en ligne

**[https://camille-vet-quiz.vercel.app](https://camille-vet-quiz.vercel.app)**

Le lien fonctionne depuis n'importe quel ordinateur ou téléphone, en France comme ailleurs. Aucune installation nécessaire.

## Fonctionnalités

- **Quiz aléatoire** : 179 questions générées uniquement à partir de tes 3 cours.
- **Choix multiples** : certaines questions acceptent plusieurs bonnes réponses.
- **Compteur interactif** : clique pour compter de 0 à 100, une popup apparaît à 100 puis le compteur revient à 0.

## Stack technique

- Vite + TypeScript pour le front
- Pipeline d'extraction des questions en local (`scripts/`)
- Déploiement continu sur Vercel

## Développement local

```bash
git clone https://github.com/mihaitapalaga/camille-vet-quiz.git
cd camille-vet-quiz
npm install
npm run dev
```

L'application est ensuite accessible sur l'adresse locale affichée dans le terminal (par défaut `http://localhost:5173`).

## Déployer une mise à jour sur Vercel

Après avoir modifié le code, depuis la racine du projet :

```bash
npx vercel deploy --prod
```

## Régénérer les questions depuis les PDFs

Place les PDFs des cours dans le dossier prévu, puis, depuis la racine du projet :

```bash
npm run extract
npx vercel deploy --prod
```

Le script dédoublonne automatiquement les questions et recalcule le total disponible.
