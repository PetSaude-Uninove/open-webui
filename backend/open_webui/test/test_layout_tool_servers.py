import pathlib

LAYOUT = pathlib.Path(__file__).resolve().parents[3] / "src" / "routes" / "(app)" / "+layout.svelte"


def test_layout_nao_carrega_conexoes_globais_no_navegador():
    """As conexões globais (TOOL_SERVER_CONNECTIONS, que incluem o PubMed MCP
    em http://pubmed-mcp:8000/mcp) são resolvidas no backend. O navegador não
    alcança a rede interna e só lê OpenAPI; carregá-las no layout gera o toast
    "Falha ao conectar ao servidor da ferramenta OpenAPI" para admins."""
    codigo = LAYOUT.read_text(encoding="utf-8")
    assert "getToolServerConnections" not in codigo
    assert "TOOL_SERVER_CONNECTIONS" not in codigo


def test_layout_carrega_so_os_servidores_do_usuario():
    codigo = LAYOUT.read_text(encoding="utf-8")
    inicio = codigo.index("const setToolServers = async () => {")
    fim = codigo.index("toolServers.set(toolServersData);", inicio)
    trecho = codigo[inicio:fim]
    assert trecho.count("getToolServersData(") == 1
    assert "getToolServersData($settings?.toolServers ?? [])" in trecho
