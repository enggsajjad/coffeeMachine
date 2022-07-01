# LaTeX-Projekt Vorlage für VS-Code

Die Vorlage beinhaltet 
- [LaTeX-Projekt Vorlage für VS-Code](#latex-projekt-vorlage-f%C3%BCr-vs-code)
- [Vorlagen](#vorlagen)
- [MakeFile für Vektorgraphiken](#makefile-f%C3%BCr-vektorgraphiken)
- [Optionen für MakeSupport.sty](#optionen-f%C3%BCr-makesupportsty)
  
aber benötigt die Erweiterung LaTex Workshop.

# Vorlagen

Im Ordner [Config](./.config/) befinden sich Vorlagen für LaTeX-Reports und LaTeX-Beamer-Präsentationen. Mithilfe dieser Vorlagen und dem MakeFile können durch

`make newTex <name>` ( bzw. `make newBeamer <name>` )

neue Ordner mit dem Namen \<name\> und den jeweiligen Vorlagen als Inhalt erzeugt werden.

# MakeFile für Vektorgraphiken

Da .eps und .svg Dateien nicht direkt in LaTeX eingefügt werden können, wird epstopdf bzw. inkscape genutzt um diese Dateien in .pdf bzw .tex Dateien zu konvertieren. Diese neuen Dateien werden in einem neuen Ordner 'BuildGraphics' gespeichert. Um diese einzubinden werden in [MakeSupport.sty](./.config/emptyReport/MakeSupport.sty) die Befehle

`\inputsvg[<width>]{<filename without .svg>}`

`\inputeps[<width>]{<filename without .eps>}`

zur Verfügung gestellt. Zudem gibt es noch die Befehle


`\inputtikz{<filename without .tex and without the tikz prefix specified in `[ Optionen](#Optionen-f%C3%BCr-MakeSupport.sty)`>}`

um tikz-Bilder mit tikzexternalize zu generieren und

`\inputplot{<filename without .tex and without the plot prefix specified in `[ Optionen](#Optionen-f%C3%BCr-MakeSupport.sty)`>}`

um mit tikz-externalize, dem Plot und en zugehörigen Dateien eine Graphik zu erzeugen. Zu der Plot-Datei `<plotprefix><name>.tex` im Plot-Verzeichnis gehören die Daten `<dataprefix><name>.<dataext>` im Daten-Verzeichnis.

# Optionen für MakeSupport.sty


| Option        | Wert                              | Effekt                                                                                                                   |
| ------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| beamer        | true/false                        | aktiviert/deaktiviert beamer Support (dabei wird pro frame eine Tikz-Graphic erstellt)                                   |
| extdir        | string (default = tikzext)        | Ordner in den die erzeugten Tikz-Grafiken abgelegt werden (im Ordner der tex-Datei)                                      |
| vectoroutdir  | string (default = BuildGraphics)  | Ordner in den die erzeugten Vektor Grafiken abgelegt werden (im Wurzelverzeichnis des Projekts)                          |
| epsdir        | string (default = VectorGraphics) | Ordner mit den .eps Dateien                                                                                              |
| svgdir        | string (default = VectorGraphics) | Ordner mit den .svg Dateien                                                                                              |
| buildepsprefix| string (default = eps)            | Prefix den erzeugte .eps Dateien erhalten                                                                                |
| buildsvgprefix| string (default = svg)            | Prefix den erzeugte .svg Dateien erhalten                                                                                |
| pictdir       | string (default = picts)          | Ordner für Tikz-Dateien                                                                                                  |
| pictprefix    | string                            | Prefix den Tikz-Dateien haben                                                                                            |
| plotdir       | string (default = plotdir)        | Ordner für Plot-Dateien                                                                                                  |
| plotprefix    | string                            | Prefix der Plot Dateien                                                                                                  |
| datadir       | string (default = plotdat)        | Ordner der Plot-Daten                                                                                                    |
| dataprefix    | string                            | Prefix der Plot-Daten                                                                                                    |
| dataext       | string (default = dat)            | Dateierweiterung der Daten                                                                                               |
| builddir      | string (default = build)          | Ordner in dem die erzeugten .pdf Dateien etc abgelegt werden (im Ordner der tex-Datei)                                   |

