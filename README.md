# Spritfinder-Predict

Ein kleiner Machine Learning Service zur Vorhersage von Spritpreisen auf Basis von historischen Daten von [tankerkoenig](https://tankerkoenig.de/). Es nutzt einen K-Nearest-Neighbor-Regressor um aus historischen Preisdaten der letzten Tage die durchschnittlichen Preise in einer Region vorherzusagen.

Dieses Projekt baut auf [TankDB](https://github.com/swip3798/TankDB) auf.

## Funktionsweise
Der Service erhält eine Liste aus StationsUUIDs, zusammen mit der aktuellen Position des Nutzers. Die Liste der Stationen sollten natürlich Stationen aus der Umgebung des Nutzers sein, da der Service jedoch für [spritfinder](https://github.com/swip3798/sprit-finder-app) erstellt wurde, kennt der Nutzer die Stationen in der aktuellen schon.   

Der Service lädt die Trainingsdaten aus der Datenbank und trainiert damit das KNN-Modell. Anschließend werden für die vom Nutzer gesetzte Position für jede Stunde des aktuellen Tages der durchschnittliche Preis der umliegenden Stationen des Nutzers vorhergesagt.    

Das Modell wird also für jede Request neu trainiert, da jedoch nur einige hundert Sätze an Trainingsdaten benutzt werden, ist die Laufzeit trotzdem sehr schnell (ca. 0.1s für eine Request inklusive Abfrage der Traingsdaten aus der Datenbank).   

Das Modell wird über eine einfache Rest-API aufgerufen, welche mit [Bottle](https://bottlepy.org/) und [Tornado](https://www.tornadoweb.org/) realisiert wurden. 

## Genauigkeit der Vorhersage
Aktuell gibt es zwei KNN-Modelle mit unterschiedlichen Vorteilen. Beide Modelle sind nur semi-optimal den tatsächlichen Spritpreis zu berechnen, jedoch eignen sie sich gut den allgemeinen Trend vorherzusagen, also beispielsweise wann Spritpreise am günstigsten sein werden. 

Die Modelle unterscheiden sich lediglich in der genutzten Distanzfunktion, das Hopper-Modell nutzt die Euklidische Abstandsfunktion, während das Perlman-Modell die Hamming-Funktion verwendet. Die Ergebnisse sind dabei sehr unterschiedlich (siehe Abbildungen). Perlman zeigt eine deutlich gemäßigtere Prognose, welche den allgemeinen Trend der Spritpreise zeigt, während Hopper sich deutlich mehr dem tatsächlichen Preisverlauf annähert, dabei jedoch weniger gut den allgemeinen Preis-Trend verdeutlichen kann.

![Hopper-Modell](docs/hopper.svg)
![Perlman-Modell](docs/perlman.svg)

Welches der beiden Modelle besser ist, hängt wohl von der jeweiligen Situation ab.

## Lizenz
Das Projekt selber ist unter der MIT Lizenz verfügbar, kann also gerne selber verwendet und erweitert werden. Jedoch ist zu beachten, dass die historischen Daten von Tankerkönig unter der BY-NC-SA-4.0-Lizenz zur Verfügung gestellt werden, also nur bei nichtkommerzieller Nutzung frei sind. 

## Installation
Dieses Projekt baut auf [TankDB](https://github.com/swip3798/TankDB) auf. Dabei erwartet es eine sqlite Datenbank im Verzeichnis `./docker/tankdb` vorzufinden. Diese wird mit TankDB generiert und sollte tagesaktuell sein, anderfalls werden die Vorhersagewerte verfälscht. Alternativ kann auch eine MySQL Datenbank mit TankDB genutzt werden. 

Zur Einrichtung des Services muss zunächst das Repository geklont werden. Anschließend muss im Hauptverzeichnis eine `.env`-Datei erstellt werden, welche folgende Werte beinhalten muss:
```
HTTP_ORIGIN=https://beispiel.de
MAX_STATIONS=7
```
Im Falle einer MySQL Datenbank mit TankDB müssen zusätzlich folgende Werte in der `.env`-Datei enthalten sein, sonst wird immer die sqlite Datenbank verwendet:
```
MYSQL_USER=user
MYSQL_ROOT_PASSWORD=000000000
MYSQL_PASSWORD=1111111111
MYSQL_PORT=4444
MYSQL_IP=127.0.0.1
```
Die Werte müssen natürlich dem entsprechenden Setup entsprechen. Anschließend kann der Service ganz einfach mit Docker gestartet werden. Um den Port, Log-Ordner etc. anzupassen, kann hier noch die `docker-compose.yml` Datei angepasst werden.

```
docker-compose up -d --build
```