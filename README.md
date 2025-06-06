Vylepšený Task Manager

Dokumentace Popis projektu:

 Tento projekt rozšiřuje správce úkolů o připojení k MySQL databázi, ukládání úkolů a podporu CRUD operací (Create, Read, Update, Delete).
 
Projekt obsahuje dvě hlavní části:

1.	vylepseny_task_manager.py: hlavní aplikace pro správu úkolů
2.	test_vylepseny_task_manager.py: automatizované testy pomocí pytest a MySQL

Použité technologie:

•	Python 3.10+
•	MySQL Workbench
•	Knihovna mysql-connector-python
•	Pytest

•	Struktura databáze produkční:

V MySQL Workbench se vytvoří databázi a tabulku ukoly s následující strukturou:
CREATE DATABASE spravce_ukolu; CREATE TABLE spravce_ukolu.ukoly ( id INT AUTO_INCREMENT PRIMARY KEY, nazev VARCHAR(255) NOT NULL, popis TEXT, stav ENUM('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno', datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP );

•	Struktura databáze testovací

CREATE DATABASE IF NOT EXISTS spravce_ukolu_test;

Poznámka: Před spuštěním testů je potřeba mít vytvořenou testovací databázi spravce_ukolu_test. Tabulka ukoly se v testech vytváří automaticky pomocí SQL dotazu CREATE TABLE IF NOT EXISTS.
Instalace závislostí Vytvoří se virtuální prostředí a nainstalují se požadované knihovny: python -m venv .venv
source .venv/bin/activate (Linux/macOS) .venv\Scripts\activate (Windows)
pip install mysql-connector-python pytest

Hlavní skript spustíte příkazem:

python vylepseny_task_manager.py

Zobrazí se hlavní menu aplikace pro správu úkolů a umožní přidat, zobrazit, aktualizovat nebo odstranit úkoly.

Automatizované testy

Testy najdete v souboru test_vylepseny_task_manager.py.

Testují přímo funkce z hlavního programu:

•	pridat_ukol_do_db() – přidání úkolu do databáze,
•	aktualizovat_ukol_stav() – změna stavu úkolu,
•	odstranit_ukol_z_db() – smazání úkolu.

Každá funkce má:

•	pozitivní test (ověřuje správné chování při platných vstupech),
•	negativní test (ověřuje chování při neplatných vstupech nebo neexistujících ID).

Spuštění testů:

Před spuštěním testů je nutné:

•	vytvořená testovací databázi spravce_ukolu_test,
•	vytvořená tabulka ukoly (vytváří se automaticky v testu pomocí CREATE TABLE IF NOT EXISTS).

Testy spustíš příkazem:

pytest test_vylepseny_task_manager_update.py



