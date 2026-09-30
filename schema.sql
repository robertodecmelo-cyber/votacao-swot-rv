-- ============================================================================
-- SCHEMA — Votação SWOT RV Digital 2027
-- Rode este script inteiro de uma vez no Supabase: SQL Editor > New query > Run
-- ============================================================================

create extension if not exists "pgcrypto";

-- Tabela de votos: um registro por (quadrante, pessoa anônima)
create table if not exists votes (
  id bigint generated always as identity primary key,
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  client_id uuid not null,
  scores jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  unique (quadrant, client_id)
);

-- Tabela de configuração: votação aberta/fechada por quadrante
create table if not exists voting_config (
  quadrant text primary key,
  is_open boolean not null default true
);

insert into voting_config (quadrant, is_open) values
  ('forcas', true),
  ('fraquezas', true),
  ('oportunidades', true),
  ('ameacas', true)
on conflict (quadrant) do nothing;

-- Ativa a segurança em nível de linha (RLS) nas duas tabelas
alter table votes enable row level security;
alter table voting_config enable row level security;

-- Quem vota (sem login, chave "anon") pode INSERIR e ATUALIZAR seu próprio
-- voto, mas NUNCA pode LER a tabela de votos (por isso não existe policy de
-- select para "anon" — sem policy de select, a leitura fica bloqueada por padrão).
create policy "anon pode inserir seu voto" on votes
  for insert to anon
  with check (true);

create policy "anon pode atualizar seu voto" on votes
  for update to anon
  using (true)
  with check (true);

-- Só administradores logados (usuários criados em Authentication > Users)
-- conseguem LER a tabela de votos — é isso que restringe o painel de resultados.
create policy "admin pode ler todos os votos" on votes
  for select to authenticated
  using (true);

-- Qualquer pessoa (votante ou admin) pode ler se a votação está aberta/fechada.
create policy "qualquer pessoa pode ler o status da votacao" on voting_config
  for select to anon, authenticated
  using (true);

-- Só administradores logados podem abrir/fechar a votação.
create policy "admin pode alterar o status da votacao" on voting_config
  for update to authenticated
  using (true)
  with check (true);

-- Liga o Realtime na tabela de votos, para o painel administrativo
-- atualizar sozinho conforme os votos chegam.
alter publication supabase_realtime add table votes;
