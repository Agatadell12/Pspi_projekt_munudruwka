from my_fanctions import add_unit
from my_fanctions import add_workers
from my_fanctions import add_solider
from my_fanctions import add_workers_to_unit
from my_fanctions import add_soliders_to_unit
from my_fanctions import update_selected_solider_in_unit
from my_fanctions import update_unit
from my_fanctions import update_workers
from my_fanctions import update_soliders
from my_fanctions import update_selected_worker_in_unit
from my_fanctions import remove_soliders
from my_fanctions import remove_unit
from my_fanctions import remove_workers
from my_fanctions import remove_unit_and_workers
from my_fanctions import remove_unit_and_soliders
from my_fanctions import show_soliders
from my_fanctions import show_unit
from my_fanctions import show_workers
from my_fanctions import show_workers_in_selected_unit
from my_fanctions import show_soliders_in_selected_unit
import psycopg2
from bs4 import BeautifulSoup
import requests
import folium
import sys
from my_fanctions import get_map_of_workers_from
from my_fanctions import get_map_of_soliders_from
from my_fanctions import get_coordinate_of
from my_fanctions import get_map_of
from my_fanctions import get_map_of_workers
from logowanie import login

db_params = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='Psip_2023',
    host='localhost',
    port=5432
)


def add() -> None:
    while True:
        print(f'Dodawanie użytkowników\n'
              f'0: Dodaj do listy oddziałow zaopatrywania w mundury oddział\n'
              f'1: Dodaj do listy pracownika\n'
              f'2: Dodaj do listy żołnierza\n'
              f'3: Dodaj pracowników do wybranego oddziału\n'
              f'4: Dodaj żołnierza do wybranego oddziału\n'
              f'5: Powrót do okna głównego\n'
              )

        menu_option = input('Podaj funkcje do wywołania')
        print(f'Wybrane funkcje {menu_option}')

        match menu_option:
            case '0':
                print('Dodaj do listy nowy oddział')
                add_unit()
            case '1':
                print('Dodaj do listy nowego pracownika')
                add_workers()
            case '2':
                print('odaj do listy nowego żołnierza')
                add_solider()
            case '3':
                print('Dodaj pracownika do wybranego oddziału')
                add_workers_to_unit(db_params)
            case '4':
                print('Dodaj żołnierza do wybranego oddziału')
                add_soliders_to_unit(db_params)
            case '5':
                break

def show () -> None:
    while True:
        print(f'Wyświetlanie użytkowników\n'
              f'0: Wyświetl liste oddziałów zaopatrywania w mundury\n'
              f'1: Wyświetl liste pracowników\n'
              f'2: Wyświetl liste żołnierzy którzy pobrali sorty mundurowe\n'
              f'3: Wyświetl pracowników z wybranego oddziału\n'
              f'4: Wyświetl żołnierzy z wybranego oddziału\n'
              f'5: Powrót do okna głównego\n'
              )
        menu_option = input('Podaj funkcje do wywołania')
        print(f'Wybrane funkcje {menu_option}')

        match menu_option:
            case '0':
                print('Wyświetl liste oddziałów zaopatrywania w mundury')
                show_unit(db_params)
            case '1':
                print('Wyświetl liste pracowników')
                show_workers(db_params)
            case '2':
                print('Wyświetl liste żołnierzy którzy pobrali sorty mundurowe')
                show_soliders(db_params)
            case '3':
                print('Wyświetl pracowników z wybranego oddziału')
                show_workers_in_selected_unit(db_params)
            case '4':
                print('Wyświetl żołnierzy z wybranego oddziału')
                show_soliders_in_selected_unit(db_params)
            case '5':
                break

def remove() -> None:
    while True:
        print(f'Usuwanie użytkowników\n'
              f'0: Usuń z listy odziałów zaopatrywania w mundury oddział\n'
              f'1: Usuń z listy pracownika\n'
              f'2: Usuń z listy żołnierza\n'
              f'3: Usuń pracowników z wybranego oddziału\n'
              f'4: Usuń żołnierzy z wybranego oddziału\n'
              f'5: Powrót do okna głównego\n'
              )
        menu_option = input('Podaj funkcje do wywołania')
        print(f'Wybrane funkcje {menu_option}')

        match menu_option:
            case '0':
                print('Usuń z listy odziałów zaopatrywania w mundury oddział')
                remove_unit(db_params)
            case '1':
                print('Usuń z listy pracownika')
                remove_workers()
            case '2':
                print('Usuń z listy żołnierza')
                remove_soliders(db_params)
            case '3':
                print('Usuń pracowników z wybranego oddziału')
                remove_unit_and_workers(db_params)
            case '4':
                print('Usuń żołnierzy z wybranego oddziału')
                remove_unit_and_soliders(db_params)
            case '5':
                break


def update () -> None:
    while True:
        print(f'Aktualizowanie użytkowników\n'
              f'0: Aktualizuj listę oddziałów zaopatrywania w mundury\n'
              f'1: Aktualizuj listę pracowników\n'
              f'2: Aktualizuj listę żołnierzy\n'
              f'3: Aktualizuj pracowników z wybranego oddziału\n'
              f'4: Aktualizuj żołnierzy z wybranego oddziału\n'
              f'5: Powrót do okna głównego\n'
              )
        menu_option = input('Podaj funkcje do wywołania')
        print(f'Wybrane funkcje {menu_option}')

        match menu_option:
            case '0':
                print('Aktualizuj listę oddziałów zaopatrywania w mundury')
                update_unit(db_params)
            case '1':
                print('Aktualizuj listę pracowników')
                update_workers(db_params)
            case '2':
                print('Aktualizuj listę żołnierzy')
                update_soliders(db_params)
            case '3':
                print('Aktualizuj pracowników z wybranego oddziału')
                update_selected_worker_in_unit(db_params)
            case '4':
                print('Aktualizuj żołnierzy z wybranego oddziału')
                update_selected_solider_in_unit(db_params)
            case '5':
                break

def generate () -> None:
    while True:
        print(f'wygeneruj mape\n'
              f'0: Wygeneruj mapę wszystkich oddziałów\n'
              f'1: Wygeneruj mapę wszystkich pracowników\n'
              f'2: Wygeneruj mapę pracowników z wybranego oddziału\n'
              f'3: Wygeneruj mapę żołnierzy pobierających sorty z wybranego oddziału z wybranego oddziału\n'
              f'4: Powrót do okna głównego \n'
              )
        menu_option = input('Podaj funkcje do wywołania')
        print(f'Wybrane funkcje {menu_option}')

        match menu_option:
            case '0':
                print('Wygeneruj mapę wszystkich oddziałów')
                get_map_of(db_params)
            case '1':
                print('Wygeneruj mapę wszystkich pracowników')
                get_map_of_workers(db_params)
            case '2':
                print('Wygeneruj mapę pracowników z wybranego oddziału')
                selected_department = input("Podaj nazwę oddziału: ")
                get_map_of_workers_from(db_params, selected_department)
            case '3':
                print('Wygeneruj mapę żołnierzy pobierających sorty z wybranego oddziału z wybranego oddziału')
                selected_department = input("Podaj nazwę oddziału: ")
                get_map_of_soliders_from(db_params, selected_department)
            case '4':
                break

def gui(db_params) -> None:
    if login():
        while True:
            print(f'MENU\n'
                  f'0: Dodaj do listy:\n'
                  f'1: Wyświetl liste:\n'
                  f'2: Usuń z listy:\n'
                  f'3: Aktualizuj listę:\n'
                  f'4: Wygeneruj mapę:\n'
                  f'5: Wyjdź')

            menu_option = input('Podaj funkcje do wywołania')
            print(f'Wybrane funkcje {menu_option}')

            match menu_option:
                case '0':
                    print('Dodaj do listy')
                    add()
                case '1':
                    print('Wyświetl listę')
                    show()
                case '2':
                    print('Usuń z listy')
                    remove()
                case '3':
                    print('Aktualizuj listę')
                    update()
                case '4':
                    print('Wygeneruj mapę')
                    generate()
                case '5':
                    print('Kończę pracę')
                    sys.exit()
