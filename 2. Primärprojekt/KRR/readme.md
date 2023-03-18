# Kernel Ridge Regression
Implementierung der Developer-Gruppe "KRR" eines Kernel Ridge Regression Ansatzes zur Bilderweiterung eines gegebenen Bild-Inputs.
## Inhaltsverzeichnis
1. [Kurzerklärung von KRR](#info)
2. [Projektaufbau](#aufbau)
    1. [Abhängigkeiten](#abhängigkeiten)
    2. [Dateiaufteilung](#aufteilung)
3. [Developer Team](#team)
<a name="info"></a>
## Kurzerklärung von KRR
Kernel Ridge Regression ist im Grunde eine Kombination aus der [Linearen Regression](https://de.wikipedia.org/wiki/Lineare_Regression),
[L2-Regularisierung](https://en.wikipedia.org/wiki/Regularization_(mathematics)) und dem [Kernel-Trick](https://en.wikipedia.org/wiki/Kernel_method).
Grundlegend wird versucht durch Anwendung von Kernel-Methoden eine Lineare Regression durch einen Datensatz durchzuführen, wobei die Regularisierung 
durch den L2-Ansatz realisiert wird.
<a name="aufbau"></a>
## Projektaufbau
Grundsätzlich besteht das Modell aus drei Bestandteilen. Angefangen mit der Normalisierung des Datensatzes, 
gefolgt von der Anwendung eines Linearen Kernels zur "hochdimensionierung". Zuletzt folgt eine Lineare Regression der Daten.
<a name="abhängigkeiten"></a>
### Abhängigkeiten
Das Projekt wird durch das [Falkon Framework](https://github.com/FalkonML/falkon) realisiert, welches für Mulit-GPU Usage optimiert wurde. Falkon kann durch Optimierungen und Annäherungen einen Performace-Vorteil gegenüber anderen Ansätzen verschaffen, worduch es besonders für das Thema Bilderweiterung interessant ist.
<a name="aufteilung"></a>
### Dateiaufteilung
Das Projekt wird in vier Teile geteilt. Das KRR-Modell wird einerseits durch ein Python-Script erstellt, dann durch ein 
anderes trainiert und zuletzt kann das trainierte Modell durch ein weiteres Script abgerufen und verwendet werden. Außerdem kann ein sogenanntes Hypertuning durchgeführt werden, um anhand mehrerer im Vorweg defenierter Parameter das beste Modell anhand der Frobenius Norm der Abweichung der Bilder zu finden.
<a name="team"></a>
## Developer Team
Tjark Prokoph, Niclas Zeiss und Fynn Thiem
