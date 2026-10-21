import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'SOS_PAE'))
from interface import modo_noturno

@pytest.mark.parametrize('hora,minuto,esperado', [(0,0,True),(5,59,True),(6,0,False),(12,0,False),(16,59,False),(17,0,True),(23,59,True)])
def test_horario_fortaleza(hora,minuto,esperado):
    assert modo_noturno(datetime(2026,10,20,hora,minuto,tzinfo=ZoneInfo('America/Fortaleza'))) is esperado

def test_horario_independe_do_servidor():
    assert modo_noturno(datetime(2026,10,20,20,0,tzinfo=timezone.utc))
    assert not modo_noturno(datetime(2026,10,20,9,0,tzinfo=timezone.utc))

def test_seletor_manual_sem_opcao_automatica(tmp_path, monkeypatch):
    from streamlit.testing.v1 import AppTest
    monkeypatch.setenv('SOS_MODO','local')
    monkeypatch.setenv('SOS_DATA_DIR',str(tmp_path))
    monkeypatch.setenv('SOS_SENHA_INICIAL','TesteLocal2026!')
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'SOS_PAE' / 'app.py'), default_timeout=30).run()
    assert not app.exception
    assert not app.toggle
    app.radio(key='sos_tema_visual').set_value('☀ Claro').run()
    assert not app.session_state.sos_modo_escuro
    app.radio(key='sos_tema_visual').set_value('☾ Escuro').run()
    assert app.session_state.sos_modo_escuro
    app.run()
    assert app.session_state.sos_modo_escuro
    assert not app.exception
