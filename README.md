# Vylepšený Task Manager

## Popis projektu

Tento projekt je jednoduchý správce úkolů v Pythonu s připojením na MySQL databázi. Podporuje klasické operace CRUD (vytvoření, čtení, aktualizace, mazání). Obsahuje také automatizované testy pomocí knihovny pytest.



### Hlavní soubory

| Soubor                     | Popis                         |
|----------------------------|-------------------------------|
| vylepseny_task_manager.py  | Hlavní aplikace pro správu úkolů |
| test_vylepseny_task_manager.py | Automatizované testy         |
| requirements.txt           | Seznam knihoven potřebných k běhu projektu |




### Použité technologie

- Python 3.10+
- MySQL (doporučeno: MySQL Workbench)
- mysql-connector-python
- pytest
- pytest-mock



### Databáze

Projekt používá dvě samostatné databáze:

Produkční databáze: spravce_ukolu
- Používá se při spuštění aplikace vylepseny_task_manager.py
- Vytváří se v ní tabulka ukoly automaticky při prvním spuštění


CREATE DATABASE spravce_ukolu;


Testovací databáze: spravce_ukolu_test

- Používá se výhradně při spouštění automatizovaných testů (pytest).
- Tabulka ukoly se automaticky vytvoří a vyčistí před každým testem pro zajištění izolovaného testovacího prostředí.

CREATE DATABASE IF NOT EXISTS spravce_ukolu_test;


Struktura tabulky ukoly:

CREATE TABLE IF NOT EXISTS ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    popis TEXT,
    stav ENUM('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno',
    datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);




### Instalace

1. Vytvoření virtuálního prostředí:
bash
python -m venv .venv


   Aktivace:
- Windows:
  bash
  .venv\Scripts\activate
  

2. Insatalace závislostí:
bash
pip install -r requirements.txt



### Spuštění hlavní aplikace


python vylepseny_task_manager.py


Zobrazí se hlavní menu, kde je volba:

1. Přidat úkol: Umožňuje zadat název a popis nového úkolu.
2. Zobrazit úkoly: Vypíše seznam aktivních úkolů (nezahájeno, probíhá).
3. Aktualizovat úkol: Umožňuje změnit stav existujícího úkolu na 'probíhá' nebo 'hotovo'.
4. Odstranit úkol: Trvale smaže úkol z databáze.
5. Ukončit: Ukončí aplikaci.



## Automatizované testy

Spustění příkazem:

bash
pytest test_vylepseny_task_manager.py


### Testované funkce:

- pridat_ukol_do_db(): Testováno na pozitivní přidání úkolu a na chování při pokusu o vložení nevalidních dat (např. chybějící název).
- aktualizovat_ukol(): Testováno na úspěšnou změnu stavu úkolu, pokus o aktualizaci neexistujícího úkolu a zadání neplatného stavu.
- odstranit_ukol(): Testováno na úspěšné odstranění úkolu a pokus o odstranění neexistujícího úkolu.
- ukol_existuje(): Tato pomocná funkce je implicitně testována v rámci ostatních testů.
Každá testovaná funkce zahrnuje jak pozitivní testy (ověřující správné chování), tak negativní testy (ověřující robustnost a správné ošetření chybných vstupů). Testy využívají fixture pro automatické nastavení a vyčištění testovací databáze, což zajišťuje jejich spolehlivost a izolaci.


 Poznámky

- Před spuštěním testů se ujistíme, že máme vytvořenou testovací databázi spravce_ukolu_test.
- Tabulka se vytváří automaticky (CREATE TABLE IF NOT EXISTS).


