import hashlib

TAILLE_MDP = 23
CAR = list('!@#$%^&*()1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')  # len = 72
N = len(CAR)

def deterministic_hash(value):
    return int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16)

identifiant = input("Identifiant : ")
mot_de_passe = input("Mot de passe : ")
    
hash_id = abs(deterministic_hash(identifiant))
hash_mdp = abs(deterministic_hash(mot_de_passe))

hash_mdp = hash_mdp * 2 + hash_id ** 2
while len(str(abs(hash_mdp))) < TAILLE_MDP * 10 :
    hash_mdp = hash_mdp * 2 + hash_id ** 2

tab_mdp = [int(str(hash_mdp)[i:i+2]) for i in range(len(str(hash_mdp))-(TAILLE_MDP*2), len(str(hash_mdp)), 2)]
new_mdp = ""

for i in tab_mdp:
    new_mdp += str(CAR[i % N])

print("Ton mot de passe :", new_mdp[:TAILLE_MDP])