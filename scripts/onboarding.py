#!/usr/bin/env python3
"""Onboarding do agente — primeira conversa no Telegram.

Fluxo: nome do agente -> apresentação livre -> Honcho opcional.
O agente organiza texto/áudio/documentos e pergunta apenas informações faltantes.

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

# Nome, apresentação livre e escolha do Honcho. Sem questionário obrigatório.
PERGUNTAS = [
    ("nome", "Como você quer me chamar?"),
    ("apresentacao", "Me conta um pouco sobre você e como gostaria que eu te ajudasse.\n\n"
     "Como prefere ser chamado e como gosta de conversar? Com o que trabalha, "
     "como é sua rotina e o que é importante para você hoje?\n\n"
     "Conta também onde está tendo dificuldade: organizar tarefas, cumprir prazos, "
     "manter hábitos, estudar, cuidar do negócio ou lidar com assuntos pessoais. "
     "O que você gostaria de ter mais organizado ou acompanhado?\n\n"
     "Pode incluir sua idade, interesses e preferências, se quiser. Mande um áudio, "
     "texto, PDF ou resumo de outra IA — não precisa seguir uma ordem nem responder "
     "tudo. Eu organizo e pergunto depois só o que faltar."),
]
PERFIL = {'dono_nome', 'dono_faz', 'dono_desejos', 'dono_limites', 'estilo', 'fuso',
          'idade', 'rotina', 'interesses', 'dificuldades', 'preferencias'}
BRAIN_MSG = ("Quer adicionar o Honcho para ajudar na continuidade entre conversas? "
             "Posso configurar e explicar a opção disponível antes de conectar. "
             "Responda sim ou pular.")


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
    if st.get('_concluido'):
        return None, None
    for chave, pergunta in PERGUNTAS:
        # Instalações antigas já podem ter respondido o perfil em perguntas separadas.
        if chave == 'apresentacao' and any(k in st for k in PERFIL):
            continue
        if chave not in st:
            return chave, pergunta
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
        if st.get('apresentacao') not in (None, '(pulado)'):
            fields = {k: st[k] for k in sorted(PERFIL) if st.get(k) not in (None, '', '(pulado)')}
            if fields and '<!-- aethon-perfil -->' not in texto:
                texto += ('\n<!-- aethon-perfil -->\n## Perfil organizado\n\n'
                          'Origem: [apresentação do dono](apresentacao.md).\n\n'
                          + json.dumps(fields, ensure_ascii=False, indent=2) + '\n<!-- /aethon-perfil -->\n')
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
    p.add_argument("--apresentacao-json", metavar="ARQUIVO", help="Texto extraído e perfil organizado pelo agente; arquivo privado JSON")
    return p.parse_args()


def main(args) -> int:
    import re
    st = carregar_estado()
    organized = None
    if args.apresentacao_json:
        if args.responder or args.pular or proxima_pendente(st)[0] != 'apresentacao':
            raise ValueError('Apresentação fora da etapa atual ou argumentos conflitantes')
        organized = json.loads(safe(args.apresentacao_json).read_text())
        if not isinstance(organized, dict) or set(organized) - {'texto', 'perfil', 'origem'}:
            raise ValueError('Use texto, perfil e origem')
        text = organized.get('texto')
        fields = organized.get('perfil', {})
        origin = organized.get('origem', 'mensagem do dono')
        if not isinstance(text, str) or not text.strip() or len(text) > 50000:
            raise ValueError('Texto extraído vazio/inválido ou maior que 50000 caracteres')
        if not isinstance(origin, str) or len(origin) > 500:
            raise ValueError('Origem inválida')
        if not isinstance(fields, dict) or set(fields) - PERFIL:
            raise ValueError('Campo de perfil desconhecido')
        if any(not isinstance(v, str) or len(v) > 1200 for v in fields.values()) or len(json.dumps(fields)) > 8000:
            raise ValueError('Valores do perfil precisam ser textos curtos')
        if fields.get('fuso'):
            from zoneinfo import ZoneInfo
            ZoneInfo(fields['fuso'])
        args.responder = ['apresentacao', text]
    submitted = json.dumps(organized, ensure_ascii=False) if organized else (args.responder[1] if args.responder else '')
    if re.search(r"(?:ghp_|github_pat_|sk-or-v1-)[A-Za-z0-9_\-]{12,}", submitted):
        print("ERRO: credencial recusada; utilize autenticação no terminal.")
        return 1

    if args.responder and len(args.responder[1]) > (50000 if args.responder[0] == 'apresentacao' else 128):
        raise ValueError('Resposta muito longa; use material privado com resumo e origem')

    if args.iniciar and not st:
        st = {"_ativo": "true"}
        salvar_estado(st)

    if args.pular:
        prox, _ = proxima_pendente(st)
        if args.pular == prox:
            st[args.pular] = "(pulado)"
        else:
            print(f"ERRO:só é possível pular a pergunta atual ({prox})")
            return 1
        salvar_estado(st)
        from modulos import registrar_intencao
        registrar_intencao(st, already_locked=True)

    elif args.responder:
        chave, resposta = args.responder
        chaves_validas = {c for c, _ in PERGUNTAS} | {"honcho"}
        if chave not in chaves_validas:
            print(f"chave invalida: {chave}")
            return 1

        prox, _ = proxima_pendente(st)
        if chave != prox:
            print(f"ERRO: responda a pergunta atual ({prox})")
            return 1
        if chave == "honcho":
            answer = resposta.strip().lower()
            if answer not in PULAR | {"sim", "yes"}:
                print("ERRO: use sim ou pular.")
                return 1
            st[chave] = "solicitado" if answer in {"sim", "yes"} else "(pulado)"
            from modulos import registrar_intencao
            registrar_intencao(st, already_locked=True)
        else:
            st = aplicar_resposta(st, chave, "(pulado)" if resposta.strip().lower() in PULAR else resposta)
        if chave == 'apresentacao' and st[chave] != '(pulado)':
            from private_state import atomic
            if organized:
                st.update({k: v for k, v in organized.get('perfil', {}).items() if v.strip()})
            origin = organized.get('origem', 'mensagem do dono') if organized else 'mensagem do dono'
            target = safe(VAULT / '01_IDENTIDADE/apresentacao.md')
            if target.exists():
                raise ValueError('Apresentação existente: revise antes de substituir')
            atomic(target, ('# Apresentação do dono\n\nOrigem: ' + origin + '\n\n' + st[chave] + '\n').encode())
            st[chave] = str(target)
        salvar_estado(st)
        if chave == 'nome':
            # O nome escolhido já identifica o agente durante a configuração.
            for target in [HERMES_HOME / 'SOUL.md', VAULT / 'AGENTS.md']:
                target = safe(target)
                if target.exists():
                    target.write_text(target.read_text().replace('{{NOME_DO_AGENTE}}',
                        'assistente' if st[chave] == '(pulado)' else st[chave]))
            from migrar import apply
            import contextlib, io
            with contextlib.redirect_stdout(io.StringIO()):
                apply()

    chave, pergunta = proxima_pendente(st)
    if chave is None:
        if not st.get("_concluido"):
            preencher_artefatos(st)
            st["_concluido"] = True
            salvar_estado(st)
        print("ONBOARDING_CONCLUIDO")
        print("Identidade configurada. Segundo cérebro é a função padrão; confira a instalação do GBrain e a recuperação antes de anunciar pronto.")

        if st.get('honcho') == 'solicitado':
            print("Etapa Honcho: continue pelo ativar-memoria.py no mesmo perfil; autenticação e validação fazem parte desta instalação.")
        print("Conexões e automações são opcionais: agenda, tarefas, YouTube ou outras que você escolher.")
        print("Cada uma depende de configuração e teste; nenhuma foi ativada aqui.")
        print("Comece pela necessidade informada pelo dono; sem questionário adicional de serviços.")
        print('Ao concluir, configure e valide a consulta semanal sem LLM por ativar-atualizacoes.py e docs/atualizacoes.md. Ela avisa sobre atualizações pendentes; para aplicar, o dono pede “Verifique e atualize meu agente pelo template”. Sem agendamento confirmado, informe pendência.')
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
