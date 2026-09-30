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

-- Quem vota (sem login) pode INSERIR e ATUALIZAR seu próprio voto, mas NUNCA
-- pode LER a tabela de votos (por isso não existe policy de select aberta —
-- sem policy de select, a leitura fica bloqueada por padrão).
-- Usamos "to public" (em vez de "to anon") para não depender de qual papel
-- exato o Supabase atribui à requisição — isso não abre brecha nenhuma, porque
-- a policy já era totalmente aberta (with check (true)); a segurança do
-- anonimato vem da ausência de uma policy de SELECT para quem não é admin.
create policy "anon pode inserir seu voto" on votes
  for insert to public
  with check (true);

create policy "anon pode atualizar seu voto" on votes
  for update to public
  using (true)
  with check (true);

-- Só administradores logados (usuários criados em Authentication > Users)
-- conseguem LER a tabela de votos — é isso que restringe o painel de resultados.
create policy "admin pode ler todos os votos" on votes
  for select to authenticated
  using (true);

-- Qualquer pessoa (votante ou admin) pode ler se a votação está aberta/fechada.
create policy "qualquer pessoa pode ler o status da votacao" on voting_config
  for select to public
  using (true);

-- Só administradores logados podem abrir/fechar a votação.
create policy "admin pode alterar o status da votacao" on voting_config
  for update to authenticated
  using (true)
  with check (true);

-- Liga o Realtime na tabela de votos, para o painel administrativo
-- atualizar sozinho conforme os votos chegam.
alter publication supabase_realtime add table votes;

-- ============================================================================
-- Tabela de edição rápida dos textos dos itens (usada pelo painel admin para
-- corrigir o texto de uma pergunta/proposta durante a reunião, sem precisar
-- editar código nem reenviar arquivos — a mudança aparece para quem está
-- votando em poucos segundos).
-- ============================================================================
create table if not exists item_edits (
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  item_id text not null,
  title text not null,
  updated_at timestamptz not null default now(),
  primary key (quadrant, item_id)
);

alter table item_edits enable row level security;

-- Qualquer pessoa (votante ou admin) pode ler os textos editados, para que
-- a tela de votação sempre mostre a versão mais atual.
create policy "qualquer pessoa pode ler os textos editados" on item_edits
  for select to public
  using (true);

-- Só administradores logados podem criar, alterar ou remover uma edição de texto.
create policy "admin pode criar edicoes de texto" on item_edits
  for insert to authenticated
  with check (true);

create policy "admin pode atualizar edicoes de texto" on item_edits
  for update to authenticated
  using (true)
  with check (true);

create policy "admin pode remover edicoes de texto" on item_edits
  for delete to authenticated
  using (true);
