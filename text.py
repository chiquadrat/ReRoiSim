import numpy as np


def text_generator(ergebnis, zinsbindung, anlagehorizont, erste_mieterhoehung, kaufpreis):
    """Function that generates interactive text outputs for all plots.

    Args:
        ergebnisse ([dict]): Estimation results
    """
    
    # Ergebnisse
    ergebnisse = f"""Im folgenden werden die Simulationsergebnisse grafisch dargestellt und beschrieben."""

    # Verkaufsfaktor
    verkaufsfaktor_text = f"""In der Simulation wird davon ausgegangen, dass sie nach
     **{anlagehorizont} Jahren**  einen 
     durchschnittlichen Verkaufsfaktor von ** {int(np.array(ergebnis["verkaufsfaktor"]).mean())}**
     erzielen werden. Bei der von Ihnen gewählten Unsicherheit wird in 90 % der Simulationsläufe ein 
     Verkaufsfaktor zwischen **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.05), 1)}** und
     **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.95), 1)}** (blau schraffierter Bereich) für die Berechnung der 
     Renditeergebnisse  angenommen. 
     Historische Werte finde sie unter: LINK"""

    # Zinsbindung
    if zinsbindung >= anlagehorizont:
        anschlusszinssatz_text = f"""Der Anschlusszinsatz ist für das von Ihnen
        gewählte Simulationsszenario nicht relevant, da Ihr gewählter Anlagehorizont
        von **{anlagehorizont} Jahren** nicht länger ist als die von Ihnen angegebene
        Zinsbindung von **{zinsbindung} Jahren**.
        """
    else:
        anschlusszinssatz_text = f"""In der Simulation wird davon ausgegangen, dass sie nach
        **{anlagehorizont} Jahren**  einen 
        durchschnittlichen Anschlusszinsatz von ** {round(np.array(ergebnis["anschlusszinssatz"]*100).mean(),2)} %**
        zahlen müssen. Bei der von Ihnen gewählten Unsicherheit wird in 90 % der Simulationsläufe ein 
        Anschlusszinsatz zwischen **{round(np.quantile(np.array(ergebnis["anschlusszinssatz"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["anschlusszinssatz"])*100, q=0.95), 2)} %** (blau schraffierter Bereich) für 
        die Berechnung der Renditeergebnisse angenommen. Historische Werte 
        finde sie unter: LINK"""

    # Erste Mieterhöhung    
    if erste_mieterhoehung > anlagehorizont:
        mietsteigerung_text = f"""Die potentielle Mietsteigerung ist für Ihr Simulationsergebnis nicht
        relevant, da Ihr gewählter Anlagehorizont von **{anlagehorizont} Jahren** vor der ersten Mieterhöhung, nach
        **{erste_mieterhoehung} Jahren** endet"""
    else:
        mietsteigerung_text = f"""In der Simulation wird ab **Jahr {erste_mieterhoehung}**,
        dem Jahr der ersten Mieterhöhung von einer jährlichen durchschnittlichen
        Mietsteigerung von ** {round(np.array(ergebnis["mietsteigerung"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt die jährliche Mietsteigerung in der Simulation
        in 90% der Fälle zwischen **{round(np.quantile(np.array(ergebnis["mietsteigerung"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["mietsteigerung"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        Historische Werte finde sie unter: LINK"""

    # Kostensteigerung
    kostensteigerung_text = f"""In der Simulation wird von einer jährlichen durchschnittlichen
        Kostensteigerung von ** {round(np.array(ergebnis["kostensteigerung"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt die jährliche Kostensteogerung in der Simulation
        in 90% der Fälle zwischen **{round(np.quantile(np.array(ergebnis["kostensteigerung"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["kostensteigerung"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        Historische Werte finde sie unter: LINK"""

    # Mietausfall
    mietausfall_text = f"""In der Simulation wird von einem jährlichen durchschnittlichen
        Mietausfall von ** {round(np.array(ergebnis["mietausfall"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt der jährliche Mietausfalls in der Simulation
        in 90% der Fälle zwischen **{round(np.quantile(np.array(ergebnis["mietausfall"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["mietausfall"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        Historische Werte finde sie unter: LINK"""
   
   # Verkaufspreis
    verkaufspreis = np.array(ergebnis["verkaufspreis"])
    verkaufspreis = verkaufspreis[~np.isnan(verkaufspreis)]
    if verkaufspreis.min() < kaufpreis:
        verkaufspreis_text = f"""Im durchschnitt werden Sie Ihr Objekt nach **{anlagehorizont} Jahren** für 
        **{int(np.array(ergebnis["verkaufspreis"]).mean())} Euro** verkaufen können. Ihr durchschnittlicher Verkaufsgewinn/verlust
        beträgt somit **{int(np.array(ergebnis["verkaufspreis"]).mean()-kaufpreis)} Euro**. In 
        **{round(len(verkaufspreis[verkaufspreis<kaufpreis])/len(verkaufspreis)*100,2)} %** der Fälle werden Sie 
        das Objekt für einen Preis verkaufen der unter dem Einkaufspreis liegt
        """
    else:
        verkaufspreis_text = f"""Im durchschnitt werden Sie Ihr Objekt nach **{anlagehorizont} Jahren** für 
        **{int(np.array(ergebnis["verkaufspreis"]).mean())} Euro** verkaufen können. Ihr durchschnittlicher Verkaufsgewinn/verlust
        beträgt somit **{int(np.array(ergebnis["verkaufspreis"]).mean()-kaufpreis)} Euro**. 
        """

    # Objektrendite
    objektrendite = np.array(ergebnis["objektrendite"])
    objektrendite = objektrendite[~np.isnan(objektrendite)]
    if objektrendite.min() < 0:
        objektrendite_text = f"""Ihre durchschnittliche Objektrendite nach **{anlagehorizont} Jahren**
        beträgt **{round(np.array(ergebnis["objektrendite"]).mean()*100, 2)} %**. In 
        **{round(len(objektrendite[objektrendite<0])/len(objektrendite)*100,2)} %** der Fälle
        wird Ihre Objektrendite negativ sein.
        """
    else:
        objektrendite_text = f"""Ihre durchschnittliche Objektrendite nach **{anlagehorizont} Jahren**
        beträgt **{round(np.array(ergebnis["objektrendite"]).mean()*100, 2)} %**. 
        """
    
    # Eigenkapitalrendite
    eigenkapitalrendite = np.array(ergebnis["eigenkapitalrendite"])
    eigenkapitalrendite = eigenkapitalrendite[~np.isnan(eigenkapitalrendite)]
    if eigenkapitalrendite.min() < 0:
        eigenkapitalrendite_text = f"""Ihre durchschnittliche Eigenkapitalrendite nach **{anlagehorizont} Jahren**
        beträgt **{round(eigenkapitalrendite.mean()*100, 2)} %**. In 
        **{round(len(eigenkapitalrendite[eigenkapitalrendite<0])/len(eigenkapitalrendite)*100,2)} %** der Fälle
        wird Ihre Eigenkapitalrendite negativ sein.
        """
    else:
        eigenkapitalrendite_text = f"""Ihre durchschnittliche Eigenkapitalrendite nach **{anlagehorizont} Jahren**
        beträgt **{round(np.array(ergebnis["eigenkapitalrendite"]).mean()*100, 2)} %**. 
        """
        
    gewinn = np.array(ergebnis["gewinn"])
    gewinn = gewinn[~np.isnan(gewinn)]
    if gewinn.min() < 0:
        gewinn_text = f"""Ihr durchschnittlicher Gewinn nach **{anlagehorizont} Jahren**
        beträgt **{int(gewinn.mean())} Euro**. In 
        **{round(len(gewinn[gewinn<0])/len(gewinn)*100,2)} %** der Fälle werden Sie mit Ihrem
        Objekt Verlust machen. Im Verlustfall beträgt die durschnittliche Höhe Ihres Verlusts
        **{int(gewinn[gewinn<0].mean())} Euro**.
        """
    else:
        gewinn_text = f"""Ihr durchschnittlicher Gewinn nach **{anlagehorizont} Jahren**
        beträgt **{int(gewinn.mean())} Euro**."""
    
    minimaler_cashflow = np.array(ergebnis["minimaler_cashflow"])
    minimaler_cashflow = minimaler_cashflow[~np.isnan(minimaler_cashflow)]
    minimaler_cashflow_text = f"""
    Ihr durchschnittlicher minimaler jährlicher Cashflow liegt bei **{int(minimaler_cashflow.mean())} Euro**. In
    5% der Fällen wird Ihr minimaler Cashflow bei unter **{int(np.quantile(minimaler_cashflow, q=0.05))} Euro ** liegen.
    """
    
    text = {
        "ergebnisse": ergebnisse,
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
    }

    return text
