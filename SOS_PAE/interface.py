from pathlib import Path
import base64
from html import escape

import streamlit as st

ASSETS = Path(__file__).parent / 'assets'

def modo_noturno(agora=None):
    from datetime import datetime
    from zoneinfo import ZoneInfo
    local = (agora or datetime.now(ZoneInfo('America/Fortaleza'))).astimezone(ZoneInfo('America/Fortaleza'))
    return local.hour >= 17 or local.hour < 6


@st.fragment(run_every='60s')
def _acompanhar_horario():
    if st.session_state.get('_sos_periodo_noturno') != modo_noturno():
        st.rerun()


def aplicar_tema():
    periodo = modo_noturno()
    if st.session_state.get('_sos_periodo_noturno') != periodo or 'sos_tema_visual' not in st.session_state:
        st.session_state.sos_tema_visual = '☾ Escuro' if periodo else '☀ Claro'
        st.session_state._sos_periodo_noturno = periodo
    with st.sidebar.container(key='seletor-aparencia'):
        escolha = st.radio('Aparência', ['☀ Claro', '☾ Escuro'], key='sos_tema_visual', horizontal=True, label_visibility='collapsed')
    escuro = escolha == '☾ Escuro'
    st.session_state.sos_modo_escuro = escuro
    _acompanhar_horario()
    css = (ASSETS / 'theme.css').read_text(encoding='utf-8')
    css += (ASSETS / 'workspace.css').read_text(encoding='utf-8')
    if escuro:
        css += (ASSETS / 'dark.css').read_text(encoding='utf-8')
    st.markdown('<style>' + css + '</style>', unsafe_allow_html=True)
    import plotly.express as px
    px.defaults.template = 'plotly_dark' if escuro else 'plotly_white'


def marca(tamanho=180, centralizado=False):
    logo = base64.b64encode((ASSETS / 'sos-exatas.png').read_bytes()).decode()
    align = 'center' if centralizado else 'left'
    st.markdown(f'<div class="sos-brand" style="text-align:{align}"><div class="sos-logo" style="width:{tamanho}px"><img src="data:image/png;base64,{logo}" alt="SOS Exatas"></div><div class="sos-brand-label">PORTAL DE APRENDIZAGEM</div></div>', unsafe_allow_html=True)

def cabecalho(escolha, usuario):
    nome = escape(usuario.get('nome', ''))
    st.markdown(f'<div class="workspace-bar"><span>SOS Exatas <span class="breadcrumb">/ &nbsp; Área de trabalho</span></span><span class="user-chip"><span class="online-dot"></span>{nome}</span></div>', unsafe_allow_html=True)

def _ir(modulo, acao):
    st.session_state.nav_modulo = modulo
    st.session_state.nav_acao = acao

def painel(db, perfil, usuario, aluno):
    from datetime import date
    gestor = perfil in ('admin', 'coordenador')
    equipe = gestor or perfil == 'professor'
    alunos = db['alunos'] if equipe else ({aluno['dados']['id']: aluno} if aluno else {})
    st.markdown('<div class="page-eyebrow">ÁREA DE TRABALHO / PAINEL</div>', unsafe_allow_html=True)
    st.title('Visão geral')
    st.caption('Acompanhe o desempenho acadêmico e organize sua rotina.')
    valores = list(alunos.values())
    filtro, pesquisa = st.columns([1.1, 1.5])
    with filtro:
        modalidade_ativa = st.selectbox('Modalidade do painel', ['Todas as modalidades'] + ['Mentoria Acadêmica Presencial', 'Mentoria Acadêmica Virtual', 'Banca de Estudos'], key='painel_modalidade')
    if modalidade_ativa != 'Todas as modalidades':
        valores = [a for a in valores if modalidade_ativa in a['dados'].get('modalidades', [])]
    with pesquisa:
        if equipe:
            opcoes = {a['dados']['id']: a for a in valores}
            if st.session_state.get('painel_aluno_busca') not in opcoes:
                st.session_state.painel_aluno_busca = None
            selecionado = st.selectbox(
                'Buscar estudante',
                sorted(opcoes, key=lambda aid: opcoes[aid]['dados'].get('nome', '').casefold()),
                index=None,
                format_func=lambda aid: f"{opcoes[aid]['dados'].get('nome', 'Estudante')} ({aid})",
                placeholder='Digite o nome e selecione o estudante…',
                key='painel_aluno_busca',
            )
            if selecionado:
                valores = [opcoes[selecionado]]
    st.markdown('<div class="scope-note"><span class="online-dot"></span> Indicadores dos estudantes exibidos · histórico completo</div>', unsafe_allow_html=True)
    horas = sum(a.get('operacao', {}).get('horas_realizadas', 0) for a in valores)
    contratadas = sum(a.get('operacao', {}).get('horas_contratadas', 0) for a in valores)
    atendimentos = sum(len(a.get('atendimentos_processo', [])) for a in valores)
    renovacoes = [a for a in valores if a.get('operacao', {}).get('horas_contratadas', 0) - a.get('operacao', {}).get('horas_realizadas', 0) <= 3]
    labels = [('Estudantes' if equipe else 'Meu acompanhamento', len(valores), 'na base de acompanhamento'), ('Horas realizadas', f'{horas:,.0f} h', f'de {contratadas:,.0f} h contratadas'), ('Atendimentos registrados', atendimentos, 'registros no histórico'), ('Renovações a acompanhar', len(renovacoes), 'saldo de até 3 horas')]
    for idx, (col, (label, value, desc)) in enumerate(zip(st.columns(4), labels)):
        with col:
            st.markdown(f'<div class="stat-card {"featured" if idx == 1 else ""}"><div class="stat-label">{label}</div><div class="stat-value">{value}</div><div class="stat-caption">{desc}</div></div>', unsafe_allow_html=True)
    st.write('')
    grafico, resumo = st.columns([1.65, 1], gap='medium')
    with grafico:
        linhas = ''
        grupos = [('Presencial', 'Mentoria Acadêmica Presencial'), ('Virtual', 'Mentoria Acadêmica Virtual'), ('Banca de estudos', 'Banca de Estudos')]
        total = len(valores)
        for nome, grupo in grupos:
            quantidade = sum(grupo in a['dados'].get('modalidades', []) for a in valores)
            largura = quantidade / total * 100 if total else 0
            linhas += f'<div class="distribution-row"><div><span>{nome}</span><strong>{quantidade}</strong></div><div class="bar-track"><div style="width:{largura:.2f}%"></div></div></div>'
        st.markdown(f'<section class="analytics-card"><div class="card-heading"><h3>Distribuição de estudantes</h3><span class="subtle-pill">Por modalidade</span></div>{linhas}<p class="chart-note">Um estudante pode participar de mais de uma modalidade.</p></section>', unsafe_allow_html=True)
    with resumo:
        percentual = max(0, min(100, horas / contratadas * 100)) if contratadas else 0
        percentual_texto = f'{horas / contratadas * 100:.0f}%' if contratadas else '—'
        st.markdown(f'<section class="analytics-card"><div class="card-heading"><h3>Utilização de horas</h3><span class="subtle-pill">Acumulado</span></div><div class="utilization"><div class="donut" style="--progress:{percentual:.2f}%"><div><strong>{percentual_texto}</strong><span>realizadas</span></div></div><div class="donut-legend"><p><i></i>Realizadas <strong>{horas:g} h</strong></p><p><i></i>Saldo contratual <strong>{contratadas - horas:g} h</strong></p></div></div><p class="chart-note">Percentual sobre as horas contratadas.</p></section>', unsafe_allow_html=True)
    st.write('')
    if equipe:
        st.markdown('<div class="quick-label">AÇÕES RÁPIDAS</div>', unsafe_allow_html=True)
        targets = [('Registrar atendimento', 'Planeje e registre a evolução.', '📄 Produzir Relatório de Acompanhamento', '📝 Relatório do Acompanhamento'), ('Consultar estudantes' if gestor else 'Publicar uma ficha', 'Encontre o próximo passo de cada aluno.' if gestor else 'Compartilhe materiais de estudo.', '🏫 Gestão Geral & Comunidade' if gestor else '📁 Materiais & Conteúdos', '📋 Diretório Geral' if gestor else '📁 Upload de Fichas de Estudo'), ('Abrir agenda', 'Organize aulas e compromissos.', '📅 Agenda & Compromissos', '📅 Agenda & Calendário')]
        for col, (title, desc, module, action) in zip(st.columns(3), targets):
            with col:
                with st.container():
                    st.button(title + ' →', key='shortcut_'+action, on_click=_ir, args=(module, action), use_container_width=True)
    left, right = st.columns([1.65, 1], gap='large')
    with left:
        st.subheader('Estudantes em acompanhamento' if equipe else 'Meu percurso')
        with st.container(border=True):
            filtrados = valores
            if not filtrados:
                st.info('Nenhum estudante encontrado para esta busca.')
            for a in filtrados[:6]:
                d, op = a['dados'], a.get('operacao', {})
                nome = escape(d.get('nome', 'Estudante'))
                iniciais = escape(''.join(p[0] for p in d.get('nome', '').split()[:2]))
                saldo = op.get('horas_contratadas', 0) - op.get('horas_realizadas', 0)
                modalidade = escape(' · '.join(d.get('modalidades', [])))
                status = 'Renovação' if saldo <= 3 else 'Em acompanhamento'
                st.markdown(f'<div class="student-row"><div class="avatar">{iniciais}</div><div class="student-info"><strong>{nome}</strong><span>{modalidade}</span></div><div class="student-status"><span class="status-pill">{status}</span><small>{saldo:g} h de saldo</small></div></div>', unsafe_allow_html=True)
            if len(filtrados) > 6:
                st.caption(f'Exibindo 6 de {len(filtrados)} estudantes. Use a busca para encontrar outros.')
    with right:
        st.subheader('Próximos compromissos')
        with st.container(border=True):
            eventos = sorted([e for e in db.get('agenda', []) if e.get('data', '') >= date.today().isoformat()], key=lambda e:(e.get('data',''), e.get('horario','')))
            if not eventos:
                st.markdown('<div class="empty-state"><span class="empty-icon">▦</span><strong>Sua agenda está livre</strong><p>Os próximos compromissos aparecem aqui assim que forem cadastrados.</p></div>', unsafe_allow_html=True)
            for e in eventos[:4]:
                st.markdown(f'<div class="agenda-row"><span class="page-eyebrow">{escape(e.get("data", ""))} · {escape(e.get("horario", ""))}</span><strong>{escape(e.get("titulo", ""))}</strong><p>{escape(e.get("local_ou_link", ""))}</p></div>', unsafe_allow_html=True)
        st.subheader('Atenção aos próximos passos')
        with st.container(border=True):
            if renovacoes:
                st.write(f'{len(renovacoes)} estudante(s) com saldo de até 3 horas.')
            else:
                st.markdown('<div class="attention-ok"><span>✓</span><div><strong>Sem alertas de renovação</strong><p>Os saldos de horas estão acima do limite de atenção.</p></div></div>', unsafe_allow_html=True)
    st.caption('Indicadores calculados a partir dos cadastros e registros disponíveis. Horas e atendimentos podem incluir saldos anteriores.')
