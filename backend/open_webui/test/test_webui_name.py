import pathlib


def _read(relative_path: str) -> str:
    raiz = pathlib.Path(__file__).resolve().parents[3]
    return (raiz / relative_path).read_text(encoding="utf-8")


def test_webui_name_nao_recebe_sufixo_open_webui():
    """O tema AskKlog exige que WEBUI_NAME (ex.: 'AskMed') seja usado tal
    como configurado, sem o antigo sufixo ' (Open WebUI)' que o upstream
    adicionava a qualquer nome customizado."""
    codigo = _read("backend/open_webui/env.py")
    assert '" (Open WebUI)"' not in codigo
    assert "WEBUI_NAME += " not in codigo
    assert 'WEBUI_NAME = os.environ.get("WEBUI_NAME", "Open WebUI")' in codigo


def test_custom_css_existe_e_usa_o_azul_da_marca_askklog():
    """static/static/custom.css é carregado em toda página (src/app.html) e
    deve conter o tema visual AskKlog, identificado pelo azul de marca."""
    conteudo = _read("static/static/custom.css")
    assert conteudo.strip() != ""
    assert "#41a5ee" in conteudo
