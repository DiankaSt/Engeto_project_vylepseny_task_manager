import pytest
from unittest.mock import patch
from vylepseny_task_manager import (
    pripojeni_test_db,
    vytvoreni_tabulky,
    vycisti_tabulku,
    pridat_ukol_do_db,
    ukol_existuje,
    aktualizovat_ukol,
    odstranit_ukol,
    zobrazit_ukoly
)
from mysql.connector.errors import DatabaseError


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Fixture pro nastavení a vyčištění testovací databáze před a po každém testu.
    Zajišťuje čisté prostředí pro každý test.
    """
    con = pripojeni_test_db()
    if con:
        vytvoreni_tabulky(con)
        vycisti_tabulku()
        yield  # Toto je místo, kde se provede samotný test
        vycisti_tabulku()
        con.close()


def test_pridat_ukol_pozitivni():
    """
    Testuje úspěšné přidání úkolu do databáze pomocí funkce pridat_ukol_do_db.
    """
    con = pripojeni_test_db()
    pridat_ukol_do_db(con, "Test úkol", "Test popis")
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Test úkol",))
        vysledek = cursor.fetchone()
    assert vysledek is not None
    assert vysledek[2] == "Test popis"


def test_pridat_ukol_negativni():
    """
    Testuje chování databáze při pokusu o přidání úkolu s chybějícím názvem (NOT NULL constraint).
    """
    con = pripojeni_test_db()
    with pytest.raises(DatabaseError):
        with con.cursor() as cursor:
            cursor.execute("INSERT INTO ukoly (popis) VALUES (%s)", ("Chybějící název",))
            con.commit()


@patch('vylepseny_task_manager.zobrazit_ukoly')  # Mockujeme volání zobrazit_ukoly, aby nezasahovalo do výstupu testu
def test_aktualizovat_ukol_pozitivni(mock_zobrazit_ukoly, mocker):
    """
    Testuje úspěšnou aktualizaci stavu úkolu pomocí funkce aktualizovat_ukol.
    Simuluje uživatelský vstup.
    """
    con = pripojeni_test_db()  # Pozor, překlep v původním kódu
    pridat_ukol_do_db(con, "Úkol k aktualizaci", "Původní popis")

    with con.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol k aktualizaci",))
        ukol_id = cursor.fetchone()[0]

    # Simulace uživatelského vstupu: ID úkolu a nový stav
    mocker.patch('builtins.input', side_effect=[str(ukol_id), 'hotovo'])

    # Volání TVOJÍ funkce pro aktualizaci úkolu
    aktualizovat_ukol(con)

    # Kontrola stavu úkolu přímo v databázi
    with con.cursor() as cursor:
        cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
        aktualizovany_stav = cursor.fetchone()[0]
    assert aktualizovany_stav == "hotovo"


@patch('vylepseny_task_manager.zobrazit_ukoly')  # Mockujeme volání zobrazit_ukoly
def test_aktualizovat_ukol_negativni_neexistujici_id(mock_zobrazit_ukoly, mocker, capsys):
    """
    Testuje chování funkce aktualizovat_ukol při pokusu o aktualizaci úkolu s neexistujícím ID.
    Ověřuje, zda program vypíše správnou chybovou zprávu.
    """
    con = pripojeni_test_db()

    # Simulace uživatelského vstupu: neexistující ID úkolu
    mocker.patch('builtins.input', side_effect=['9999', 'hotovo'])

    # Volání funkce pro aktualizaci úkolu
    aktualizovat_ukol(con)

    # Zachycení výstupu do konzole a kontrola chybové zprávy
    captured = capsys.readouterr()
    assert "Úkol s tímto ID neexistuje." in captured.out


@patch('vylepseny_task_manager.zobrazit_ukoly')  # Mockujeme volání zobrazit_ukoly
def test_aktualizovat_ukol_negativni_neplatny_stav(mock_zobrazit_ukoly, mocker, capsys):
    """
    Testuje chování funkce aktualizovat_ukol při pokusu o nastavení neplatného stavu.
    Ověřuje, zda program vypíše správnou chybovou zprávu a stav úkolu se nezmění.
    """
    con = pripojeni_test_db()
    pridat_ukol_do_db(con, "Úkol pro neplatný stav", "Popis")

    with con.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol pro neplatný stav",))
        ukol_id = cursor.fetchone()[0]

    # Simulace uživatelského vstupu: platné ID, ale neplatný stav
    mocker.patch('builtins.input', side_effect=[str(ukol_id), 'nesmysl'])

    # Volání funkce pro aktualizaci úkolu
    aktualizovat_ukol(con)

    # Zachycení výstupu a kontrola chybové zprávy
    captured = capsys.readouterr()
    assert "Neplatný stav." in captured.out

    # Ověření, že se stav úkolu nezměnil
    with con.cursor() as cursor:
        cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
        stav_po_pokusu = cursor.fetchone()[0]
    assert stav_po_pokusu == 'nezahájeno'  # Předpokládáme výchozí stav


@patch('vylepseny_task_manager.zobrazit_ukoly')  # Mockujeme volání zobrazit_ukoly
def test_odstranit_ukol_pozitivni(mock_zobrazit_ukoly, mocker):
    """
    Testuje úspěšné odstranění úkolu pomocí funkce odstranit_ukol.
    Simuluje uživatelský vstup.
    """
    con = pripojeni_test_db()
    pridat_ukol_do_db(con, "Úkol k odstranění", "Popis k odstranění")

    with con.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol k odstranění",))
        ukol_id = cursor.fetchone()[0]

    # Simulace uživatelského vstupu: ID úkolu k odstranění
    mocker.patch('builtins.input', side_effect=[str(ukol_id)])

    # Volání funkce pro odstranění úkolu
    odstranit_ukol(con)

    # Kontrola, zda úkol v databázi již neexistuje
    assert not ukol_existuje(con, ukol_id)


@patch('vylepseny_task_manager.zobrazit_ukoly')  # Mockujeme volání zobrazit_ukoly
def test_odstranit_ukol_negativni_neexistujici_id(mock_zobrazit_ukoly, mocker, capsys):
    """
    Testuje chování funkce odstranit_ukol při pokusu o odstranění úkolu s neexistujícím ID.
    Ověřuje, zda program vypíše správnou chybovou zprávu.
    """
    con = pripojeni_test_db()

    # Simulace uživatelského vstupu: neexistující ID úkolu
    mocker.patch('builtins.input', side_effect=['9999'])

    # Volání funkce pro odstranění úkolu
    odstranit_ukol(con)

    # Zachycení výstupu a kontrola chybové zprávy
    captured = capsys.readouterr()
    assert "Úkol s tímto ID neexistuje." in captured.out

    # Doplňková kontrola, že úkol s daným ID skutečně neexistuje
    assert not ukol_existuje(con, 9999)

def test_zobrazit_ukoly_vypisuje_pridany_ukol(capsys):
    """
    Testuje, že funkce zobrazit_ukoly vypíše správně přidaný úkol do konzole.
    """
    con = pripojeni_test_db()
    pridat_ukol_do_db(con, "Zobrazit test", "Popis zobrazení")

    # Spustíme funkci, která vypisuje do konzole
    zobrazit_ukoly(con)

    # Zachytíme výstup do konzole a ověříme, že obsahuje název úkolu
    captured = capsys.readouterr()
    assert "Zobrazit test" in captured.out
    assert "Popis zobrazení" in captured.out


