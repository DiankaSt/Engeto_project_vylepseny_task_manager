import mysql.connector
from mysql.connector import Error
from datetime import datetime

# 1. Připojení k databázi
def pripojeni_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1111',
            database='spravce_ukolu'
        )
        return connection
    except Error as e:
        print("Chyba při připojení k databázi:", e)
        return None

# 2. Vytvoření tabulky, pokud neexistuje
def vytvoreni_tabulky(connection):
    try:
        cursor = connection.cursor()
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
    except Error as e:
        print("Chyba při vytváření tabulky:", e)

# 4. Přidání úkolu
def pridat_ukol(connection):
    cursor = connection.cursor()
    while True:
        nazev = input("Zadejte název úkolu:\n ").strip()
        if not nazev:
            print("Název nesmí být prázdný.")
            continue

        popis = input("Zadejte popis úkolu:\n ").strip()
        if not popis:
            print("Popis nesmí být prázdný.")
            continue

        try:
            cursor.execute(
                "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
                (nazev, popis)
            )
            connection.commit()
            print("Úkol byl úspěšně přidán.")
            break
        except Error as e:
            print("Chyba při vkládání úkolu:", e)
            break

# 5. Zobrazení úkolů
def zobrazit_ukoly(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT id, nazev, popis, stav FROM ukoly
            WHERE stav IN ('nezahájeno', 'probíhá')
        """)
        ukoly = cursor.fetchall()
        if not ukoly:
            print("Žádné úkoly k zobrazení.")
        else:
            print("Seznam úkolů:")
            for ukol in ukoly:
                print(f"ID: {ukol[0]}, Název: {ukol[1]}, Popis: {ukol[2]}, Stav: {ukol[3]}")
    except Error as e:
        print("Chyba při načítání úkolů:", e)

# 6. Aktualizace stavu úkolu
def aktualizovat_ukol(connection):
    zobrazit_ukoly(connection)
    cursor = connection.cursor()
    try:
        id_ukolu = int(input("Zadejte ID úkolu, který chcete aktualizovat:\n "))
        novy_stav = input("Zadejte nový stav (probíhá/hotovo):\n ").strip().lower()
        if novy_stav not in ['probíhá', 'hotovo']:
            print("Neplatný stav.")
            return

        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        if cursor.fetchone() is None:
            print("Zadané ID úkolu neexistuje.")
            return

        cursor.execute(
            "UPDATE ukoly SET stav = %s WHERE id = %s",
            (novy_stav, id_ukolu)
        )
        connection.commit()
        print("Úkol byl aktualizován.")
    except ValueError:
        print("Zadejte platné číselné ID.")
    except Error as e:
        print("Chyba při aktualizaci:", e)

# 7. Odstranění úkolu
def odstranit_ukol(connection):
    zobrazit_ukoly(connection)
    cursor = connection.cursor()
    try:
        id_ukolu = int(input("Zadejte ID úkolu, který chcete odstranit:\n "))
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        if cursor.fetchone() is None:
            print("Zadané ID úkolu neexistuje.")
            return

        cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
        connection.commit()
        print("Úkol byl odstraněn.")
    except ValueError:
        print("Zadejte platné číselné ID.")
    except Error as e:
        print("Chyba při odstraňování úkolu:", e)

# 3. Hlavní nabídka
def hlavni_menu(connection):
    while True:
        print("\nSprávce úkolů - Hlavní menu")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        volba = input("Vyberte možnost (1-5):\n ").strip()
        if volba == "1":
            pridat_ukol(connection)
        elif volba == "2":
            zobrazit_ukoly(connection)
        elif volba == "3":
            aktualizovat_ukol(connection)
        elif volba == "4":
            odstranit_ukol(connection)
        elif volba == "5":
            print("Konec programu.")
            break
        else:
            print("Neplatná volba. Zadejte prosím číslo od 1 do 5.")

# Spuštění programu
if __name__ == "__main__":
    conn = pripojeni_db()
    if conn:
        vytvoreni_tabulky(conn)
        hlavni_menu(conn)
        conn.close()
