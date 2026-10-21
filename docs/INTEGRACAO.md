# Integração do MVP SOS Exatas

## Escopo da entrega

Base: commit `0d62acd87b54629c5bae2c5ab98ba763ba36be34` de F1siko/sos-exatas-pae.
Branch de desenvolvimento: `codex/ambiente-testes`.
Esta entrega inclui interface, modo local, correções de persistência e permissões.
Não é apenas uma troca de arquivos de imagem ou de CSS.

- Visão geral com indicadores calculados, modalidades e busca de estudantes com sugestões.
- Identidade SOS, favicon, tema claro/escuro e navegação Início.
- Tema inicial por horário de Fortaleza (escuro 17h–6h), com escolha manual até a próxima faixa de horário.
- Modo local com dados fictícios, separado do Supabase.
- Preservação de bases pequenas, falha de banco sem fallback de demonstração e comparação de versão zero.
- Consulta de agenda e contratos para os perfis previstos; links de arquivos na nuvem com duração de cinco minutos.

## Revisão antes da integração

1. Revisar a PR e executar os testes em Python 3.12.
2. Usar um Supabase separado para testar o fluxo remoto. O SQL em supabase/schema-testes.sql é exclusivo de testes; não executar em produção sem análise do esquema e das políticas existentes.
3. Conferir as tabelas sistema_estado e materiais_oficiais e o bucket materiais_oficiais. Para arquivos privados, usar bucket privado. O app utiliza service_role no servidor; nunca enviar essa chave ao navegador.
4. Se a tabela sistema_estado já tiver dados, não definir SOS_PERMITIR_BOOTSTRAP=1.
5. Testar no staging dois usuários editando, interrupção de conexão, links temporários, upload e download, contratos e agenda.

## Migração dos anexos existentes

Pare a aplicação antes da cópia. Faça backup do banco, do Storage e das pastas locais
abaixo, incluindo dados/notas e dados/notificacoes. Registre também a versão anterior do
código e suas dependências para poder voltar a ela.

Caminhos relativos ao diretório de trabalho atual do servidor:

| Origem anterior | Destino novo (SOS_DATA_DIR=dados) |
| --- | --- |
| fichas_professores/ | dados/fichas_professores/ |
| envios_alunos/ | dados/envios_alunos/ |
| docs_professores/ | dados/docs_professores/ |
| dados/notas/ | permanece no mesmo caminho |
| dados/notificacoes/ | permanece no mesmo caminho |

Copie os arquivos conservando exatamente seus nomes. Não mova nem apague as origens
antes de validar os downloads. Se já existir um arquivo com mesmo nome no destino,
compare o conteúdo e resolva divergências antes de continuar. Configure SOS_DATA_DIR
como caminho absoluto para eliminar dependência do diretório de execução.

Se os anexos não existirem mais no disco da instalação antiga, esta atualização não
os recupera: será necessário usar um backup. Em contêineres, monte um volume persistente
para SOS_DATA_DIR. Não use o sistema de arquivos efêmero como armazenamento definitivo.

## Configuração e publicação

- Python 3.12; instalar SOS_PAE/requirements.txt.
- SOS_MODO=supabase (também é o padrão).
- SUPABASE_URL e SUPABASE_KEY do servidor configuradas como segredos.
- SOS_DATA_DIR apontando para o diretório persistente migrado.
- SOS_SENHA_INICIAL só é necessária para inicialização de uma base vazia.
- O arquivo .env.example é uma referência; .env não é lido automaticamente.
- Construção Docker: `docker build -t sos-pae:mvp SOS_PAE`.
- O Docker escuta em 8080. Configure o serviço e o proxy conforme o ambiente.
- As proteções CORS/XSRF padrão foram restauradas; validar acesso no domínio real do staging.

## Validação e limites

A suíte automatizada cobre os cinco perfis, navegação, retorno ao Início, troca inicial
de senha, horários do tema, permissões, preservação de cadastros e falhas de banco com
simulações. Os testes usam dados temporários e não acessam produção.

A integração real com Supabase, a imagem Docker e o fluxo de CI Linux não foram
executados nesta máquina Windows. A interface foi inspecionada no navegador, mas
não houve uma auditoria completa de segurança ou acessibilidade.
O modo local foi feito para demonstração sequencial em um processo; não é o backend
recomendado para múltiplos usuários. Permanecem pendentes normalização do banco,
revogação de sessões, revisão de autorização por estudante e persistência na nuvem
de todas as notas/notificações/anexos. Não usar a senha de demonstração em produção.

## Reversão

Pare o serviço, restaure o código e as dependências anteriores e reaponte a aplicação
para os dados respaldados. Se houve alterações no banco durante o teste, avalie antes
se é necessário restaurar o backup: não descarte lançamentos novos sem revisão.
As pastas de origem preservadas permitem reativar o caminho anterior dos anexos.

## Referência visual e mídia

Logo fornecida pelo solicitante. Design adaptado, sem copiar os arquivos de design,
a partir de Monty, de Valeria Gutsu:
https://www.behance.net/gallery/256155715/Monty-Simplifying-Affiliate-Management
Os prints em docs/imagens usam apenas dados fictícios e mostram etapas da evolução
visual. O código desta entrega é a fonte de verdade para os ajustes finais.
