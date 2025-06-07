Vylepšený Task Manager

Popis projektu

Tento projekt je jednoduchý správce úkolů v Pythonu s připojením na MySQL databázi. Podporuje klasické operace CRUD (vytvoření, čtení, aktualizace, mazání). Obsahuje také automatizované testy pomocí knihovny pytest.



Hlavní soubory

| Soubor                     | Popis                         |
|----------------------------|-------------------------------|
| vylepseny_task_manager.py  | Hlavní aplikace pro správu úkolů |
| test_vylepseny_task_manager.py | Automatizované testy         |
| requirements.txt           | Seznam knihoven potřebných k běhu projektu |




Použité technologie

- Python 3.10+
- MySQL (doporučeno: MySQL Workbench)
- mysql-connector-python
- pytest



Databáze

Projekt používá dvě samostatné databáze:

Produkční databáze: spravce_ukolu
- Používá se při spuštění aplikace vylepseny_task_manager.py
- Vytváří se v ní tabulka ukoly automaticky při prvním spuštění


CREATE DATABASE spravce_ukolu;


Testovací databáze: spravce_ukolu_test
- Používá se při spouštění testů (pytest)
- Tabulka ukoly se vytváří automaticky v testech

CREATE DATABASE spravce_ukolu_test;


Struktura tabulky ukoly:

CREATE TABLE IF NOT EXISTS ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT,
    stav ENUM('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno',
    datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);




Instalace

1. Vytvoření virtuálního prostředí:
bash
python -m venv .venv


1. Aktivace:
- Windows:
  bash
  .venv\Scripts\activate
  

2. Insatalace závislostí:
bash
pip install -r requirements.txt




Spuštění hlavní aplikace


python vylepseny_task_manager.py


Zobrazí se hlavní menu, kde je volba:

- přidat úkol,
- zobrazit aktivní úkoly,
- aktualizovat stav úkolu,
- odstranit úkol.



Automatizované testy

Spustění příkazem:

bash
pytest test_vylepseny_task_manager.py


Testované funkce:
- pridat_ukol_do_db()
- ukol_existuje()
- aktualizace a mazání úkolů

Každá funkce má:
- pozitivní test – ověřuje, že vše probíhá správně
- negativní test – ověřuje chování při chybných vstupech



 Poznámky

- Před spuštěním testů se ujistíme, že máme vytvořenou testovací databázi spravce_ukolu_test.
- Tabulka se vytváří automaticky (CREATE TABLE IF NOT EXISTS).


