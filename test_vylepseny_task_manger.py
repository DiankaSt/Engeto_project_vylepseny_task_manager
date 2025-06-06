import pytest
from vylepseny_task_manager import (
    pripojeni_test_db,
    vytvoreni_tabulky,
    vycisti_tabulku,
    pridat_ukol_do_db,
    ukol_existuje
)
from mysql.connector.errors import DatabaseError

@pytest.fixture(autouse=True)
def setup_and_teardown():
    con = pripojeni_test_db()
    if con:
        vytvoreni_tabulky(con)
        vycisti_tabulku()
        yield
        vycisti_tabulku()
        con.close()

def test_pridat_ukol_pozitivni():
    con = pripojeni_test_db()
    pridat_ukol_do_db(con, "Test úkol", "Test popis")
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Test úkol",))
        vysledek = cursor.fetchone()
    con.close()
    assert vysledek is not None
    assert vysledek[2] == "Test popis"

def test_pridat_ukol_negativni():
    con = pripojeni_test_db()
    with pytest.raises(DatabaseError):
        with con.cursor() as cursor:
            cursor.execute("INSERT INTO ukoly (popis) VALUES (%s)", ("Chybějící název",))
            con.commit()
    con.close()

def test_aktualizovat_ukol_pozitivni():
    con = pripojeni_test_db()
    pridat_ukol_do_db(con, "Úkol", "Popis")
    with con.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol",))
        ukol_id = cursor.fetchone()[0]
        cursor.execute("UPDATE ukoly SET stav = 'hotovo' WHERE id = %s", (ukol_id,))
        con.commit()
        cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
        vysledek = cursor.fetchone()[0]
    con.close()
    assert vysledek == "hotovo"

def test_aktualizovat_ukol_negativni():
    con = pripojeni_test_db()
    with con.cursor() as cursor:
        cursor.execute("UPDATE ukoly SET stav = 'hotovo' WHERE id = -1")
        con.commit()
        cursor.execute("SELECT * FROM ukoly WHERE id = -1")
        vysledek = cursor.fetchone()
    con.close()
    assert vysledek is None

def test_odstranit_ukol_pozitivni():
    con = pripojeni_test_db()
    pridat_ukol_do_db(con, "Smazat", "Popis")
    with con.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Smazat",))
        ukol_id = cursor.fetchone()[0]
        cursor.execute("DELETE FROM ukoly WHERE id = %s", (ukol_id,))
        con.commit()
        cursor.execute("SELECT * FROM ukoly WHERE id = %s", (ukol_id,))
        vysledek = cursor.fetchone()
    con.close()
    assert vysledek is None

def test_odstranit_ukol_negativni():
    con = pripojeni_test_db()
    with con.cursor() as cursor:
        cursor.execute("DELETE FROM ukoly WHERE id = -999")
        con.commit()
    con.close()
    assert True
