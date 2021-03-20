import numpy as np


def text_generator(ergebnis, zinsbindung, anlagehorizont, erste_mieterhoehung):
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
     **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.95), 1)}** für die Berechnung der 
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
        **{round(np.quantile(np.array(ergebnis["anschlusszinssatz"])*100, q=0.95), 2)} %** für 
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
        **{round(np.quantile(np.array(ergebnis["mietsteigerung"])*100, q=0.95), 2)} %**. 
        Historische Werte finde sie unter: LINK"""

    kostensteigerung_text = "Sicke Kostensteigerung"
    verkaufspreis_text = "Sicker Verkaufspreis"
    objektrendite_text = "Sicke Objektrendite"
    eigenkapitalrendite_text = "Sicke Eigenkapitalrendite"
    gewinn_text = "Sicker Gewinn"
    minimaler_cashflow_text = "Sicker minimaler Cashflow"
    mietausfall_text = "Sicker Mietausfall"
    
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
