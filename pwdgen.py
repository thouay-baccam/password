import re
import hashlib
import json
import random
import string

# Fonction pour vérifier si le mot de passe respecte les exigences de sécurité
def verifmdpexigence(mdp):
    return (
        len(mdp) >= 8 and
        any(char.isupper() for char in mdp) and
        any(char.islower() for char in mdp) and
        any(char.isdigit() for char in mdp) and
        any(char in "!@#$%^&*" for char in mdp)
    )

# Fonction pour obtenir le mot de passe de l'utilisateur
def mdputilisateur():
    affexigencemdp()  # Afficher les exigences de sécurité
    while True:
        mdp = input("Choisissez un mot de passe : ")
        if verifmdpexigence(mdp):
            return mdp
        else:
            print("Le mot de passe ne respecte pas les exigences de sécurité. Veuillez réessayer.")

# Fonction pour hacher le mot de passe en utilisant l'algorithme SHA-256
def hashmdp(mdp):
    hashed_password = hashlib.sha256(mdp.encode()).hexdigest()
    return hashed_password

# Fonction pour enregistrer les mots de passe dans un fichier JSON
def mdpsauvegarde(passwords):
    with open('passwords.json', 'w') as file:
        json.dump(passwords, file)

# Fonction pour charger les mots de passe depuis le fichier JSON
def chargemdp():
    try:
        with open('passwords.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Fonction pour afficher les exigences de sécurité du mot de passe
def affexigencemdp():
    print("Exigences de sécurité du mot de passe :")
    print("1. Il doit contenir au moins huit caractères.")
    print("2. Il doit contenir au moins une lettre majuscule.")
    print("3. Il doit contenir au moins une lettre minuscule.")
    print("4. Il doit contenir au moins un chiffre.")
    print("5. Il doit contenir au moins un caractère spécial (!, @, #, $, %, ^, &, *).")

# Fonction principale
def main():
    # Charger les mots de passe existants depuis le fichier JSON
    passwords = chargemdp()

    while True:
        # Afficher le menu de choix
        print("\nMenu :")
        print("1. Ajouter un nouveau mot de passe")
        print("2. Afficher les mots de passe enregistrés")
        print("0. Quitter")

        # Obtenir le choix de l'utilisateur
        menuchoix = input("Veuillez entrer votre choix : ")

        if menuchoix == '1':
            # Ajouter un nouveau mot de passe
            user_password = mdputilisateur()
            hashed_password = hashmdp(user_password)

            # Vérifier si le mot de passe est déjà présent dans la liste
            if hashed_password not in passwords:
                # Ajouter le mot de passe à la liste
                passwords.append(hashed_password)
                # Enregistrer la liste mise à jour dans le fichier JSON
                mdpsauvegarde(passwords)
                print("Mot de passe enregistré avec succès !")
            else:
                print("Ce mot de passe existe déjà dans la base de données. Veuillez en choisir un nouveau.")
        elif menuchoix == '2':
            # Afficher les mots de passe enregistrés
            print("Mots de passe enregistrés :")
            for hashed_pass in passwords:
                print(hashed_pass)
        elif menuchoix == '0':
            # Quitter le programme si l'utilisateur choisit 0
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

# Exécuter la fonction principale si le script est exécuté directement
if __name__ == "__main__":
    main()