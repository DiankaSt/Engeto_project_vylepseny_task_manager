#  Vylepšený Task Manager

##  Popis projektu

Tento projekt je správce úkolů napsaný v jazyce Python s připojením na databázi MySQL. Podporuje operace CRUD – vytvoření, čtení, aktualizaci a mazání úkolů.

Součástí projektu jsou také automatizované testy pomocí knihovny `pytest`, které ověřují správnou funkčnost základních databázových operací.

---

##  Struktura souborů

| Soubor                          | Popis                                           |
|---------------------------------|--------------------------------------------------|
| `vylepseny_task_manager.py`     | Hlavní aplikace pro správu úkolů (konzole)       |
| `test_vylepseny_task_manager.py`| Automatizované testy pomocí `pytest`             |
| `requirements.txt`              | Seznam potřebných Python balíčků                 |

---

##  Použité technologie

- Python 3.10+
- MySQL (např. pomocí MySQL Workbench)
- `mysql-connector-python`
- `pytest`

---

##  Databáze

Projekt pracuje s **jedinou databází**:

###  Databáze: `spravce_ukolu`

- Používá se jak pro hlavní aplikaci, tak pro běh testů.
- Tabulka `ukoly` se vytvoří automaticky při spuštění aplikace nebo testů.

#### Vytvoření databáze:
```sql
CREATE DATABASE spravce_ukolu;
Struktura tabulky ukoly:
sql
Zkopírovat
Upravit
CREATE TABLE IF NOT EXISTS ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT,
    stav ENUM('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno',
    datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

 Spuštění aplikace

python vylepseny_task_manager.py

Po spuštění se zobrazí hlavní menu:

Přidat úkol

Zobrazit úkoly

Aktualizovat úkol

Odstranit úkol

Ukončit aplikaci

🧪 Spuštění testů
Testy ověřují funkce pro přidávání, aktualizaci a mazání úkolů v databázi.

Spuštění:
bash

pytest test_vylepseny_task_manager.py
✅ Testované funkce
pridat_ukol_do_db()
✅ Test na úspěšné přidání úkolu
❌ Pokus o nevalidní vložení bez názvu

aktualizovat_stav_ukolu()
✅ Test úspěšné změny stavu
❌ Pokus o aktualizaci neexistujícího úkolu

odstranit_ukol_z_db()
✅ Test úspěšného odstranění úkolu
❌ Pokus o odstranění neexistujícího úkolu

ukol_existuje()
 Nepřímo testováno v rámci ostatních funkcí

Testy jsou izolované – při každém běhu se tabulka ukoly vyčistí (DELETE FROM ukoly), aby bylo prostředí vždy konzistentní.

 Requirements
Instalace knihoven:

pip install -r requirements.txt
