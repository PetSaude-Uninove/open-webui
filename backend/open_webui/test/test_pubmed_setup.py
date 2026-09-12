from open_webui.utils.mcp.pubmed_setup import get_pubmed_mcp_config, registrar_pubmed_mcp
from open_webui.utils import medical_integration


def test_config_do_pubmed_aponta_para_streamable_http():
    cfg = get_pubmed_mcp_config()
    assert cfg["url"] == "http://pubmed-mcp:8000/mcp"
    assert cfg["type"] == "mcp"
    assert cfg["info"]["id"] == "pubmed-mcp"


def test_medical_integration_usa_a_mesma_url():
    assert medical_integration.get_pubmed_mcp_config()["url"] == "http://pubmed-mcp:8000/mcp"


def test_medical_integration_usa_o_mesmo_dicionario_de_config():
    assert medical_integration.get_pubmed_mcp_config() == get_pubmed_mcp_config()


class FakeAppConfig:
    """Imita open_webui.config.AppConfig: só acesso por atributo, sem .get nem item assignment."""

    def __init__(self, conns=None):
        object.__setattr__(self, "_state", {"TOOL_SERVER_CONNECTIONS": list(conns or [])})
        object.__setattr__(self, "saves", 0)

    def __getattr__(self, key):
        return self._state[key]

    def __setattr__(self, key, value):
        self._state[key] = value
        object.__setattr__(self, "saves", self.saves + 1)


class FakeState:
    def __init__(self, conns=None):
        self.config = FakeAppConfig(conns)


def test_registra_uma_vez_e_persiste_por_atributo():
    st = FakeState()
    assert registrar_pubmed_mcp(st) is True
    assert st.config.saves == 1
    conns = st.config.TOOL_SERVER_CONNECTIONS
    assert len(conns) == 1 and conns[0]["type"] == "mcp" and conns[0]["url"].endswith("/mcp")
    assert conns[0]["config"]["enable"] is True and conns[0]["info"]["id"] == "pubmed-mcp"


def test_nao_duplica_por_id_nem_por_url():
    st = FakeState([{"type": "mcp", "url": "http://pubmed-mcp:8000/mcp", "info": {"id": "outro"}}])
    assert registrar_pubmed_mcp(st) is False
    st2 = FakeState([{"type": "mcp", "url": "http://x/mcp", "info": {"id": "pubmed-mcp"}}])
    assert registrar_pubmed_mcp(st2) is False


def test_ensure_retorna_true_quando_ja_existe():
    st = FakeState([get_pubmed_mcp_config()])
    assert medical_integration.ensure_pubmed_mcp_registered(st) is True
