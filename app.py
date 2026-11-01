"""
app.py — Aplicação de login VULNERÁVEL para fins educacionais.

ATENÇÃO: Este código contém vulnerabilidades INTENCIONAIS.
Use APENAS em ambiente de laboratório local. Nunca em produção.

Vulnerabilidades presentes (propositalmente):
  1. SQL Injection por concatenação de string na query
  2. Senha armazenada em texto puro (sem hash)
  3. Exposição da query SQL no stdout (debug info leak)
"""

import sqlite3


def criar_banco():
    """Cria o banco de dados de laboratório com um usuário de teste."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user TEXT, pass TEXT)"
    )
    # Senha em texto puro — vulnerabilidade intencional para análise
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, user, pass) VALUES (1, 'admin', 'senha123')"
    )
    conn.commit()
    conn.close()


def login(username, password):
    """
    VULNERÁVEL: monta a query concatenando diretamente a entrada do usuário.

    Payload de ataque:
      username: admin' --
      password: qualquer_coisa

    Query resultante:
      SELECT * FROM users WHERE user='admin' --' AND pass='...'

    O '--' comenta o restante, ignorando a verificação de senha.
    Resultado: acesso total sem conhecer a senha.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # FALHA: concatenação direta — nunca faça isso em produção
    query = (
        "SELECT * FROM users WHERE user='"
        + username
        + "' AND pass='"
        + password
        + "'"
    )

    # FALHA: exposição da query no stdout (information disclosure)
    print(f"\n[DEBUG] Query executada: {query}\n")

    cursor.execute(query)
    resultado = cursor.fetchone()
    conn.close()
    return resultado


def main():
    criar_banco()
    print("=== Sistema de Login (Laboratório Vulnerável) ===")
    username = input("Usuário: ")
    password = input("Senha:   ")

    if login(username, password):
        print("\n✅ Login bem-sucedido!")
    else:
        print("\n❌ Usuário ou senha incorretos.")


if __name__ == "__main__":
    main()
