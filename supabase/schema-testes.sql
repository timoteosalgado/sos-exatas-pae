-- Executar SOMENTE em projeto Supabase exclusivo para testes.
create table if not exists public.sistema_estado (
 id text primary key,
 dados jsonb not null,
 atualizado_em timestamptz not null default now()
);
alter table public.sistema_estado enable row level security;
create table if not exists public.materiais_oficiais (
 id uuid primary key default gen_random_uuid(),
 titulo text not null, descricao text, disciplina text, serie text, tipo text,
 modulo text, tags text, autor text, versao text, file_path text not null,
 file_size_kb numeric, file_ext text, criado_por text,
 criado_em timestamptz not null default now()
);
alter table public.materiais_oficiais enable row level security;
-- Sem políticas anon/authenticated: acesso apenas pelo servidor com service_role.
-- Criar manualmente bucket materiais_oficiais no Storage do projeto de testes.
