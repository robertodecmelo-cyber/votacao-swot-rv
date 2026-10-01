-- ============================================================================
-- SCHEMA — Votação SWOT RV Digital 2027 (site único, 2 etapas)
-- Rode este script inteiro de uma vez no Supabase: SQL Editor > New query > Run
--
-- Este script é SEGURO para rodar MAIS DE UMA VEZ (idempotente) e é SEGURO
-- rodar em cima do projeto que já está em produção com os votos da etapa
-- Telecom + Ambos: ele não apaga nenhum voto. Ele faz uma MIGRAÇÃO ADITIVA:
--   - adiciona a coluna "stage" ('telecom' ou 'naotelecom') em todas as
--     tabelas que antes só conheciam um universo de votação;
--   - todo voto/edição/proposta que já existia é automaticamente marcado
--     como stage = 'telecom' (porque é exatamente isso que ele é: a etapa
--     Telecom + Ambos, que já estava rodando neste projeto);
--   - cria a tabela nova item_prioritized (checkbox de priorização do admin);
--   - cria a função save_vote nova, com o parâmetro de etapa.
--
-- Se você está criando um projeto Supabase do ZERO para este site único,
-- pode rodar este mesmo script — ele cria tudo já na estrutura final.
-- ============================================================================

create extension if not exists "pgcrypto";

-- ============================================================================
-- Tabela de votos: um registro por (etapa, quadrante, pessoa anônima)
-- ============================================================================
create table if not exists votes (
  id bigint generated always as identity primary key,
  stage text not null default 'telecom' check (stage in ('telecom','naotelecom')),
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  client_id uuid not null,
  scores jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table votes add column if not exists stage text not null default 'telecom';
update votes set stage = 'telecom' where stage is null;
alter table votes drop constraint if exists votes_stage_check;
alter table votes add constraint votes_stage_check check (stage in ('telecom','naotelecom'));
alter table votes drop constraint if exists votes_quadrant_client_id_key;
alter table votes drop constraint if exists votes_stage_quadrant_client_id_key;
alter table votes add constraint votes_stage_quadrant_client_id_key unique (stage, quadrant, client_id);

-- ============================================================================
-- Tabela de configuração: votação aberta/fechada por (etapa, quadrante)
-- ============================================================================
create table if not exists voting_config (
  stage text not null default 'telecom' check (stage in ('telecom','naotelecom')),
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  is_open boolean not null default true
);

alter table voting_config add column if not exists stage text not null default 'telecom';
update voting_config set stage = 'telecom' where stage is null;
alter table voting_config drop constraint if exists voting_config_pkey;
alter table voting_config add constraint voting_config_pkey primary key (stage, quadrant);
alter table voting_config drop constraint if exists voting_config_stage_check;
alter table voting_config add constraint voting_config_stage_check check (stage in ('telecom','naotelecom'));

insert into voting_config (stage, quadrant, is_open) values
  ('telecom', 'forcas', true),
  ('telecom', 'fraquezas', true),
  ('telecom', 'oportunidades', true),
  ('telecom', 'ameacas', true)
on conflict (stage, quadrant) do nothing;

-- A etapa Não Telecom + Ambos começa FECHADA de propósito: só deve abrir
-- depois que o admin priorizar os itens da etapa Telecom + Ambos (ver
-- tabela item_prioritized mais abaixo). Abra pelo botão "Votação aberta"
-- no painel admin, na aba Não Telecom + Ambos, quando estiver pronto.
insert into voting_config (stage, quadrant, is_open) values
  ('naotelecom', 'forcas', false),
  ('naotelecom', 'fraquezas', false),
  ('naotelecom', 'oportunidades', false),
  ('naotelecom', 'ameacas', false)
on conflict (stage, quadrant) do nothing;

-- Ativa a segurança em nível de linha (RLS)
alter table votes enable row level security;
alter table voting_config enable row level security;

-- Quem vota (sem login) pode INSERIR e ATUALIZAR seu próprio voto, mas NUNCA
-- pode LER a tabela de votos (por isso não existe policy de select aberta —
-- sem policy de select, a leitura fica bloqueada por padrão).
drop policy if exists "anon pode inserir seu voto" on votes;
create policy "anon pode inserir seu voto" on votes
  for insert to public
  with check (true);

drop policy if exists "anon pode atualizar seu voto" on votes;
create policy "anon pode atualizar seu voto" on votes
  for update to public
  using (true)
  with check (true);

-- Só administradores logados conseguem LER a tabela de votos.
drop policy if exists "admin pode ler todos os votos" on votes;
create policy "admin pode ler todos os votos" on votes
  for select to authenticated
  using (true);

-- Admin pode apagar todos os votos de uma etapa/quadrante ("Reiniciar votação").
drop policy if exists "admin pode remover votos" on votes;
create policy "admin pode remover votos" on votes
  for delete to authenticated
  using (true);

-- Qualquer pessoa (votante ou admin) pode ler se a votação está aberta/fechada.
drop policy if exists "qualquer pessoa pode ler o status da votacao" on voting_config;
create policy "qualquer pessoa pode ler o status da votacao" on voting_config
  for select to public
  using (true);

-- Só administradores logados podem abrir/fechar a votação.
drop policy if exists "admin pode alterar o status da votacao" on voting_config;
create policy "admin pode alterar o status da votacao" on voting_config
  for update to authenticated
  using (true)
  with check (true);

-- ============================================================================
-- Função save_vote_v2: grava o voto já com a etapa. Roda com "security
-- definer" para poder fazer upsert sem exigir permissão de leitura da
-- tabela votes de quem está votando (ver explicação detalhada no script
-- original — o motivo não mudou, só ganhou o parâmetro de etapa).
-- ============================================================================
create or replace function public.save_vote_v2(p_stage text, p_quadrant text, p_client_id uuid, p_scores jsonb)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  if p_stage not in ('telecom','naotelecom') then
    raise exception 'etapa invalida: %', p_stage;
  end if;
  if p_quadrant not in ('forcas','fraquezas','oportunidades','ameacas') then
    raise exception 'quadrante invalido: %', p_quadrant;
  end if;
  insert into votes (stage, quadrant, client_id, scores, updated_at)
  values (p_stage, p_quadrant, p_client_id, p_scores, now())
  on conflict (stage, quadrant, client_id)
  do update set scores = excluded.scores, updated_at = excluded.updated_at;
end;
$$;

revoke all on function public.save_vote_v2(text, text, uuid, jsonb) from public;
grant execute on function public.save_vote_v2(text, text, uuid, jsonb) to public;

-- Liga o Realtime na tabela de votos, para o painel administrativo
-- atualizar sozinho conforme os votos chegam.
do $$
begin
  if not exists (
    select 1 from pg_publication_tables
    where pubname = 'supabase_realtime' and schemaname = 'public' and tablename = 'votes'
  ) then
    alter publication supabase_realtime add table votes;
  end if;
end $$;

-- ============================================================================
-- Tabela de edição rápida dos textos dos itens, agora por (etapa, quadrante).
-- ============================================================================
create table if not exists item_edits (
  stage text not null default 'telecom' check (stage in ('telecom','naotelecom')),
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  item_id text not null,
  title text not null,
  updated_at timestamptz not null default now()
);
alter table item_edits add column if not exists stage text not null default 'telecom';
update item_edits set stage = 'telecom' where stage is null;
alter table item_edits drop constraint if exists item_edits_pkey;
alter table item_edits add constraint item_edits_pkey primary key (stage, quadrant, item_id);
alter table item_edits drop constraint if exists item_edits_stage_check;
alter table item_edits add constraint item_edits_stage_check check (stage in ('telecom','naotelecom'));
alter table item_edits enable row level security;

drop policy if exists "qualquer pessoa pode ler os textos editados" on item_edits;
create policy "qualquer pessoa pode ler os textos editados" on item_edits
  for select to public
  using (true);
drop policy if exists "admin pode criar edicoes de texto" on item_edits;
create policy "admin pode criar edicoes de texto" on item_edits
  for insert to authenticated
  with check (true);
drop policy if exists "admin pode atualizar edicoes de texto" on item_edits;
create policy "admin pode atualizar edicoes de texto" on item_edits
  for update to authenticated
  using (true)
  with check (true);
drop policy if exists "admin pode remover edicoes de texto" on item_edits;
create policy "admin pode remover edicoes de texto" on item_edits
  for delete to authenticated
  using (true);

-- ============================================================================
-- Tabela de propostas ADICIONADAS pelo admin durante a reunião, por
-- (etapa, quadrante). origin agora também aceita 'Não Telecom', usado
-- quando a proposta é criada diretamente na etapa Não Telecom + Ambos.
-- ============================================================================
create table if not exists item_added (
  stage text not null default 'telecom' check (stage in ('telecom','naotelecom')),
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  item_id text not null,
  title text not null,
  origin text not null default 'Ambos',
  division text,
  created_at timestamptz not null default now()
);
alter table item_added add column if not exists stage text not null default 'telecom';
update item_added set stage = 'telecom' where stage is null;
alter table item_added drop constraint if exists item_added_pkey;
alter table item_added add constraint item_added_pkey primary key (stage, quadrant, item_id);
alter table item_added drop constraint if exists item_added_stage_check;
alter table item_added add constraint item_added_stage_check check (stage in ('telecom','naotelecom'));
alter table item_added drop constraint if exists item_added_origin_check;
alter table item_added add constraint item_added_origin_check check (origin in ('Telecom','Ambos','Não Telecom'));
alter table item_added enable row level security;

drop policy if exists "qualquer pessoa pode ler propostas adicionadas" on item_added;
create policy "qualquer pessoa pode ler propostas adicionadas" on item_added
  for select to public
  using (true);
drop policy if exists "admin pode criar propostas" on item_added;
create policy "admin pode criar propostas" on item_added
  for insert to authenticated
  with check (true);
drop policy if exists "admin pode remover propostas adicionadas" on item_added;
create policy "admin pode remover propostas adicionadas" on item_added
  for delete to authenticated
  using (true);

-- ============================================================================
-- Tabela de propostas ORIGINAIS ocultadas da votação, por (etapa, quadrante).
-- ============================================================================
create table if not exists item_removed (
  stage text not null default 'telecom' check (stage in ('telecom','naotelecom')),
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  item_id text not null,
  removed_at timestamptz not null default now()
);
alter table item_removed add column if not exists stage text not null default 'telecom';
update item_removed set stage = 'telecom' where stage is null;
alter table item_removed drop constraint if exists item_removed_pkey;
alter table item_removed add constraint item_removed_pkey primary key (stage, quadrant, item_id);
alter table item_removed drop constraint if exists item_removed_stage_check;
alter table item_removed add constraint item_removed_stage_check check (stage in ('telecom','naotelecom'));
alter table item_removed enable row level security;

drop policy if exists "qualquer pessoa pode ler propostas ocultadas" on item_removed;
create policy "qualquer pessoa pode ler propostas ocultadas" on item_removed
  for select to public
  using (true);
drop policy if exists "admin pode ocultar propostas" on item_removed;
create policy "admin pode ocultar propostas" on item_removed
  for insert to authenticated
  with check (true);
drop policy if exists "admin pode restaurar propostas ocultadas" on item_removed;
create policy "admin pode restaurar propostas ocultadas" on item_removed
  for delete to authenticated
  using (true);

-- ============================================================================
-- Tabela de ordem manual do ranking (Top N), por (etapa, quadrante).
-- ============================================================================
create table if not exists rank_overrides (
  stage text not null default 'telecom' check (stage in ('telecom','naotelecom')),
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  item_id text not null,
  position integer not null,
  updated_at timestamptz not null default now()
);
alter table rank_overrides add column if not exists stage text not null default 'telecom';
update rank_overrides set stage = 'telecom' where stage is null;
alter table rank_overrides drop constraint if exists rank_overrides_pkey;
alter table rank_overrides add constraint rank_overrides_pkey primary key (stage, quadrant, item_id);
alter table rank_overrides drop constraint if exists rank_overrides_stage_check;
alter table rank_overrides add constraint rank_overrides_stage_check check (stage in ('telecom','naotelecom'));
alter table rank_overrides enable row level security;

drop policy if exists "admin pode ler ordem do ranking" on rank_overrides;
create policy "admin pode ler ordem do ranking" on rank_overrides
  for select to authenticated
  using (true);
drop policy if exists "admin pode gravar ordem do ranking" on rank_overrides;
create policy "admin pode gravar ordem do ranking" on rank_overrides
  for insert to authenticated
  with check (true);
drop policy if exists "admin pode atualizar ordem do ranking" on rank_overrides;
create policy "admin pode atualizar ordem do ranking" on rank_overrides
  for update to authenticated
  using (true)
  with check (true);
drop policy if exists "admin pode limpar ordem do ranking" on rank_overrides;
create policy "admin pode limpar ordem do ranking" on rank_overrides
  for delete to authenticated
  using (true);

-- ============================================================================
-- Tabela NOVA: priorização (checkbox do admin na etapa Telecom + Ambos).
-- A existência de uma linha (quadrant, item_id) significa "priorizado".
-- É sempre relativa à etapa Telecom + Ambos (é dali que vem a priorização
-- que define o SWOT final e os itens com tag Ambos que migram para a
-- votação Não Telecom + Ambos) — por isso não tem coluna "stage".
-- ============================================================================
create table if not exists item_prioritized (
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  item_id text not null,
  prioritized_at timestamptz not null default now(),
  primary key (quadrant, item_id)
);
alter table item_prioritized enable row level security;

drop policy if exists "qualquer pessoa pode ler priorizacao" on item_prioritized;
create policy "qualquer pessoa pode ler priorizacao" on item_prioritized
  for select to public
  using (true);
drop policy if exists "admin pode priorizar itens" on item_prioritized;
create policy "admin pode priorizar itens" on item_prioritized
  for insert to authenticated
  with check (true);
drop policy if exists "admin pode despriorizar itens" on item_prioritized;
create policy "admin pode despriorizar itens" on item_prioritized
  for delete to authenticated
  using (true);

-- ============================================================================
-- Verificação rápida: rode esta consulta separadamente (selecione só as
-- linhas abaixo e clique em "Run") para conferir se tudo ficou certo.
-- ============================================================================
-- select schemaname, tablename, policyname, roles, cmd
-- from pg_policies
-- where tablename in ('votes','voting_config','item_edits','item_added','item_removed','rank_overrides','item_prioritized')
-- order by tablename, policyname;
--
-- select stage, quadrant, count(*) from votes group by 1,2 order by 1,2;
