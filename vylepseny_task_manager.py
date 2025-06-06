from datetime import datetime
from mysql.connector import connect, Error

# Připojení k produkční databázi
def pripojeni_db():
    try:
        return connect(
            host="localhost",
            user="root",
            password="1111",
            database="spravce_ukolu"
        )
    except Error as e:
        print("Chyba při připojení k databázi:", e)
        return None

# Připojení k testovací databázi (používá se v testech)
def pripojeni_test_db():
    try:
        return connect(
            host="localhost",
            user="root",
            password="1111",
            database="spravce_ukolu_test"
        )
    except Error as e:
        print("Chyba při připojení k testovací databázi:", e)
        return None

# Vytvoření tabulky (používá se v obou databázích)
def vytvoreni_tabulky(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT,
                stav ENUM('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno',
                datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()

# Vymazání všech záznamů – pro testy
def vycisti_tabulku():
    con = pripojeni_test_db()
    if con:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM ukoly")
            con.commit()
        con.close()

# Ověření existence úkolu podle ID
def ukol_existuje(connection, id_ukolu):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        return cursor.fetchone() is not None

# Přidání úkolu do databáze – využívá se i v testech
def pridat_ukol_do_db(connection, nazev, popis):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        connection.commit()

# Interaktivní přidání úkolu (přes input)
def pridat_ukol(connection):
    while True:
        nazev = input("Zadejte název úkolu: ").strip()
        if not nazev:
            print("Název nesmí být prázdný.")
            continue
        popis = input("Zadejte popis úkolu: ").strip()
        if not popis:
            print("Popis nesmí být prázdný.")
            continue
        try:
            pridat_ukol_do_db(connection, nazev, popis)
            print("Úkol byl úspěšně přidán.")
            break
        except Error as e:
            print("Chyba při přidávání úkolu:", e)
            break

# Výpis aktivních úkolů
def zobrazit_ukoly(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN ('nezahájeno', 'probíhá')")
        ukoly = cursor.fetchall()
        if not ukoly:
            print("Žádné úkoly k zobrazení.")
        else:
            print("Seznam úkolů:")
            for u in ukoly:
                print(f"ID: {u[0]}, Název: {u[1]}, Popis: {u[2]}, Stav: {u[3]}")

# Změna stavu úkolu
def aktualizovat_ukol(connection):
    zobrazit_ukoly(connection)
    try:
        id_ukolu = int(input("Zadejte ID úkolu k aktualizaci: "))
        if not ukol_existuje(connection, id_ukolu):
            print("Úkol s tímto ID neexistuje.")
            return
        novy_stav = input("Zadejte nový stav (probíhá/hotovo): ").strip().lower()
        if novy_stav not in ['probíhá', 'hotovo']:
            print("Neplatný stav.")
            return
        with connection.cursor() as cursor:
            cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
            connection.commit()
            print("Stav úkolu byl aktualizován.")
    except ValueError:
        print("Neplatné ID.")
    except Error as e:
        print("Chyba při aktualizaci:", e)

# Odstranění úkolu
def odstranit_ukol(connection):
    zobrazit_ukoly(connection)
    try:
        id_ukolu = int(input("Zadejte ID úkolu k odstranění: "))
        if not ukol_existuje(connection, id_ukolu):
            print("Úkol s tímto ID neexistuje.")
            return
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
            connection.commit()
            print("Úkol byl odstraněn.")
    except ValueError:
        print("Neplatné ID.")
    except Error as e:
        print("Chyba při odstranění:", e)

# Hlavní menu aplikace
def hlavni_menu(connection):
    while True:
        print("\nSprávce úkolů - Hlavní menu")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit")

        volba = input("Zadejte volbu (1-5): ").strip()
        if volba == "1":
            pridat_ukol(connection)
        elif volba == "2":
            zobrazit_ukoly(connection)
        elif volba == "3":
            aktualizovat_ukol(connection)
        elif volba == "4":
            odstranit_ukol(connection)
        elif volba == "5":
            print("Ukončuji program.")
            break
        else:
            print("Neplatná volba.")

# Spuštění aplikace
if __name__ == "__main__":
    conn = pripojeni_db()
    if conn:
        vytvoreni_tabulky(conn)
        hlavni_menu(conn)
        conn.close()



