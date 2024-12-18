import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import numpy as np
import pandas as pd

energie = pd.read_csv("energie.csv")
equipements = pd.read_csv("equipements.csv")
aliments = pd.read_csv("aliments.csv")

viandes = aliments[aliments['main_type'].str.contains('viandes', case=False)]
cereales = aliments[aliments['main_type'].str.contains('Produits céréaliers',case=False)]
Boisson = aliments[aliments['main_type'].str.contains('Boisson')]
Fruits= aliments[aliments['main_type'].str.contains('Fruits,légumes,légumineuses et oléagineux')]
Entreés= aliments[aliments['main_type'].str.contains('Entrées et plats composés')]
lait = aliments[aliments['main_type'].str.contains('Lait et produits laitiers')]
aides = aliments[aliments['main_type'].str.contains('Aides culinaires et ingrédients divers')]
sucres = aliments[aliments['main_type'].str.contains('Produits sucrés')]
glaces = aliments[aliments['main_type'].str.contains('Glaces et sorbets')]
gras = aliments[aliments['main_type'].str.contains(' Matières grasses')]
bebes = aliments[aliments['main_type'].str.contains('Aliments infantiles')]

nom_equipement = equipements['complete_name'].to_list()

def merge(L,M: list):
    N=[]
    for i in range(len(L)):
        if M[i] != 'Nan' :
            N.append(str(L[i])+'-'+str(M[i]))
    return N

def tri(L :list ):
    T = []
    for i in L:
        if i not in T:
            T = T + [i]
    return T


class SelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sélections Multiples")
        self.root.geometry("800x400")
        
        # Options pour les menus déroulants
        self.options_categorie = tri(list(aliments['main_type']))
        self.options_items = {
            tri(list(aliments['main_type']))[0] : merge(list(cereales['french_name']),list(cereales['french_attribut'])),
            tri(list(aliments['main_type']))[1]: merge(list(Boisson['french_name']),list(Boisson['french_attribut'])),
            tri(list(aliments['main_type']))[2]: merge(list(Fruits['french_name']),list(Fruits['french_attribut'])),
            tri(list(aliments['main_type']))[3]: merge(list(Entreés['french_name']),list(Entreés['french_attribut'])),
            tri(list(aliments['main_type']))[4]: merge(list(lait['french_name']),list(lait['french_attribut'])),
            tri(list(aliments['main_type']))[5]: merge(list(viandes['french_name']),list(viandes['french_attribut'])),
            tri(list(aliments['main_type']))[6]: merge(list(aides['french_name']),list(aides['french_attribut'])),
            tri(list(aliments['main_type']))[7]: merge(list(sucres['french_name']),list(sucres['french_attribut'])),
            tri(list(aliments['main_type']))[8]: merge(list(glaces['french_name']),list(glaces['french_attribut'])),
            tri(list(aliments['main_type']))[9]: merge(list(gras['french_name'])+'-'+list(gras['french_attribut'])),
            tri(list(aliments['main_type']))[10]: merge(list(bebes['french_name']),list(bebes['french_attribut']))

        }
        
        self.setup_interface()
        
    def setup_interface(self):
        # Frame pour les contrôles
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, padx=10, fill="x")
        
        
        # Labels et Combobox
        ttk.Label(control_frame, text="Catégorie:").grid(row=0, column=2, padx=5)
        self.combo_categorie = ttk.Combobox(control_frame, values=self.options_categorie)
        self.combo_categorie.grid(row=0, column=3, padx=5)
        self.combo_categorie.bind("<<ComboboxSelected>>", self.update_items)
        
        ttk.Label(control_frame, text="Item:").grid(row=0, column=4, padx=5)
        self.combo_items = ttk.Combobox(control_frame)
        self.combo_items.grid(row=0, column=5, padx=5)
        
        # Boutons
        ttk.Button(control_frame, text="Ajouter", command=self.ajouter_selection).grid(row=0, column=6, padx=5)
        ttk.Button(control_frame, text="Sauvegarder", command=self.sauvegarder_selections).grid(row=0, column=7, padx=5)
        
        treeViewFrame = ttk.Frame(self.root)
        treeViewFrame.pack(pady=10, padx=10, fill="x")
        
        # Zone de texte pour l'historique
        self.historique = ttk.Treeview(treeViewFrame, height=15, columns=('cat', 'prod', 'CO2'))
        
        self.historique.heading ('cat', text='Catégorie')
        self.historique.heading ('prod', text='Produits')
        self.historique.heading ('CO2', text="Qtt CO2")
        
        self.historique.pack(pady=10, padx=10, fill="both", expand=False)
        self.historique.bind("<KeyPress>", self.keyHandler)
        
    def keyHandler(self, event=None):
        if (event.keycode in [46,8]):
            self.supprimer_ligne()
            return
        
    def update_items(self, event=None):
        ## Récupérer la catégorie séléctionnée dans "Catégorie"
        categorie = self.combo_categorie.get()
        
        ## Met la valeur de ton dropdown "Item" aux items qui ont la catégorie
        self.combo_items['values'] = self.options_items.get(categorie, [])
        
        ## Actualise le dropdown
        self.combo_items.set('')
        
    def supprimer_ligne(self):
        ## Si aucin item selectionné
        if (not self.historique.selection()):
            tk.messagebox.showwarning(title="Aucune selection", message="Aucune ligne séléctionnée, suppression impossible")
            return
        
        ## Récupérer le nom de tout les items séléctionné
        selected_items = list(map(lambda item: self.historique.item(item)["values"][1], self.historique.selection()))
        
        ## Afficher un message de confirmation
        res = tk.messagebox.askquestion("Delete line ?", message=f"Êtes vous sure de vouloir supprimer {"la ligne" if len(selected_items) == 1 else "les lignes"} suivante\n- {"\n- ".join(selected_items)}")
        
        ## Si non, return
        if (res == "no"):
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
            selectedItem = aliments.loc[aliments["french_name"] == item]

            ## ajouter la categorie, l'item et la quantitée de CO2
            self.historique.insert("", "end", values=(list(selectedItem["main_type"])[0], list(selectedItem["french_name"])[0], list(selectedItem["CO2"])[0]), )

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
                
            print(result_json['TTCO2'])
                
            json.dump(result_json, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Succès", f"Sélections sauvegardées dans {filename}")



def calculate():
    print ( " l evaluation est approximative car elle regroupe les consommations de plusieurs produits d une meme categorie pour faciliter l utilisation.")
          
    questions = {
        "energie": {
            "type": 
            "Quel type d'énergie utilisez-vous"\
            "(écrire : fioul, gaz, granules, electricite) ?\n",
            "qty": "Quantite (en kWh) ?"
        },
        "equipements": {
            "type":
            "Quels équipements utilisez vous parmis les suivants"\
            "Appareil à raclettes 6-8p ; Aspirateur ménager avec sac; Aspirateur ménager sans sac; Aspirateur professionnel à traineaux;Ballon électrique chauffe-eau 200L ;"
            "Bouilloire ;Climatiseur mobile ;Congélateur armoire;Congélateur coffre;Four électrique encastrable;Four professionnel;Gazinière Gazinière;Hotte décorative à extraction;" 
            "Hotte visière à recyclage d'air;Lave-linge capacité 5 kg;Lave-linge capacité 7kg;Lave-vaisselle compact;Lave-vaisselle professionnel;Lave-vaisselle standard;Machine à café dosette;"
            "Machine à café expresso;Machine à café filtre;Machine à pain ;Micro-onde ;Mini-four électrique;Plaques de cuisson à induction  9000W;Plaques de cuisson au gaz 9000W;"
            "Plaques de cuisson vitrocéramiques 9000W;Radiateur électrique 1000 W à inertie;Radiateur électrique 1000 W à rayonnement;Réfrigérateur combiné;Réfrigérateur mini-bar;"
            "Réfrigétateur 1 grande porte;Robot multifonction ;Séche linge à évacuation;Sèche-linge à condensation;Sèche-linge à pompe à chaleur;yaourtière 8 pots"

        }
    }
    

    for ty in questions:
        print(f"\n\nCatégorie : {ty}")
        for subty in questions.get(ty):
            input(questions.get(ty).get(subty))


    #print(f"Votre empreinte carbone est de {carbone_empreinte:.1f} tonnes")

    print("\n\nDétails")
    #print(f"Alimentation : {'TTCO2':.1f} t")
    #print(f"Energie : {energie:.1f} t")
    #print(f"Equipements: {equipement:.1f}t")

if __name__ == "__main__":
    root = tk.Tk()
    app = SelectionApp(root)
    root.mainloop()
    calculate()