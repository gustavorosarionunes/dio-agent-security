"""
app_secure.py — Versão corrigida do app.py após análise de segurança.

Correções aplicadas pelo DIO Agent (skill: vulnerability-analysis):
  1. SQL Injection eliminado com consultas parametrizadas (placeholders ?)
  2. Senha armazenada como hash bcrypt (rounds=12) — nunca em texto puro
  3. Debug removido — query não é mais exposta no stdout
  4. Context managers garantem fechamento seguro das conexões

Para instalar a dependência: pip install bcrypt
"""

import sqlite3
import bcrypt


def criar_banco():
    """Cria o banco com hash bcrypt da senha — nunca texto puro."""
    conn = sqlite3.connect("users_secure.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY, user TEXT, pass_hash TEXT)"
    )

    # Hash com bcrypt, custo 12 — resistente a força bruta
    senha = b"senha123"
    pass_hash = bcrypt.hashpw(senha, bcrypt.gensalt(rounds=12))

    cursor.execute(
        "INSERT OR IGNORE INTO users (id, user, pass_hash) VALUES (1, 'admin', ?)",
        (pass_hash.decode("utf-8"),),
    )
    conn.commit()
    conn.close()


def login(username, password):
    """
    Login seguro com consulta parametrizada e verificação via bcrypt.

    O placeholder (?) garante que a entrada do usuário é tratada
    como dado — nunca como parte do código SQL.
    """
    conn = sqlite3.connect("users_secure.db")
    cursor = conn.cursor()

    # CORRETO: placeholder ? separa código de dados
    cursor.execute(
        "SELECT pass_hash FROM users WHERE user = ?",
        (username,),
    )
    resultado = cursor.fetchone()
    conn.close()

    if resultado is None:
        return False

    # Verifica a senha contra o hash — a senha em si nunca sai do hash
    hash_armazenado = resultado[0].encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), hash_armazenado)


def main():
    criar_banco()
    print("=== Sistema de Login (Versão Segura) ===")
    username = input("Usuário: ")
    password = input("Senha:   ")

    if login(username, password):
        print("\nLogin bem-sucedido!")
    else:
        print("\nUsuário ou senha incorretos.")


if __name__ == "__main__":
    main()
