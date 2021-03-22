import numpy as np


def text_generator(ergebnis, zinsbindung, anlagehorizont, erste_mieterhoehung, kaufpreis):
    """Function that generates interactive text outputs for all plots.

    Args:
        ergebnisse ([dict]): Estimation results
    """
    ergebnisse = f"""Im folgenden werden die Simulationsergebnisse grafisch dargestellt und beschrieben."""

    verkaufsfaktor_text = f"""In der Simulation wird davon ausgegangen, dass sie nach
     **{anlagehorizont}** Jahren  einen 
     durchschnittlichen Verkaufsfaktor von ** {int(np.array(ergebnis["verkaufsfaktor"]).mean())}**
     erzielen werden. Bei der von Ihnen gewählten Unsicherheit wird in 90 % der Simulationsläufe ein 
     Verkaufsfaktor zwischen **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.05), 1)}** und
     **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.95), 1)}** (blau schraffierter Bereich) für die Berechnung der 
     Renditeergebnisse  angenommen. 
     Historische Werte finde sie unter: LINK"""

    if zinsbindung >= anlagehorizont:
        anschlusszinssatz_text = f"""Der Anschlusszinsatz ist für das von Ihnen
        gewählte Simulationsszenario nicht relevant, da Ihr gewählter Anlagehorizont
        von **{anlagehorizont}** Jahren nicht länger ist als die von Ihnen angegebene
        Zinsbindung von **{zinsbindung}** Jahren.
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

    if erste_mieterhoehung > anlagehorizont:
        mietsteigerung_text = f"""Die potentielle Mietsteigerung ist für Ihr Simulationsergebnis nicht
        relevant, da Ihr gewählter Anlagehorizont von **{anlagehorizont}** Jahren vor der ersten Mieterhöhung, nach
        **{erste_mieterhoehung}** Jahren endet"""
    else:
        mietsteigerung_text = f"""In der Simulation wird ab Jahr **{erste_mieterhoehung}**,
        dem Jahr der ersten Mieterhöhung von einer jährlichen durchschnittlichen
        Mietsteigerung von ** {round(np.array(ergebnis["mietsteigerung"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt die jährliche Mietsteigerung in der Simulation
        in 90% der Fälle zwischen **{round(np.quantile(np.array(ergebnis["mietsteigerung"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["mietsteigerung"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        Historische Werte finde sie unter: LINK"""

    kostensteigerung_text = f"""In der Simulation wird von einer jährlichen durchschnittlichen
        Kostensteigerung von ** {round(np.array(ergebnis["kostensteigerung"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt die jährliche Kostensteogerung in der Simulation
        in 90% der Fälle zwischen **{round(np.quantile(np.array(ergebnis["kostensteigerung"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["kostensteigerung"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        Historische Werte finde sie unter: LINK"""

    mietausfall_text = f"""In der Simulation wird von einem jährlichen durchschnittlichen
        Mietausfall von ** {round(np.array(ergebnis["mietausfall"]*100).mean(),2)} %** ausgegangen. 
        Bei der von Ihnen gewählten Unsicherheit liegt der jährliche Mietausfalls in der Simulation
        in 90% der Fälle zwischen **{round(np.quantile(np.array(ergebnis["mietausfall"])*100, q=0.05), 2)} %** und
        **{round(np.quantile(np.array(ergebnis["mietausfall"])*100, q=0.95), 2)} %** (blau schraffierter Bereich). 
        Historische Werte finde sie unter: LINK"""
   
    verkaufspreis = np.array(ergebnis["verkaufspreis"])
    verkaufspreis = verkaufspreis[~np.isnan(verkaufspreis)]
    if verkaufspreis.min() < kaufpreis:
        verkaufspreis_text = f"""Im durchschnitt werden Sie Ihr Objekt nach **{anlagehorizont}** Jahren für 
        **{int(np.array(ergebnis["verkaufspreis"]).mean())}** Euro verkaufen können. Ihr durchschnittlicher Verkaufsgewinn/verlust
        beträgt somit **{int(np.array(ergebnis["verkaufspreis"]).mean()-kaufpreis)}** Euro. In 
        **{round(len(verkaufspreis[verkaufspreis<kaufpreis])/len(verkaufspreis)*100,2)}** % der Fälle werden Sie 
        das Objekt für einen Preis verkaufen der unter dem Einkaufspreis liegt
        """
    else:
        verkaufspreis_text = f"""Im durchschnitt werden Sie Ihr Objekt nach **{anlagehorizont}** Jahren für 
        **{int(np.array(ergebnis["verkaufspreis"]).mean())}** Euro verkaufen können. Ihr durchschnittlicher Verkaufsgewinn/verlust
        beträgt somit **{int(np.array(ergebnis["verkaufspreis"]).mean()-kaufpreis)}** Euro. 
        """

    objektrendite = np.array(ergebnis["objektrendite"])
    objektrendite = objektrendite[~np.isnan(objektrendite)]
    
    if objektrendite.min() < 0:
        objektrendite_text = f"""Ihre durchschnittliche Objektrendite nach **{anlagehorizont}** Jahren
        beträgt **{round(np.array(ergebnis["objektrendite"]).mean()*100, 2)} %**. In 
        **{round(len(objektrendite[objektrendite<0])/len(objektrendite)*100,2)}** % der Fälle
        wird Ihre Objektrendite negativ sein.
        """
    else:
        objektrendite_text = f"""Ihre durchschnittliche Objektrendite nach **{anlagehorizont}** Jahren
        beträgt **{round(np.array(ergebnis["objektrendite"]).mean()*100, 2)} %**. 
        """
    
    
    eigenkapitalrendite_text = "Sicke Eigenkapitalrendite"
    gewinn_text = "Sicker Gewinn"
    minimaler_cashflow_text = "Sicker minimaler Cashflow"
    
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
