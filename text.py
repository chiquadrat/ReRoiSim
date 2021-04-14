import numpy as np

def text_static():
    # Einleitung
    einleitung = f"""
    Hier folgt die sicke Einleitung. 
    """
    
    # Ergebnisse
    ergebnisse = f"""Im Folgenden werden die Simulationsergebnisse grafisch dargestellt und beschrieben.
    """
    
    # berechnete_kennzahlen = f"""
    # Auf Basis Ihrer Eingabe wurden die folgenden anfänglichen Kennzahlen für Ihre Immobilie berechnet.
    # """
    berechnete_kennzahlen = ""
    
    export_import = f"""
    >Die Exportfunktion bietet Ihnen die Möglichkeit, Ihre Eingabewerte
    >in Form einer CSV-Datei herunterzuladen. Sollten Sie die Simulation erneut durchführen
    >wollen, mit gegebenenfalls  leicht veränderte Eingabewerten, können Sie mithilfe der Importfunktion
    >die zuvor exportierte CSV-Datei wieder importieren und Ihre Eingabeparameter verändern. Somit ersparen Sie sich die erneute Eingabe.
    """
    
    simulation = f"""
    >**Wichtig:** Die Simulation wird erst durch das Klicken des
    >*Buttons*  gestartet. Wenn Sie anschließend Eingabeparameter
    >verändern, müssen Sie die Simulation erneut starten.
    """
    
    eingabeparameter = f"""
    Im Folgenden können Sie sich einen Überblick darüber verschaffen, wie die 
    von Ihnen gewählte Unsicherheit (die Standardabweichung) Ihre Eingabeparameter beeinflusst; also wie stark
    die mit Unsicherheit behaftet Eingabeparameter zwischen den einzelnen Simulationsläufen schwanken. 
    Sollte Ihnen die Schwankungen zu groß oder klein erscheinen, 
    können Sie diese verringern  oder vergrößern  indem Sie die Unsicherheit
    der Eingabeparameter über die Eingabemaske reduzieren, bzw. vergrößern. Dies ermöglicht Ihnen
    das Risiko Ihrer Investition deutlich besser einzuschätzen als bei einer rein
    deterministischen Betrachtung.
    """
    
    haftungsausschluss = f"""
    >Wir möchten ausdrücklich darauf hinweisen, dass wir keine Gewähr für die 
    >Richtigkeit der Berechnungen, Darstellungen und Angaben übernehmen. 
    >Das Simulations-Tool ersetzt keine Rechts-, Steuer oder Finanzberatung.
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
    verkaufsfaktor_text = f"""In der Simulation wird davon ausgegangen, dass sie nach
     **{anlagehorizont} Jahren**  einen 
     durchschnittlichen Verkaufsfaktor von ** {int(np.array(ergebnis["verkaufsfaktor"]).mean())}**
     erzielen werden. Bei der von Ihnen gewählten Unsicherheit wird in 90 % der Simulationsläufe ein 
     Verkaufsfaktor zwischen **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.05), 1)}** und
     **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.95), 1)}** (blau schraffierter Bereich) für die Berechnung der 
     Rendite Ergebnisse  angenommen.
     """

    # Zinsbindung
    if zinsbindung >= anlagehorizont:
        anschlusszinssatz_text = f"""Der Anschlusszinssatz ist für das von Ihnen
        gewählte Simulationsszenario nicht relevant, da Ihr gewählter Anlagehorizont
        von **{anlagehorizont} Jahren** nicht länger ist, als die von Ihnen angegebene
        Zinsbindung von **{zinsbindung} Jahren**.
        """
    else:
        anschlusszinssatz_text = f"""In der Simulation wird davon ausgegangen, dass sie nach
        **{zinsbindung} Jahren**  einen 
        durchschnittlichen Anschlusszinsatz von ** {round(np.array(ergebnis["anschlusszinssatz"]*100).mean(),2)} %**
        zahlen müssen. Bei der von Ihnen gewählten Unsicherheit wird in 90 % der Simulationsläufe ein 
        Anschlusszinsatz zwischen **{round(np.quantile(np.array(ergebnis["anschlusszinssatz"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["anschlusszinssatz"])*100, q=0.95), 2)} %** (blau schraffierter Bereich) für 
        die Berechnung der Rendite Ergebnisse angenommen."""

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
        in 90% der Fälle zwischen **{round(np.quantile(np.array(ergebnis["mietsteigerung"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["mietsteigerung"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        """

    # Kostensteigerung
    kostensteigerung_text = f"""In der Simulation wird von einer jährlichen durchschnittlichen
        Kostensteigerung von ** {round(np.array(ergebnis["kostensteigerung"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt die jährliche Kostensteigerung  in der Simulation
        in 90% der Fälle zwischen **{round(np.quantile(np.array(ergebnis["kostensteigerung"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["kostensteigerung"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        """

    # Mietausfall
    mietausfall_text = f"""In der Simulation wird von einem jährlichen durchschnittlichen
        Mietausfall von ** {round(np.array(ergebnis["mietausfall"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt der jährliche Mietausfall in der Simulation
        in 90% der Fälle zwischen **{round(np.quantile(np.array(ergebnis["mietausfall"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["mietausfall"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        """
   
   # Verkaufspreis
    verkaufspreis = np.array(ergebnis["verkaufspreis"])
    verkaufspreis = verkaufspreis[~np.isnan(verkaufspreis)]
    if verkaufspreis.min() < kaufpreis:
        verkaufspreis_text = f"""Im Durchschnitt werden Sie Ihr Objekt nach **{anlagehorizont} Jahren** für 
        **{int(np.array(ergebnis["verkaufspreis"]).mean())} Euro** verkaufen können. Ihr durchschnittlicher Verkaufsgewinn/verlust
        beträgt somit **{int(np.array(ergebnis["verkaufspreis"]).mean()-kaufpreis)} Euro**. Mit einer
        Wahrscheinlichkeit von  
        **{round(len(verkaufspreis[verkaufspreis<kaufpreis])/len(verkaufspreis)*100,2)} %** wird der 
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
    Der durchschnittliche minimale jährliche Cashflow liegt bei **{int(minimaler_cashflow.mean())} Euro**. Mit einer
    Wahrscheinlichkeit von
    5% wird der minimale jährliche Cashflow bei unter **{int(np.quantile(minimaler_cashflow, q=0.05))} Euro ** liegen.
    """
    etf_rendite_text = f"""
    Die durchschnittliche EK Rendite (nach Steuern) bei Anlage Ihres initialen Eigenkapitals
    und der jährlichen negativen Cashflows (falls vorhanden) in einen ETF
    beträgt **{round(np.array(ergebnis['etf_ek_rendite']).mean() * 100, 2)} %**. Mit einer Wahrscheinlichkeit von 
    **{round((sum(np.array(ergebnis['etf_ek_rendite']) > np.array(ergebnis['eigenkapitalrendite']))/len(ergebnis['eigenkapitalrendite']))*100, 2)}  %** hätten Sie mit einer ETF Investition eine höhere Rendite erzielt 
    als mit dem Kauf der Immobilie.
    """
 
 
    etf_gewinn_text = f"""
    Der durchschnittliche Gewinn bei Anlage Ihres initialen Eigenkapitals
    und der jährlichen negativen Cashflows (falls vorhanden) in einen ETF
    beträgt **{int(np.array(ergebnis['etf_gewinn']).mean())} Euro**. Mit einer Wahrscheinlichkeit von 
    **{round((sum(np.array(ergebnis['etf_gewinn']) > np.array(ergebnis['gewinn']))/len(ergebnis['etf_gewinn']))*100, 2)}  %** 
    hätten Sie mit einer ETF Investition einen höheren Gewinn erzielt  als mit dem Kauf der Immobilie.
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
