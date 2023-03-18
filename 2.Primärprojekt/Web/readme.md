# Web-Anwendung für das testen der von den Gruppen erstellten Modelle
Im Rahmen des Softwareprojekts sollte eine Webanwendung erstellt werden, über die alle trainierten Modelle getesten werden können. Diese Web-Anwendung hat die Funktion alle Modelle vergleichen zu können und lässt den Nutzer eigene Bilder hochladen.
## Inhaltsverzeichnis
1. [Allgemeine Informationen](#general-info)
2. [Funktionsweise](#technologies)
3. [Installation](#installation)
4. [Developer Team](#collaboration)
<a name="general-info"></a>
### Allgemeine Informationen
Die Web-Anwendung lässt den Nutzer zwei Bilder hochladen (Input- und Referenzbild). Notwendig für den Prozess ist jedoch nur das Inputbild, da das Referenzbild lediglich zur Ausgabe eines Fehlerwertes vom berechneten zum erwarteten Bild besteht. Der Nutzer hat darauf folgend die Möglichkeit die Modelle, sowie die Trainingssatzgröße der Modelle auszuwählen. Wenn der Nutzer mit seiner Auswahl zufrieden ist, kann er die Auswahl absenden und erhält seine Ergebnisse nach Berechnungsschluss.
<a name="technologies"></a>
### Funktionsweise
In unserem Anwendungsfall läuft der Webserver in einem Singularity-Container auf einem Server. Dieser Container ist wie folgt aufgebaut:
![Webservercontainer Aufbau](./aufbauWebServer.png)
Innerhalb des Conatiners läuft ein NPM NodeJS Server, der über das NodeJS Modul [Child Process](https://nodejs.org/api/child_process.html) (Vers.: 15.5.0) die Modell das vom Nutzer übertragene Bild vervollständigen lässt und je nach Möglichkeit den Fehlerwert berechnet.
Über das bekannte aus dem NPM Umfeld bekannte lässt sich der Web-Server starten und über den Port 3000 aufrufen.
<a name="installation"></a>
### Installation
Es handelt sich um die normale Installation über NPM. Wenn das Projekt aus dem Repository ausgecheckt wurde, müssen die Abhängigkeiten installiert werden.
```
npm install
```
Wenn dieser Vorgang abgeschlossen ist, kann der Server gestartet werden und ist damit ready to deploy.
```
npm start
```
***ACHTUNG**
Die Installation und die voreingestelleten Pfade sind für Anwendungsfall des Softwareprojektes eingestellt und sollten daher nicht außerhalb des Umfeldes verwendet werden, da für einen einwandfreien Ablauf nicht garantiert werden kann.*
<a name="collaboration"></a>
### Developer Team
by Lisa Brundert, Vanessa Dobmann, Tjark Prokoph, David Roos
