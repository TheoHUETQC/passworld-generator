from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivy.graphics import Color, RoundedRectangle
import hashlib

TAILLE_MDP = 23
CAR = list('!@#$%^&*()1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')  # len = 72
N = len(CAR)
error = []

def deterministic_hash(value):
    return int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16)

class StyledButton(Button):
    """Custom Button with always-rounded corners."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.63, 0.71, 0.78, 0)  # Transparent (we draw the background manually)
        self.color = (1, 1, 1, 1)  # White text
        self.font_size = 16
        self.size_hint = (None, None)
        self.radius = [20]

        with self.canvas.before:
            Color(rgba=(0.63, 0.71, 0.78, 1))  # Blue-gray color
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=self.radius)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        """Update the size and position of the background rectangle."""
        self.rect.pos = self.pos
        self.rect.size = self.size

class GenerateurMDP(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        # GridLayout pour aligner les labels et champs de saisie
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Champ pour l'identifiant
        self.identifiant_label = Label(text="Identifiant :", font_size=16, size_hint_y=None, height=30)
        self.identifiant_input = TextInput(hint_text="Entrez votre identifiant", multiline=False, size_hint_y=None, height=40)

        form_layout.add_widget(self.identifiant_label)
        form_layout.add_widget(self.identifiant_input)

        # Champ pour le mot de passe avec bouton Afficher/Masquer
        self.mdp_label = Label(text="Mot de Passe :", font_size=16, size_hint_y=None, height=30)
        self.mdp_input = TextInput(hint_text="Entrez votre mot de passe", multiline=False, password=True, size_hint_y=None, height=40)

        self.mdp_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.mdp_toggle_button = StyledButton(text="O", size=(40, 40))  # Small button for toggle
        self.mdp_toggle_button.bind(on_press=self.toggle_mdp_input)

        self.mdp_layout.add_widget(self.mdp_input)
        self.mdp_layout.add_widget(self.mdp_toggle_button)

        form_layout.add_widget(self.mdp_label)
        form_layout.add_widget(self.mdp_layout)

        self.add_widget(form_layout)

        # Boutons
        self.generate_button = StyledButton(text="Générer le mot de passe", size=(250, 50))
        self.generate_button.bind(on_press=self.generer_mdp)
        self.add_widget(self.generate_button)

        self.copy_button = StyledButton(text="Copier", disabled=True, size=(150, 40))
        self.copy_button.bind(on_press=self.copier_mdp)
        self.add_widget(self.copy_button)

        self.toggle_button = StyledButton(text="Afficher", disabled=True, size=(150, 40))  # Restored original larger button
        self.toggle_button.bind(on_press=self.toggle_mdp_generated)
        self.add_widget(self.toggle_button)

        # Résultat
        self.result_label = Label(text="Ton mot de passe : ", font_size=16, size_hint_y=None, height=40)
        self.add_widget(self.result_label)

        # Variable pour stocker le mot de passe généré
        self.generated_mdp = ""

    def toggle_mdp_input(self, instance):
        """Afficher ou masquer le mot de passe entré par l'utilisateur."""
        if self.mdp_input.password:
            self.mdp_input.password = False
            self.mdp_toggle_button.text = "X"
        else:
            self.mdp_input.password = True
            self.mdp_toggle_button.text = "O"

    def generer_mdp(self, instance):
        identifiant = self.identifiant_input.text.strip()
        mot_de_passe = self.mdp_input.text.strip()

        if not identifiant or not mot_de_passe:
            self.result_label.text = "Erreur : Identifiant ou mot de passe manquant"
            return
        elif identifiant == "Théo" and mot_de_passe == "HUET":
            self.result_label.text = f"Erreur list : {error}"
            return
    
        hash_id = abs(deterministic_hash(identifiant))
        hash_mdp = abs(deterministic_hash(mot_de_passe))

        hash_mdp = hash_mdp * 2 + hash_id ** 2
        while len(str(abs(hash_mdp))) < TAILLE_MDP * 10 :
            hash_mdp = hash_mdp * 2 + hash_id ** 2

        tab_mdp = [int(str(hash_mdp)[i:i+2]) for i in range(len(str(hash_mdp))-(TAILLE_MDP*2), len(str(hash_mdp)), 2)]
        new_mdp = ""
        
        for i in tab_mdp :
            new_mdp += str(CAR[i % N])

        self.generated_mdp = new_mdp[:TAILLE_MDP]
        self.result_label.text = "Ton mot de passe : " + "*" * TAILLE_MDP

        # Activer les boutons Copier et Afficher/Masquer
        self.copy_button.disabled = False
        self.toggle_button.disabled = False
        self.toggle_button.text = "Afficher"

    def copier_mdp(self, instance):
        if self.generated_mdp:
            Clipboard.copy(self.generated_mdp)
            self.result_label.text = "Mot de passe copié dans le presse-papiers !"

    def toggle_mdp_generated(self, instance):
        """Afficher ou masquer le mot de passe généré."""
        if self.toggle_button.text == "Afficher":
            self.result_label.text = f"Ton mot de passe : {self.generated_mdp}"
            self.toggle_button.text = "Masquer"
        else:
            self.result_label.text = "Ton mot de passe : " + "*" * TAILLE_MDP
            self.toggle_button.text = "Afficher"

class GenerateurMDPApp(App):
    def build(self):
        return GenerateurMDP()

if __name__ == '__main__':
    GenerateurMDPApp().run()
