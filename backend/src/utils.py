import logging
#regex pour extraire le salaire min et autres (peut etre utile plus tard)
import re 

def extraire_salaire(salaire_str):
    """
    Extraire le salaire min et max d'une chaine de caractères

    problème rencontré : il faut differencier le salaire mensuel et annuel
    """
    #Exemple de string retourne par l'api : "Mensuel de 1823.03 Euros à 2500.0 Euros sur 12.0 mois"
    #On doit utiliser une expression reguliere pour extraire le salaire min
    if not salaire_str:
        return None
    #Expression reguliere pour extraire le salaire min
    #on extrait les nombres (\d) avec point ou pas (\.?) une ou plusieurs fois car findall retourne une liste
    nombres = re.findall(r'\d+\.?\d+', salaire_str)
    
    if not nombres:
        return None

    salaire_min = float(nombres[0])
    salaire_str_lower = salaire_str.lower()
    if "annuel" in salaire_str_lower:
        salaire_min = salaire_min / 12
    elif "mensuel" in salaire_str_lower:
        pass
    else:
        return None
    return salaire_min

Logger = logging.getLogger("uvicorn.error")