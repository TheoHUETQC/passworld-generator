import tkinter as tk
from tkinter import messagebox
import hashlib

TAILLE_MDP = 23
CAR = list('!@#$%^&*()1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')  # len = 72
N = len(CAR)
error = []

def deterministic_hash(value):
    return int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16)

def generer_mot_de_passe():
    identifiant = entry_identifiant.get().strip()
    mot_de_passe = entry_mdp.get().strip()

    if not identifiant or not mot_de_passe:
        messagebox.showerror("Erreur", "Identifiant ou mot de passe manquant")
        return
    elif identifiant == "Théo" and mot_de_passe == "HUET" :
        messagebox.showerror("Erreur list : ", error)
        return
    
    hash_id = abs(deterministic_hash(identifiant))
    hash_mdp = abs(deterministic_hash(mot_de_passe))

    hash_mdp = hash_mdp * 2 + hash_id ** 2
    while len(str(abs(hash_mdp))) < TAILLE_MDP * 10 :
        hash_mdp = hash_mdp * 2 + hash_id ** 2

    tab_mdp = [int(str(hash_mdp)[i:i+2]) for i in range(len(str(hash_mdp))-(TAILLE_MDP*2), len(str(hash_mdp)), 2)]
    new_mdp = ""
    
    for i in tab_mdp:
        new_mdp += str(CAR[(i % N)])

    # Enregistrer le mot de passe généré
    global generated_mdp
    generated_mdp = new_mdp[:TAILLE_MDP]  # Mot de passe généré

    # Afficher le mot de passe masqué sous forme d'astérisques
    label_resultat.config(text="Ton mot de passe : " + "*" * TAILLE_MDP)
    
    # Griser le bouton "Générer"
    btn_generer.config(state="disabled", bg="#d3d3d3")
    
    # Activer le bouton "Copier" et le mettre en bleu-gris
    btn_copier.config(state="normal", bg="#A1B5C7")

    # Activer le bouton "Afficher/Masquer" et le mettre en gris
    btn_afficher_masquer.config(state="normal", text="O", bg="#D3D3D3", command=afficher_mdp)

def toggle_mdp():
    """Fonction pour basculer l'affichage du mot de passe"""
    if entry_mdp.cget('show') == "*":
        entry_mdp.config(show="")  # Affiche le texte
        btn_toggle.config(text="X", bg="#F47C7C")  # Change le texte et le fond pour "Cacher"
    else:
        entry_mdp.config(show="*")  # Masque le texte
        btn_toggle.config(text="O", bg="#A1B5C7")  # Change le texte et le fond pour "Afficher"

def copier_mot_de_passe():
    """Fonction pour copier le mot de passe généré dans le presse-papiers"""
    try :
        if generated_mdp:
            root.clipboard_clear()  # Vide le presse-papiers
            root.clipboard_append(generated_mdp)  # Ajoute le mot de passe au presse-papiers
            root.update()  # Mise à jour du presse-papiers
            btn_copier.config(state="disabled", bg="#d3d3d3")  # Désactive le bouton "Copier" et le grise
    except Exception as e:
        error.append(e)
        #messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

def masquer_mdp():
    """Masque le mot de passe et change le bouton pour afficher"""
    label_resultat.config(text="Ton mot de passe : " + "*" * TAILLE_MDP)
    btn_afficher_masquer.config(text="O", bg="#D3D3D3", command=afficher_mdp)

def afficher_mdp():
    """Affiche le mot de passe et change le bouton pour masquer"""
    label_resultat.config(text=f"Ton mot de passe : {generated_mdp}")
    btn_afficher_masquer.config(text="X", bg="#D3D3D3", command=masquer_mdp)

def reinitialiser():
    """Réinitialise les boutons et le champ de mot de passe pour générer un nouveau mot de passe"""
    label_resultat.config(text="Ton mot de passe : ")
    btn_generer.config(state="normal", bg="#A1B5C7")  # Réactive le bouton "Générer"
    btn_copier.config(state="disabled", bg="#d3d3d3")  # Désactive le bouton "Copier"
    btn_afficher_masquer.config(state="disabled", text="O", bg="#D3D3D3", command=afficher_mdp)

def activer_generer(event):
    """Réactive le bouton "Générer" lorsqu'un champ est modifié."""
    if event.keysym == "Return":  # Vérifie si la touche est "Entrée"
        return  # Ignore l'événement
    btn_generer.config(state="normal", bg="#A1B5C7")  # Réactive le bouton "Générer"
    btn_copier.config(state="disabled", bg="#d3d3d3")  # Désactive le bouton "Copier"
    btn_afficher_masquer.config(state="disabled", text="O", bg="#D3D3D3", command=afficher_mdp)

def on_enter(event):
    """Exécute la génération de mot de passe lorsqu'on appuie sur Entrée, puis désactive la génération."""
    if btn_generer["state"] == "normal":  # Vérifie si le bouton "Générer" est actif
        generer_mot_de_passe()  # Génère le mot de passe
        copier_mot_de_passe() #copie le mot de passe
        
# Création de la fenêtre principale
root = tk.Tk()
root.title("Générateur de Mot de Passe")

# Configuration de la taille de la fenêtre et couleur de fond
root.geometry("500x350")
root.resizable(False, False)
root.configure(bg="#f5f5f5")  # Couleur de fond gris clair

# Interface utilisateur avec des couleurs modernes et sobres
label_identifiant = tk.Label(root, text="Identifiant :", font=("Helvetica", 12), bg="#f5f5f5", fg="#333")
label_identifiant.pack(pady=10)

# Zone de texte pour l'identifiant avec plus de contraste
entry_identifiant = tk.Entry(root, width=30, font=("Helvetica", 12), bd=2, relief="flat", fg="#333", bg="#e0e0e0", highlightthickness=0)
entry_identifiant.pack(pady=5, padx=10)
entry_identifiant.bind("<KeyRelease>", activer_generer)  # Active le bouton "Générer" lors de la modification de l'identifiant

label_mdp = tk.Label(root, text="Mot de Passe :", font=("Helvetica", 12), bg="#f5f5f5", fg="#333")
label_mdp.pack(pady=10)

# Champ de mot de passe avec icône "O" ou "X"
frame_mdp = tk.Frame(root, bg="#f5f5f5")
entry_mdp = tk.Entry(frame_mdp, width=25, font=("Helvetica", 12), show="*", bd=2, relief="flat", fg="#333", bg="#e0e0e0", highlightthickness=0)
entry_mdp.pack(side="left", padx=10)
entry_mdp.bind("<KeyRelease>", activer_generer)  # Active le bouton "Générer" lors de la modification du mot de passe

# Bouton pour afficher/masquer le mot de passe avec les caractères "O" (cacher) et "X" (afficher)
btn_toggle = tk.Button(frame_mdp, text="O", command=toggle_mdp, bd=0, bg="#A1B5C7", fg="white", font=("Helvetica", 14, "bold"), relief="flat", width=3, height=1)
btn_toggle.pack(side="left")

frame_mdp.pack(pady=10)

# Frame pour le bouton générer et le bouton copier
frame_buttons = tk.Frame(root, bg="#f5f5f5")
# Bouton pour générer le mot de passe dans des tons bleu-gris avec des coins arrondis
btn_generer = tk.Button(frame_buttons, text="Générer le mot de passe", command=generer_mot_de_passe, font=("Helvetica", 12), bg="#A1B5C7", fg="white", relief="flat", bd=0, padx=15, pady=10, highlightthickness=0)
btn_generer.pack(side="left", padx=10)

# Bouton pour copier le mot de passe dans le presse-papiers
btn_copier = tk.Button(frame_buttons, text="Copier", command=copier_mot_de_passe, font=("Helvetica", 12), bg="#d3d3d3", fg="white", relief="flat", bd=0, padx=10, pady=5, highlightthickness=0, state="disabled")
btn_copier.pack(side="left", padx=10)

frame_buttons.pack(pady=20)

# Label pour afficher le mot de passe généré
frame_resultat = tk.Frame(root, bg="#f5f5f5")
label_resultat = tk.Label(frame_resultat, text="Ton mot de passe : ", font=("Helvetica", 12), bg="#f5f5f5", fg="#333")
label_resultat.pack(side="left", padx=10)

# Bouton pour masquer/afficher le mot de passe généré
btn_afficher_masquer = tk.Button(frame_resultat, text="O", font=("Helvetica", 12), bg="#D3D3D3", fg="white", relief="flat", bd=0, padx=5, pady=5, highlightthickness=0, command=afficher_mdp, state="disabled")
btn_afficher_masquer.pack(side="left", padx=10)

frame_resultat.pack(pady=20)

# Bouton pour réinitialiser
btn_reinitialiser = tk.Button(root, text="Réinitialiser", font=("Helvetica", 12), bg="#D3D3D3", fg="white", relief="flat", bd=0, padx=10, pady=5, highlightthickness=0, command=reinitialiser)
btn_reinitialiser.pack(pady=20)

#touche entrer
root.bind("<Return>", on_enter)

# Lancement de la fenêtre principale
root.mainloop()