import hashlib
import json
import random
import string

class PasswordManager:
    def __init__(self, file_path="passwords.json"):
        self.file_path = file_path
        self.passwords = self.load_passwords()

    def load_passwords(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_passwords(self):
        with open(self.file_path, "w") as file:
            json.dump(self.passwords, file)

    def check_password_requirements(self, password):
        return (
            len(password) >= 8
            and any(char.isupper() for char in password)
            and any(char.islower() for char in password)
            and any(char.isdigit() for char in password)
            and any(char in "!@#$%^&*" for char in password)
        )

    def encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_random_password(self):
        # Générer un mot de passe aléatoire qui respecte les exigences
        length = random.randint(8, 12)
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(random.choice(chars) for _ in range(length))

        # Vérifier si le mot de passe généré respecte les exigences
        while not self.check_password_requirements(password):
            password = "".join(random.choice(chars) for _ in range(length))

        return password

    def add_password(self, username, password=None):
        if password is None:
            password = self.generate_random_password()

        if username in self.passwords:
            print("Ce nom d'utilisateur a déjà un mot de passe enregistré.")
            return

        hashed_password = self.encrypt_password(password)
        self.passwords[username] = hashed_password
        self.save_passwords()
        print(f"Mot de passe enregistré avec succès pour {username}.")

    def display_passwords(self):
        if self.passwords:
            print("Mots de passe enregistrés :")
            for username, hashed_password in self.passwords.items():
                print(f"{username}: {hashed_password}")
        else:
            print("Aucun mot de passe enregistré.")

def main():
    manager = PasswordManager()

    while True:
        print("1. Ajouter un nouveau mot de passe")
        print("2. Afficher les mots de passe enregistrés")
        print("3. Quitter")

        choice = input("Choisissez une option (1, 2 ou 3) : ")

        if choice == "1":
            username = input("Entrez un nom d'utilisateur : ")
            manager.add_password(username)
        
        elif choice == "2":
            manager.display_passwords()

        elif choice == "3":
            break

        else:
            print("Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    main()