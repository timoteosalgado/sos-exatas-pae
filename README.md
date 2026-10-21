# SOS Exatas — MVP

Portal em Streamlit com perfis de administrador, coordenação, professor, aluno e família.
Inclui identidade SOS Exatas, Visão geral, busca com sugestões, tema claro/escuro,
agenda, contratos, acompanhamento pedagógico e ambiente de demonstração local.

## Executar para testes no Windows

Requer Python 3.12. Na raiz do projeto:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt --no-cache-dir
powershell -ExecutionPolicy Bypass -File .\Iniciar-Testes.ps1
```

Abra http://127.0.0.1:8501. O servidor local escuta somente neste computador.
Contas fictícias: admin, coordenacao, professor, aluno, familia.
Senha inicial da demonstração: `TesteLocal2026!`; troca exigida no primeiro acesso.
Os dados locais ficam em dados_teste/ e são ignorados pelo Git. A biblioteca em nuvem
exige um Supabase separado. Não colocar dados pessoais no ambiente demonstrativo.
Para encerrar, pressione Ctrl+C no terminal que executa o servidor.

O menu abre recolhido. A seta superior esquerda abre a barra lateral, onde há Início
e o seletor Claro/Escuro. O tema segue o horário de Fortaleza na abertura e nas
mudanças de faixa (17h/6h); uma escolha manual vale até a próxima mudança de faixa.

## Verificações

```powershell
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pip check
```

As versões principais estão fixadas em SOS_PAE/requirements.txt.
requirements-lock-windows.txt registra o ambiente validado no Windows.
O fluxo .github/workflows/tests.yml foi preparado para testar a PR em Linux/Python 3.12.

## Supabase, migração e implantação

Consulte [o guia de integração](docs/INTEGRACAO.md) antes de substituir uma instalação.
**Os caminhos dos anexos mudaram:** é necessário copiar os arquivos e configurar
armazenamento persistente. A entrega também altera permissões e comportamento do banco.

.env.example documenta as variáveis; a aplicação não carrega .env automaticamente.
Credenciais Supabase devem ficar apenas no servidor. O SQL fornecido é para um
projeto exclusivo de testes. Não executar automaticamente em produção.

## Escopo do MVP

A suíte cobre os fluxos principais em modo local. Validações remotas, persistência
em produção e revisão completa de segurança ainda são necessárias antes de usar
com dados reais. Ver [limitações e reversão](docs/INTEGRACAO.md).
