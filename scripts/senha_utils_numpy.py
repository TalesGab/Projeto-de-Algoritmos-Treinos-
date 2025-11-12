# senha_utils_numpy.py
import numpy as np
import hashlib
import base64
import secrets

def gerar_salt_numpy(n_bytes=16):
    """Gera um salt aleatório usando NumPy (não recomendado para crypto real, mas funcional)."""
    arr = np.random.randint(0, 256, size=(n_bytes,), dtype=np.uint8)
    return arr.tobytes()

def gerar_hash_senha(password: str, iterations: int = 100_000):
    """Cria o hash da senha com salt aleatório."""
    salt = gerar_salt_numpy()
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    return {
        "salt": base64.b64encode(salt).decode(),
        "hash": base64.b64encode(hash_bytes).decode(),
        "iterations": iterations
    }

def verificar_senha(stored: dict, password: str) -> bool:
    """Verifica se a senha fornecida gera o mesmo hash."""
    salt = base64.b64decode(stored["salt"])
    hash_original = base64.b64decode(stored["hash"])
    iterations = stored["iterations"]

    hash_teste = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    return secrets.compare_digest(hash_original, hash_teste)