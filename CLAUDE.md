# CLAUDE.md
Contexto fixo do projeto. Leia antes de qualquer edição e respeite em todas elas.

## O que é
Página-presente romântica, **arquivo único** `index.html` (HTML + CSS + JS inline).
Feita pelo Cazé pra namorada (Vick). Os dois editam e deixam mensagens, fotos e
músicas um pro outro.

## Tom e identidade (não descaracterizar)
- Português **brincalhão e carinhoso**. Apelidos: *bobaião* = Cazé, *bobaiona* = Vick.
  Qualquer texto de interface novo segue esse tom.
- Identidade visual: fontes **Fraunces / Caveat / Spectral**, paleta **plum / rose / gold**
  (variáveis em `:root`). Não trocar a "cara" da página.

## Nunca quebrar
- A capa `#cover` e o botão **"abrir"** (gatilho que libera o áudio).
- A acessibilidade já existente: skip-link, `:focus-visible`, `alt` e `loading` nas imagens.
- O conteúdo já escrito nos capítulos (são memórias reais — não reescrever sem pedir).
- O sistema de blocos em árvore (`_blocks`) e o Supabase sync.

## Decisões trancadas (implementar, não re-discutir)
1. **Sync via Supabase** — fonte de verdade. `localStorage` é só cache offline.
   - `id="shared"`: `{ blocks, music }` — conteúdo compartilhado entre os dois.
   - `id="caze_prefs"` e `id="vick_prefs"`: `{ theme, colors, fonts }` — prefs por pessoa.
2. **Conteúdo compartilhado** — blocos são os mesmos pra Cazé e Vick. O que muda por
   versão são só as prefs (tema, fontes, cores). Cada bloco tem um `autor` ("caze"/"vick"/null)
   que controla o alinhamento (estilo WhatsApp: autor fica à direita na sua versão).
3. **Música via YouTube IFrame Player API** com `start`/`end` por seção.
   Nunca Spotify. Suporte a links normais e Shorts.
4. **Temas:** 5 paletas predefinidas trocando variáveis CSS do `:root`, por versão.
5. **Editor amigável** pra quem não programa: toolbar por bloco, painel lateral (desktop),
   bottom sheet com abas edit/music/style/add (mobile). Sem JSON nem termos técnicos.
6. **Senha leve** pra editar (não pra ver). Hardcoded como `'bobaiona'`.
7. **Upload de mídia** via Supabase Storage (bucket `midia`, público).
   Limite de 10MB por arquivo. URL pública salva no bloco.

## Arquitetura atual (~2200 linhas)
- `<head>`: CSS inline (~220 linhas)
- `<body>`: esqueleto HTML (conteúdo real vem do Supabase em runtime)
- `<script>`: toda a lógica JS (~1900 linhas)

### Sistemas principais
- **Blocos em árvore**: `hero/chapter/finale` como raízes; `story/pull/note/chat/
  polaroid/gallery/vwall/vfeat/stats/menu` como filhos de chapter.
- **`parsePageToBlocks()`**: parse do HTML original como fallback offline.
- **`renderBlocks()`**: reconstrói `#main` a partir de `_blocks`.
- **`_rebuildToolbars()`**: toolbar `↑↓✎+🗑` em modo edição.
- **Editor desktop**: `#blkPanel` (painel lateral direito).
- **Editor mobile**: `#blkSheet` (bottom sheet com abas, alça de drag).
- **Font picker**: `_mkFontPicker()` — busca ao vivo via Google Fonts API
  (key: `AIzaSyBbjlDbRZrWCPyMlEuKqN9WFwoa0wHedP8`), preview lazy.
- **Color picker por bloco**: swatch + input hex, reset de estilo.
- **Cores/fontes globais por versão**: `_buildColorPickers()`, 7 CSS vars.
- **Supabase sync**: `supaLoad(ver)`, `supaSave(ver, payload)`.
  Headers explícitos `sb_publishable_` (não usa SDK).
- **Auto-reload**: `_checkFreshness()` compara `atualizado_em` do shared e prefs.
  Não recarrega se `editMode === true` — mostra toast de aviso.
- **Service Worker**: `sw.js` com VERSION bump automático via pre-commit hook.
- **Autor por bloco**: `data.autor = "caze"|"vick"|null`.
  `.blk-autor-eu` (direita) / `.blk-autor-outro` (esquerda), relativo ao `currentVersion`.

## Config Supabase
```js
const SUPABASE_URL = 'https://vmkzffuwsndmpkgpxzbz.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_Pcq-v4gUzOy_6SdmnkSR2Q_cw3h9kYJ';
const EDIT_PASSWORD = 'bobaiona';
```

## Deploy
- GitHub Pages: `lunaanulraven-ai.github.io/bobaiona`
- Service Worker path: `/bobaiona/sw.js`
- Pre-commit hook atualiza `VERSION` no `sw.js` automaticamente.

### Cloudflare Worker (proxy Piped)
O proxy está em `worker/piped-proxy.js`. Para publicar:
```bash
cd worker
npx wrangler deploy
```
Após o deploy, copiar a URL exibida (formato `piped-proxy.SEU_SUBDOMINIO.workers.dev`)
e atualizar a constante `PIPED_PROXY` no topo do `<script>` em `index.html`.

## Como trabalhar
- Leia este arquivo antes de qualquer edição.
- Uma mudança por vez. Commit ao final de cada mudança com mensagem clara.
- Arquivo único `index.html`. Só sugerir separar se ficar inviável — perguntar antes.
- Em dúvida sobre conteúdo pessoal (textos, fotos, datas): **perguntar**.
- Se contexto chegar a 80%+: `/compact`. Se 100%: nova sessão com este arquivo como contexto.
- Não muda CSS da página base sem motivo. Não muda textos dos capítulos.

## Bugs conhecidos / pendentes
- `removeMusicBtn` não chama `saveAll()` após remover música.
- `rstBtn` (reset de estilo) chama `_openPanel` em vez de `_refreshPanel`.
- Toast de reload fica no DOM se usuário sair do edit mode sem recarregar.
- Upload direto de vídeo não existe — vwall/vfeat só aceitam URL manual.
- Save concorrente sem merge (último salva ganha).
- Sem retry automático em falha de rede no `saveAll()`.
- Fotos órfãs no Storage ao deletar blocos com imagem.
- `gatherPhotos()` usa `data-user-added` que o sistema de blocos não atribui.