import pytest
import mysql.connector
from mysql.connector.errors import DatabaseError


from vylepseny_task_manager import (
    pridat_ukol_do_db,
    aktualizovat_stav_ukolu,
    odstranit_ukol_z_db,
)

def pripojeni_test_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="spravce_ukolu_test"
    )

@pytest.fixture(autouse=True)
def setup_and_teardown():
    vytvor_tabulku()
    vycisti_tabulku()
    yield
    vycisti_tabulku()

def vytvor_tabulku():
    con = pripojeni_test_db()
    with con.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT,
                stav ENUM('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno',
                datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        con.commit()
    con.close()

def vycisti_tabulku():
    con = pripojeni_test_db()
    with con.cursor() as cursor:
        cursor.execute("DELETE FROM ukoly")
        con.commit()
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
            cursor.execute("INSERT INTO ukoly (popis) VALUES (%s)", ("Chybí název",))
            con.commit()
    con.close()

def test_aktualizovat_ukol_pozitivni():
    con = pripojeni_test_db()
    pridat_ukol_do_db(con, "Aktualizační úkol", "Popis")
    with con.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Aktualizační úkol",))
        ukol_id = cursor.fetchone()[0]
    aktualizovat_stav_ukolu(con, ukol_id, "hotovo")
    with con.cursor() as cursor:
        cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
        stav = cursor.fetchone()[0]
    con.close()
    assert stav == "hotovo"

def test_aktualizovat_ukol_negativni():
    con = pripojeni_test_db()
    aktualizovat_stav_ukolu(con, -1, "hotovo")
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM ukoly WHERE id = -1")
        vysledek = cursor.fetchone()
    con.close()
    assert vysledek is None

def test_odstranit_ukol_pozitivni():
    con = pripojeni_test_db()
    pridat_ukol_do_db(con, "Smazat mě", "Popis")
    with con.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Smazat mě",))
        ukol_id = cursor.fetchone()[0]
    odstranit_ukol_z_db(con, ukol_id)
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM ukoly WHERE id = %s", (ukol_id,))
        vysledek = cursor.fetchone()
    con.close()
    assert vysledek is None

def test_odstranit_ukol_negativni():
    con = pripojeni_test_db()
    odstranit_ukol_z_db(con, -999)
    con.close()
    assert True
