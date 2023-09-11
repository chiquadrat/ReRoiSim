# ReRoiSim - Real Estate ROI Simulation

- [Einleitung](#einleitung)
- [Innhaltliche Erläuterung](#innhalt)
	- [Der Immobilienrendite-Simulator](#immo)
	- [Mieten vs. Kaufen](#miet)
- [Disclaimer](#disc)

<a name="einleitung"></a>
## Einleitung

Seit längerem beschäftigen wir (Paul Walter - Machine Learning Engineer / Statistiker und Markus Juling - Ingenieur / Metrologe) uns intensiv mit dem Thema Immobilienkauf als Kapitalanlage. Bei den bereits im Internet verfügbaren Kalkulationstools zur Berechnung der Wirtschaftlichkeit einer potenziellen Immobilieninvestition hat uns immer eine Abschätzung des Risikos gefehlt. Als Investoren sind wir unter anderem daran interessiert zu wissen, mit welcher Wahrscheinlichkeit z. B. die Eigenkapitalrendite negativ werden könnte und wie hoch dann der durchschnittliche Verlust sein würde. Um das Risiko einer Immobilieninvestition besser abschätzen zu können und es zu objektivieren, haben wir uns entschieden, ein eigenes Kalkulationstool (einen Immobilienrendite-Simulator) zu implementieren. 

Außerdem wollten wir die - oft hitzig - geführte Mieten vs. Kaufen Diskussion objektivieren. Aufgrund dessen, haben wir auch einen Mieten vs. Kaufen Simulator implementiert.

Hier geht's zum [Mieten vs. Kaufen](https://reroisim.herokuapp.com/app_mieten_vs_kaufen) und hier zum [Immobilienrendite-Simulator](https://reroisim.herokuapp.com/app_immo_kapitalanlage).

Da wir leider wenig Zeit haben, um an den Simulatoren weiterzuarbeiten, haben wir uns entschieden, den Code zu veröffentlichen. Wir würden uns über Code Contributions, Feedback, Fragen und Anregungen freuen.

<a name="innhalt"></a>
## Inhaltliche Erläuterung

<a name="immo"></a>
### Der Immobilienrendite-Simulator

Der Simulator bietet Euch die Möglichkeit, die objektbezogene und subjektbezogene dynamische Rendite Eurer Immobilieninvestition zu berechnen und mit einer ETF-Anlage zu vergleichen. Gegenüber einer statischen Berechnung der Anfangsrendite, bei der nur die Ausgaben und Einnahmen zum Kaufzeitpunkt berücksichtigt werden, werden bei der Berechnung der objektbezogenen dynamischen Rendite auch zeitlich veränderliche Faktoren, wie z. B. die Wertentwicklung der Immobilie oder eventuelle Mietsteigerungen, berücksichtigt. Bei der subjektbezogenen dynamischen Renditeberechnung werden darüber hinaus noch individuelle Faktoren des Investierenden berücksichtigt, wie zum Beispiel der Steuersatz oder die Finanzierungskonditionen. 

Ein Teil der für die Rendite entscheidenden Faktoren ist durch die Immobilie vorgegeben, wie zum Beispiel der Kaufpreis oder die Nebenkosten. Andere Faktoren wie, z. B. die Höhe des eingesetzten Eigenkapitals oder der Tilgungssatz können vom Investierenden selbst gewählt werden. Diese Faktoren könnt Ihr mit dem Rendite-Simulator hinsichtlich Eurer Ziele optimieren, z. B. um eine möglichst hohe Eigenkapitalrendite zu erwirtschaften. Für einen Großteil, der für die Berechnung der Wirtschaftlichkeit der Immobilie entscheidenden Faktoren, müsst Ihr allerdings Annahmen treffen und zum Teil deren zeitliche Entwicklung prognostizieren. Dazu zählen z. B. die Wertentwicklung des Objekts oder die Mietpreisentwicklung. Die zukünftige Entwicklung dieser Faktoren ist unbekannt und deren Prognose mit einer Unsicherheit behaftet.

Die meisten im Internet verfügbaren Renditerechner nehmen für diese mit Unsicherheit behafteten Faktoren konstante Werte an. Beispielhaft könnte davon ausgegangen werden, dass die jährliche Mietpreissteigerung 2 % entspricht. Da die Berechnung der dynamischen Renditen von diesem Faktor abhängig ist, wäre die Renditeberechnung mit einem klassischen Renditerechner nur präzise (nah an dem erzielten Renditewert am Ende des Anlagehorizonts), wenn die Mietpreissteigerung auch wirklich bei 2 % liegt. Die Wahrscheinlichkeit, dass dies eintritt, ist jedoch verschwindend gering. Daraus folgt, dass die berechnete dynamische Rendite auch nicht mit der letztendlich erzielten Rendite am Ende des Anlagehorizonts übereinstimmen wird.

Im Gegensatz zu den meisten klassischen Renditerechnern wird bei unserem Simulator bei den mit Unsicherheit behafteten Parametern nicht von einem konstanten Wert für die Renditeberechnung ausgegangen. Unser Simulator berücksichtigt für die Renditeberechnung vielmehr eine Bandbreite an möglichen Werten mit unterschiedlicher Eintrittswahrscheinlichkeit. Die Berechnung der dynamischen Rendite erfolgt dann mehrmals mit jeweils unterschiedlichen Werten für die mit Unsicherheit behafteten Faktoren. Zum Beispiel lässt sich die Höhe der Mietpreissteigerung so spezifizieren, dass die jährliche Mietsteigerung im Mittel bei 2 % und in 90 % der Fälle zwischen 1 % und 3 % liegt. Bei dieser Spezifikation würde die Höhe der Mietpreissteigerung pro Jahr mit hoher Wahrscheinlichkeit nahe der 2 % liegen, aber auch extremere Szenarien mit höherer oder niedrigerer Mietsteigerung würden in die Renditeberechnung einfließen. Dies ermöglicht Euch, die Unsicherheit der Mietpreissteigerung und der anderen mit Unsicherheit behafteten Faktoren in der Berechnung der Renditen abzubilden. Als Ergebnis liegen dann eine Vielzahl von Renditegrößen sowie deren Verteilung (deren Eintrittswahrscheinlichkeit) vor. Die Vielzahl der berechneten Renditegrößen ermöglicht Euch abzuschätzen, wie hoch Eure Rendite durchschnittlich ausfallen wird, aber auch was in schlechten und sehr guten Fällen zu erwarten ist.

Die theoretische Grundlage für diese Art der Berechnung bildet die Monte-Carlo Analyse. Im Vergleich zu einer rein deterministischen Betrachtung ermöglicht Euch die Simulation, das Risiko Eurer Investition deutlich besser einzuschätzen. Man spricht auch von einer Objektivierung der Renditeberechnung. Selbstverständlich ist jedoch auch die Simulation von Annahmen (z. B. Annahmen über die Höhe der Unsicherheit) abhängig, die die Qualität der Ergebnisse maßgeblich beeinflussen. 



<a name="miet"></a>
### Mieten vs. Kaufen

Eine Erläuterung folgt. 

<a name="disc"></a>
## Disclaimer

Wir möchten ausdrücklich darauf hinweisen, dass wir keine Gewähr für die Richtigkeit der Berechnungen, Darstellungen und Angaben übernehmen. Das Simulations-Tool ersetzt keine Rechts-, Steuer- oder Finanzberatung.


