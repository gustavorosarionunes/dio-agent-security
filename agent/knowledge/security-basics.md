# Fundamentos de Segurança da Informação

Este arquivo fornece ao DIO Agent o vocabulário e os conceitos essenciais de segurança para conduzir análises de vulnerabilidade com rigor técnico e didática.

---

## Conceitos Fundamentais

### Vulnerabilidade
Uma fraqueza em um sistema, aplicação, processo ou controle que pode ser explorada por um agente de ameaça. Pode ser técnica (ex.: falta de validação de entrada) ou humana (ex.: senha fraca).

### Ameaça
Qualquer agente ou evento com potencial de explorar uma vulnerabilidade e causar dano. Pode ser:
- **Interna**: usuário mal-intencionado com acesso ao sistema.
- **Externa**: atacante externo, malware, grupo APT.

### Risco
A combinação entre a **probabilidade** de uma ameaça explorar uma vulnerabilidade e o **impacto** causado caso isso aconteça.

> **Fórmula simplificada:** Risco = Probabilidade × Impacto

### Exploit
Código, técnica ou sequência de ações que aproveita uma vulnerabilidade para obter acesso não autorizado, escalar privilégios ou causar dano.

---

## A Tríade CIA (Confidencialidade, Integridade e Disponibilidade)

| Pilar | O que protege | Exemplo de violação |
|---|---|---|
| **Confidencialidade** | Acesso apenas a quem tem permissão | Vazamento de dados de clientes |
| **Integridade** | Dados não modificados sem autorização | Manipulação de registros no banco |
| **Disponibilidade** | Sistema acessível quando necessário | Ataque DDoS derruba o serviço |

Toda análise de vulnerabilidade deve avaliar qual(is) pilar(es) da tríade são afetados.

---

## Avaliação de Severidade (baseada em CVSS)

O CVSS (Common Vulnerability Scoring System) é o padrão da indústria para pontuar vulnerabilidades de 0 a 10.

| Faixa | Severidade | Ação esperada |
|---|---|---|
| 9.0 – 10.0 | Crítica | Correção imediata |
| 7.0 – 8.9 | Alta | Correção prioritária |
| 4.0 – 6.9 | Média | Planejar correção |
| 0.1 – 3.9 | Baixa | Monitorar |
| 0.0 | Nenhuma | Sem impacto |

Fatores que influenciam o score:
- **Vetor de ataque**: remoto (pior) ou local (melhor).
- **Complexidade**: simples de explorar ou exige pré-condições.
- **Privilégios necessários**: nenhum (pior) ou administrativo (melhor).
- **Impacto na CIA**: alto, baixo ou nenhum para cada pilar.

---

## Vulnerabilidades Comuns (OWASP Top 10)

### A01 – Broken Access Control
Usuário acessa recursos além do seu nível de permissão. Exemplo: acessar `/admin` sem autenticação.

### A02 – Cryptographic Failures
Dados sensíveis expostos por uso de algoritmos fracos ou ausência de criptografia. Exemplo: senhas salvas em texto puro.

### A03 – Injection
Dados não validados são interpretados como comandos. O tipo mais comum é o **SQL Injection**.

**Exemplo de código vulnerável:**
```python
query = "SELECT * FROM users WHERE user='" + username + "' AND pass='" + password + "'"
```

**Payload de ataque:**
```
username: admin' --
```

**Query resultante (maliciosa):**
```sql
SELECT * FROM users WHERE user='admin' --' AND pass='qualquer_coisa'
```

O `--` comenta o restante da query, ignorando a senha.

**Correção — consulta parametrizada:**
```python
cursor.execute("SELECT * FROM users WHERE user=? AND pass=?", (username, password))
```

### A04 – Insecure Design
Falhas no modelo de negócio ou na arquitetura, não apenas no código. Exemplo: fluxo de recuperação de senha sem confirmação de identidade.

### A05 – Security Misconfiguration
Configurações padrão inseguras mantidas em produção. Exemplo: porta de debug aberta, credenciais padrão de banco de dados.

### A07 – Identification and Authentication Failures
Falhas no processo de autenticação. Exemplos: sem limite de tentativas de login (força bruta), tokens de sessão previsíveis.

### A09 – Security Logging and Monitoring Failures
Ausência de logs ou alertas que permitiriam detectar e responder a ataques a tempo.

---

## MITRE ATT&CK

O MITRE ATT&CK é uma base de conhecimento pública de táticas, técnicas e procedimentos (TTPs) usados por atacantes reais. Organizado em:

- **Táticas**: o objetivo do atacante (ex.: Initial Access, Privilege Escalation, Exfiltration).
- **Técnicas**: como o objetivo é alcançado (ex.: T1190 – Exploit Public-Facing Application).
- **Sub-técnicas**: variações específicas de uma técnica.

**Técnicas mais relevantes para análise de código:**

| ID | Nome | Descrição resumida |
|---|---|---|
| T1190 | Exploit Public-Facing Application | Explorar aplicações expostas à internet (SQL Injection, RCE) |
| T1059 | Command and Scripting Interpreter | Injeção de comandos no sistema operacional |
| T1110 | Brute Force | Tentativas massivas de adivinhar credenciais |
| T1552 | Unsecured Credentials | Credenciais armazenadas de forma insegura |
| T1078 | Valid Accounts | Uso de credenciais legítimas comprometidas |

---

## Boas Práticas de Desenvolvimento Seguro (DevSecOps)

1. **Validar e sanitizar toda entrada de usuário.** Nunca confie em dados vindos de fora do sistema.
2. **Usar consultas parametrizadas.** Jamais concatenar entrada do usuário em queries SQL.
3. **Princípio do menor privilégio.** Cada componente deve ter apenas as permissões que precisa.
4. **Não armazenar segredos no código.** Use variáveis de ambiente ou cofres de segredos (Vault, Secret Manager).
5. **Criptografar dados sensíveis em repouso e em trânsito.** Use TLS 1.2+ e algoritmos modernos (AES-256, bcrypt para senhas).
6. **Manter dependências atualizadas.** Bibliotecas desatualizadas frequentemente têm CVEs conhecidas.
7. **Implementar logging e monitoramento.** Registre eventos de segurança (logins, erros, acessos negados).
8. **Fazer revisão de código com foco em segurança.** Analise Pull Requests considerando vetores de ataque.
9. **Testar antes de produzir.** Use ferramentas SAST (análise estática) e DAST (análise dinâmica) no pipeline CI/CD.
10. **Planejar resposta a incidentes.** Tenha um plano claro para quando (não se) um incidente acontecer.

---

## Glossário Rápido

| Termo | Significado |
|---|---|
| CVE | Common Vulnerabilities and Exposures — identificador único de vulnerabilidade conhecida |
| CVSS | Common Vulnerability Scoring System — sistema de pontuação de severidade |
| SAST | Static Application Security Testing — análise de código sem executá-lo |
| DAST | Dynamic Application Security Testing — análise com a aplicação em execução |
| Pentest | Teste de penetração — simulação controlada de ataque |
| Zero-day | Vulnerabilidade sem patch disponível |
| Payload | Dados maliciosos enviados para explorar uma vulnerabilidade |
| Hardening | Processo de tornar um sistema mais resistente a ataques |
| APT | Advanced Persistent Threat — grupo atacante sofisticado e persistente |
| TTP | Táticas, Técnicas e Procedimentos — formas de agir de um atacante |
