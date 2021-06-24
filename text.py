import numpy as np

def text_static():
    # Einleitung
    einleitung = f"""
    """
    
#     einleitung = f"""
#   Der Simulator bietet Ihnen die Möglichkeit die objektbezogene und subjektbezogene dynamische Rendite Ihrer Immobilieninvestition zu berechnen und mit einer ETF-Anlage zu vergleichen. Gegenüber einer statischen Berechnung der Anfangsrendite, bei der nur die Ausgaben und Einnahmen zum Kaufzeitpunkt berücksichtigt werden, werden bei der Berechnung der objektbezogenen dynamischen Rendite auch zeitlich veränderliche Faktoren, wie z.B. die Wertentwicklung der Immobilie oder eventuelle Mietsteigerungen berücksichtigt. Bei der subjektbezogenen dynamischen Renditeberechnung werden darüber hinaus noch individuelle Faktoren des Investors berücksichtigt, wie zum Beispiel der Steuersatz oder die Finanzierungskonditionen.

# Ein Teil, der für die Rendite entscheidenden Faktoren ist durch die Immobilie vorgegebenen, wie zum Beispiel der Kaufpreis oder die Nebenkosten. Andere Faktoren wie z.B. die Höhe des eingesetzten Eigenkapitals oder der Tilgungssatz können von Investierenden selbst gewählt werden. Diese Faktoren können Sie mit dem Rendite-Simulator hinsichtlich ihrer Ziele optimieren, z.B. um eine möglichst hohe Eigenkapitalrendite zu erwirtschaften. Für einen Großteil, der für die Berechnung der Wirtschaftlichkeit der Immobilie entscheidenden Faktoren, müssen Sie allerdings Annahmen treffen und zum Teil deren zeitliche Entwicklung prognostizieren. Dazu zählen z.B. die Wertentwicklung des Objekts oder die Mietpreisentwicklung. Die zukünftige Entwicklung dieser Faktoren ist unbekannt und deren Prognose damit mit einer Unsicherheit behaftet.

# Die meisten im Internet verfügbaren Renditerechner nehmen für diese, mit Unsicherheit behafteten, Faktoren konstante Werte an. Beispielhaft könnte davon ausgegangen werden, dass die jährliche Mietpreissteigerung 2 % entspricht. Da die Berechnung der dynamischen Renditen von diesem Faktor abhängig ist, wäre die Renditeberechnung mit einem klassischen Renditerechner nur präzise (nah an dem erzielten Renditewert am Ende des Anlagehorizonts), wenn die Mietpreissteigerung auch wirklich bei 2 % liegt. Die Wahrscheinlichkeit, dass dies Eintritt ist jedoch verschwindend gering. Daraus folgt, dass die berechnete dynamische Rendite auch nicht mit der letztendlich erzielten Rendite am Ende des Anlagehorizonts übereinstimmen wird.

# Im Gegensatz zu den meisten klassischen Renditerechnern wird bei unserem Simulator, bei den mit Unsicherheit behafteten Parametern, nicht von einem konstanten Wert für die Renditeberechnung ausgegangen.Unser Simulator berücksichtigt für die Renditeberechnung vielmehr eine Bandbreite an möglichen Werten mit unterschiedlicher Eintrittswahrscheinlichkeit. Die Berechnung der dynamischen Rendite erfolgt dann mehrmals mit jeweils unterschiedlichen Werte für die mit Unsicherheit behafteten Faktoren. Zum Beispiel lässt sich die Höhe der Mietpreissteigerung so spezifizieren, dass die jährliche Mietsteigerung im Mittel bei 2% und in 90% der Fälle zwischen 1% und 3% liegt. Bei dieser Spezifikation würden die Höhe der Mietpreissteigerung pro Jahr mit hoher Wahrscheinlichkeit nahe der 2% liegen, aber auch extremere Szenarien, mit höherer oder niedrigerer Mietsteigerung würden in die Renditeberechnung einfließen. Dies ermöglicht Ihnen die Unsicherheit der Mietpreissteigerung und der anderen mit Unsicherheit behafteten Faktoren in der Berechnung der Renditen abzubilden. Als Ergebnis liegen dann eine vielzahl von Renditegrößen sowie deren Verteilung (deren Eintrittswahrscheinlichkeit) vor. Die vielzahl der berechneten Renditegrößen ermöglicht Ihnen abzuschätzen wie hoch Ihre Rendite durchschnittlich ausfallen wird, aber auch was in schlechten und sehr guten Fällen zu erwarten ist.

# Die theoretische Grundlage für diese Art der Berechnung bildet die Monte-Carlo Analyse. Im Vergleich zu einer rein deterministischen Betrachtung ermöglicht Ihnen die Simulation das Risiko Ihrer Investition deutlich besser einzuschätzen. Man spricht auch von einer Objektivierung der Renditeberechnung. Selbstverständlich ist jedoch auch die Simulation von Annahmen (z.B. Annahmen über die Höhe der Unsicherheit) abhängig die die Qualität der Ergebnisse maßgeblich beeinflussen. 

#     """
    
    # Ergebnisse
    ergebnisse = f"""Im Folgenden werden die Simulationsergebnisse grafisch dargestellt und beschrieben.
    """
    
    # berechnete_kennzahlen = f"""
    # Auf Basis Ihrer Eingabe wurden die folgenden anfänglichen Kennzahlen für Ihre Immobilie berechnet.
    # """
    berechnete_kennzahlen = ""
    
    export_import = f"""
    >Die Exportfunktion bietet die Möglichkeit, die Eingabewerte
    >in Form einer CSV-Datei herunterzuladen und lokal zu speichern. Wenn Sie die Simulation in Zukunft erneut durchführen
    >möchten, können Sie mithilfe der Importfunktion
    >die zuvor exportierte CSV-Datei wieder importieren. Somit ersparen Sie sich die erneute Eingabe.
    """
    
    simulation = f"""
    >**Wichtig:** Die Simulation wird erst durch das Klicken des
    >Buttons "START DER SIMULATION" gestartet. Wenn Sie anschließend Eingabeparameter
    >verändern, müssen Sie die Simulation erneut durch Klicken des Buttons starten.
    > Die Simulation wird numerisch mithilfe der Monte-Carlo-Methode durchgeführt. Eine höhere Anzahl an Simulationsläufen verbessert das Ergebnis führt allerdings zu längerer Rechenzeit.
    """
    
    eingabeparameter = f"""
    Im Folgenden können Sie sich einen Überblick darüber verschaffen, wie die 
    von Ihnen gewählte Unsicherheit (die Standardabweichung) Ihre Eingabeparameter beeinflusst; also wie stark
    die mit Unsicherheit behafteten Eingabeparameter zwischen den einzelnen Simulationsläufen schwanken. 
    Sollte Ihnen die Schwankungen zu groß oder klein erscheinen, 
    können Sie diese verringern  oder vergrößern  indem Sie die Unsicherheit
    der Eingabeparameter über die Eingabemaske reduzieren, bzw. erhöhen. 
    """
    
    haftungsausschluss = f"""
    Wir möchten ausdrücklich darauf hinweisen, dass wir keine Gewähr für die 
    Richtigkeit der Berechnungen, Darstellungen und Angaben übernehmen. 
    Das Simulations-Tool ersetzt keine Rechts-, Steuer oder Finanzberatung.
    """
    
    text_statisch = {
        "simulation":simulation,
        "export_import":export_import,
        "berechnete_kennzahlen":berechnete_kennzahlen,
        "einleitung": einleitung,
        "ergebnisse": ergebnisse,
        "eingabeparameter":eingabeparameter,
        "haftungsausschluss":haftungsausschluss,
    }

    return text_statisch

    


def text_generator(ergebnis, zinsbindung, anlagehorizont, erste_mieterhoehung, kaufpreis):
    """Function that generates interactive text outputs for all plots.

    Args:
        ergebnisse ([dict]): Estimation results
    """
    
    


    # Verkaufsfaktor
    verkaufsfaktor_text = f"""In der Simulation wird davon ausgegangen, dass Sie nach
     **{anlagehorizont} Jahren**  einen 
     durchschnittlichen Verkaufsfaktor von ** {round(np.array(ergebnis["verkaufsfaktor"]).mean(), 1)}**
     erzielen werden. Bei der von Ihnen gewählten Unsicherheit wird in 90 % der Simulationsläufe ein 
     Verkaufsfaktor zwischen **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.05), 1)}** und
     **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.95), 1)}** (blau schraffierter Bereich) für die Berechnung der 
     Rendite und Ergebnisse  angenommen.
     """

    # Zinsbindung
    if zinsbindung >= anlagehorizont:
        anschlusszinssatz_text = f"""Der Anschlusszinssatz ist für das von Ihnen
        gewählte Simulationsszenario nicht relevant, da Ihr gewählter Anlagehorizont
        von **{anlagehorizont} Jahren** nicht länger ist als die von Ihnen angegebene
        Zinsbindung von **{zinsbindung} Jahren**.
        """
    else:
        anschlusszinssatz_text = f"""In der Simulation wird davon ausgegangen, dass sie nach
        **{zinsbindung} Jahren**  einen 
        durchschnittlichen Anschlusszinssatz von ** {round(np.array(ergebnis["anschlusszinssatz"]*100).mean(),2)} %**
        zahlen müssen. Bei der von Ihnen gewählten Unsicherheit wird in 90 % der Simulationsläufe ein 
        Anschlusszinssatz zwischen **{round(np.quantile(np.array(ergebnis["anschlusszinssatz"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["anschlusszinssatz"])*100, q=0.95), 2)} %** (blau schraffierter Bereich) für 
        die Berechnung der Rendite und Ergebnisse angenommen."""

    # Erste Mieterhöhung    
    if erste_mieterhoehung > anlagehorizont:
        mietsteigerung_text = f"""Die potenziellen Mietsteigerungen sind für Ihr Simulationsergebnis nicht
        relevant, da Ihr gewählter Anlagehorizont von **{anlagehorizont} Jahren** vor der ersten Mieterhöhung, nach
        **{erste_mieterhoehung} Jahren** endet"""
    else:
        mietsteigerung_text = f"""In der Simulation wird ab **Jahr {erste_mieterhoehung}**,
        dem Jahr der ersten Mieterhöhung, von einer jährlichen durchschnittlichen
        Mietsteigerung von ** {round(np.array(ergebnis["mietsteigerung"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt die jährliche Mietsteigerung in der Simulation
        in 90 % der Fälle zwischen **{round(np.quantile(np.array(ergebnis["mietsteigerung"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["mietsteigerung"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        """

    # Kostensteigerung
    kostensteigerung_text = f"""In der Simulation wird von einer jährlichen durchschnittlichen
        Kostensteigerung von ** {round(np.array(ergebnis["kostensteigerung"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt die jährliche Kostensteigerung  in der Simulation
        in 90 % der Fälle zwischen **{round(np.quantile(np.array(ergebnis["kostensteigerung"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["kostensteigerung"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        """

    # Mietausfall
    mietausfall_text = f"""
    Bei der Simulation werden negative Mietausfälle nicht ausgewertet. Dadurch ist 
    die resultierende Häufigkeitsverteilung 
    für den Mietausfall gegebenenfalls nicht normalverteilt. 
    In der Simulation wird von einem jährlichen durchschnittlichen
        Mietausfall von ** {round(np.array(ergebnis["mietausfall"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt der jährliche Mietausfall in der Simulation
        in 90 % der Fälle zwischen **{round(np.quantile(np.array(ergebnis["mietausfall"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["mietausfall"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        """
   
   # Verkaufspreis
    verkaufspreis = np.array(ergebnis["verkaufspreis"])
    verkaufspreis = verkaufspreis[~np.isnan(verkaufspreis)]
    if verkaufspreis.min() < kaufpreis:
        verkaufspreis_text = f"""Im Durchschnitt werden Sie Ihr Objekt nach **{anlagehorizont} Jahren** für 
        **{int(np.array(ergebnis["verkaufspreis"]).mean())} Euro** verkaufen können. Bei einem Kaufpreis
        von  **{int(kaufpreis)} Euro** beträgt Ihr durchschnittlicher Verkaufsgewinn bzw. Verlust
        somit **{int(np.array(ergebnis["verkaufspreis"]).mean()-kaufpreis)} Euro**. Mit einer
        Wahrscheinlichkeit von  **{round(len(verkaufspreis[verkaufspreis<kaufpreis])/len(verkaufspreis)*100,2)} %** wird der 
        zu erzielende
        Verkaufspreis
        unter dem Kaufpreis liegen.
        """
    else:
        verkaufspreis_text = f"""Im Durchschnitt werden Sie Ihr Objekt nach **{anlagehorizont} Jahren** für 
        **{int(np.array(ergebnis["verkaufspreis"]).mean())} Euro** verkaufen können. Ihr durchschnittlicher Verkaufsgewinn
        beträgt somit **{int(np.array(ergebnis["verkaufspreis"]).mean()-kaufpreis)} Euro**. 
        """

    # Objektrendite
    objektrendite = np.array(ergebnis["objektrendite"])
    objektrendite = objektrendite[~np.isnan(objektrendite)]
    if objektrendite.min() < 0:
        objektrendite_text = f"""Die durchschnittliche Objektrendite nach **{anlagehorizont} Jahren**
        beträgt **{round(np.array(ergebnis["objektrendite"]).mean()*100, 2)} %**. Mit einer Wahrscheinlichkeit von 
        **{round(len(objektrendite[objektrendite<0])/len(objektrendite)*100,2)} %** 
        wird die Objektrendite negativ sein.
        """
    else:
        objektrendite_text = f"""Die durchschnittliche Objektrendite nach **{anlagehorizont} Jahren**
        beträgt **{round(np.array(ergebnis["objektrendite"]).mean()*100, 2)} %**. 
        """
    
    # Eigenkapitalrendite
    eigenkapitalrendite = np.array(ergebnis["eigenkapitalrendite"])
    eigenkapitalrendite = eigenkapitalrendite[~np.isnan(eigenkapitalrendite)]
    if eigenkapitalrendite.min() < 0:
        eigenkapitalrendite_text = f"""Die durchschnittliche Eigenkapitalrendite nach **{anlagehorizont} Jahren**
        beträgt **{round(eigenkapitalrendite.mean()*100, 2)} %**. Mit einer Wahrscheinlichkeit von
        **{round(len(eigenkapitalrendite[eigenkapitalrendite<0])/len(eigenkapitalrendite)*100,2)} %** 
        wird die Eigenkapitalrendite negativ sein.
        """
    else:
        eigenkapitalrendite_text = f"""Die durchschnittliche Eigenkapitalrendite nach **{anlagehorizont} Jahren**
        beträgt **{round(np.array(ergebnis["eigenkapitalrendite"]).mean()*100, 2)} %**. 
        """
        
    gewinn = np.array(ergebnis["gewinn"])
    gewinn = gewinn[~np.isnan(gewinn)]
    if gewinn.min() < 0:
        gewinn_text = f"""Der durchschnittliche Gewinn nach **{anlagehorizont} Jahren**
        beträgt **{int(gewinn.mean())} Euro**. Mit einer Wahrscheinlichkeit von 
        **{round(len(gewinn[gewinn<0])/len(gewinn)*100,2)} %** werden Sie mit Ihrem
        Objekt Verlust machen. Im Verlustfall beträgt die durchschnittliche Höhe Ihres Verlusts
        **{int(gewinn[gewinn<0].mean())} Euro**.
        """
    else:
        gewinn_text = f"""Der durchschnittliche Gewinn nach **{anlagehorizont} Jahren**
        beträgt **{int(gewinn.mean())} Euro**."""
    
    minimaler_cashflow = np.array(ergebnis["minimaler_cashflow"])
    minimaler_cashflow = minimaler_cashflow[~np.isnan(minimaler_cashflow)]
    minimaler_cashflow_text = f"""
    Der minimale jährliche Cashflow liegt bei durchschnittlich **{int(minimaler_cashflow.mean())} Euro**. Mit einer
    Wahrscheinlichkeit von
    5% wird der minimale jährliche Cashflow bei unter **{int(np.quantile(minimaler_cashflow, q=0.05))} Euro ** liegen.
    """
    etf_rendite_text = f"""
    Beim Kauf der Immobilie können Sie eine durchschnittliche Eigenkapitalrendite von **{round(eigenkapitalrendite.mean()*100, 2)} %** 
    erwarten. Wenn Sie stattdessen das initial eingesetzte Eigenkapital und die jährlichen negativen Cashflows (falls vorhanden) 
    in einen ETF investieren würden, könnten Sie eine durchschnittliche Eigenkapitalrendite 
    von **{round(np.array(ergebnis['etf_ek_rendite']).mean() * 100, 2)} %** (nach Steuern) erwarten.
    Mit einer Wahrscheinlichkeit von 
    **{round((sum(np.array(ergebnis['etf_ek_rendite']) > np.array(ergebnis['eigenkapitalrendite']))/len(ergebnis['eigenkapitalrendite']))*100, 2)}  %** würden Sie mit einer ETF-Investition eine höhere Rendite erzielen 
    als mit dem Kauf der Immobilie.
    """
 
 
    etf_gewinn_text = f"""
    Beim Kauf der Immobilie beträgt ihr durchschnittlicher Gewinn **{int(gewinn.mean())} Euro**. 
    Der durchschnittliche Gewinn bei der Anlage Ihres initialen Eigenkapitals
    und der jährlichen negativen Cashflows (falls vorhanden) in einen ETF
    beträgt **{int(np.array(ergebnis['etf_gewinn']).mean())} Euro**. Mit einer Wahrscheinlichkeit von 
    **{round((sum(np.array(ergebnis['etf_gewinn']) > np.array(ergebnis['gewinn']))/len(ergebnis['etf_gewinn']))*100, 2)}  %** 
    hätten Sie mit einer ETF-Investition einen höheren Gewinn erzielt  als mit dem Kauf der Immobilie.
    """
    
    text_dynamisch = {
        "verkaufsfaktor": verkaufsfaktor_text,
        "anschlusszinssatz": anschlusszinssatz_text,
        "mietsteigerung": mietsteigerung_text,
        "kostensteigerung":kostensteigerung_text,
        "verkaufspreis":verkaufspreis_text,
        "objektrendite": objektrendite_text, 
        "eigenkapitalrendite":eigenkapitalrendite_text,
        "gewinn":gewinn_text,
        "minimaler_cashflow":minimaler_cashflow_text,
        "mietausfall":mietausfall_text,
        "etf_rendite":etf_rendite_text,
        "etf_gewinn":etf_gewinn_text,
    }

    return text_dynamisch
