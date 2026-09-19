#!/usr/bin/env python3
"""Onboarding do agente — primeira conversa no Telegram.

Fluxo: nome do agente -> quem e o dono -> preferencias -> fuso ->
nome do bot Telegram -> backup GitHub (OPCIONAL, tudo pode ser pulado).

Nao improvisa nada: o gateway chama este script e o agente usa EXATAMENTE
o texto de saida. Toda pergunta aceita "pular". Idempotente.

Uso:
    python3 onboarding.py --iniciar
    python3 onboarding.py --responder CHAVE "resposta"
    python3 onboarding.py --pular CHAVE
Env: HERMES_HOME, VAULT_PATH
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
VAULT = Path(os.environ.get("VAULT_PATH", Path.home() / "vault"))
STATE = HERMES_HOME / "state" / "onboarding.json"

PULAR = {"pular", "depois", "skip", "pula", "não", "nao"}

# As perguntas, em ordem. A PRIMEIRA e sempre o NOME do agente.
PERGUNTAS = [
    ("nome", "Oi! Sou seu agente pessoal, rodando no SEU servidor.\n"
             "Antes de tudo: como você quer me chamar?"),
    ("dono_nome", "Prazer! E como você quer ser chamado?"),
    ("dono_faz", "O que você faz? (trabalho/projeto principal)"),
    ("dono_desejos", "O que você mais quer que eu faça por você? (até 3 coisas)"),
    ("dono_limites", "Tem algo que eu NUNCA devo fazer? (ou 'pular')"),
    ("estilo", "Como prefere minhas respostas?\n"
               "1) curtas e diretas  2) com contexto  3) tanto faz"),
    ("fuso", "Em que fuso você está? (ex.: America/Sao_Paulo)"),
]

BOT_MSG = ("Última coisa: seu bot no Telegram pode ter esse mesmo nome.\n"
           "No @BotFather: /setname → escolha seu bot → digite: {nome}\n"
           "(e /setdescription e /setuserpic se quiser)\n"
           "Feito? Responde 'pronto' — ou 'pular' para fazer depois.")

# Backup GitHub: etapa separada, sempre opcional.
GITHUB_MSG = (
    "Quer que eu faça backup do seu vault num repositório PRIVADO do seu GitHub?\n"
    "Se sim, me manda um token de acesso:\n"
    "1. https://github.com/settings/tokens/new\n"
    "2. Marque só 'repo'\n"
    "3. Gere e cole aqui\n"
    "⚠️ O repo que eu criar será PRIVADO (só você vê) e o token fica salvo\n"
    "só neste servidor, com permissão restrita. Ou digite 'pular'."
)


def carregar_estado() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {}


def salvar_estado(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2))


def proxima_pendente(st: dict):
    for chave, pergunta in PERGUNTAS:
        if chave not in st:
            return chave, pergunta
    if "bot_telegram" not in st:
        return ("bot_telegram",
                BOT_MSG.replace("{nome}", st.get("nome", "assistente")))
    if "github_token" not in st:
        return "github_token", GITHUB_MSG
    return None, None


def aplicar_resposta(st: dict, chave: str, resposta: str) -> dict:
    st[chave] = resposta.strip()
    if chave == "dono_limites" and st[chave] == "":
        st[chave] = "(nenhum declarado)"
    return st


def validar_github_token(token: str):
    """Retorna (login, erro). Nao imprime o token."""
    req = urllib.request.Request(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json", "User-Agent": "aethon"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read())
            return d.get("login"), None
    except Exception as e:
        return None, str(e)


def salvar_token_github(st: dict, token: str) -> tuple:
    """Valida, salva com permissao 600 FORA de qualquer repo e cria o repo privado."""
    login, err = validar_github_token(token)
    if err:
        return False, f"token inválido ({err[:80]}). Tenta de novo ou digite 'pular'."

    creds = Path.home() / ".git-credentials"
    linha = f"https://{login}:{token}@github.com"
    existente = creds.read_text() if creds.exists() else ""
    github_antiga = [l for l in existente.splitlines() if "github.com" in l]
    if github_antiga:
        existente = existente.replace(github_antiga[0], linha)
    else:
        existente = (existente.rstrip("\n") + "\n" + linha) if existente else linha + "\n"
    creds.write_text(existente)
    creds.chmod(0o600)
    os.system("git config --global credential.helper store")

    nome_repo = "meu-vault-privado"
    body = json.dumps({"name": nome_repo, "private": True,
                       "description": f"Backup do vault de {login} (Aethon)"}).encode()
    req = urllib.request.Request(
        "https://api.github.com/user/repos", data=body, method="POST",
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json", "User-Agent": "aethon"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read())
            url = d.get("html_url", "")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            url = f"https://github.com/{login}/{nome_repo} (ja existia)"
        else:
            return False, f"token OK ({login}) mas falhei ao criar o repo: {e.code}"
    st["github_login"] = login
    st["github_repo"] = url
    return True, f"✓ conectado como {login}. Repo privado: {url}"


def preencher_artefatos(st: dict) -> None:
    """Onboarding concluido: grava soul e perfil no vault com as respostas."""
    soul_tpl = HERMES_HOME / "SOUL.md"
    if soul_tpl.exists():
        texto = soul_tpl.read_text()
        for k, v in {
            "{{NOME_DO_AGENTE}}": st.get("nome", "assistente"),
            "{{NOME_DO_DONO}}": st.get("dono_nome", ""),
            "{{O_QUE_FAZ}}": st.get("dono_faz", ""),
            "{{DESEJOS_ATE_3}}": st.get("dono_desejos", ""),
            "{{LIMITES}}": st.get("dono_limites", ""),
            "{{ESTILO: curtas-diretas | com-contexto | decidir-sozinho}}": st.get("estilo", ""),
            "{{FUSO}}": st.get("fuso", ""),
            "{{IDIOMA}}": "português",
            "{{DATA}}": date.today().isoformat(),
            "{{CONEXOES}}": "nenhuma ativada ainda — me peça quando quiser",
        }.items():
            texto = texto.replace(k, v)
        soul_tpl.write_text(texto)

    perfil = VAULT / "01_IDENTIDADE" / "perfil.md"
    if perfil.exists():
        texto = perfil.read_text()
        for k, v in {
            "{{NOME_DO_DONO}}": st.get("dono_nome", ""),
            "{{O_QUE_FAZ}}": st.get("dono_faz", ""),
            "{{FUSO}}": st.get("fuso", ""),
            "{{IDIOMA}}": "português",
            "{{DATA}}": date.today().isoformat(),
        }.items():
            texto = texto.replace(k, v)
        perfil.write_text(texto)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--iniciar", action="store_true", help="retorna a proxima pergunta")
    p.add_argument("--responder", nargs=2, metavar=("CHAVE", "RESPOSTA"))
    p.add_argument("--pular", metavar="CHAVE")
    args = p.parse_args()

    st = carregar_estado()

    if args.iniciar and not st:
        st = {"_ativo": "true"}
        salvar_estado(st)

    if args.pular:
        prox, _ = proxima_pendente(st)
        if args.pular == "github_token":
            st["github_token"] = "(pulado)"
            st["github_login"] = "(sem backup)"
        elif args.pular == prox:
            st[args.pular] = "(pulado)"
        else:
            print(f"ERRO:só é possível pular a pergunta atual ({prox})")
            return 1
        salvar_estado(st)

    elif args.responder:
        chave, resposta = args.responder
        chaves_validas = {c for c, _ in PERGUNTAS} | {"github_token", "bot_telegram"}
        if chave not in chaves_validas:
            print(f"chave invalida: {chave}")
            return 1

        if chave == "github_token":
            if resposta.strip().lower() in PULAR:
                st = aplicar_resposta(st, "github_token", "(pulado)")
                salvar_estado(st)
            else:
                ok, msg = salvar_token_github(st, resposta.strip())
                if not ok:
                    print(f"ERRO:{msg}")
                    print(GITHUB_MSG)
                    return 0
                st["github_token"] = f"salvo ({st.get('github_login')})"
                salvar_estado(st)
        else:
            st = aplicar_resposta(st, chave, resposta)
            salvar_estado(st)

    chave, pergunta = proxima_pendente(st)
    if chave is None:
        preencher_artefatos(st)
        backup = st.get("github_repo", "não configurado")
        print("ONBOARDING_CONCLUIDO")
        print(f"Pronto, {st['nome']} está no ar! 🚀")
        print(f"Backup do vault: {backup}")
        print("Posso conectar quando você quiser: 📅 Agenda+Tasks · 📧 Gmail · "
              "🎬 YouTube · 🎙️ Reuniões · 𝕏")
        print("Quer ativar alguma agora, ou prefere me usar já?")
        return 0

    print(f"PERGUNTA:{chave}")
    print(pergunta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
