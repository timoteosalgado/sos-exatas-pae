from pathlib import Path
from streamlit.testing.v1 import AppTest
import pytest

APP = Path(__file__).resolve().parents[1] / 'SOS_PAE' / 'app.py'

@pytest.mark.parametrize("login", ["admin", "coordenacao", "professor", "aluno", "familia"])
def test_login_troca_senha_e_saida(tmp_path, monkeypatch, login):
    monkeypatch.setenv('SOS_MODO','local')
    monkeypatch.setenv('SOS_DATA_DIR',str(tmp_path))
    monkeypatch.setenv('SOS_SENHA_INICIAL','TesteLocal2026!')
    app = AppTest.from_file(str(APP), default_timeout=30).run()
    assert not app.exception
    assert app.warning
    app.text_input[0].input(login)
    app.text_input[1].input('TesteLocal2026!')
    app.button[0].click().run()
    assert not app.exception
    assert any('nova senha' in t.value.lower() for t in app.title)
    app.text_input[0].input('TesteLocal2026!')
    app.text_input[1].input('NovaSenhaTeste2026!')
    app.text_input[2].input('NovaSenhaTeste2026!')
    app.button[0].click().run()
    assert not app.exception
    assert app.sidebar.selectbox or app.sidebar.radio
    if login in ('admin','coordenacao','professor'):
        modules = list(next(x for x in app.sidebar.selectbox if x.label == 'Módulo Principal:').options)
        for module in modules:
            next(x for x in app.sidebar.selectbox if x.label == 'Módulo Principal:').select(module).run()
            assert not app.exception, module
            radios = [r for r in app.sidebar.radio if r.label != 'Aparência']
            if not radios:
                continue
            for option in list(radios[0].options):
                next(r for r in app.sidebar.radio if r.label != 'Aparência').set_value(option).run()
                assert not app.exception, option
    else:
        for option in list(next(r for r in app.sidebar.radio if r.label != 'Aparência').options):
            next(r for r in app.sidebar.radio if r.label != 'Aparência').set_value(option).run()
            assert not app.exception, option
    app.button(key='voltar_inicio').click().run()
    assert not app.exception
    assert any(t.value == 'Visão geral' for t in app.title)
    next(b for b in app.button if 'Logout' in b.label).click().run()
    assert not app.exception
    assert any(b.label == 'Acessar o Sistema' for b in app.button)
