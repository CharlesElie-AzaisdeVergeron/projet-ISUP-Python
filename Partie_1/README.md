# projet-ISUP-Python
Projet Python statistique M1


# README

Ce fichier décrit le projet **vehicle_analyse.py** qui vise analyser et visualiser l'impact de differents parametres d' une voiture sur son emission de CO2. 

## Installation

La première étape est de télécharger les fichiers de ce dossier, en utilisant la commande : 
```
git clone 
```

Pour exécuter les scripts dans ce fichier certaines bibliothèques python sont nécessaires, exécuter la commande suivante dans le dossier téléchargé avec votre env python activé avant de commencer :
```
pip install scipy.stat

 
```

## Utilisation

Le script principal est dans le fichier `calculator_carbon.py`. Pour l'utiliser exécuter :
```
python calculator_carbon.py
```
et suivez les instructions !


Le package vehicle_visualisation.py utilise les librairies numpy, pandas, matplotlib ainsi que scpipy.stat. Il fait l'étude de données du fichier "vehicles.csv" dans le but de détérminer les caracteristiques du vehicueles impactant les emissions de CO2, par le module statistics_1.py (comportant une regression lineaire). De plus, le module visualisation.py permet de visualiser les données et les corrélations entre elles.
