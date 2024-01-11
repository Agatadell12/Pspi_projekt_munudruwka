from psycopg2 import cursor
import psycopg2
from bs4 import BeautifulSoup
import requests
import folium

db_params = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='Psip_2023',
    host='localhost',
    port=5432
)



# Funkcje aplikacji

def add_unit() -> None:
    """
    Dodaj oddział do listy.
    """
    # Utwórz kursor w oparciu o db_params (uzyskasz dostęp do zmiennej globalnej)
    cursor = db_params.cursor()

    # Pobierz dane od użytkownika
    oddzial = input('Podaj nazwę oddziału:')
    miejscowosc = input('Podaj nazwę miasta:')

    # Wykonaj zapytanie SQL, aby dodać nowy oddział
    sql_query = f"INSERT INTO public.mudnurowki(oddzial, miejscowosc) VALUES('{oddzial}', '{miejscowosc}');"
    cursor.execute(sql_query)

    # Zatwierdź zmiany
    db_params.commit()

    # Zamknij kursor po użyciu
    cursor.close()



def gui(db_params) -> None:
    while True:
        print(f'MENU\n'
              f'0: Wyświetl liste oddziałów zaopatrywania w mundury\n'
              f'1: Dodaj do listy oddziałow zaopatrywania w mundury oddział\n'
              f'2: Usuń z listy odziałów zaopatrywania w mundury oddział\n'
              f'3: Aktualizuj listę oddziałów zaopatrywania w mundury\n'
              f'4: Wygeneruj mapę wszystkich oddziałów\n'
              f'5: Wyjdź')

        menu_option = input('Podaj funkcje do wywołania')
        print(f'Wybrane funkcje {menu_option}')

        match menu_option:
            case '0':
                print('Wyświetl liste oddziałów zaopatrywania w mundury')
                show_unit(db_params)
            case '1':
                print('Dodaj do listy oddziałow zaopatrywania w mundury oddział')
                add_unit()
            case '2':
                print('Usuń z listy odziałów zaopatrywania w mundury oddział')
                remove_unit()
            case '3':
                print('Aktualizuj listę oddziałów zaopatrywania w mundury')
                update_unit()
            case '4':
                print('Wygeneruj mapę wszystkich oddziałów')
                get_map_of()
            case '5':
                print('Kończę pracę')
                break


def show_unit(db_params) -> None:
    # Utwórz kursor w oparciu o db_params
    cursor = db_params.cursor()

    sql_query_1 = f"SELECT * FROM public.mudnurowki;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'{row[2]}')

    # Zamknij kursor po użyciu
    cursor.close()


# reszta kodu bez zmian...

# Wywołanie funkcji gui() z przekazaniem db_params jako argument
gui(db_params)



def remove_unit() -> None:
    """
    remove custom object from list
    :param users_list: list - user list
    :return: None
    """
    oddzial = input('Podaj oddzial do usuniecia:')
    sql_query_1 = f"SELECT * FROM public.mudnurowki WHERE oddzial='{oddzial}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'znaleziono ')
    print('0: usun wszystkich znalezionych użytkowników')

    for numerek, user_to_be_removed in enumerate(query_result):
        print(f'{numerek + 1}. {user_to_be_removed}')

    numer = int(input(f'Podaj użytkownika do usunięcia '))

    if numer == 0:
        sql_query_2 = f"DELETE FROM public.mudnurowki;"
        cursor.execute(sql_query_2)
        db_params.commit()
    elif 0 < numer <= len(query_result):
        user_id_to_remove = query_result[numer - 1][0]
        sql_query_2 = f"DELETE FROM public.mudnurowki WHERE id='{query_result[numer - 1][0]}';"
        cursor.execute(sql_query_2)
        db_params.commit()
    else:
        print('Błędny numer, nie usunięto żadnego użytkownika.')

def update_unit() -> None:
    unit = input("Podaj oddział do modyfikacji:")
    sql_query_1 = f"SELECT * FROM public.mudnurowki WHERE oddzial='{unit}';"
    cursor.execute(sql_query_1)
    print('Znaleziono')
    oddzial = input('Podaj nowy oddział: ')
    miejscowosc = input('Podaj nazwe miasta: ')
    sql_query_2 = f"UPDATE public.mudnurowki SET oddzial='{oddzial}',miejscowosc='{miejscowosc}' WHERE oddzial='{unit}';"
    cursor.execute(sql_query_2)
    db_params.commit()

def get_cooordinate_of(city: str) -> list[float, float]:
    # pobranie strony internetowej

    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adres_URL) #zwraca obiekty
    response_html = BeautifulSoup(response.text, 'html.parser')

    # pobranie współrzędnych z treści strony internetowej
    response_html_latitude = response_html.select('.latitude')[1].text  # . ponieważ class
    response_html_latitude = float(response_html_latitude.replace(',', '.'))

    response_html_longitude = response_html.select('.longitude')[1].text  # . ponieważ class
    response_html_longitude = float(response_html_longitude.replace(',', '.'))

    return [response_html_latitude, response_html_longitude]

def get_map_of() -> None:
    map = folium.Map(
        location=[52.3, 21.8],
        tiles='OpenStreetMap',
        zoom_start=14, )
    sql_query_1 = f"SELECT * FROM public.mudnurowki;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for user in query_result:
        folium.Marker(
            location=get_cooordinate_of(miejscowosc=user[1]),
            popup=f'Użytkownik: {user[2]}\n'
                  f'Liczba postów {user[4]}'
        ).add_to(map)
        map.save(f'mapka.html')


gui()

