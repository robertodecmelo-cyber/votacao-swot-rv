-- ============================================================================
-- SCHEMA — Votação SWOT RV Digital 2027
-- Rode este script inteiro de uma vez no Supabase: SQL Editor > New query > Run
-- Este script é seguro para rodar MAIS DE UMA VEZ (idempotente): se algo já
-- existir, ele recria do jeito certo em vez de dar erro "already exists".
-- Se o erro de RLS voltar a aparecer no site, rode este script inteiro de
-- novo — ele corrige qualquer policy que tenha sido perdida ou sobrescrita.
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
drop policy if exists "anon pode inserir seu voto" on votes;
create policy "anon pode inserir seu voto" on votes
  for insert to public
  with check (true);

drop policy if exists "anon pode atualizar seu voto" on votes;
create policy "anon pode atualizar seu voto" on votes
  for update to public
  using (true)
  with check (true);

-- Só administradores logados (usuários criados em Authentication > Users)
-- conseguem LER a tabela de votos — é isso que restringe o painel de resultados.
drop policy if exists "admin pode ler todos os votos" on votes;
create policy "admin pode ler todos os votos" on votes
  for select to authenticated
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
-- Função save_vote: é por AQUI que o site grava o voto — em vez de fazer um
-- "upsert" direto na tabela a partir do navegador.
--
-- Motivo: quando a mesma pessoa salva o voto uma 2ª vez (já existe uma linha
-- dela naquele quadrante), o Postgres precisa localizar essa linha para
-- decidir "atualizar em vez de inserir" — e isso exige, por regra do próprio
-- Postgres, uma permissão de LEITURA (SELECT) na tabela. Só que a gente
-- propositalmente NÃO dá select a quem não é administrador (é isso que
-- impede qualquer votante de ver os votos dos outros). Resultado: a 2ª
-- gravação batia na regra de segurança e dava o erro
-- "new row violates row-level security policy for table votes".
--
-- A função abaixo roda com "security definer" (privilégio de quem a criou,
-- normalmente o dono do banco), então ela mesma consegue inserir/atualizar
-- sem precisar que quem chamou tenha permissão de leitura na tabela. Só
-- damos permissão para EXECUTAR a função (não para ler a tabela) — o
-- anonimato continua garantido.
-- ============================================================================
create or replace function public.save_vote(p_quadrant text, p_client_id uuid, p_scores jsonb)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  if p_quadrant not in ('forcas','fraquezas','oportunidades','ameacas') then
    raise exception 'quadrante invalido: %', p_quadrant;
  end if;
  insert into votes (quadrant, client_id, scores, updated_at)
  values (p_quadrant, p_client_id, p_scores, now())
  on conflict (quadrant, client_id)
  do update set scores = excluded.scores, updated_at = excluded.updated_at;
end;
$$;

-- Remove qualquer permissão antiga e concede só o necessário: qualquer
-- pessoa (logada ou não) pode EXECUTAR a função (ou seja, gravar seu voto),
-- mas isso não dá acesso de leitura à tabela.
revoke all on function public.save_vote(text, uuid, jsonb) from public;
grant execute on function public.save_vote(text, uuid, jsonb) to public;

-- Liga o Realtime na tabela de votos, para o painel administrativo
-- atualizar sozinho conforme os votos chegam. (Se já estiver ligado, o
-- bloco abaixo simplesmente não faz nada — por isso o "do $$ ... $$".)
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
drop policy if exists "qualquer pessoa pode ler os textos editados" on item_edits;
create policy "qualquer pessoa pode ler os textos editados" on item_edits
  for select to public
  using (true);

-- Só administradores logados podem criar, alterar ou remover uma edição de texto.
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

-- Admin pode apagar todos os votos de um quadrante (botão "Reiniciar votação").
drop policy if exists "admin pode remover votos" on votes;
create policy "admin pode remover votos" on votes
  for delete to authenticated
  using (true);

-- ============================================================================
-- Tabela de propostas ADICIONADAS pelo admin durante a reunião (além das
-- que já vêm prontas no site). Aparecem na votação como qualquer outro item.
-- ============================================================================
create table if not exists item_added (
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  item_id text not null,
  title text not null,
  origin text not null default 'Ambos' check (origin in ('Telecom','Ambos')),
  division text,
  created_at timestamptz not null default now(),
  primary key (quadrant, item_id)
);
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
-- Tabela de propostas ORIGINAIS que o admin decidiu OCULTAR da votação
-- (não apaga a proposta do site, só esconde — pode ser restaurada depois).
-- ============================================================================
create table if not exists item_removed (
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  item_id text not null,
  removed_at timestamptz not null default now(),
  primary key (quadrant, item_id)
);
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
-- Tabela de ordem manual do ranking (Top N): o admin pode reordenar as
-- posições exibidas no painel administrativo. Só o admin lê/escreve aqui —
-- não interfere na votação em si, apenas na exibição do ranking.
-- ============================================================================
create table if not exists rank_overrides (
  quadrant text not null check (quadrant in ('forcas','fraquezas','oportunidades','ameacas')),
  item_id text not null,
  position integer not null,
  updated_at timestamptz not null default now(),
  primary key (quadrant, item_id)
);
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
-- Verificação rápida: rode esta consulta separadamente (selecione só as
-- linhas abaixo e clique em "Run") para conferir se tudo ficou certo.
-- ============================================================================
-- select schemaname, tablename, policyname, roles, cmd
-- from pg_policies
-- where tablename in ('votes','voting_config','item_edits','item_added','item_removed','rank_overrides')
-- order by tablename, policyname;
