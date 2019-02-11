# OSD Generator
Semestrálna práca z predmetu "UNIX - vývojové prostredie"<br/>

## Popis
Program vygeneruje a vloží do videa OSD (On Screen Display) zo súboru CSV.<br/>
Predpokladané použitie je na vloženie telemetrických údajov do palubného videa z RC modelu.<br/>

## Spustenie
```
osd.py [-h] -v FILE -l FILE [-o FILE] [-t TITLE] [-i LOG_NAME,TITLE,UNIT] [-O n] [-p] [-T n] [-b n]
```
### Dostupné argumenty
```
-h, --help                      Zobrazí pomoc a skončí

-v SÚBOR, --video SÚBOR         POVINNÉ - Súbor so zdrojovým videom

-l SÚBOR, --logfile SÚBOR       POVINNÉ - Zdrojový CSV súbor

-o SÚBOR, --out SÚBOR           Cieľový súbor. Ak nezadané, použije sa "out.mp4"

-t NADPIS, --title NADPIS       Nadpis videa - zobrazený prvé 3 sekundy

-i STĹPEC,NÁZOV,JEDNOTKA, --item STĹPEC,NÁZOV,JEDNOTKA
                                Pridanie položky na zobrazenie. STĹPEC je názov stĺpca v CSV súbore.
                                NÁZOV sa zobrazý pred hodnotou, JEDNOTKA za hodnotou

                                napr.: "ALT(m),Alt,m" pridá "Alt:10m"
                                       "BatV(V),,V" pridá "12.6V"

-O n, --offset n                Posunie log oproti videu o n sekúnd. Hodnota môže byť záponá

-p, --preview                   Iba zobrazí náhľad, výsledok sa nebude ukladať

-T n, --threads n               Počet vlakien použitých na enkódovanie výstupného súboru

-b n, --bitrate n               bitrate výstupného súboru
  ```
