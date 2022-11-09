import sqlite3
from datetime import date
from collections import defaultdict

# Établissement d'une connection avec le fichier de base de donnée.
conn = sqlite3.connect("dbed.db")
# Création du curseur, un objet qui permet de parcourir la BDD et d'exécuter des requêtes SQL.
cur = conn.cursor()

class Matiere:
    def __init__(self, id_: str, type_: str, nom: str, nomCourt: str):
        self.id = id_
        self.type = type_
        self.nom = nom
        self.nomCourt = nomCourt
    def __str__(self):
        return f'{self.type} / {self.nom}'

class Evaluation:
    def __init__(self, id_: str, titre: str, dateEval: date, noteMax: int, coef: float, id_matiere: str):
        self.id = id_
        self.titre = titre
        self.dateEval = dateEval
        self.noteMax = noteMax
        self.coef = coef
        self.id_matiere = id_matiere
        
class Eleve:
    def __init__(self, id_: str, nom: str, prenom: str, id_classe: str):
        self.id = id_
        self.nom = nom
        self.prenom = prenom,
        self.id_classe = id_classe
        
    def __str__(self):
        # Pour une raison iconnue, self.prenom devient un tuple à 1 élément ici?
        return f'{self.nom.upper()} {self.prenom[0]}'

def MEM(eleve: Eleve):
    """ Cette fonction permet d'obtenir un graphique retraçant chaque moyenne pour toutes les matière d'un élève choisi
    Retour : dictionnaire (dict)
    clés : matières
    valeurs : moyenne sur 1 """

    # Obtention de la liste des matières auquelles l'élève est inscrit.
    matieres = [Matiere(*t) for t in cur.execute(f'SELECT DISTINCT MATIERES.* FROM COURS\
                                                   INNER JOIN MATIERES on MATIERES.id = id_matiere\
                                                   WHERE id_eleve = {eleve.id}').fetchall()]
    
    moyennes = defaultdict(float)
    
    for matiere in matieres: # SELECTION DE CHAQUE MATIERE
        evals = getEvaluations(matiere)
        if not evals: # Si il n'y a aucune évaluation pour cette matière
            continue
        for evaluation in evals:
            cur.execute(f'SELECT valeur FROM NOTES WHERE id_eleve = {eleve.id} AND id_evaluation = {evaluation.id}')
            moyennes[matiere] += cur.fetchone()[0] / evaluation.noteMax * evaluation.coef
        moyennes[matiere] /= sum((evaluation.coef for evaluation in evals))

    return dict(moyennes)

def MNM(matiere: Matiere):
    """ Retour : dictionnaire (dict)
            clés : élèves
            valeurs : moyenne sur 1
            OU None si aucune évaluation dans matière"""
    
    eleves = [Eleve(*t) for t in cur.execute(f'SELECT DISTINCT ELEVES.* FROM COURS\
                                               INNER JOIN ELEVES on ELEVES.id = id_eleve\
                                               WHERE id_matiere = {matiere.id}').fetchall()]
    evals = getEvaluations(matiere)
    
    # Dictionnaire avec valeur par défaut (0) pour les clés inconnues
    moyennes = defaultdict(float)
    
    # On commence par remplir les moyennes avec le numérateur
    for evaluation in evals:
        for eleve in eleves:
            # Obtient la valeur de la note de l'élève dans l'évaluation
            note = cur.execute(f'SELECT valeur FROM NOTES where id_eleve={eleve.id} AND id_evaluation={evaluation.id}').fetchone()[0]
            # On divise par noteMax pour obtenir la note sur 1.
            moyennes[eleve] += note / evaluation.noteMax * evaluation.coef
    
    # On calcule la moyenne pondérée en divisant par la somme des coefficients.
    sommeCoefs = sum((evaluation.coef for evaluation in evals))
    if (sommeCoefs == 0):
        # Retourner None si il n'y a pas d'évaluation
        return None
    for eleve in eleves:
        moyennes[eleve] /= sommeCoefs 
    return dict(moyennes)

def NEM(eleve: Eleve, matiere: Matiere):
    pass

def getEvaluations(matiere):
    return [Evaluation(t[0],
                       t[1],
                       date(*map(int, t[2].split('-'))),
                       int(t[3]),
                       float(t[4]),
                       t[5])
            for t in cur.execute(f'SELECT * FROM EVALUATIONS WHERE id_matiere={matiere.id}').fetchall()]

def getEleves():
    return [Eleve(*t) for t in cur.execute('SELECT * from ELEVES').fetchall()]

def getMatieres():
    return [Matiere(*t) for t in cur.execute('SELECT * from MATIERES').fetchall()]

    