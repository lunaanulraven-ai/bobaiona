# CLAUDE.md

Contexto fixo do projeto. Leia antes de qualquer edição e respeite em todas elas.
O roteiro do que construir está em `plano-bobaiona.md`.

## O que é

Página-presente romântica, **arquivo único** `index.html` (HTML + CSS + JS inline).
Feita pelo Cazé pra namorada (Vick). A meta é evoluí-la pra que os dois editem e
deixem mensagens, fotos e músicas um pro outro.

## Tom e identidade (não descaracterizar)

- Português **brincalhão e carinhoso**. Apelidos: *bobaião* = Cazé, *bobaiona* = Vick.
  Qualquer texto de interface novo segue esse tom.
- Identidade visual: fontes **Fraunces / Caveat / Spectral**, paleta **plum / rose / gold**
  (variáveis em `:root`). Não trocar a "cara" da página.

## Nunca quebrar

- A capa `#cover` e o botão **"abrir"** (é o gatilho que libera o áudio também).
- A acessibilidade já existente: skip-link, `:focus-visible`, `alt` e `loading` nas imagens.
- O conteúdo já escrito nos capítulos (são memórias reais — não reescrever sem pedir).

## Decisões trancadas (implementar, não re-discutir)

1. **Sync via Supabase** (backend grátis). `localStorage` vira só cache offline; a fonte de
   verdade é o Supabase.
2. **Música via YouTube IFrame Player API** com `start`/`end` pra tocar só um trecho.
   **Nunca Spotify** (embed só toca prévia de ~30s e não deixa escolher o trecho).
3. **Duas versões de conteúdo:** `caze` e `vick`, com seletor no topo. Cada um edita a sua;
   os dois veem as duas.
4. **Temas:** paletas predefinidas trocando as variáveis CSS de `:root`.
5. **Editor amigável** pra quem não programa: tocar pra escrever, botão de foto do celular,
   colar link de música + início/fim, escolher tema. **Sem JSON nem termos técnicos** na frente
   da Vick.
6. **Senha leve** pra editar (não pra ver).
7. O editor "Blocos" / `#advEditor` está no HTML sem JS — **remover** por enquanto.

## Estrutura do index.html (555 linhas)

- Linhas 1–130: `<head>` + CSS inline completo.
- Linhas 130–178: `<body>` abertura, capa `#cover`, botões de editor.
- Linhas 180–393: `<main>` — 11 capítulos/seções, galeria polaroid, chats, footer.
- Linhas 394–555: `<script>` — reveal por IntersectionObserver, barra de progresso, editor inline, localStorage.

## Config Supabase (bloco no topo do `<script>`)

```js
const SUPABASE_URL = ''; // Project URL
const SUPABASE_ANON_KEY = ''; // anon public key
```

Tabela `paginas`: `id` (text PK — `"caze"` ou `"vick"`), `conteudo` (jsonb), `atualizado_em` (timestamp).

## Como trabalhar

- Mexer em **uma fase de cada vez** e testar antes de seguir.
- Usar **git**: commit a cada fase concluída, pra dar pra reverter.
- Continua sendo arquivo único. Só sugerir separar se o arquivo ficar difícil de manter — e perguntar antes.
- Em dúvida sobre conteúdo pessoal (textos, fotos, datas), **perguntar** em vez de inventar.

## Fases (ordem de implementação)

1. **Fase 1 — Música** (YouTube IFrame, player flutuante, trecho por seção, liberar no "abrir").
2. **Fase 2 — Versões + temas** (seletor caze/vick, 5 paletas com nomes carinhosos).
3. **Fase 3 — Supabase + editor amigável + senha** (sync real, UI sem termos técnicos).
4. **Fase 4 — Polimento** (remover Blocos, offline, mobile, acessibilidade).