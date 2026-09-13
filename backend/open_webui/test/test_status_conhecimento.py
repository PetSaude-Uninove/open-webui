"""Regressão de petsaude-platform#41: bloqueio no inlet deixava o status de busca aberto."""
import asyncio
import pathlib
import re


def _carregar_helper():
    """Carrega só a função auxiliar do middleware, sem importar o pacote inteiro."""
    fonte = pathlib.Path(__file__).resolve().parents[1] / "utils" / "middleware.py"
    codigo = fonte.read_text(encoding="utf-8")
    inicio = codigo.index("async def encerrar_status_conhecimento(")
    fim = codigo.index("async def process_chat_payload(", inicio)
    ns = {}
    exec(codigo[inicio:fim], ns)
    return ns["encerrar_status_conhecimento"], codigo


def test_helper_emite_status_done_e_oculto():
    helper, _ = _carregar_helper()
    eventos = []

    async def emitter(evento):
        eventos.append(evento)

    asyncio.run(helper(emitter, "pergunta"))
    assert eventos == [{
        "type": "status",
        "data": {"action": "knowledge_search", "query": "pergunta", "done": True, "hidden": True},
    }]


def test_os_dois_blocos_de_excecao_dos_filtros_fecham_o_status():
    _, codigo = _carregar_helper()
    inicio = codigo.index("async def process_chat_payload(")
    fim = codigo.index("features = form_data.pop(\"features\", None)", inicio)
    trecho = codigo[inicio:fim]
    blocos = re.findall(r"except Exception as e:\n(.*?)raise", trecho, flags=re.S)
    assert len(blocos) == 2, "esperava os dois blocos de exceção (pipeline inlet e filter functions)"
    for bloco in blocos:
        assert "encerrar_status_conhecimento(event_emitter, user_message)" in bloco
