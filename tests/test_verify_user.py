import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.src.db import create_user, verify_user
import uuid

print("\n--- TEST VERIFY USER MANUELLE---")

#créer un user unique
email = f"test_{uuid.uuid4()}@mail.com"
password = "1234"

user = create_user(email, password)

# bon mot de passe
auth_ok = verify_user(email, password)
print("Login OK :", auth_ok)

# mauvais mot de passe
auth_fail = verify_user(email, "wrongpassword")
print("Login FAIL :", auth_fail)



def test_verify_user():
    print("\n--- TEST VERIFY USER ---")

    # créer un user unique
    email = f"test_{uuid.uuid4()}@mail.com"
    password = "1234"

    user = create_user(email, password)
    print("User créé :", user)

    # bon mot de passe
    auth_ok = verify_user(email, password)
    print("Login OK :", auth_ok)

    if auth_ok:
        print("Test bon mot de passe : OK")
    else:
        print("Test bon mot de passe : FAIL")

    # mauvais mot de passe
    auth_fail = verify_user(email, "wrongpassword")
    print("Login FAIL :", auth_fail)

    if not auth_fail:
        print("Test mauvais mot de passe : OK")
    else:
        print("Test mauvais mot de passe : FAIL")


if __name__ == "__main__":
    test_verify_user()