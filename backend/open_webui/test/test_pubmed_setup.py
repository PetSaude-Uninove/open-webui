from open_webui.utils.mcp.pubmed_setup import get_pubmed_mcp_config
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
