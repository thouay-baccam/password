import hashlib
import json
import random
import string

class GestionMotDePasse:
    def __init__(self, chemin_fichier="passwords.json"):
        self.chemin_fichier = chemin_fichier
        self.mots_de_passe = self.charger()

    def charger(self):
        try:
            with open(self.chemin_fichier, "r") as fichier:
                return json.load(fichier)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def sauvegarder(self):
        with open(self.chemin_fichier, "w") as fichier:
            json.dump(self.mots_de_passe, fichier)

    def verif_exigences(self, mdp):
        return (
            len(mdp) >= 8
            and any(char.isupper() for char in mdp)
            and any(char.islower() for char in mdp)
            and any(char.isdigit() for char in mdp)
            and any(char in "!@#$%^&*" for char in mdp)
        )

    def encrypter(self, mdp):
        return hashlib.sha256(mdp.encode()).hexdigest()

    def gen_mdp_alea(self):
        longueur = random.randint(8, 12)
        caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
        mdp = "".join(random.choice(caracteres) for _ in range(longueur))

        while not self.verif_exigences(mdp):
            mdp = "".join(random.choice(caracteres) for _ in range(longueur))

        return mdp

    def ajoutmdp(self, utilisateur, mdp=None):
        if mdp is None:
            mdp = self.gen_mdp_alea()

        if utilisateur in self.mots_de_passe:
            print("Cet utilisateur a déjà un mot de passe enregistré.")
            return

        if self.verif_exigences(mdp):
            mdp_crypte = self.encrypter(mdp)
            self.mots_de_passe[utilisateur] = mdp_crypte
            self.sauvegarder()
            print(f"Mot de passe enregistré avec succès pour {utilisateur}.")
        else:
            print("Le mot de passe généré ne respecte pas les exigences de sécurité. Veuillez réessayer.")

    def affichermotsdepasse(self):
        if self.mots_de_passe:
            print("Mots de passe enregistrés :")
            for utilisateur, mdp_crypte in self.mots_de_passe.items():
                print(f"{utilisateur}: {mdp_crypte}")
        else:
            print("Aucun mot de passe enregistré.")

def main():
    gestionnaire = GestionMotDePasse()

    while True:
        print("1. Ajouter un nouveau mot de passe")
        print("2. Afficher les mots de passe enregistrés")
        print("3. Quitter")

        choix = input("Choisissez une option (1, 2 ou 3) : ")

        if choix == "1":
            utilisateur = input("Nom d'utilisateur : ")
            gestionnaire.ajoutmdp(utilisateur)
        
        elif choix == "2":
            gestionnaire.affichermotsdepasse()

        elif choix == "3":
            break

        else:
            print("Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    main()