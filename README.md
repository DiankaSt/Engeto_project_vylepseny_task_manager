Vylepšený Task Manager – Dokumentace
Popis projektu
Tento projekt rozšiřuje správce úkolů o připojení k MySQL databázi, ukládání úkolů a podporu CRUD operací (Create, Read, Update, Delete). Projekt obsahuje dvě hlavní části:

- vylepseny_task_manager.py: hlavní aplikace pro správu úkolů
- test_vylepseny_task_manager.py: automatizované testy pomocí pytest a MySQL
Použité technologie
- Python 3.10+
- MySQL Workbench
- Knihovna mysql-connector-python
- pytest
Struktura databáze
V MySQL Workbench si vytvořte databázi a tabulku ukoly s následující strukturou:
CREATE DATABASE spravce_ukolu;

CREATE TABLE spravce_ukolu.ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT,
    stav ENUM('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno',
    datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
Instalace závislostí
Vytvořte si virtuální prostředí a nainstalujte požadované knihovny:
python -m venv .venv
source .venv/bin/activate     (Linux/macOS)
.venv\Scripts\activate       (Windows)

pip install mysql-connector-python pytest
Spuštění aplikace
Hlavní skript spustíte příkazem:

python vylepseny_task_manager.py

Aplikace zobrazí menu a umožní přidat, zobrazit, aktualizovat nebo odstranit úkoly.
Automatizované testy
Testy najdete v souboru test_vylepseny_task_manager.py. Spuštění testů:

pytest test_vylepseny_task_manager.py

Testy pracují s testovací databází a po testech automaticky odstraňují testovací data.
