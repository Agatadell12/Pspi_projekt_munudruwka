import psycopg2
from bs4 import BeautifulSoup
import requests
import folium

#Logowanie do aplikacjii

db_params = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='Psip_2023',
    host='localhost',
    port=5432
)


#Funkcje do wyszukiwania,dodawania,aktualizowania,usuwania oddziałów oraz generowanie mapy wszystkich oddziałów

def add_unit() -> None:
    """
    Dodaj oddział do listy.
    """
    # Utwórz kursor w oparciu o db_params (uzyskasz dostęp do zmiennej globalnej)
    cursor = db_params.cursor()

    # Pobierz dane od użytkownika
    nazwa = input('Podaj nazwę oddziału:')
    city = input('Podaj nazwę miasta:')

    # Wykonaj zapytanie SQL, aby dodać nowy oddział
    sql_query = f"INSERT INTO public.oddzialy(nazwa, city) VALUES('{nazwa}', '{city}');"
    cursor.execute(sql_query)

    # Zatwierdź zmiany
    db_params.commit()

    # Zamknij kursor po użyciu
    cursor.close()



def show_unit(db_params) -> None:
    # Utwórz kursor w oparciu o db_params
    cursor = db_params.cursor()

    sql_query_1 = f"SELECT * FROM public.oddzialy;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'Oddział {row[1]} w miejscowości {row[2]}')

    # Zamknij kursor po użyciu
    cursor.close()




def remove_unit(db_params) -> None:
    """
    remove custom object from list
    :param users_list: list - user list
    :return: None
    """
    cursor = db_params.cursor()
    oddzialy = input('Podaj oddzial do usuniecia:')
    sql_query_1 = f"SELECT * FROM public.oddzialy WHERE nazwa='{oddzialy}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'znaleziono ')
    print('0: Usuń wszystkie znalezione oddziały')

    for numerek, user_to_be_removed in enumerate(query_result):
        print(f'{numerek + 1}. {user_to_be_removed}')

    numer = int(input(f'Podaj nazwę oddziału do usunięcia '))

    if numer == 0:
        sql_query_2 = f"DELETE FROM public.oddzialy;"
        cursor.execute(sql_query_2)
        db_params.commit()
    elif 0 < numer <= len(query_result):
        user_id_to_remove = query_result[numer - 1][0]
        sql_query_2 = f"DELETE FROM public.oddzialy WHERE id='{query_result[numer - 1][0]}';"
        cursor.execute(sql_query_2)
        db_params.commit()
    else:
        print('Błędny numer, nie usunięto żadnego użytkownika.')

        cursor.close()

def update_unit(db_params) -> None:
    cursor = db_params.cursor()
    unit = input("Podaj oddział do modyfikacji:")
    sql_query_1 = f"SELECT * FROM public.oddzialy WHERE nazwa ='{unit}';"
    cursor.execute(sql_query_1)
    print('Znaleziono')
    nazwa= input('Podaj nowy oddział: ')
    city = input('Podaj nazwe miasta: ')
    sql_query_2 = f"UPDATE public.oddzialy SET nazwa='{nazwa}',city='{city}' WHERE nazwa='{unit}';"
    cursor.execute(sql_query_2)
    db_params.commit()

    cursor.close()


def get_coordinate_of(city: str) -> list[float, float]:
    # Pobranie strony internetowej

    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')

    # Pobranie współrzędnych z treści strony internetowej
    latitude_elements = response_html.select('.latitude')
    longitude_elements = response_html.select('.longitude')

    if len(latitude_elements) > 1 and len(longitude_elements) > 1:
        try:
            response_html_latitude = float(latitude_elements[1].text.replace(',', '.'))
            response_html_longitude = float(longitude_elements[1].text.replace(',', '.'))
            return [response_html_latitude, response_html_longitude]
        except ValueError as e:
            print(f"Błąd konwersji współrzędnych: {e}")
    else:
        print("Błąd: Nie udało się znaleźć elementów z szerokością i długością geograficzną na stronie internetowej.")

    return [0.0, 0.0]  # Domyślne współrzędne w przypadku błędu


def get_map_of(db_params) -> None:
    cursor = db_params.cursor()
    map = folium.Map(
        location=[52.3, 21.8],
        tiles='OpenStreetMap',
        zoom_start=14, )
    sql_query_1 = f"SELECT * FROM public.oddzialy;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for user in query_result:
        folium.Marker(
            location=get_coordinate_of(city=user[2]),
            popup=f'Oddział: {user[1]}\n'
                  f'{user[2]}'
        ).add_to(map)
        map.save(f'mapka.html')

    cursor.close()

#Funkcje do wyszukiwania,dodawania,aktualizowania,usuwania pracowników ze wszytkich oddziałów oraz generowanie mapy wszystkich pracowników

def add_workers() -> None:
    """
    Dodaj oddział do listy.
    """
    # Utwórz kursor w oparciu o db_params (uzyskasz dostęp do zmiennej globalnej)
    cursor = db_params.cursor()

    # Pobierz dane od użytkownika
    imie = input('Podaj imię prawcownika:')
    nazwisko = input('Podaj nazwisko pracownika:')
    city = input('Podaj nazwę miasta:')
    stanowiskopracy = input('Podaj stanowisko pracy pracownika:')
    oddzial = input('Podaj oddzial w którym pracuje pracownik:')

    # Wykonaj zapytanie SQL, aby dodać nowy oddział
    sql_query = f"INSERT INTO public.pracownicy(imie, nazwisko, city, stanowiskopracy, oddzial) VALUES('{imie}', '{nazwisko}', '{city}','{stanowiskopracy}','{oddzial}');"
    cursor.execute(sql_query)

    # Zatwierdź zmiany
    db_params.commit()

    # Zamknij kursor po użyciu
    cursor.close()



def show_workers(db_params) -> None:
    # Utwórz kursor w oparciu o db_params
    cursor = db_params.cursor()

    sql_query_1 = f"SELECT * FROM public.pracownicy;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'{row[1]} {row[2]} z miejscowości {row[3]} pracujący na stanowisku {row[4]} w oddziale {row[5]}')

    # Zamknij kursor po użyciu
    cursor.close()




def remove_workers(db_params) -> None:
    cursor = db_params.cursor()
    nazwisko = input('Podaj nazwisko pracownika do usunięcia:')
    sql_query_1 = f"SELECT * FROM public.pracownicy WHERE nazwisko='{nazwisko}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono:')
    print('0: Usuń wszystkich znalezionych pracowników')

    for numerek, user_to_be_removed in enumerate(query_result):
        print(f'{numerek + 1}. {user_to_be_removed}')

    numer = int(input(f'Podaj numer pracownika do usunięcia '))

    if numer == 0:
        sql_query_2 = f"DELETE FROM public.pracownicy;"
        cursor.execute(sql_query_2)
        db_params.commit()
    elif 0 < numer <= len(query_result):
        user_id_to_remove = query_result[numer - 1][0]
        sql_query_2 = f"DELETE FROM public.pracownicy WHERE id='{query_result[numer - 1][0]}';"
        cursor.execute(sql_query_2)
        db_params.commit()
        print(f'Usunięto pracownika o nazwisku {nazwisko}.')
    else:
        print('Błędny numer, nie usunięto żadnego pracownika.')

    cursor.close()


def update_workers(db_params) -> None:
    cursor = db_params.cursor()
    unit = input("Podaj nazwisko pracownika do modyfikacji:")
    sql_query_1 = f"SELECT * FROM public.pracownicy WHERE nazwisko ='{unit}';"
    cursor.execute(sql_query_1)
    print('Znaleziono')
    imie= input('Podaj imię pracownika:')
    nazwisko= input('Podaj nazwisko pracownika:')
    city = input('Podaj nazwe miasta:')
    stanowiskopracy = input('Podaj stanowisko pracy:')
    oddzial = input('Podaj oddział w którym pracuje:')
    sql_query_2 = f"UPDATE public.pracownicy SET imie='{imie}',nazwisko='{nazwisko}',city='{city}',stanowiskopracy='{stanowiskopracy}',oddzial='{oddzial}' WHERE nazwisko='{unit}';"
    cursor.execute(sql_query_2)
    db_params.commit()

    cursor.close()


def get_map_of_workers(db_params) -> None:
    cursor = db_params.cursor()
    map = folium.Map(
        location=[52.3, 21.8],
        tiles='OpenStreetMap',
        zoom_start=14, )
    sql_query_1 = f"SELECT * FROM public.pracownicy;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for user in query_result:
        city = user[3]  # Zakładając, że informacja o miejscowości znajduje się w 4. kolumnie (indeks 3)
        folium.Marker(
            location=get_coordinate_of(city),
            popup=f'Pracownik: {user[1]} {user[2]}\n'
                  f'mieszka w {user[3]}'
        ).add_to(map)
    map.save(f'mapkapracownicy.html')

    cursor.close()

#Funkcje do wyszukiwania,dodawania,aktualizowania,usuwania żolnierzy którzy pobrali sorty mundurowe ze wszytkich oddziałów
###wyświetlanie dodanie, usuwanie, aktualizacja listy pracowników wybranego oddziału (musi mieć współrzędne)
#------Generowanie mapy pracowników wybranego oddziału-------


def get_map_for_department(db_params) -> None:
    cursor = db_params.cursor()
    department = input('Wpisz oddział: ')

    # Create an SQL query to retrieve employees in the specified department with their respective cities
    sql_query = sql_query = f"SELECT p.*, o.city FROM pracownicy p " \
                            f"JOIN oddzialy o ON p.oddzial = o.nazwa " \
                            f"WHERE o.nazwa = '{department}';"

    cursor.execute(sql_query)
    query_result = cursor.fetchall()

    # Check if there are any results from the database query
    if query_result:
        # Create an empty list to store unique cities for employees
        unique_cities = set()

        # Create a folium map with a default location (center of the first result)
        map = folium.Map(
            location=[0, 0],  # Default location, will be updated later
            tiles='OpenStreetMap',
            zoom_start=14
        )

        # Add markers to the map for each employee in the query result
        for employee in query_result:
            # Extract employee city
            employee_city = employee[5]  # Assuming column 7 is the city column

            # Geocode the city to obtain coordinates
            employee_coordinates = get_coordinate_of(employee_city)

            # Update the map's location based on the first result
            if map.location == [0, 0]:
                map.location = employee_coordinates

            # Add a marker for each employee
            folium.Marker(
                location=employee_coordinates,
                popup=f'Pracownik: {employee[2]} {employee[3]}\n'
                      f'Oddział: {department}\n'
                      f'Liczba postów: {employee[4]}'
            ).add_to(map)

            # Add the employee's city to the unique_cities set
            unique_cities.add(employee_city)

        # Save the generated map to an HTML file with a name based on the department
        map.save(f'map_{department}.html')

        # Print the unique cities found for the employees in the department
        print(f'Unikalne miasta pracowników w oddziale {department}: {", ".join(unique_cities)}')

    else:
        # If there are no results, print a message indicating that no map can be created
        print(f'Brak wyników zapytania dla oddziału {department}. Nie można utworzyć mapy.')



#Funkcje do wyszukiwania,dodawania,aktualizowania,usuwania żolnierzy którzy pobrali sorty mundurowe ze wszytkich oddziałów

def add_solider() -> None:
    """
    Dodaj oddział do listy.
    """
    # Utwórz kursor w oparciu o db_params (uzyskasz dostęp do zmiennej globalnej)
    cursor = db_params.cursor()

    # Pobierz dane od użytkownika
    stopien = input('Podaj stopień żołnierza:')
    imie = input('Podaj imię żołnierza:')
    nazwisko = input('Podaj nazwisko żołnierza:')
    oddzial = input('Podaj odział w którym pobrał sorty mundurowe:')
    city = input('Podaj miasto w którym pracuje żołnierz:')


    # Wykonaj zapytanie SQL, aby dodać nowy oddział
    sql_query = f"INSERT INTO public.zolnierze(stopien, imie, nazwisko, oddzial, city) VALUES('{stopien}', '{imie}', '{nazwisko}', '{oddzial}', '{city}');"
    cursor.execute(sql_query)

    # Zatwierdź zmiany
    db_params.commit()

    # Zamknij kursor po użyciu
    cursor.close()



def show_soliders(db_params) -> None:
    # Utwórz kursor w oparciu o db_params
    cursor = db_params.cursor()

    sql_query_1 = f"SELECT * FROM public.zolnierze;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'{row[1]} {row[2]} {row[3]} pobrał sorty mundurowe w oddziale {row[4]}')

    # Zamknij kursor po użyciu
    cursor.close()




def remove_soliders(db_params) -> None:
    cursor = db_params.cursor()
    nazwisko = input('Podaj nazwisko pracownika do usunięcia:')
    sql_query_1 = f"SELECT * FROM public.zolnierze WHERE nazwisko='{nazwisko}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'Znaleziono:')
    print('0: Usuń wszystkich znalezionych żołnierzy')

    for numerek, user_to_be_removed in enumerate(query_result):
        print(f'{numerek + 1}. {user_to_be_removed}')

    numer = int(input(f'Podaj numer żołnierza do usunięcia:'))

    if numer == 0:
        sql_query_2 = f"DELETE FROM public.zolnierze;"
        cursor.execute(sql_query_2)
        db_params.commit()
    elif 0 < numer <= len(query_result):
        user_id_to_remove = query_result[numer - 1][0]
        sql_query_2 = f"DELETE FROM public.zolnierze WHERE id='{query_result[numer - 1][0]}';"
        cursor.execute(sql_query_2)
        db_params.commit()
        print(f'Usunięto żołnierza o nazwisku {nazwisko}.')
    else:
        print('Błędny numer, nie usunięto żadnego żołnierza.')

    cursor.close()

#!!!!!!!!!!!!!Funkcja do poprawy!!!!!!!!
def update_soliders(db_params) -> None:
    cursor = db_params.cursor()
    unit = input("Podaj nazwisko żołnierza do modyfikacji:")
    sql_query_1 = f"SELECT * FROM public.zolnierze WHERE nazwisko ='{unit}';"
    cursor.execute(sql_query_1)
    print('Znaleziono')
    stopien = input('Podaj stopien żołnierza:')
    imie= input('Podaj imię żołnierza:')
    nazwisko= input('Podaj nazwisko żołnierza:')
    oddzial = input('Podaj oddział w którym żołnierz pobrał sorty:')
    city = input('Podaj nazwe miasta w którym żołnierz pracuje:')
    sql_query_2 = f"UPDATE public.zolnierze SET stopien = '{stopien}', imie='{imie}',nazwisko='{nazwisko}',oddzial='{oddzial}', city='{city}' WHERE nazwisko='{unit}';"
    cursor.execute(sql_query_2)
    db_params.commit()

    cursor.close()

###wyświetlanie dodanie, usuwanie, aktualizacja listy żołnierzy którzy pobrali sorty w wybranym oddziale (musi mieć współrzędne)

#_-_-_-__Generowanie mapy żołnierzy pobierających sorty z wybranego oddziału_-_-_-_-


def gui(db_params) -> None:
    while True:
        print(f'MENU\n'
              f'0: Wyświetl liste oddziałów zaopatrywania w mundury\n'
              f'1: Wyświetl liste pracowników\n'
              f'2: Wyświetl liste żołnierzy którzy pobrali sorty mundurowe\n'
              f'3: Dodaj do listy oddziałow zaopatrywania w mundury oddział\n'
              f'4: Dodaj do listy pracownika\n'
              f'5: Dodaj do listy żołnierza\n'
              f'6: Usuń z listy odziałów zaopatrywania w mundury oddział\n'
              f'7: Usuń z listy pracownika\n'
              f'8: Usuń z listy żołnierza\n'
              f'9: Aktualizuj listę oddziałów zaopatrywania w mundury\n'
              f'10: Aktualizuj listę pracowników\n'
              f'11: Aktualizuj listę żołnierzy\n'
              f'12: Wygeneruj mapę wszystkich oddziałów\n'
              f'13: Wygeneruj mapę wszystkich pracowników\n'
              f'14: Wygeneruj mapę pracowników z wybranego oddziału\n'
              f'15: Wyjdź')

        menu_option = input('Podaj funkcje do wywołania')
        print(f'Wybrane funkcje {menu_option}')

        match menu_option:
            case '0':
                print('Oddziały zaopatrujące żołnierzy w mundury')
                show_unit(db_params)
            case'1':
                print('Lista pracowników')
                show_workers(db_params)
            case '2':
                print('Lista żołnierzy którzy pobrali sorty mundurowe')
                show_soliders(db_params)
            case '3':
                print('Dodaj do listy nowy oddział')
                add_unit()
            case '4':
                print('Dodaj do listy nowego pracownika')
                add_workers()
            case '5':
                print('Dodaj do listy nowego żołnierza')
                add_solider()
            case '6':
                print('Usuń z listy oddział')
                remove_unit(db_params)
            case '7':
                print('Usuń z listy pracownika')
                remove_workers(db_params)
            case '8':
                print('Usuń z listy żołnierza')
                remove_soliders(db_params)
            case '9':
                print('Aktualizuj listę oddziałów zaopatrywania w mundury')
                update_unit(db_params)
            case '10':
                print('Aktualizuj listę pracowników')
                update_workers(db_params)
            case '11':
                print('Aktualizuj listę żołnierzy')
                update_soliders(db_params)
            case '12':
                print('Wygeneruj mapę wszystkich oddziałów')
                get_map_of(db_params)
            case '13':
                print('Wygeneruj mapę wszystkich pracowników')
                get_map_of_workers(db_params)
            case '14':
                print('Wygeneruj mapę wszystkich pracowników z wybranego oddziału')
                get_map_for_department(db_params)
            case '15':
                print('Kończę pracę')
                break

gui(db_params)

