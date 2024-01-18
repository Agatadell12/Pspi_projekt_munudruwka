import my_fanctions
users_database = {"admin": "admin123"}  # Tutaj dodaj inne pary login:hasło

def check_credentials(username, password):
    """
    Sprawdza poprawność podanych danych logowania.
    """
    return username in users_database and users_database[username] == password

def login():
    """
    Prosi użytkownika o podanie danych logowania.
    """
    while True:
        username = input("Podaj login: ")
        password = input("Podaj hasło: ")

        if check_credentials(username, password):
            print("Poprawne dane logowania.")
            return True
        else:
            print("Błędne dane logowania. Spróbuj ponownie.")

