# projet-ISUP-Python
Projet Python statistique M1

# README

Ce fichier décrit le projet **vehicle_analyse.py** qui vise à analyser et visualiser l'impact de différents paramètres d'une voiture sur ses émissions de CO2.

## Installation

La première étape est de télécharger les fichiers de ce dépôt en utilisant la commande : 
```
git clone https://github.com/votre-utilisateur/projet-ISUP-Python.git
```

Pour exécuter les scripts de ce projet, certaines bibliothèques Python sont nécessaires. Installez-les en exécutant la commande suivante dans le dossier du projet avec votre environnement Python activé :
```
( je n ais pas reussit a generer le fichier requierements.txt. Les bibliotheques necessaires sont dans le fichier setup.cfg)
pip install .
```

## Utilisation

Le script principal se trouve dans le fichier `Partie_2/vehicule_analyse/vehicule_analyse.py`. Pour l'utiliser, exécutez :
```
python Partie_2/vehicule_analyse/vehicle_analyse.py
```
et suivez les instructions !

Le package `vehicle_visualisation.py` est composé de deux modules principaux :
- `statistics_1.py` : effectue une analyse statistique des données du fichier "vehicles.csv" incluant une régression linéaire pour déterminer l'impact des caractéristiques des véhicules sur leurs émissions de CO2
- `visualisation.py` : génère des visualisations graphiques des données et met en évidence les corrélations entre les différentes variables
