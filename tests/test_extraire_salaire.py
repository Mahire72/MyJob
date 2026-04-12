import sys
from pathlib import Path

#avant les imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.src.utils import extraire_salaire




def test_extraire_salaire():
    print("\n--- TEST EXTRAIRE SALAIRE ---")

    # cas mensuel
    s1 = "Mensuel de 2000 Euros à 3000 Euros"
    result = extraire_salaire(s1)
    assert result == 2000.0, "Mensuel incorrect"
    print("Test mensuel OK")

    # cas annuel
    s2 = "Annuel de 24000 Euros à 36000 Euros"
    result = extraire_salaire(s2)
    assert result == 2000.0, "Annuel incorrect"
    print("Test annuel OK")

    # cas string vide
    result = extraire_salaire("")
    assert result is None, "Doit retourner None"
    print("Test string vide OK")

    # cas None
    result = extraire_salaire(None)
    assert result is None, "Doit retourner None"
    print("Test None OK")

    # cas format inconnu
    s3 = "Salaire compétitif"
    result = extraire_salaire(s3)
    assert result is None, "Doit retourner None"
    print("Test format inconnu OK")


if __name__ == "__main__":
    test_extraire_salaire()