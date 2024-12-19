"""Calculator for measuring carbon footprint based on food, energy and equipment usage.

This module provides a GUI application for tracking and calculating carbon emissions
from various sources including food items, energy consumption and household equipment.
"""

import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

aliments = pd.read_csv("aliments.csv")
energies = pd.read_csv("energie.csv")
equipements = pd.read_csv("equipements.csv")

meats = aliments[aliments['main_type'].str.contains('viandes', case=False)]
cereals = aliments[aliments['main_type'].str.contains('Produits céréaliers',case=False)]
drinks = aliments[aliments['main_type'].str.contains('Boisson')]
fruits = aliments[aliments['main_type'].str.contains('Fruits,légumes,légumineuses et oléagineux')]
entrees = aliments[aliments['main_type'].str.contains('Entrées et plats composés')]
dairy = aliments[aliments['main_type'].str.contains('Lait et produits laitiers')]
cooking_aids = aliments[aliments['main_type'].str.contains(
    'Aides culinaires et ingrédients divers')]
sweets = aliments[aliments['main_type'].str.contains('Produits sucrés')]
ice_cream = aliments[aliments['main_type'].str.contains('Glaces et sorbets')]
fats = aliments[aliments['main_type'].str.contains(' Matières grasses')]
baby_food = aliments[aliments['main_type'].str.contains('Aliments infantiles')]



def remove_duplicates(input_list: list) -> list:
    """Remove duplicate items from a list while preserving order.
    
    Args:
        input_list: The input list that may contain duplicates
    
    Returns:
        list: A new list with duplicates removed while preserving original order
    """
    unique_items = []
    for item in input_list:
        if item not in unique_items:
            unique_items.append(item)
    return unique_items

class SelectionApp:
    """Main application class for handling food item selections and carbon tracking.
    
    This class provides a GUI interface for selecting food items by category,
    tracking their carbon footprint, and saving the selections to a file.
    """

    def __init__(self, root):
        """Initialize the selection application window.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("Sélections Multiples")
        self.root.geometry("800x400")
        # Liste pour stocker les sélections
        self.selections = []
        # Options pour les menus déroulants
        self.options_category = remove_duplicates(list(aliments['main_type']))
        self.options_items = {
            remove_duplicates(list(aliments['main_type']))[0]: list(cereals['french_tag']),
            remove_duplicates(list(aliments['main_type']))[1]: list(drinks['french_tag']),
            remove_duplicates(list(aliments['main_type']))[2]: list(fruits['french_tag']),
            remove_duplicates(list(aliments['main_type']))[3]: list(entrees['french_tag']),
            remove_duplicates(list(aliments['main_type']))[4]: list(dairy['french_tag']),
            remove_duplicates(list(aliments['main_type']))[5]: list(meats['french_tag']),
            remove_duplicates(list(aliments['main_type']))[6]: list(cooking_aids['french_tag']),
            remove_duplicates(list(aliments['main_type']))[7]: list(sweets['french_tag']),
            remove_duplicates(list(aliments['main_type']))[8]: list(ice_cream['french_tag']),
            remove_duplicates(list(aliments['main_type']))[9]: list(fats['french_tag']),
            remove_duplicates(list(aliments['main_type']))[10]: list(baby_food['french_tag'])

        }
        self.setup_interface()
    def setup_interface(self):
        # Frame pour les contrôles
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, padx=10, fill="x")
        # Labels et Combobox
        ttk.Label(control_frame, text="Catégorie:").grid(row=0, column=2, padx=5)
        self.combo_categorie = ttk.Combobox(control_frame, values=self.options_category)
        self.combo_categorie.grid(row=0, column=3, padx=5)
        self.combo_categorie.bind("<<ComboboxSelected>>", self.update_items)
        ttk.Label(control_frame, text="Item:").grid(row=0, column=4, padx=5)
        self.combo_items = ttk.Combobox(control_frame)
        self.combo_items.grid(row=0, column=5, padx=5)
        # Boutons
        ttk.Button(
            control_frame, text="Ajouter", command=self.ajouter_selection
        ).grid(row=0, column=6, padx=5)
        ttk.Button(
            control_frame, text="Sauvegarder", command=self.sauvegarder_selections
        ).grid(row=0, column=7, padx=5)
        tree_view_frame = ttk.Frame(self.root)
        tree_view_frame.pack(pady=10, padx=10, fill="x")
        # Zone de texte pour l'historique
        self.historique = ttk.Treeview(tree_view_frame, height=15, columns=('cat', 'prod', 'CO2'))
        self.historique.heading ('cat', text='Catégorie')
        self.historique.heading ('prod', text='Produits')
        self.historique.heading ('CO2', text="Qtt CO2")
        self.historique.pack(pady=10, padx=10, fill="both", expand=False)
        self.historique.bind("<KeyPress>", self.handle_key)
    def handle_key(self, event=None):
        """Handle keyboard events.
        
        Args:
            event: The keyboard event to handle. Default is None.
        """
        if event.keycode in [46, 8]:  # Delete or backspace
            self.delete_line()
    def update_items(self, event=None):
        ## Récupérer la catégorie séléctionnée dans "Catégorie"
        categorie = self.combo_categorie.get()
        ## Met la valeur de ton dropdown "Item" aux items qui ont la catégorie
        self.combo_items['values'] = self.options_items.get(categorie, [])
        ## Actualise le dropdown
        self.combo_items.set('')
    def supprimer_ligne(self):
        ## Si aucin item selectionné
        if not self.historique.selection():
            tk.messagebox.showwarning(
                title="Aucune selection",
                message="Aucune ligne séléctionnée, suppression impossible"
            )
            return
        ## Récupérer le nom de tout les items séléctionné
        selected_items = list(map(
            lambda item: self.historique.item(item)["values"][1],
            self.historique.selection()
        ))
        ## Afficher un message de confirmation
        msg = tk.messagebox.askquestion("Delete line ?", message=f"Êtes vous sure de vouloir supprimer {"la ligne" if len(selected_items) == 1 else "les lignes"} suivante\n- {"\n- ".join(selected_items)}")
        
        res = tk.messagebox.askquestion("Delete line ?", message=msg)
        ## Si non, return
        if res == "no":
            return
        ## Suprimer tout les items
        for item in self.historique.selection():
            self.historique.delete(item)
    def ajouter_selection(self):
        categorie = self.combo_categorie.get()
        item = self.combo_items.get()
        if categorie and item:
            #selection = f"{categorie} - {item}"
            #self.selections.append(selection)
            #self.historique.insert("end", f"{selection}\n")
            ## Récupérer l'item
            selectedItem = aliments.loc[aliments["french_tag"] == item]

            ## ajouter la categorie, l'item et la quantitée de CO2
            self.historique.insert(
                "", "end",
                values=(
                    list(selectedItem["main_type"])[0],
                    list(selectedItem["french_tag"])[0],
                    list(selectedItem["CO2"])[0]
                )
            )

            ## Display confirmation message
            messagebox.showinfo("Succès", "Sélection ajoutée avec succès!")
        else:
            ## Afficher message d'erreur
            messagebox.showwarning("Attention", "Veuillez sélectionner une catégorie et un item.")
    def sauvegarder_selections(self):
        if (not self.historique.get_children()):
            messagebox.showwarning("Attention", "Aucune sélection à sauvegarder.")
            return
        filename = f"selections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            result_json = {"produits": [], "TTCO2": 0}
            for item in self.historique.get_children():
                cat, prod, co2 = self.historique.item(item)['values']
                co2 = float(co2)
                result_json["produits"].append({"cat": cat, "prod": prod, "co2": co2})
                result_json['TTCO2'] += co2
                result_json['TTCO2'] = round(result_json['TTCO2'], 2)
            print(
                f"les émission de Co2 totales pour les aliments sont de : "
                f"{result_json['TTCO2']:.1f}t"
            )
            json.dump(result_json, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Succès", f"Sélections sauvegardées dans {filename}")


def retrieve_from_dict(df: pd.DataFrame, answer: str) -> float:
    """Retrieve CO2 value from dataframe based on name match.
    
    Args:
        df: DataFrame containing CO2 and name data
        answer: String to search for in name columns
        
    Returns:
        float: CO2 value if found, -1.0 if not found
    """
    keys: list = df.keys()    
    answer = answer.replace(" ", "")

    for key in keys:
        if key.find("name") >= 0:
            col: dict = df.get(key).to_dict()
            for entry in col:
                match = (col[entry].find(answer.capitalize()) >= 0 or
                        col[entry].find(answer.lower()) >= 0)
                if match:  # Check if answer exists in possible names
                    return float(df["CO2"][entry])
    return -1.0


questions = {
        "Energie": {
            "type": ("Quel type d'énergie utilisez-vous "
                    "(écrire :'Electricité ; Fioul domestique ; Granulés ; Gaz naturel - 2022'\n" ),
            "qty": "Quantité (en kWh) ?"
        },
        "Equipements": {
            "type": (
                "Quels équipements utilisez-vous parmi les suivants :\n"
                "- Appareil à raclettes 6-8p\n"
                "- Aspirateur ménager avec sac\n"
                "- Aspirateur ménager sans sac\n"
                "- Aspirateur professionnel à traineaux\n"
                "- Ballon électrique chauffe-eau 200L\n"
                "- Bouilloire\n"
                "- Climatiseur mobile\n"
                "- Congélateur armoire\n"
                "- Congélateur coffre\n"
                "- Four électrique encastrable\n"
                "- Four professionnel\n"
                "- Gazinière\n"
                "- Hotte décorative à extraction\n"
                "- Hotte visière à recyclage d'air\n"
                "- Lave-linge capacité 5 kg\n"
                "- Lave-linge capacité 7kg\n"
                "- Lave-vaisselle compact\n"
                "- Lave-vaisselle professionnel\n"
                "- Lave-vaisselle standard\n"
                "- Machine à café dosette\n"
                "- Machine à café expresso\n"
                "- Machine à café filtre\n"
                "- Machine à pain\n"
                "- Micro-onde\n"
                "- Mini-four électrique\n"
                "- Plaques de cuisson à induction 9000W\n"
                "- Plaques de cuisson au gaz 9000W\n"
                "- Plaques de cuisson vitrocéramiques 9000W\n"
                "- Radiateur électrique 1000W à inertie\n"
                "- Radiateur électrique 1000W à rayonnement\n"
                "- Réfrigérateur combiné\n"
                "- Réfrigérateur mini-bar\n"
                "- Réfrigérateur 1 grande porte\n"
                "- Robot multifonction\n"
                "- Sèche-linge à évacuation\n"
                "- Sèche-linge à condensation\n"
                "- Sèche-linge à pompe à chaleur\n"
                "- Yaourtière 8 pots\n"
            )
        }
    }


def calculate(reponses : tuple, energies: pd.DataFrame, equipements: pd.DataFrame) -> tuple[float, float]:
    type_en : str = reponses[0]
    type_eq : str = reponses[2]
    qte_en = float(reponses[1])

    cout_en : float = retrieve_from_dict(energies, type_en) * qte_en
    cout_eq : float = 0.0

    for eq in type_eq.split(","):
        cout_eq += retrieve_from_dict(equipements, eq)
    
    return cout_en, cout_eq


def gather_inputs(questions : dict) -> tuple:
    type_en = input(questions.get("Energie").get("type"))
    qte_en = input(questions.get("Energie").get("qty"))
    type_eq = input(questions.get("Equipements").get("type"))

    return type_en, qte_en, type_eq



if __name__ == "__main__":
    root = tk.Tk()
    app = SelectionApp(root)
    root.mainloop()

    res = calculate(gather_inputs(questions), energies, equipements)
    print(f"Total CO2 énergie : {res[0]}")
    print(f"Total CO2 équipements : {res[1]}")