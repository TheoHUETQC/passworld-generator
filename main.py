import hashlib

MDP_SIZE = 23 # taille du mot de passe final que l'on souhaite
CAR = list('!@#$%^&*()1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') # liste de caractère qui composera le mot de passe generé
N = len(CAR) # len = 72

def deterministic_hash(value) : # Hashage : transforme une chaine de caractère en entier
    return int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16)

# entrée de l'utilisateur
identifier = input("Identifier : ")
mot_de_passe = input("PassWord : ")

# hashage
hash_id = abs(deterministic_hash(identifier))
hash_wp = abs(deterministic_hash(mot_de_passe))

# manipulation de l'id et le mdp hashés pour créer un grand entier unique
hash_wp = hash_wp * 2 + hash_id ** 2
while len(str(abs(hash_wp))) < MDP_SIZE * 10 :
    hash_wp = hash_wp * 2 + hash_id ** 2

# utilisation du résultat pour créer une liste d'indice de taille 2 : 24908273 -> [24, 90, 82, 73]
tab_wp = [int(str(hash_wp)[i:i+2]) for i in range(len(str(hash_wp))-(MDP_SIZE*2), len(str(hash_wp)), 2)]

# création du nouveau mot de passe en utilisant la liste d'indice pour piocher des caractères dans la liste CAR
new_wp = ""
for i in tab_wp :
    new_wp += str(CAR[i % N])

# affichage final du nouveau mot de passe
print("Ton mot de passe : ", new_wp[:MDP_SIZE])