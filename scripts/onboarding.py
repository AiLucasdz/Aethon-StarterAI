#!/usr/bin/env python3
"""Onboarding do agente — primeira conversa no Telegram.

Fluxo: nome do agente -> quem e o dono -> preferencias -> fuso ->
nome do bot Telegram -> backup GitHub -> Honcho (opcionais; perguntas podem ser puladas).

O agente chama este script pela instrução no SOUL e usa
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
from datetime import date
from pathlib import Path
from private_state import safe

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
    "Quer configurar backup privado depois? Responda 'sim' ou 'pular'. "
    "Não envie tokens aqui. A autenticação será feita no terminal com o "
    "fluxo seguro do GitHub. Esta escolha não cria repositório nem ativa backup."
)

# Segundo cérebro é a função do agente; apenas Honcho admite recusa.
BRAIN_MSG = (
    "Seu agente é um segundo cérebro: arquivos, memória nativa e GBrain fazem parte da instalação.\n"
    "Vou configurar também o Honcho para continuidade entre conversas? Ele usa uma "
    "conta própria e processa contexto no serviço; pode ter custo. Responda 'sim' "
    "para configurar com segurança ou 'pular' para recusar. Não envie chaves aqui. "
    "Isso não desativa o GBrain nem muda a função do agente."
)


def carregar_estado() -> dict:
    if STATE.exists():
        state = json.loads(STATE.read_text())
        # Estado v0.3: a resposta antiga vira apenas a escolha do Honcho.
        if 'segundo_cerebro' in state and 'honcho' not in state:
            state['honcho'] = state['segundo_cerebro']
        return state
    return {}


def salvar_estado(st: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    import tempfile
    fd, name = tempfile.mkstemp(dir=STATE.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(st, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, STATE)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def proxima_pendente(st: dict):
    for chave, pergunta in PERGUNTAS:
        if chave not in st:
            return chave, pergunta
    if "bot_telegram" not in st:
        return ("bot_telegram",
                BOT_MSG.replace("{nome}", st.get("nome", "assistente")))
    if "github_token" not in st:
        return "github_token", GITHUB_MSG
    if "honcho" not in st:
        return "honcho", BRAIN_MSG
    return None, None


def aplicar_resposta(st: dict, chave: str, resposta: str) -> dict:
    st[chave] = resposta.strip()
    if chave == "dono_limites" and st[chave] == "":
        st[chave] = "(nenhum declarado)"
    return st


def preencher_artefatos(st: dict) -> None:
    """Onboarding concluido: grava soul e perfil no vault com as respostas."""
    soul_tpl = safe(HERMES_HOME / "SOUL.md")
    if soul_tpl.is_symlink():
        raise ValueError("SOUL é symlink")
    if soul_tpl.exists():
        texto = soul_tpl.read_text()
        for k, v in {
            "{{NOME_DO_AGENTE}}": "assistente" if st.get("nome") == "(pulado)" else st.get("nome", "assistente"),
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
        import re
        texto = re.sub(r"\n<!-- onboarding-aethon -->.*?<!-- /onboarding-aethon -->\n?", "\n", texto, flags=re.S)
        soul_tpl.write_text(texto)
        soul_tpl.chmod(0o600)

    rules = safe(VAULT / "AGENTS.md")
    if rules.is_symlink():
        raise ValueError("AGENTS privado é symlink")
    if rules.exists():
        text = rules.read_text().replace("{{NOME_DO_AGENTE}}", st.get("nome", "assistente"))
        rules.write_text(text.replace("{{NOME_DO_DONO}}", st.get("dono_nome", "")))
        rules.chmod(0o600)

    perfil = safe(VAULT / "01_IDENTIDADE" / "perfil.md")
    if perfil.is_symlink():
        raise ValueError("Perfil é symlink")
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
        perfil.chmod(0o600)

    # Projeta escolhas mesmo quando o SOUL preexistente não tem placeholders.
    from migrar import apply
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        apply()


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--iniciar", action="store_true", help="retorna a proxima pergunta")
    p.add_argument("--responder", nargs=2, metavar=("CHAVE", "RESPOSTA"))
    p.add_argument("--pular", metavar="CHAVE")
    return p.parse_args()


def main(args) -> int:
    import re
    if args.responder and re.search(r"(?:ghp_|github_pat_|sk-or-v1-)[A-Za-z0-9_\-]{12,}", args.responder[1]):
        print("ERRO: credencial recusada; utilize autenticação no terminal.")
        return 1
    st = carregar_estado()

    if args.iniciar and not st:
        st = {"_ativo": "true"}
        salvar_estado(st)

    if args.pular:
        prox, _ = proxima_pendente(st)
        if args.pular == "github_token" and args.pular == prox:
            st["github_token"] = "(pulado)"
            st["github_login"] = "(sem backup)"
        elif args.pular == prox:
            st[args.pular] = "(pulado)"
        else:
            print(f"ERRO:só é possível pular a pergunta atual ({prox})")
            return 1
        salvar_estado(st)
        from modulos import registrar_intencao
        registrar_intencao(st, already_locked=True)

    elif args.responder:
        chave, resposta = args.responder
        chaves_validas = {c for c, _ in PERGUNTAS} | {"github_token", "bot_telegram",
                                                      "honcho"}
        if chave not in chaves_validas:
            print(f"chave invalida: {chave}")
            return 1

        prox, _ = proxima_pendente(st)
        if chave != prox:
            print(f"ERRO: responda a pergunta atual ({prox})")
            return 1
        if chave == "github_token":
            answer = resposta.strip().lower()
            if answer not in PULAR | {"sim", "yes"}:
                print("ERRO: use sim ou pular. Não envie credenciais.")
                return 1
            st[chave] = "solicitado" if answer in {"sim", "yes"} else "(pulado)"
        elif chave == "honcho":
            answer = resposta.strip().lower()
            if answer not in PULAR | {"sim", "yes"}:
                print("ERRO: use sim ou pular.")
                return 1
            st[chave] = "solicitado" if answer in {"sim", "yes"} else "(pulado)"
            from modulos import registrar_intencao
            registrar_intencao(st, already_locked=True)
        else:
            if chave == "fuso" and resposta.strip().lower() not in PULAR:
                from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
                try:
                    ZoneInfo(resposta.strip())
                except (ValueError, ZoneInfoNotFoundError):
                    print("ERRO: fuso inválido; exemplo: America/Sao_Paulo")
                    return 1
            st = aplicar_resposta(st, chave, "(pulado)" if resposta.strip().lower() in PULAR else resposta)
        salvar_estado(st)

    chave, pergunta = proxima_pendente(st)
    if chave is None:
        if not st.get("_concluido"):
            preencher_artefatos(st)
            st["_concluido"] = True
            salvar_estado(st)
        backup = "não configurado (solicitação anotada)" if st.get("github_token") == "solicitado" else "não configurado"
        print("ONBOARDING_CONCLUIDO")
        print("Identidade configurada. Segundo cérebro é a função padrão; confira a instalação do GBrain e a recuperação antes de anunciar pronto.")
        print(f"Backup do vault: {backup}")
        if st.get('honcho') == 'solicitado':
            print("Etapa Honcho: continue pelo ativar-memoria.py no mesmo perfil; autenticação e validação fazem parte desta instalação.")
        print("Conexões e automações são opcionais: agenda, tarefas, YouTube ou outras que você escolher.")
        print("Cada uma depende de configuração e teste; nenhuma foi ativada aqui.")
        print("Quer configurar alguma agora, criar outra automação ou prefere me usar já?")
        return 0

    print(f"PERGUNTA:{chave}")
    print(pergunta)
    return 0


if __name__ == "__main__":
    import fcntl
    from private_state import locked
    args = parse_args()
    HERMES_HOME = safe(HERMES_HOME)
    VAULT = safe(VAULT)
    STATE = safe(HERMES_HOME / "state" / "onboarding.json")
    STATE.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(STATE.with_suffix('.lock'), os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as guard:
        fcntl.flock(guard, fcntl.LOCK_EX)
        with locked():
            raise SystemExit(main(args))
