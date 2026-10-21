# Validação da entrega

Data: 20/10/2026.
Base: 0d62acd87b54629c5bae2c5ab98ba763ba36be34.
Ambiente: Windows, Python 3.12.10.

- `python -m pytest -q`: **21 testes passaram** (108,69 segundos).
- `python -m pip check`: nenhuma dependência incompatível encontrada.
- `git diff --check`: sem erros de espaços nas alterações.
- Busca por padrões comuns de tokens GitHub/Supabase/JWT nos fontes, testes e documentos novos: nenhuma correspondência. Isso não equivale a uma auditoria de segredos completa.
- Exclusão de dados locais, anexos, ambientes Python, caches e arquivos temporários da entrega.
- O JSON demonstrativo legado foi removido por não ser utilizado pelo aplicativo.

Cobertura: cinco perfis, login/troca de senha/saída, abertura dos menus, botão Início,
preservação de bases com zero/um/nove/dez alunos, permissões de consulta, indisponibilidade
do banco com simulação, conflito de versão zero e tema/manual/horários de Fortaleza.
Inspeções visuais no navegador foram feitas ao longo do desenvolvimento para contraste,
seletores, formulário, upload, agenda e gráficos, usando dados fictícios.

Não executados: testes contra Supabase real, construção Docker e CI Linux.
Os screenshots mostram a evolução visual e não substituem validação da versão final.
