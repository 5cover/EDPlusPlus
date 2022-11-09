import bdd
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt

def creerFenetre():
    # La note maximale à utiliser pour les moyennes
    NOTE_MAX = 20
    def MEM(eleve: bdd.Eleve):
        """ Affiche le graphique MEM. """
        res = bdd.MEM(eleve)
        plt.bar([key.nomCourt for key in res.keys()], [val * NOTE_MAX for val in res.values()], 0.5)
        plt.suptitle(f"Moyennes de {eleve}")
        plt.xticks(rotation='30')
        plt.show()
        
    def MNM(matiere: bdd.Matiere):
        """ Affiche le graphique MNM. """
        res = bdd.MNM(matiere)
        print(res)
        if (res is None):
            plt.figure() # graphique vide
        else:
            plt.bar([str(key) for key in res.keys()], [val * NOTE_MAX for val in res.values()], 0.5)
        plt.suptitle(f"Moyennes en {matiere}")
        plt.xticks(rotation='vertical')
        plt.show()
        
    def NEM(eleve: bdd.Eleve, matiere: bdd.Matiere):
        """ Affiche le graphique NEM. """
        pass
    
    eleves = bdd.getEleves()
    matieres = bdd.getMatieres()
    
    def creerComboboxEleve():
        return ttk.Combobox(values = eleves, state = 'normal')
    def creerComboboxMatiere():
        return ttk.Combobox(values = matieres, state = 'normal')
    def grille(widget, r, c, cspan=1):
        widget.grid(sticky='nsew', row=r, column=c, padx=12, pady=12, columnspan=cspan)
        
    root = tk.Tk();
    root.title("ED++")
    root.geometry('700x175')
    root.resizable(True, False)
    root.iconbitmap("icon.ico")
    
    for i in range(4):
        root.rowconfigure(i, weight=1)
        
    for i in range(3):
        root.columnconfigure(i, weight=1)
    
    nemEleve = creerComboboxEleve()
    grille(nemEleve, 0, 0)
    nemMatiere = creerComboboxMatiere()
    grille(nemMatiere, 0, 1)
    grille(ttk.Button(text="Notes d’un élève pour une matière", command=lambda: NEM(eleves[nemEleve.current()], matieres[nemMatiere.current()])), 0, 2)
    
    mem = creerComboboxEleve()
    grille(mem, 1, 0, 2)
    grille(ttk.Button(text="Moyenne d’un élève par matière", command=lambda: MEM(eleves[mem.current()])), 1, 2)
    
    mnm = creerComboboxMatiere()
    grille(mnm, 2, 0, 2)
    grille(ttk.Button(text="Moyenne des notes pour une matière", command=lambda: MNM(matieres[mnm.current()])), 2, 2)
    
    root.mainloop()