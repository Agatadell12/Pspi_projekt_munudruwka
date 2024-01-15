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
def add_soliders_to_unit(db_params) -> None:
    """
    Dodaj żołnierzy do wybranego oddziału.
    """
    # Utwórz kursor w oparciu o db_params (uzyskasz dostęp do zmiennej globalnej)
    cursor = db_params.cursor()

    # Pobierz nazwę oddziału od użytkownika
    nazwa_oddzialu = input('Podaj nazwę oddziału, do którego chcesz dodać żołnierza: ')

    # Sprawdź, czy oddział istnieje
    sql_check_unit = f"SELECT * FROM public.oddzialy WHERE nazwa = %s;"
    cursor.execute(sql_check_unit, (nazwa_oddzialu,))
    unit_exists = cursor.fetchone()

    if unit_exists:
        # Pobierz dane pracownika od użytkownika
        imie = input('Podaj imię pracownika: ')
        nazwisko = input('Podaj nazwisko pracownika: ')
        city_pracownika = input('Podaj miasto pracownika: ')
        stanowisko_pracy = input('Podaj stanowisko pracy pracownika: ')

        # Wykonaj zapytanie SQL, aby dodać pracownika do wybranego oddziału
        sql_query = f"INSERT INTO public.pracownicy(imie, nazwisko, city, stanowiskopracy, oddzial) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(sql_query, (imie, nazwisko, city_pracownika, stanowisko_pracy, nazwa_oddzialu))

        # Zatwierdź zmiany
        db_params.commit()
        print(f'Dodano pracownika do oddziału {nazwa_oddzialu}.')
    else:
        print(f"Oddział o nazwie {nazwa_oddzialu} nie istnieje.")

    # Zamknij kursor po użyciu
    cursor.close()
###wyświetlanie dodanie, usuwanie, aktualizacja listy pracowników wybranego oddziału (musi mieć współrzędne)

def add_workers_to_unit(db_params) -> None:
    """
    Dodaj pracowników do wybranego oddziału.
    """
    # Utwórz kursor w oparciu o db_params (uzyskasz dostęp do zmiennej globalnej)
    cursor = db_params.cursor()

    # Pobierz nazwę oddziału od użytkownika
    nazwa_oddzialu = input('Podaj nazwę oddziału, do którego chcesz dodać pracowników: ')

    # Sprawdź, czy oddział istnieje
    sql_check_unit = f"SELECT * FROM public.oddzialy WHERE nazwa = %s;"
    cursor.execute(sql_check_unit, (nazwa_oddzialu,))
    unit_exists = cursor.fetchone()

    if unit_exists:
        # Pobierz dane pracownika od użytkownika
        imie = input('Podaj imię pracownika: ')
        nazwisko = input('Podaj nazwisko pracownika: ')
        city_pracownika = input('Podaj miasto pracownika: ')
        stanowisko_pracy = input('Podaj stanowisko pracy pracownika: ')

        # Wykonaj zapytanie SQL, aby dodać pracownika do wybranego oddziału
        sql_query = f"INSERT INTO public.pracownicy(imie, nazwisko, city, stanowiskopracy, oddzial) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(sql_query, (imie, nazwisko, city_pracownika, stanowisko_pracy, nazwa_oddzialu))

        # Zatwierdź zmiany
        db_params.commit()
        print(f'Dodano pracownika do oddziału {nazwa_oddzialu}.')
    else:
        print(f"Oddział o nazwie {nazwa_oddzialu} nie istnieje.")

    # Zamknij kursor po użyciu
    cursor.close()
def show_workers_in_selected_unit(db_params) -> None:
    """
    Wyświetl pracowników w wybranym oddziale.
    """
    # Utwórz kursor w oparciu o db_params
    cursor = db_params.cursor()

    # Pobierz nazwę oddziału od użytkownika
    nazwa_oddzialu = input('Podaj nazwę oddziału, dla którego chcesz wyświetlić pracowników: ')

    # Sprawdź, czy oddział istnieje
    sql_check_unit = f"SELECT * FROM public.oddzialy WHERE nazwa = %s;"
    cursor.execute(sql_check_unit, (nazwa_oddzialu,))
    unit_exists = cursor.fetchone()

    if unit_exists:
        # Wykonaj zapytanie SQL, aby wyświetlić pracowników wybranego oddziału
        sql_query = f"SELECT imie, nazwisko, city, stanowiskopracy FROM public.pracownicy WHERE oddzial = %s;"
        cursor.execute(sql_query, (nazwa_oddzialu,))
        query_result = cursor.fetchall()

        print(f"Pracownicy w oddziale {nazwa_oddzialu}:")
        for row in query_result:
            print(f'{row[0]} {row[1]} z miejscowości {row[2]} pracujący na stanowisku {row[3]}')

    else:
        print(f"Oddział o nazwie {nazwa_oddzialu} nie istnieje.")

    # Zamknij kursor po użyciu
    cursor.close()

def remove_unit_and_workers(db_params) -> None:
    """
    Usuń oddział i jego pracowników.
    """
    cursor = db_params.cursor()

    # Pobierz nazwę oddziału od użytkownika
    nazwa_oddzialu = input('Podaj nazwę oddziału do usunięcia:')

    # Sprawdź, czy oddział istnieje
    sql_check_unit = f"SELECT * FROM public.oddzialy WHERE nazwa = %s;"
    cursor.execute(sql_check_unit, (nazwa_oddzialu,))
    unit_exists = cursor.fetchone()

    if unit_exists:
        print('Czy na pewno chcesz usunąć ten oddział wraz z pracownikami?')
        confirmation = input('Wpisz "tak", aby potwierdzić: ')

        if confirmation.lower() == 'tak':
            # Usuń pracowników przypisanych do tego oddziału
            sql_remove_workers = f"DELETE FROM public.pracownicy WHERE oddzial = %s;"
            cursor.execute(sql_remove_workers, (nazwa_oddzialu,))

            # Usuń sam oddział
            sql_remove_unit = f"DELETE FROM public.oddzialy WHERE nazwa = %s;"
            cursor.execute(sql_remove_unit, (nazwa_oddzialu,))

            db_params.commit()
            print(f'Usunięto oddział {nazwa_oddzialu} wraz z pracownikami.')
        else:
            print('Anulowano usuwanie oddziału.')
    else:
        print(f"Oddział o nazwie {nazwa_oddzialu} nie istnieje.")

    # Zamknij kursor po użyciu
    cursor.close()
def update_selected_worker_in_unit(db_params) -> None:
    cursor = db_params.cursor()

    # Pobierz nazwę oddziału od użytkownika
    nazwa_oddzialu = input("Podaj nazwę oddziału, dla którego chcesz zaktualizować pracowników:")

    # Sprawdź, czy oddział istnieje
    sql_check_unit = f"SELECT * FROM public.oddzialy WHERE nazwa = %s;"
    cursor.execute(sql_check_unit, (nazwa_oddzialu,))
    unit_exists = cursor.fetchone()

    if unit_exists:
        print('Znaleziono oddział.')

        # Wyświetl pracowników pracujących w danym oddziale
        sql_show_workers = f"SELECT * FROM public.pracownicy WHERE oddzial = %s;"
        cursor.execute(sql_show_workers, (nazwa_oddzialu,))
        workers_in_unit = cursor.fetchall()

        if not workers_in_unit:
            print(f'Brak pracowników w oddziale {nazwa_oddzialu}.')
        else:
            print(f'Pracownicy w oddziale {nazwa_oddzialu}:')
            for worker in workers_in_unit:
                print(f'{worker[1]} {worker[2]}, Stanowisko: {worker[4]}')

            # Pobierz ID pracownika do aktualizacji od użytkownika
            id_pracownika_do_aktualizacji = int(input('Podaj ID pracownika do aktualizacji: '))

            # Pobierz nowe dane od użytkownika
            nowe_stanowisko = input('Podaj nowe stanowisko pracownika (naciśnij Enter, aby pozostawić bez zmian): ')

            # Zaktualizuj dane wybranego pracownika
            sql_update_worker = "UPDATE public.pracownicy SET "
            if nowe_stanowisko:
                sql_update_worker += f"stanowiskopracy='{nowe_stanowisko}',"
            sql_update_worker = sql_update_worker.rstrip(',')  # Usuń ostatnią przecinkę
            sql_update_worker += f" WHERE id={id_pracownika_do_aktualizacji} AND oddzial='{nazwa_oddzialu}';"

            cursor.execute(sql_update_worker)
            db_params.commit()

            print(f'Zaktualizowano dane pracownika o ID {id_pracownika_do_aktualizacji} w oddziale {nazwa_oddzialu}.')
    else:
        print(f"Nie znaleziono oddziału o nazwie {nazwa_oddzialu}.")

    # Zamknij kursor po użyciu
    cursor.close()




#------Generowanie mapy pracowników wybranego oddziału-------
def get_map_of_workers_from(db_params, selected_department: str) -> None:
    cursor = db_params.cursor()

    # Pobierz id, nazwę miasta i miasto dla wybranego oddziału
    sql_query_1 = f"SELECT id, nazwa, city FROM public.oddzialy WHERE nazwa = %s;"
    cursor.execute(sql_query_1, (selected_department,))
    department_result = cursor.fetchone()

    if department_result:
        id, nazwa, city = department_result

        # Utwórz mapę z danymi oddziału
        map = folium.Map(
            location=get_coordinate_of(city),
            tiles='OpenStreetMap',
            zoom_start=14
        )

        # Pobierz pracowników dla danego oddziału
        sql_query_2 = f"SELECT * FROM public.pracownicy WHERE oddzial = %s;"
        cursor.execute(sql_query_2, (nazwa,))
        query_result = cursor.fetchall()

        # Dodaj znaczniki pracowników do mapy
        for user in query_result:
            city = user[3]
            folium.Marker(
                location=get_coordinate_of(city),
                popup=f'Pracownik: {user[1]} {user[2]}\n'
                      f'mieszka w {user[3]}'
            ).add_to(map)

        # Zapisz mapę do pliku HTML
        map.save(f'Mapa_{nazwa}_pracownicy.html')
    else:
        print(f"Nie znaleziono oddziału o nazwie {selected_department}.")

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
              f'15: Dodaj pracowników do wybranego oddziału\n'
              f'16: Pokaż użytkowników z wybranego oddziału\n'
              f'17: Usuń pracowników z wybranego oddziału\n'
              f'18: Aktualizuj pracowników z wybranego oddziału\n'
              f'19: Wyjdź')

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
                selected_department = input("Podaj nazwę oddziału: ")
                get_map_of_workers_from(db_params, selected_department)
            case '15':
                print('Dodaj użytkowników z wybranego oddziału')
                add_workers_to_unit(db_params)
            case '16':
                print('Pokaż użytkowników z wybranego oddziału')
                show_workers_in_selected_unit(db_params)
            case '17':
                print('Usuń użytkowników z wybranego oddziału')
                remove_unit_and_workers(db_params)
            case '18':
                print('Aktualizuj użytkowników z wybranego oddziału')
                update_selected_worker_in_unit(db_params)
            case '19':
                print('Kończę pracę')
                break

gui(db_params)

