import pandas as pd
import os
import re

# Beállítások
xls_fajl = "C:\\Users\\Kolos\\Documents\\SZRT\\Files\\tmp001.xlsx"  # Az xls fájl neve
mezon_ev = "CR_REF_INFO_USTRD"  # Az oszlop neve, amelyből az értékeket szeretnénk kiolvasni
eredeti_txt = "C:\\Users\\Kolos\\Documents\\SZRT\\Files\\erste3ut202501131.txt"  # A meglévő txt fájl neve
uj_txt = "C:\\Users\\Kolos\\Documents\\SZRT\\Files\\erste3ut202501131_uj.txt"  # Az új txt fájl neve

# Az xls fájl beolvasása
try:
    data = pd.read_excel(xls_fajl)
except FileNotFoundError:
    print(f"Nem található a megadott XLS fájl: {xls_fajl}")
    exit(1)
except Exception as e:
    print(f"Hiba történt az XLS beolvasása közben: {e}")
    exit(1)

# Ellenőrizzük, hogy az oszlop létezik-e
if mezon_ev not in data.columns:
    print(f"A megadott oszlop ({mezon_ev}) nem található az xls fájlban.")
    exit(1)

# Az oszlop értékeinek lekérdezése (X-el kezdődő azonosítók kivonása a szóközig)
def kinyer_azonositot(sor):
    match = re.match(r"X(\S*)", sor)
    return match.group(0) if match else None

azonositok = data[mezon_ev].dropna().apply(kinyer_azonositot).dropna().tolist()
azonosito_set = set(azonositok)  # Az azonosítók halmazba rendezve a gyors kereséshez


# Az eredeti txt fájl beolvasása (ANSI kódolással)
if not os.path.exists(eredeti_txt):
    print(f"Nem található a megadott txt fájl: {eredeti_txt}")
    exit(1)

try:
    with open(eredeti_txt, "r", encoding="mbcs") as file:
        sorok = file.readlines()
except Exception as e:
    print(f"Hiba történt a txt fájl beolvasása közben: {e}")
    exit(1)

# Szűrés: csak azok a sorok, amelyek tartalmazzák az Excel fájlból származó azonosítókat, sorrend megtartásával
# szurt_sorok = [sor for sor in sorok if any(azonosito in sor for azonosito in azonosito_set)]

szurt_sorok= []
for sor in sorok:
    if any(azonosito in sor for azonosito in azonosito_set):
       szurt_sorok.append(sor)


# Az új txt fájl írása (ANSI kódolással)
try:
    with open(uj_txt, "w", encoding="mbcs") as file:
        file.writelines(szurt_sorok)
    print(f"Az új txt fájl sikeresen létrejött: {uj_txt}")
except Exception as e:
    print(f"Hiba történt az új txt fájl létrehozása közben: {e}")
    exit(1)


# print(azonositok)
##for sor in szurt_sorok:
##    print(sor)