import numpy as np

def text_generator(ergebnis, zinsbindung, anlagehorizont):
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
     **{round(np.quantile(np.array(ergebnis["verkaufsfaktor"]), q=0.95), 1)}**für  die Berechnung der Renditeergebnisse  angenommen. 
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
    
    return ergebnisse, verkaufsfaktor_text, anschlusszinssatz_text

