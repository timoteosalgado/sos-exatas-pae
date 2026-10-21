import ast
import copy
from pathlib import Path
from enum import Enum
import pytest

APP = Path(__file__).resolve().parents[1] / 'SOS_PAE' / 'app.py'
TREE = ast.parse(APP.read_text(encoding='utf-8'))

def extract(names, scope):
    nodes = [n for n in TREE.body if getattr(n, 'name', None) in names or
             isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets)]
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(APP), 'exec'), scope)
    return scope

@pytest.mark.parametrize('count', [0, 1, 9, 10])
def test_preserva_cadastros(count):
    template = dict(usuarios={}, professores=[], alunos={}, habilidades_cadastradas=[], mensagens_familias=[], docs_professores=[], config=dict(periodos=[], disciplinas=[]), bloqueios={}, auditoria=[], agenda=[])
    scope = extract({'sanitizar_banco'}, {'_template_banco': lambda: copy.deepcopy(template), '_VERSAO_ESTADO':'versao', 'novo_id':lambda p:'novo'})
    alunos = {f'ALU-{i}': {'dados': {'nome':f'Teste {i}'}} for i in range(count)}
    result = scope['sanitizar_banco']({'alunos':copy.deepcopy(alunos)})
    assert set(result['alunos']) == set(alunos)
    assert [a['dados']['nome'] for a in result['alunos'].values()] == [a['dados']['nome'] for a in alunos.values()]

def test_permissoes_de_consulta_sem_edicao():
    s = extract({'Perfil','_BASE_PROF','PERMISSOES','pode'}, {'Enum':Enum})
    for perfil in ('aluno','familia','professor','coordenador','admin'):
        assert s['pode'](perfil, 'consultar_agenda')
    assert s['pode']('familia', 'consultar_contratos')
    for perfil in ('aluno','familia'):
        assert not s['pode'](perfil, 'gerenciar_agenda')
        assert not s['pode'](perfil, 'gerenciar_contratos')
    assert not s['pode']('desconhecido','visualizar')

def test_indisponibilidade_nao_retorna_demo():
    class Offline:
        def table(self,*args): raise ConnectionError('offline')
    class Log:
        def warning(self,*args): pass
    node = next(n for n in TREE.body if getattr(n,'name',None)=='_carregar_banco_remoto')
    node = copy.deepcopy(node)
    node.decorator_list = []
    scope = {'supabase':Offline(), 'log':Log(), 'Optional':__import__('typing').Optional}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(APP),'exec'),scope)
    with pytest.raises(RuntimeError, match='indisponível'):
        scope['_carregar_banco_remoto']()

def test_conflito_versao_zero_nao_sobrescreve():
    from typing import Optional
    from datetime import datetime, timezone
    class Query:
        def __init__(self): self.filters=[]
        def table(self,*a): return self
        def update(self,*a): return self
        def eq(self,*a): self.filters.append(a); return self
        def execute(self): return type('Response',(),{'data':[]})()
    query=Query()
    scope=extract({'ConflitoDeVersao','salvar_banco'}, {'Optional':Optional, 'MODO_LOCAL':False, '_VERSAO_ESTADO':'versao','supabase':query,'datetime':datetime,'timezone':timezone})
    dados={'versao':0}
    with pytest.raises(scope['ConflitoDeVersao']):
        scope['salvar_banco'](dados)
    assert ('dados->>versao','0') in query.filters
    assert dados['versao']==0
