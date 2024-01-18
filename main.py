users_database = {}

def register_user(login, password):
    """
    Rejestruje nowego użytkownika w systemie.
    """
    if login in users_database:
        print("Użytkownik o podanym loginie już istnieje.")
    else:
        users_database[login] = password
        print("Użytkownik zarejestrowany pomyślnie.")

def login_user():
    """
    Loguje użytkownika do systemu.
    """
    login = input("Podaj login: ")
    password = input("Podaj hasło: ")

    if login in users_database and users_database[login] == password:
        print("Zalogowano pomyślnie.")
    else:
        print("Błąd logowania. Sprawdź login i hasło.")

# Przykłady użycia
register_user("jan_kowalski", "haslo123")
login_user()