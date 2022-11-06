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
        plt.bar([key.nomCourt for key in res.keys()], [val * NOTE_MAX for val in res.values()])
        plt.suptitle(f"Moyennes de {eleve}")
        plt.xticks(rotation='30')
        plt.show()
        
    def MNM(matiere: bdd.Matiere):
        """ Affiche le graphique MNM. """
        res = bdd.MNM(matiere)
        plt.bar(res.keys(), [val * NOTE_MAX for val in res.values()])
        plt.suptitle(f"Moyennes en {matiere}")
        plt.show()
        
    def NEM(eleve: bdd.Eleve):
        """ Affiche le graphique NEM. """
        pass
    
    eleves = bdd.getEleves()
    matieres = bdd.getMatieres()
    
    def creerComboboxEleve():
        return ttk.Combobox(values = eleves, state = 'normal')
    def creerComboboxMatiere():
        return ttk.Combobox(values = matieres, state = 'normal')
    def grille(widget, r, c):
        widget.grid(sticky='nsew', row=r, column=c, padx=12, pady=12)
        
    root = tk.Tk();
    root.title("ED++")
    root.geometry('700x175')
    root.resizable(True, False)
    root.iconbitmap("icon.ico")
    
    for i in range(4):
        root.rowconfigure(i, weight=1)
        
    for i in range(2):
        root.columnconfigure(i, weight=1)
    
    nem = creerComboboxEleve()
    grille(nem, 0, 0)
    grille(ttk.Button(text="Note d’un élève pour une matière", command=lambda: NEM(eleves[nem.current()])), 0, 1)
    
    mem = creerComboboxEleve()
    grille(mem, 1, 0)
    grille(ttk.Button(text="Moyenne d’un élève par matière", command=lambda: MEM(eleves[mem.current()])), 1, 1)
    
    mnm = creerComboboxMatiere()
    grille(mnm, 2, 0)
    grille(ttk.Button(text="Moyenne des notes pour une matière", command=lambda: MNM(matieres[mnm.current()])), 2, 1)
    
    root.mainloop()