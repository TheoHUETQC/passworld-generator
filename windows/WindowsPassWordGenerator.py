import tkinter as tk
from tkinter import messagebox
import hashlib

MDP_SIZE = 23 # taille du mot de passe final que l'on souhaite
CAR = list('!@#$%^&*()1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') # liste de caractère qui composera le mot de passe generé
N = len(CAR) # len = 72 
error = [] # liste qui stock les erreurs

# Valeur par défaut de la longueur de mot de passe
default_mdp_size = MDP_SIZE
current_mdp_size = default_mdp_size

# État actuel du thème
theme = "light"

#etat des parametres
parametres_visibles = False 

# Couleurs claires
light_bg = "#f5f5f5"
light_fg = "#333"
light_entry_bg = "#e0e0e0"
light_button_bg = "#A1B5C7"

# Couleurs sombres
dark_bg = "#2e2e2e"
dark_fg = "#f5f5f5"
dark_entry_bg = "#4a4a4a"
dark_button_bg = "#5c7d99"

def deterministic_hash(value) : 
    """Hashage : transforme une chaine de caractère en entier"""
    return int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16)

def generate_password() :
    """géneration du mot de passe de taille MDP_SIZE"""
    # entrée de l'utilisateur
    id = entry_identifiant.get().strip()
    password = entry_mdp.get().strip()

    if not id or not password : # si il manque le mdp ou id
        messagebox.showerror("Erreur", "Identifier or password missing")
        return
    elif id == "Théo" and password == "HUET" : # id et mdp a rentrer pour voir la liste d'erreur
        messagebox.showerror("Erreur list : ", error)
        return
    
    global current_mdp_size
    try :
        current_mdp_size = abs(int(spinbox_length.get()))
    except ValueError as e :
        error.append(str(e) + " => current_mdp_size =" + str(default_mdp_size))
        current_mdp_size = default_mdp_size

    # hashage
    hash_id = abs(deterministic_hash(id))
    hash_pw = abs(deterministic_hash(password))

    # manipulation de l'id et le mdp hashés pour créer un grand entier unique
    hash_pw = hash_pw * 2 + hash_id ** 2
    while len(str(abs(hash_pw))) < current_mdp_size  * 10 :
        hash_pw = hash_pw * 2 + hash_id ** 2
    
    # utilisation du résultat pour créer une liste d'indice de taille 2 : 24908273 -> [24, 90, 82, 73]
    tab_pw = [int(str(hash_pw)[i:i+2]) for i in range(len(str(hash_pw))-(current_mdp_size *2), len(str(hash_pw)), 2)]
    
    # création du nouveau mot de passe en utilisant la liste d'indice pour piocher des caractères dans la liste CAR
    new_pw = ""
    for i in tab_pw:
        new_pw += str(CAR[(i % N)])

    # Enregistrer le mot de passe généré
    global generated_pw
    generated_pw = new_pw[:current_mdp_size ]  # Mot de passe généré

    # Afficher le mot de passe masqué sous forme d'astérisques
    label_resultat.config(text="Your Password : " + "*" * current_mdp_size)
    
    # Griser le bouton "Générer"
    btn_generer.config(state="disabled", bg="#d3d3d3")
    
    # Activer le bouton "Copier" et le mettre en bleu-gris
    btn_copier.config(state="normal", bg="#A1B5C7")
    
    # Activer le bouton "Afficher/Masquer" et le mettre en gris
    btn_afficher_masquer.config(state="normal", text="O", bg="#D3D3D3", command=show_password)

def on_enter_button(e):
    e.widget['background'] = "#879bb0" if theme == "light" else "#7691ad"  # couleur hover

def on_leave_button(e):
    e.widget['background'] = light_button_bg if theme == "light" else dark_button_bg

def toggle_parametres():

    global parametres_visibles
    if parametres_visibles:
        frame_parametres.place_forget()
        parametres_visibles = False
    else:
        frame_parametres.place(x=10, y=50)  # Juste en dessous du bouton
        frame_parametres.tkraise()
        parametres_visibles = True

def toggle_mdp():
    """Fonction pour basculer l'affichage du mot de passe"""
    if entry_mdp.cget('show') == "*":
        entry_mdp.config(show="")  # Affiche le texte
        btn_toggle.config(text="X", bg="#F47C7C")  # Change le texte et le fond pour "Cacher"
    else:
        entry_mdp.config(show="*")  # Masque le texte
        btn_toggle.config(text="O", bg="#A1B5C7")  # Change le texte et le fond pour "Afficher"

def copy_password():
    """Fonction pour copier le mot de passe généré dans le presse-papiers"""
    try :
        if generated_pw:
            root.clipboard_clear()  # Vide le presse-papiers
            root.clipboard_append(generated_pw)  # Ajoute le mot de passe au presse-papiers
            root.update()  # Mise à jour du presse-papiers
            btn_copier.config(state="disabled", bg="#d3d3d3")  # Désactive le bouton "Copier" et le grise
    except Exception as e:
        error.append(e)
        #messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

def hide_password():
    """Masque le mot de passe et change le bouton pour afficher"""
    label_resultat.config(text="Your Password : " + "*" * current_mdp_size)
    btn_afficher_masquer.config(text="O", bg="#D3D3D3", command=show_password)

def show_password():
    """Affiche le mot de passe et change le bouton pour masquer"""
    label_resultat.config(text=f"Your Password : {generated_pw}")
    btn_afficher_masquer.config(text="X", bg="#D3D3D3", command=hide_password)

def reset():
    """Réinitialise les boutons et le champ de mot de passe pour générer un nouveau mot de passe"""
    label_resultat.config(text="Your Password : ")
    btn_generer.config(state="normal", bg="#A1B5C7")  # Réactive le bouton "Générer"
    btn_copier.config(state="disabled", bg="#d3d3d3")  # Désactive le bouton "Copier"
    btn_afficher_masquer.config(state="disabled", text="O", bg="#D3D3D3", command=show_password)

def activate_generate(event):
    """Réactive le bouton "Générer" lorsqu'un champ est modifié."""
    if event.keysym == "Return":  # Vérifie si la touche est "Entrée"
        return  # Ignore l'événement
    btn_generer.config(state="normal", bg="#A1B5C7")  # Réactive le bouton "Générer"
    btn_copier.config(state="disabled", bg="#d3d3d3")  # Désactive le bouton "Copier"
    btn_afficher_masquer.config(state="disabled", text="O", bg="#D3D3D3", command=show_password)

def on_enter(event):
    """Exécute la génération de mot de passe lorsqu'on appuie sur Entrée, puis désactive la génération."""
    if btn_generer["state"] == "normal":  # Vérifie si le bouton "Générer" est actif
        generate_password()  # Génère le mot de passe
        copy_password() #copie le mot de passe

def switch_theme():
    global theme
    if theme == "light":
        # Basculer vers sombre
        root.configure(bg=dark_bg)
        label_identifiant.config(bg=dark_bg, fg=dark_fg)
        label_mdp.config(bg=dark_bg, fg=dark_fg)
        label_resultat.config(bg=dark_bg, fg=dark_fg)
        label_length.config(bg=dark_bg, fg=dark_fg) 
        frame_mdp.config(bg=dark_bg)
        frame_buttons.config(bg=dark_bg)
        frame_resultat.config(bg=dark_bg)
        frame_length.config(bg=dark_bg) 
        frame_parametres.config(bg=dark_bg)
        
        entry_identifiant.config(bg=dark_entry_bg, fg=dark_fg)
        entry_mdp.config(bg=dark_entry_bg, fg=dark_fg)
        spinbox_length.config(bg=dark_entry_bg, fg=dark_fg)

        btn_toggle.config(bg=dark_button_bg)
        btn_generer.config(bg=dark_button_bg)
        btn_copier.config(bg=dark_button_bg)
        btn_afficher_masquer.config(bg=dark_button_bg)
        btn_reinitialiser.config(bg=dark_button_bg)
        btn_theme.config(bg=dark_button_bg)
        btn_theme.config(bg=dark_button_bg)
        btn_parametres.config(bg=dark_button_bg)
        label_length.config(bg=dark_bg, fg=dark_fg)

        theme = "dark"
    else:
        # Basculer vers clair
        root.configure(bg=light_bg)
        label_identifiant.config(bg=light_bg, fg=light_fg)
        label_mdp.config(bg=light_bg, fg=light_fg)
        label_resultat.config(bg=light_bg, fg=light_fg)
        label_length.config(bg=light_bg, fg=light_fg) 
        frame_mdp.config(bg=light_bg)
        frame_buttons.config(bg=light_bg)
        frame_resultat.config(bg=light_bg)
        frame_length.config(bg=light_bg) 
        frame_parametres.config(bg=light_bg)

        entry_identifiant.config(bg=light_entry_bg, fg=light_fg)
        entry_mdp.config(bg=light_entry_bg, fg=light_fg)
        spinbox_length.config(bg=light_entry_bg, fg=light_fg)  

        btn_toggle.config(bg=light_button_bg)
        btn_generer.config(bg=light_button_bg)
        btn_copier.config(bg=light_button_bg)
        btn_afficher_masquer.config(bg=light_button_bg)
        btn_reinitialiser.config(bg=light_button_bg)
        btn_theme.config(bg=light_button_bg)
        btn_theme.config(bg=light_button_bg)  
        btn_parametres.config(bg=light_button_bg) 
        label_length.config(bg=light_bg, fg=light_fg) 

        theme = "light"


# Création de la fenêtre principale
root = tk.Tk()
root.title("Password Generator")

# Configuration de la taille de la fenêtre et couleur de fond
root.geometry("500x400") #500x350
root.resizable(False, False)
root.configure(bg="#f5f5f5")  # Couleur de fond gris clair

frame_parametres = tk.Frame(root, bg=light_bg, bd=2, relief="groove") # parametre dans les quel on mettra les deux boutons

# Bouton parametres 
btn_parametres = tk.Button(root, text="⚙️", command=toggle_parametres, font=("Helvetica", 16), bg=light_button_bg, fg="white", relief="flat", bd=0)
btn_parametres.place(x=10, y=10)  # Tout en haut à gauche
btn_parametres.bind("<Enter>", on_enter_button)
btn_parametres.bind("<Leave>", on_leave_button)

# Bouton changement de thème
btn_theme = tk.Button(frame_parametres, text="Switch Theme", command=switch_theme, font=("Helvetica", 12), bg=light_button_bg, fg="white", relief="flat", bd=0)
btn_theme.pack(pady=5)
btn_theme.bind("<Enter>", on_enter_button)
btn_theme.bind("<Leave>", on_leave_button)

# Frame pour le choix de la taille du mot de passe
frame_length = tk.Frame(frame_parametres, bg="#f5f5f5")
label_length = tk.Label(frame_length, text="Password length:", font=("Helvetica", 10), bg="#f5f5f5", fg="#333")
label_length.pack(side="left", padx=5)
spinbox_length = tk.Spinbox(frame_length, from_=8, to=64, width=5, font=("Helvetica", 10), bd=2, relief="flat", bg="#e0e0e0", fg="#333")
spinbox_length.delete(0, "end")
spinbox_length.insert(0, str(default_mdp_size))
spinbox_length.pack(side="left", padx=5)
frame_length.pack(pady=5)

# Interface utilisateur avec des couleurs modernes et sobres
label_identifiant = tk.Label(root, text="Identifier :", font=("Helvetica", 12), bg="#f5f5f5", fg="#333")
label_identifiant.pack(pady=10)

# Zone de texte pour l'identifiant avec plus de contraste
entry_identifiant = tk.Entry(root, width=30, font=("Helvetica", 12), bd=2, relief="flat", fg="#333", bg="#e0e0e0", highlightthickness=0)
entry_identifiant.pack(pady=5, padx=10)
entry_identifiant.bind("<KeyRelease>", activate_generate)  # Active le bouton "Générer" lors de la modification de l'identifiant

label_mdp = tk.Label(root, text="Password :", font=("Helvetica", 12), bg="#f5f5f5", fg="#333")
label_mdp.pack(pady=10)

# Champ de mot de passe avec icône "O" ou "X"
frame_mdp = tk.Frame(root, bg="#f5f5f5")
frame_mdp.pack(pady=10)
entry_mdp = tk.Entry(frame_mdp, width=25, font=("Helvetica", 12), show="*", bd=2, relief="flat", fg="#333", bg="#e0e0e0", highlightthickness=0)
entry_mdp.pack(side="left", padx=10)
entry_mdp.bind("<KeyRelease>", activate_generate)  # Active le bouton "Générer" lors de la modification du mot de passe

# Bouton pour afficher/masquer le mot de passe avec les caractères "O" (cacher) et "X" (afficher)
btn_toggle = tk.Button(frame_mdp, text="O", command=toggle_mdp, bd=0, bg="#A1B5C7", fg="white", font=("Helvetica", 14, "bold"), relief="flat", width=3, height=1)
btn_toggle.pack(side="left")
btn_toggle.bind("<Enter>", on_enter_button)
btn_toggle.bind("<Leave>", on_leave_button)

# Frame pour le bouton générer et le bouton copier
frame_buttons = tk.Frame(root, bg="#f5f5f5")

# Bouton pour générer le mot de passe dans des tons bleu-gris avec des coins arrondis
btn_generer = tk.Button(frame_buttons, text="Generate Password", command=generate_password, font=("Helvetica", 12), bg="#A1B5C7", fg="white", relief="flat", bd=0, padx=15, pady=10, highlightthickness=0)
btn_generer.pack(side="left", padx=10)
btn_generer.bind("<Enter>", on_enter_button)
btn_generer.bind("<Leave>", on_leave_button)

# Bouton pour copier le mot de passe dans le presse-papiers
btn_copier = tk.Button(frame_buttons, text="Copy", command=copy_password, font=("Helvetica", 12), bg="#d3d3d3", fg="white", disabledforeground="white", relief="flat", bd=0, padx=10, pady=5, highlightthickness=0, state="disabled")
btn_copier.pack(side="left", padx=10)
btn_copier.bind("<Enter>", on_enter_button)
btn_copier.bind("<Leave>", on_leave_button)

frame_buttons.pack(pady=20)

# Label pour afficher le mot de passe généré
frame_resultat = tk.Frame(root, bg="#f5f5f5")
label_resultat = tk.Label(frame_resultat, text="Your Password : ", font=("Helvetica", 12), bg="#f5f5f5", fg="#333")
label_resultat.pack(side="left", padx=10)

# Bouton pour masquer/afficher le mot de passe généré
btn_afficher_masquer = tk.Button(frame_resultat, text="O", font=("Helvetica", 12), bg="#D3D3D3", fg="white", relief="flat", bd=0, padx=5, pady=5, highlightthickness=0, command=show_password, state="disabled")
btn_afficher_masquer.pack(side="left", padx=10)
btn_afficher_masquer.bind("<Enter>", on_enter_button)
btn_afficher_masquer.bind("<Leave>", on_leave_button)

frame_resultat.pack(pady=20)

# Bouton pour réinitialiser
btn_reinitialiser = tk.Button(root, text="Reset", font=("Helvetica", 12), bg="#D3D3D3", fg="white", relief="flat", bd=0, padx=10, pady=5, highlightthickness=0, command=reset)
btn_reinitialiser.pack(pady=20)
btn_reinitialiser.bind("<Enter>", on_enter_button)
btn_reinitialiser.bind("<Leave>", on_leave_button)

#touche entrer
root.bind("<Return>", on_enter)

# Lancement de la fenêtre principale
root.mainloop()
