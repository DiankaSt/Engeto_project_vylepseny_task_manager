import mysql.connector
import pytest

def pripojeni_test_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="spravce_ukolu_test"
    )

@pytest.fixture(autouse=True)
def setup_and_teardown():
    vycisti_tabulku()
    yield
    vycisti_tabulku()

def vycisti_tabulku():
    con = pripojeni_test_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM ukoly")
    con.commit()
    con.close()

def test_pridat_ukol_pozitivni():
    con = pripojeni_test_db()
    cursor = con.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Test úkol", "Popis"))
    con.commit()
    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Test úkol",))
    vysledek = cursor.fetchone()
    con.close()
    assert vysledek is not None
    assert vysledek[1] == "Test úkol"

def test_pridat_ukol_negativni():
    con = pripojeni_test_db()
    cursor = con.cursor()
    with pytest.raises(mysql.connector.Error):
        cursor.execute("INSERT INTO ukoly (popis) VALUES (%s)", ("Chybný",))
        con.commit()
    con.close()

def test_aktualizovat_ukol_pozitivni():
    con = pripojeni_test_db()
    cursor = con.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Úkol", "Popis"))
    con.commit()
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
    cursor = con.cursor()
    cursor.execute("UPDATE ukoly SET stav = 'hotovo' WHERE id = -1")
    con.commit()
    cursor.execute("SELECT * FROM ukoly WHERE id = -1")
    vysledek = cursor.fetchone()
    con.close()
    assert vysledek is None

def test_odstranit_ukol_pozitivni():
    con = pripojeni_test_db()
    cursor = con.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Smazat", "Popis"))
    con.commit()
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
    cursor = con.cursor()
    cursor.execute("DELETE FROM ukoly WHERE id = -999")
    con.commit()
    con.close()
    assert True
