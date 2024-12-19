# projet-ISUP-Python
Projet Python statistique M1


# README

Ce fichier décrit le projet **carbsimulator** qui vise à créer un package python permettant à un professionel de la restauration d'évaluer l'empreinte carbone de son activité.

## Installation

La première étape est de télécharger les fichiers de ce dossier, en utilisant la commande : 
```
git clone 
```

Pour exécuter les scripts dans ce fichier certaines bibliothèques python sont nécessaires, exécuter la commande suivante dans le dossier téléchargé avec votre env python activé avant de commencer :
``` 
( je n ais pas reussit a generer le fichier requierements.txt. Les bibliotheques necessaires sont dans le fichier setup.cfg)
pip install .
 
```

## Utilisation

Le script principal est dans le fichier `calculator_carbon/calculator_carbon.py`. Pour l'utiliser exécuter :
```
python calculator_carbon/calculator_carbon.py
```
et suivez les instructions !

## Description 

LE script python se base sur trois base de données  :  aliments.csv , energie.csv et equipements.csv . Il permet a un restaurateur d estimer son emission carbon totale ; celle des matieres premieres utilisée , de son equipement et de sa consommation energetique. Pour les aliments, l'utilisateur rentre les informations via un menu deroulants ; pour l energie ainsi que l equipement, cela se fait via le terminal directement.   
