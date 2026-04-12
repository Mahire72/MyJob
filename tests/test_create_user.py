import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.src.db import create_user
import uuid

print("\n--- TEST CREATE USER ---")

user = create_user("test@mail.com", "1234")
print("User créé :", user)


def test_create_user():
    print("\n--- TEST CREATE USER ---")

    #toujours email unique
    email = f"test_{uuid.uuid4()}@mail.com"
    password = "1234"

    user = create_user(email, password)
    print("User créé :", user)

    assert user is not None, "User non créé"
    assert isinstance(user, dict), "User doit être un dictionnaire"
    assert "id" in user, "ID manquant"
    assert user["email"] == email, "Email incorrect"

    print("TEST CREATE USER OK")


if __name__ == "__main__":
    test_create_user()