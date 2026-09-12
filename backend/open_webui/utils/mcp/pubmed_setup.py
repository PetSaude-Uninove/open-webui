"""
Setup script to register PubMed MCP server with Open WebUI

Fonte única de verdade para a configuração e o registro do PubMed MCP.
`app.state.config` é uma instância de `open_webui.config.AppConfig`, que
persiste apenas via atribuição de atributo (`__setattr__`/`__getattr__`);
ela não tem `.get` nem suporta atribuição por item (`obj["chave"] = valor`).
"""
import logging
import os

log = logging.getLogger("open_webui.pubmed_mcp")
log.setLevel(logging.INFO)

PUBMED_MCP_ID = "pubmed-mcp"
PUBMED_MCP_URL = os.getenv("PUBMED_MCP_URL", "http://pubmed-mcp:8000/mcp")


def get_pubmed_mcp_config() -> dict:
    """Get the PubMed MCP server configuration"""
    return {
        "type": "mcp",
        "url": PUBMED_MCP_URL,
        "path": "/mcp",
        "spec_type": "url",
        "spec": "",
        "auth_type": "none",
        "key": "",
        "config": {
            "enable": True,
            "access_control": None,
        },
        "info": {
            "id": PUBMED_MCP_ID,
            "name": "PubMed MCP Server",
            "description": "Busca e análise de literatura médica no PubMed",
        },
    }


def registrar_pubmed_mcp(app_state) -> bool:
    """
    Registra o PubMed MCP em app_state.config.TOOL_SERVER_CONNECTIONS.

    app_state.config só persiste por atribuição de atributo, por isso a
    lista é lida, alterada em memória e reatribuída ao atributo (nunca via
    `.get`/item assignment, que não existem em AppConfig).

    Retorna True se registrou agora, False se já existia ou se algo falhou.
    """
    try:
        conns = list(app_state.config.TOOL_SERVER_CONNECTIONS or [])

        ja_existe = any(
            (conn.get("info", {}) or {}).get("id") == PUBMED_MCP_ID
            or conn.get("url") == PUBMED_MCP_URL
            for conn in conns
        )

        if ja_existe:
            log.info("PubMed MCP já está registrado em TOOL_SERVER_CONNECTIONS")
            return False

        conns.append(get_pubmed_mcp_config())
        app_state.config.TOOL_SERVER_CONNECTIONS = conns

        log.info("PubMed MCP registrado com sucesso em TOOL_SERVER_CONNECTIONS")
        return True
    except Exception:
        log.exception("Falha ao registrar o PubMed MCP")
        return False


async def setup_pubmed_mcp(app_state) -> bool:
    """Wrapper assíncrono chamado no lifespan de main.py."""
    return registrar_pubmed_mcp(app_state)
