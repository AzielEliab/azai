import * as engine from "./engine.js";
const EXAMPLE_PAYLOAD = {
  "text": "hello",
  "model": "local",
  "site_context": [
    {"title": "Florence", "summary": "Public Corpus/Library record summary"}
  ],
  "note": "Corpus callers POST site_context to local azai serve. Hosted /v1 is lamb-check ONLY.",
};

const SKILL_MARKDOWN = "---\nname: AZAI\ndescription: Use when calling AZAI hosted /v1 or installing the local true-AI package. Ask Jeeves research assistant for the public Corpus/Library. Author Aziel Eliab.\n---\n\n# AZAI\n\nAZAI packages a **true local AI** stack on an **Ollama** base with **JEEVES**.\nOpenAI-compatible local API. Not a hosted paid-key proxy. Author: **Aziel Eliab**.\n\n**THIS IS:** true local AI. Ollama is the local model base. JEEVES is the\nethics/assistant layer inside the shell (**Ask Jeeves** research assistant).\nJEEVES is not sovereign — Lamb Lens first; public Corpus posture; never the\noperator.\n\n**THIS IS NOT:** a new foundation model, a kernel, a worm, IP-blocking malware,\na VPN, a hosted paid-key proxy, GPT, or a sovereign agent.\n\nAlways send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.\n\n## Call these URLs\n\n- Worker OpenAPI: https://azai-download-tracker.vibelock.workers.dev/openapi.json\n- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json\n- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`\n- Live skill (this markdown): `GET https://azai-download-tracker.vibelock.workers.dev/v1/skill`\n\nOps (do **not** increment downloads or views):\n\n- `GET /v1/health` — liveness\n- `GET /v1/skill` — this file\n- `GET /v1/jeeves` — Ask Jeeves research-assistant contract (not chat)\n- Product POSTs listed in OpenAPI\n\nHosted `/v1` is **lamb-check ONLY**. It does not run Ollama and does not\nspend paid keys. Jeeves chat runs on local `azai serve`.\n\nGrok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.\n\n## Ask Jeeves (Corpus / Library research assistant)\n\n**Ask Jeeves** is the documented research-assistant mode of JEEVES for site\nassistants, especially https://www.azielcorpuslibrary.net/. It is not GPT\nand is not sovereign. Ollama is the local base. JEEVES is the ethics/assistant\nlayer. **Lamb Lens first** — public Corpus posture; never the operator.\n\nHard refusals (in `azai/jeeves.py` SYSTEM):\n\n- Never reveal operator account info, credentials, admin hashes, hidden routes\n- Never advise actions that risk the corpus (wipe, score forge, quarantine bypass)\n- **Cannot modify scores** — research assistant only; same rights as a normal user\n\nAdaptive learning hook: pass optional retrieved public record titles/summaries\nas `site_context` so answers improve as the library grows. Persist nothing secret.\n\nUpload is **out of band**. Jeeves may *guide* upload but files still run full\nSPRE×CLCE×PhysLing + Bayesian ingest — no score shortcut.\n\nHow the Corpus/Library calls AZAI/Jeeves:\n\n1. Search the library: `GET https://www.azielcorpuslibrary.net/v1/search?q=`\n2. POST those public titles/summaries to **local** AZAI (not hosted chat):\n\n```bash\ncurl -s http://127.0.0.1:8860/v1/chat/completions \\\n  -H 'content-type: application/json' \\\n  -d '{\n    \"model\": \"local\",\n    \"messages\": [{\"role\": \"user\", \"content\": \"What does the library say about Florence?\"}],\n    \"site_context\": [\n      {\"title\": \"Florence\", \"summary\": \"Public record summary\"}\n    ]\n  }'\n```\n\nRead the contract: `GET http://127.0.0.1:8860/v1/jeeves` (local) or\n`GET https://azai-download-tracker.vibelock.workers.dev/v1/jeeves` (hosted\ncard only). Hosted AZAI `/v1` does **not** run Jeeves chat.\n\n## Example\n\n```bash\ncurl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/health\ncurl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/skill\ncurl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/jeeves\n```\n\n## Local (after one-click install)\n\n```bash\ncurl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash\nazai ui\nazai doctor\nazai ollama\nazai jeeves\n```\n\nThe install path:\n\n1. Downloads the counted tarball and `pip install -e .`\n2. Runs `scripts/setup-ollama.sh` — installs or reuses Ollama, starts\n   `ollama serve` if needed, pulls `llama3.2` (or `AZAI_OLLAMA_MODEL`)\n3. If Ollama cannot be installed here, the script prints the exact steps\n   and AZAI still runs with the JEEVES constitution stub\n\nThen open http://127.0.0.1:8860 (loopback only). Default model is `local`\n(Ollama + JEEVES / Ask Jeeves). Point other software at:\n\n```bash\nexport OPENAI_BASE_URL=http://127.0.0.1:8860/v1\nexport OPENAI_API_KEY=dummy\n```\n\nExact Ollama steps if doctor reports the base missing:\n\n```bash\ncurl -fsSL https://ollama.com/install.sh | sh\nollama serve\nollama pull llama3.2\nazai doctor\n```\n\nCounted download (gzip HTTP 200, no 302): https://azai-download-tracker.vibelock.workers.dev/download?asset=azai-0.3.1.tar.gz\nGitHub: https://github.com/AzielEliab/azai\n\n## Catalog + local UI\n\nAuthor: **Aziel Eliab**. Honest scope: true local AI on an Ollama base with\nJEEVES (Ask Jeeves research assistant). Not a new foundation model. JEEVES\nis not sovereign.\n\n- Catalog product: https://aziel-runtime.vibelock.workers.dev/p/azai/\n- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json\n- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`\n- This Worker skill: `GET https://azai-download-tracker.vibelock.workers.dev/v1/skill`\n- This Worker OpenAPI: https://azai-download-tracker.vibelock.workers.dev/openapi.json\n- Ask Jeeves card: `GET https://azai-download-tracker.vibelock.workers.dev/v1/jeeves`\n- Sample payload: `GET https://azai-download-tracker.vibelock.workers.dev/v1/example`\n\nLocal UI: **Ask Jeeves** research assistant, **Import JSON file** (`type=file`)\nand **Export JSON**. Then `azai doctor`.\n\nGrok: import catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.\n";

/**
 * AZAI download tracker (Cloudflare Worker).
 *
 * GET  /download?asset=azai-0.3.1.tar.gz
 *      increments KV, serves the tarball via env.ASSETS.fetch
 *      (does not 302 to GitHub)
 * GET  /stats   JSON totals + per-repo + per-branch breakdown
 * POST /event   forks report a download {owner,repo,branch,fork,asset}
 *
 * KV binding DOWNLOADS. Keys: project|owner|repo|branch|fork
 * totalKey() = azai|__total__
 * CORS *. No secrets in this tree.
 * Isolated counter: Worker azai-download-tracker, project azai.
 * Not mixed with any other product.
 *
 * Hosted /v1 is a protocol mirror + Lamb check + models list.
 * NOT a proxy that spends the author's paid keys.
 */

const PROJECT = "azai";
const DEFAULT_ASSET = "azai-0.3.1.tar.gz";
const MAX_BODY = 1048576;
const DEFAULT_OWNER = "AzielEliab";
const DEFAULT_REPO = "azai";
const DEFAULT_BRANCH = "main";
const HOST = "https://azai-download-tracker.vibelock.workers.dev";
const GITHUB_REPO = "https://github.com/AzielEliab/azai";

const GITHUB_RELEASES = "https://github.com/AzielEliab/azai/releases";
const GITHUB_LATEST = "https://github.com/AzielEliab/azai/releases/latest";
const INSTALL_LINE = "curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash";

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...corsHeaders() },
  });
}

function redirect(url) {
  return new Response(null, {
    status: 302,
    headers: { Location: url, ...corsHeaders() },
  });
}

function splitOwnerRepo(value, fallbackOwner, fallbackRepo) {
  if (typeof value === "string" && value.includes("/")) {
    const [o, r] = value.split("/").filter(Boolean);
    if (o && r) return { owner: o, repo: r };
  }
  return { owner: fallbackOwner, repo: fallbackRepo };
}

function parseDims(src) {
  const get = (k) => {
    if (src == null) return null;
    if (typeof src.get === "function") {
      const v = src.get(k);
      return v == null || v === "" ? null : v;
    }
    const v = src[k];
    return v == null || v === "" ? null : v;
  };

  let owner = get("owner") || DEFAULT_OWNER;
  let repo = get("repo") || DEFAULT_REPO;
  if (typeof repo === "string" && repo.includes("/")) {
    const split = splitOwnerRepo(repo, owner, DEFAULT_REPO);
    owner = split.owner;
    repo = split.repo;
  }

  const branch = get("branch") || DEFAULT_BRANCH;
  const tag = get("tag") || "latest";
  const asset = get("asset") || "";

  const forkRaw = get("fork");
  let fork = "0";
  if (forkRaw === 1 || forkRaw === true || forkRaw === "1" || forkRaw === "true") {
    fork = "1";
  } else if (typeof forkRaw === "string" && forkRaw.includes("/")) {
    const split = splitOwnerRepo(forkRaw, owner, repo);
    owner = split.owner;
    repo = split.repo;
    fork = "1";
  } else if (forkRaw != null && forkRaw !== 0 && forkRaw !== false && forkRaw !== "0" && forkRaw !== "false") {
    fork = "1";
  }

  if (`${owner}/${repo}`.toLowerCase() !== `${DEFAULT_OWNER}/${DEFAULT_REPO}`.toLowerCase()) {
    fork = "1";
  }

  return { project: PROJECT, owner, repo, branch, fork, tag, asset };
}

function kvKey(dims) {
  return `${dims.project}|${dims.owner}|${dims.repo}|${dims.branch}|${dims.fork}`;
}

function githubAssetUrl(owner, repo, tag, asset) {
  if (!asset) {
    if (owner === DEFAULT_OWNER && repo === DEFAULT_REPO) return GITHUB_RELEASES;
    return `https://github.com/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/releases`;
  }
  if (!tag || tag === "latest") {
    return `https://github.com/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/releases/latest/download/${encodeURIComponent(asset)}`;
  }
  return `https://github.com/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/releases/download/${encodeURIComponent(tag)}/${encodeURIComponent(asset)}`;
}

function totalKey() {
  return PROJECT + "|__total__";
}

async function increment(env, dims) {
  const key = kvKey(dims);
  const n = parseInt((await env.DOWNLOADS.get(key)) || "0", 10) + 1;
  await env.DOWNLOADS.put(key, String(n));
  const tot = parseInt((await env.DOWNLOADS.get(totalKey())) || "0", 10) + 1;
  await env.DOWNLOADS.put(totalKey(), String(tot));
  return tot;
}

async function listAllKeys(env) {
  const keys = [];
  let cursor;
  do {
    const page = await env.DOWNLOADS.list(cursor ? { cursor } : {});
    keys.push(...page.keys);
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return keys;
}

async function collectStats(env) {
  const keys = await listAllKeys(env);
  let total = 0;
  const by_repo = {};
  const by_branch = {};
  const by_fork = { "0": 0, "1": 0 };
  const breakdown = [];

  for (const k of keys) {
    const name = k.name;
    if (name === viewsKey() || name === totalKey() || name === githubCacheKey()) continue;
    const n = parseInt((await env.DOWNLOADS.get(name)) || "0", 10);
    if (!Number.isFinite(n) || n <= 0) continue;
    const parts = name.split("|");
    if (parts.length < 5) continue;
    const [project, owner, repo, branch, fork] = parts;
    total += n;
    const repoId = `${owner}/${repo}`;
    by_repo[repoId] = (by_repo[repoId] || 0) + n;
    by_branch[branch] = (by_branch[branch] || 0) + n;
    const forkFlag = fork === "1" ? "1" : "0";
    by_fork[forkFlag] = (by_fork[forkFlag] || 0) + n;
    breakdown.push({ project, owner, repo, branch, fork: forkFlag, count: n });
  }

  const totalDirect = parseInt((await env.DOWNLOADS.get(totalKey())) || "0", 10);
  const shown = Number.isFinite(totalDirect) && totalDirect > 0 ? totalDirect : total;
  return {
    project: PROJECT,
    total: shown,
    views: parseInt((await env.DOWNLOADS.get(viewsKey())) || "0", 10) || 0,
    downloads: shown,
    by_repo,
    by_branch,
    by_fork,
    breakdown,
    github: (await githubStats(env)),
    note: "Forks identified by GitHub owner/repo. Key layout: project|owner|repo|branch|fork",
  };
}



function viewsKey() {
  return PROJECT + "|__views__";
}

function githubCacheKey() {
  return PROJECT + "|__github__";
}

async function incrementViews(env) {
  const n = parseInt((await env.DOWNLOADS.get(viewsKey())) || "0", 10) + 1;
  await env.DOWNLOADS.put(viewsKey(), String(n));
  return n;
}

async function githubStats(env) {
  const cached = await env.DOWNLOADS.get(githubCacheKey());
  if (cached) {
    try {
      const obj = JSON.parse(cached);
      if (obj && obj.fetched_at && Date.now() - obj.fetched_at < 5 * 60 * 1000) {
        return obj;
      }
    } catch {
      /* ignore */
    }
  }
  const headers = { "User-Agent": "Mozilla/5.0 AZAI-download-tracker", Accept: "application/vnd.github+json" };
  let stars = 0;
  let forks = 0;
  let watchers = 0;
  let release_download_count = 0;
  try {
    const repoRes = await fetch("https://api.github.com/repos/AzielEliab/azai", { headers });
    if (repoRes.ok) {
      const repo = await repoRes.json();
      stars = Number(repo.stargazers_count) || 0;
      forks = Number(repo.forks_count) || 0;
      watchers = Number(repo.subscribers_count != null ? repo.subscribers_count : repo.watchers_count) || 0;
    }
    const relRes = await fetch("https://api.github.com/repos/AzielEliab/azai/releases/latest", { headers });
    if (relRes.ok) {
      const rel = await relRes.json();
      const assets = Array.isArray(rel.assets) ? rel.assets : [];
      release_download_count = assets.reduce((s, a) => s + (Number(a.download_count) || 0), 0);
    }
  } catch {
    /* public API; empty is fine */
  }
  const out = { stars, forks, watchers, release_download_count, fetched_at: Date.now() };
  try {
    await env.DOWNLOADS.put(githubCacheKey(), JSON.stringify(out));
  } catch {
    /* ignore */
  }
  return out;
}

function installScript() {
  return `#!/usr/bin/env bash\n# AZAI one-click install. Counted download via this Worker.\n# True local AI on an Ollama base. JEEVES is not sovereign.\nset -euo pipefail\nHOST="${HOST}"\nASSET="${DEFAULT_ASSET}"\nWORKDIR="\${AZAI_HOME:-\$HOME/azai}"\nmkdir -p "\$WORKDIR"\ncd "\$WORKDIR"\necho "Downloading counted tarball from \${HOST}/download (User-Agent Mozilla/5.0)…"\ncurl -fsSL -A 'Mozilla/5.0' "\${HOST}/download?asset=\${ASSET}" -o "\${ASSET}"\ntar -xzf "\${ASSET}"\nDIR=\"\$(find . -maxdepth 1 -type d -name 'azai-*' | head -n 1)\"\nif [ -n "\${DIR}" ]; then\n  cd "\${DIR}"\nfi\npython3 -m venv .venv\n. .venv/bin/activate\npython -m pip install -U pip\npython -m pip install -e .\necho\necho "Installed AZAI (true local AI on an Ollama base; JEEVES is not sovereign)."\nif [ -f scripts/setup-ollama.sh ]; then\n  bash scripts/setup-ollama.sh || true\nelse\n  echo "Exact Ollama steps: curl -fsSL https://ollama.com/install.sh | sh && ollama serve && ollama pull llama3.2 && azai doctor"\nfi\necho\necho "Run:  azai ui"\necho "Then open http://127.0.0.1:8860  (loopback only)"\necho "OPENAI_BASE_URL=http://127.0.0.1:8860/v1  OPENAI_API_KEY=dummy"\necho "Author: Aziel Eliab."\n`;
}

async function serveAsset(request, env, asset, { head = false } = {}) {
  if (!env.ASSETS) {
    return json({ error: "assets binding missing" }, 500);
  }
  const assetUrl = new URL("/" + asset, request.url);
  const assetRes = await env.ASSETS.fetch(new Request(assetUrl, { method: "GET" }));
  if (!assetRes.ok) {
    return json({ error: "asset not hosted", asset, status: assetRes.status }, 404);
  }
  const headers = new Headers();
  headers.set("Content-Type", "application/gzip");
  headers.set("Content-Disposition", 'attachment; filename="' + asset.replaceAll('"', "") + '"');
  headers.set("Cache-Control", "private, no-store");
  const len = assetRes.headers.get("Content-Length");
  if (len) headers.set("Content-Length", len);
  for (const [k, v] of Object.entries(corsHeaders())) headers.set(k, v);
  if (head) {
    return new Response(null, { status: 200, headers });
  }
  return new Response(assetRes.body, { status: 200, headers });
}

async function indexHtml(env) {
  const stats = await collectStats(env);
  const downloads = Number(stats.downloads != null ? stats.downloads : stats.total) || 0;
  const views = parseInt((await env.DOWNLOADS.get(viewsKey())) || "0", 10) || 0;
  const v = views.toLocaleString("en-US");
  const n = downloads.toLocaleString("en-US");
  const breakdown = (stats.breakdown || [])
    .map(
      (b) =>
        `<li><code>${b.owner}/${b.repo}</code> branch <code>${b.branch}</code> fork=${b.fork} → ${b.count}</li>`,
    )
    .join("") || "<li>none yet</li>";
  return `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AZAI — Aziel Eliab</title>
<meta name="description" content="True local AI on an Ollama base with JEEVES by Aziel Eliab. OpenAI-compatible local API. Not a hosted paid-key proxy.">
<meta name="author" content="Aziel Eliab">
<link rel="canonical" href="https://azai-download-tracker.vibelock.workers.dev/">
<meta property="og:title" content="AZAI — Aziel Eliab">
<meta property="og:description" content="True local AI on an Ollama base with JEEVES by Aziel Eliab. OpenAI-compatible local API. Not a hosted paid-key proxy.">
<meta property="og:url" content="https://azai-download-tracker.vibelock.workers.dev/">
<meta property="og:type" content="website">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "AZAI",
  "author": {
    "@type": "Person",
    "name": "Aziel Eliab"
  },
  "codeRepository": "https://github.com/AzielEliab/azai",
  "downloadUrl": "https://azai-download-tracker.vibelock.workers.dev/download",
  "license": "https://www.apache.org/licenses/LICENSE-2.0",
  "url": "https://azai-download-tracker.vibelock.workers.dev/",
  "description": "True local AI on an Ollama base with JEEVES by Aziel Eliab. OpenAI-compatible local API. Not a hosted paid-key proxy."
}
</script>
<!-- gitbaby-seo -->
<style>
  :root { color-scheme: dark; }
  body { font: 16px/1.45 system-ui, sans-serif; max-width: 42rem; margin: 3rem auto; padding: 0 1.25rem 4rem; background: #0e1014; color: #e8eaef; }
  h1 { font-size: 1.75rem; margin: 0 0 .35rem; }
  .motto { color: #9aa3b2; margin: 0 0 1.5rem; }
  .card { border: 1px solid #2a3140; border-radius: 12px; padding: 1.25rem 1.35rem; background: #151922; }
  .nums { display: grid; grid-template-columns: 1fr 1fr; gap: .8rem; margin: 0 0 1rem; }
  .count { font-size: 2.2rem; font-variant-numeric: tabular-nums; font-weight: 700; margin: 0; }
  .count span { display: block; font-size: .95rem; font-weight: 500; color: #9aa3b2; }
  .kid { font-size: 1.05rem; margin: 0 0 1rem; }
  .btns { display: grid; grid-template-columns: 1fr 1fr; gap: .75rem; margin: 0 0 .85rem; }
  @media (max-width: 520px) { .btns { grid-template-columns: 1fr; } }
  a.btn, button.btn { display: block; width: 100%; box-sizing: border-box; text-align: center; font: inherit; font-size: 1.2rem; font-weight: 750; padding: 1rem 1.1rem; border-radius: 10px; border: 0; cursor: pointer; text-decoration: none; }
  a.btn.primary { background: #e8eaef; color: #0e1014; }
  button.btn.install { background: #c9a227; color: #14110a; }
  button.btn.install.copied { background: #7dcf9a; color: #0e1014; }
  .meta { margin-top: 1.1rem; color: #9aa3b2; font-size: .92rem; }
  .meta a { color: #c9d4ff; }
  .iso { margin-top: .85rem; font-size: .85rem; color: #7d8696; }
  .banner { border: 1px solid #5c4a1a; background: #241c0d; color: #f0d78c; padding: .85rem 1rem; border-radius: 8px; margin: 0 0 1.2rem; font-size: .92rem; }
  pre { background: #0e1014; padding: .75rem .9rem; overflow: auto; border-radius: 8px; font-size: .82rem; }
  code { font-size: .88rem; }

  .cite { margin-top: 1.4rem; padding-top: 1rem; border-top: 1px solid #2a3140; }
  .cite h2 { font-size: 1.05rem; margin: 0 0 .4rem; }
  .cite p { color: #c5ccd8; font-size: .95rem; }
  .cite a { color: #c9d4ff; }
</style>
<body>
  <h1>AZAI</h1>
  <p class="motto">Ask Jeeves research assistant. Jeeves speaks inside the shell. Lamb Lens first — public Corpus posture; never the operator. Author Aziel Eliab.</p>
  <p class="banner">AZAI packages a true local AI stack on an Ollama base with JEEVES (Ask Jeeves research assistant). OpenAI-compatible local API. Not a hosted paid-key proxy. JEEVES is not sovereign. Hosted /v1 is lamb-check ONLY. Author: Aziel Eliab.</p>
  <div class="card">
    <div class="nums">
      <p class="count">${v}<span>Views</span></p>
      <p class="count">${n}<span>Downloads</span></p>
    </div>
    <p class="kid"><strong>Two big buttons.</strong> Download saves the gzip (the Downloads number goes up). One-click install copies a Terminal command. After it finishes, type <code>azai ui</code>.</p>
    <div class="btns">
      <a class="btn primary dl" href="/download?asset=${DEFAULT_ASSET}">Download</a>
      <button type="button" class="btn install" id="install-btn">One-click install</button>
    </div>
    <pre id="install-cmd">curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash</pre>
    <p class="kid">Then run: <code>azai ui</code> and open http://127.0.0.1:8860 (this computer only). Install pulls Ollama + <code>llama3.2</code> when it can; otherwise it prints the exact steps. Ask Jeeves is the research assistant. JEEVES is the ethics layer, not sovereign.</p>
    <p class="meta">The download count ticks on the Download click. The Worker serves the gzip (HTTP 200). No 302 to GitHub. Forks using this same link are counted automatically. ${DEFAULT_ASSET} — ${n} counted.</p>
    <p class="iso">Isolated counter: Worker <code>azai-download-tracker</code>, project <code>azai</code>, KV <code>AZAI_DOWNLOADS</code>. Not mixed with any other product. /v1 does not increment downloads.</p>
    
    <p class="meta"><a href="/stats">JSON stats</a> · <a href="/openapi.json">OpenAPI</a> · <a href="/v1/skill">Skill</a> · <a href="/ai">AI runtime</a> · <a href="${GITHUB_REPO}">GitHub</a> · <a href="${GITHUB_LATEST}">releases</a></p>
    <script>
      (function () {
        var cmd = "curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash";
        var btn = document.getElementById("install-btn");
        var pre = document.getElementById("install-cmd");
        if (!btn) return;
        btn.addEventListener("click", function () {
          function done(ok) {
            btn.textContent = ok ? "Copied! Paste in Terminal, then run azai ui" : "Select the command, copy it, then run azai ui";
            btn.classList.add("copied");
          }
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(cmd).then(function () { done(true); }).catch(function () { done(false); });
          } else {
            done(false);
            if (pre && window.getSelection) {
              var r = document.createRange();
              r.selectNodeContents(pre);
              var sel = window.getSelection();
              sel.removeAllRanges();
              sel.addRange(r);
            }
          }
        });
      })();
    </script>
    <h2>Per repo / branch / fork</h2>
    <ul>${breakdown}</ul>
  </div>

<section class="cite" id="cite">
  <h2>How to cite</h2>
  <p>Aziel Eliab. AZAI. https://github.com/AzielEliab/azai. https://azai-download-tracker.vibelock.workers.dev.</p>
  <p><a href="https://aziel-runtime.vibelock.workers.dev/">Catalog</a> · <a href="https://github.com/AzielEliab/azai">GitHub</a> · <a href="https://azai-download-tracker.vibelock.workers.dev/download">Download</a> · <a href="https://azai-download-tracker.vibelock.workers.dev/cite.json">cite.json</a></p>
</section>
<!-- /gitbaby-seo -->
</body>
</html>`;
}


function html(body) {
  return new Response(body, {
    headers: { "Content-Type": "text/html; charset=utf-8", ...corsHeaders() },
  });
}

function originOf(request) {
  try {
    return new URL(request.url).origin;
  } catch {
    return "https://azai-download-tracker.vibelock.workers.dev";
  }
}

function openapiSpec(request) {
  const origin = originOf(request);
  return {
    openapi: "3.1.0",
    info: {
      title: "AZAI hosted runtime",
      version: "0.3.1",
      summary: "True local AI on an Ollama base with Ask Jeeves research assistant. Hosted /v1 is lamb-check ONLY. Never a paid-key proxy. Jeeves is not sovereign.",
      description: engine.LIMITATION + " Corpus/Library site assistants (www.azielcorpuslibrary.net) call local azai serve: POST /v1/chat/completions with model=local and optional site_context (public titles/summaries). Read GET /v1/jeeves. Persist nothing secret. Jeeves cannot modify scores.",
    },
    servers: [{ url: origin }],
    paths: {
            "/v1/example": { get: { operationId: "azaiExample", summary: "Sample JSON payload. Does not increment downloads.", responses: { "200": { description: "OK" } } } },
      "/v1/health": { get: { operationId: "azai_health", summary: "Liveness. Does not increment download KV. Not a provider proxy.", responses: { "200": { description: "ok" } } } },
      "/v1/skill": { get: { operationId: "azai_skill", summary: "AZAI skill markdown, including how the Corpus/Library calls Ask Jeeves. Does not increment downloads.", responses: { "200": { description: "markdown" } } } },
      "/v1/jeeves": { get: { operationId: "azai_jeeves", summary: "Ask Jeeves research-assistant contract. Not chat. Not sovereign. Not GPT. How www.azielcorpuslibrary.net calls local AZAI/Jeeves.", responses: { "200": { description: "ask-jeeves mode card" } } } },
      "/v1/models": { get: { operationId: "azai_models", summary: "Protocol mirror of local, ollama, blend, gpt, grok, venice. Live Ollama+JEEVES is local azai serve.", responses: { "200": { description: "models" } } } },
      "/v1/lamb-check": {
        post: {
          operationId: "azai_lamb_check",
          summary: "Run Lamb Lens (peace/clarity/service) on {text}. No provider call.",
          requestBody: { required: true, content: { "application/json": { schema: { type: "object", properties: { text: { type: "string" } } } } } },
          responses: { "200": { description: "lamb" } },
        },
      },
      "/v1/lamb_check": {
        post: {
          operationId: "azai_lamb_check_alias",
          summary: "Alias of /v1/lamb-check for MCP azai_lamb_check.",
          requestBody: { required: true, content: { "application/json": { schema: { type: "object" } } } },
          responses: { "200": { description: "lamb" } },
        },
      },
    },
  };
}

function aiHelpPage(request) {
  const origin = originOf(request);
  return `<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AZAI — AI runtime</title>
<style>
  :root { color-scheme: dark; }
  body { font: 16px/1.45 system-ui, sans-serif; max-width: 44rem; margin: 3rem auto; padding: 0 1.25rem; background: #0e1014; color: #e8eaef; }
  a { color: #c9d4ff; }
  code, pre { background: #151922; padding: .15rem .35rem; border-radius: 4px; }
  pre { padding: .85rem 1rem; overflow: auto; }
  .banner { border: 1px solid #5c4a1a; background: #241c0d; color: #f0d78c; padding: .85rem 1rem; border-radius: 8px; }
</style>
<body>
<h1>AZAI hosted runtime</h1>
<p class="banner">${engine.LIMITATION}</p>
<p>OpenAPI: <a href="${origin}/openapi.json">${origin}/openapi.json</a></p>
<p>Catalog: <a href="https://aziel-runtime.vibelock.workers.dev/">aziel-runtime.vibelock.workers.dev</a></p>
<p>Local true-AI backend (Ollama + Ask Jeeves): <code>azai serve</code> then <code>OPENAI_BASE_URL=http://127.0.0.1:8860/v1</code>. Corpus callers POST <code>site_context</code> (public titles/summaries) to local chat. Hosted <code>/v1</code> is lamb-check ONLY.</p>
<pre>curl ${origin}/v1/health
curl ${origin}/v1/models
curl -X POST ${origin}/v1/lamb-check -H 'content-type: application/json' \\
  -d '{"text":"hello"}'
</pre>
<p>GET/POST under <code>/v1</code> never increment the download counter. Lamb check does not call GPT/Grok/Venice. This is not a provider proxy.</p>
<p><a href="/">Downloads</a></p>
</body></html>`;
}

async function handleRuntime(request, url) {
  const path = url.pathname.replace(/\/+$/, "") || "/";
  if (path === "/v1/health" && request.method === "GET") {
    return json({
      ok: true, author: "Aziel Eliab",
      product: "azai",
      instrument: "Jeeves",
      runtime: true,
      kv_increment: false,
      provider_proxy: false,
      hosted_v1: "lamb-check-only",
      not_a_foundation_model: true,
      jeeves_sovereign: false,
      jeeves_layer: "ethics/assistant",
      jeeves_mode: "ask-jeeves",
      ask_jeeves: true,
      jeeves_posture: "public-corpus",
      can_modify_scores: false,
      corpus_library: "https://www.azielcorpuslibrary.net/",
      local_ai: "ollama-base",
      true_local_ai: true,
      limitation: engine.LIMITATION,
    });
  }
  if ((path === "/v1/example" || path === "/v1/example/") && (request.method === "GET" || request.method === "HEAD")) {
    return json({
      ok: true,
      product: "azai",
      author: "Aziel Eliab",
      example: EXAMPLE_PAYLOAD,
      note: "Sample payload only. Does not increment downloads.",
    });
  }


  if (path === "/v1/skill" && request.method === "GET") {
    return new Response(SKILL_MARKDOWN, {
      status: 200,
      headers: {
        "Content-Type": "text/markdown; charset=utf-8",
        "Cache-Control": "private, no-store",
        "X-KV-Increment": "false",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }

  if (path === "/v1/jeeves" && request.method === "GET") {
    return json({
      ok: true,
      product: "azai",
      author: "Aziel Eliab",
      mode: "ask-jeeves",
      label: "Ask Jeeves research assistant",
      sovereign: false,
      not_gpt: true,
      posture: "public-corpus",
      lamb_lens_first: true,
      operator: false,
      can_modify_scores: false,
      same_rights_as: "normal user",
      base: "ollama",
      layer: "ethics/assistant",
      corpus_library: "https://www.azielcorpuslibrary.net/",
      ingest: "SPRE\u00d7CLCE\u00d7PhysLing + Bayesian ingest",
      upload: "out-of-band",
      upload_guidance: "Upload is out of band. I may guide an upload, but files still run full SPRE\u00d7CLCE\u00d7PhysLing + Bayesian ingest. There is no score shortcut.",
      refusals: [
        "Never reveal operator account info, credentials, admin hashes, or hidden routes.",
        "Never advise actions that risk the corpus (wipe, score forge, quarantine bypass).",
        "Cannot modify scores — research assistant only; same rights as a normal user.",
      ],
      adaptive: "Optional site_context: public record titles/summaries so answers improve as the library grows. Persist nothing secret.",
      how_corpus_calls: "Site assistants search https://www.azielcorpuslibrary.net/v1/search then POST model=local + site_context to local azai serve (http://127.0.0.1:8860/v1/chat/completions). Hosted AZAI /v1 is lamb-check ONLY — not Jeeves chat and not a paid-key proxy.",
      hosted_v1: "lamb-check-only",
      local_chat: "http://127.0.0.1:8860/v1/chat/completions",
      kv_increment: false,
    });
  }

  if (path === "/v1/models" && request.method === "GET") {
    return json(engine.models());
  }
  if (path === "/openapi.json" && request.method === "GET") {
    return json(openapiSpec(request));
  }
  if ((path === "/ai" || url.pathname === "/ai/") && request.method === "GET") {
    return html(aiHelpPage(request));
  }
  if (path === "/v1/chat/completions" || path === "/v1/chat") {
    return json({
      error: "hosted /v1 is lamb-check ONLY, never a paid-key proxy",
      provider_proxy: false,
      hint: "True local AI (Ollama + Ask Jeeves) and optional paid calls happen on local azai serve (127.0.0.1:8860). Corpus callers POST site_context there. GET /v1/jeeves for the contract.",
      limitation: engine.LIMITATION,
    }, 403);
  }
  if ((path === "/v1/lamb-check" || path === "/v1/lamb_check") && request.method === "POST") {
    const buf = await request.arrayBuffer();
    if (buf.byteLength > MAX_BODY) {
      return json({ error: "payload too large", max: MAX_BODY, provider_proxy: false }, 413);
    }
    let body;
    try { body = JSON.parse(new TextDecoder().decode(buf) || "{}"); } catch {
      return json({ error: "JSON body required", limitation: engine.LIMITATION }, 400);
    }
    const text = (body && (body.text || body.prompt)) || "";
    return json(engine.lambCheck(text));
  }
  if (path.startsWith("/v1/") || path === "/v1") {
    return json({ error: "not found", hint: "GET /v1/health /v1/models /v1/skill /v1/jeeves ; POST /v1/lamb-check — hosted /v1 is lamb-check ONLY, never a paid-key proxy. Ask Jeeves chat is local azai serve.", limitation: engine.LIMITATION, provider_proxy: false }, 404);
  }
  return null;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    const runtime = await handleRuntime(request, url);
    if (runtime) return runtime;

    if ((url.pathname === "/install.sh" || url.pathname === "/install.sh/") && request.method === "GET") {
      return new Response(installScript(), {
        status: 200,
        headers: {
          "Content-Type": "text/x-shellscript; charset=utf-8",
          "Cache-Control": "private, no-store",
          ...corsHeaders(),
        },
      });
    }

    if (url.pathname === "/" && request.method === "GET") {
      await incrementViews(env);
      return new Response(await indexHtml(env), {
        headers: { "Content-Type": "text/html; charset=utf-8", ...corsHeaders() },
      });
    }

    if (url.pathname === "/count" && request.method === "GET") {
      const stats = await collectStats(env);
      return json({ project: PROJECT, total: stats.total || 0 });
    }

    if (url.pathname === "/stats" && request.method === "GET") {
      return json(await collectStats(env));
    }

    if (url.pathname === "/event" && request.method === "POST") {
      let body;
      try {
        body = await request.json();
      } catch {
        return json({ error: "JSON body required" }, 400);
      }
      const dims = parseDims(body || {});
      const count = await increment(env, dims);
      return json({
        ok: true,
        key: kvKey(dims),
        count,
        owner: dims.owner,
        repo: dims.repo,
        branch: dims.branch,
        fork: dims.fork,
        asset: dims.asset || null,
      });
    }

    if (url.pathname === "/go" && (request.method === "GET" || request.method === "HEAD")) {
      const dims = parseDims(url.searchParams);
      const asset = dims.asset || DEFAULT_ASSET;
      dims.asset = asset;
      if (request.method === "GET") await increment(env, dims);
      return serveAsset(request, env, asset, { head: request.method === "HEAD" });
    }

    if ((url.pathname === "/download" || url.pathname.startsWith("/download/")) && (request.method === "GET" || request.method === "HEAD")) {
      const dims = parseDims(url.searchParams);
      if (!dims.asset && url.pathname.startsWith("/download/")) {
        dims.asset = decodeURIComponent(url.pathname.slice("/download/".length));
      }
      const asset = dims.asset || DEFAULT_ASSET;
      dims.asset = asset;
      if (request.method === "GET") await increment(env, dims);
      return serveAsset(request, env, asset, { head: request.method === "HEAD" });
    }


    // gitbaby-seo-routes
    if ((url.pathname === "/robots.txt" || url.pathname === "/robots.txt/") && request.method === "GET") {
      const body = "User-agent: *\nAllow: /\nSitemap: " + HOST + "/sitemap.xml\n";
      return new Response(body, {
        status: 200,
        headers: { "Content-Type": "text/plain; charset=utf-8", ...corsHeaders() },
      });
    }
    if ((url.pathname === "/sitemap.xml" || url.pathname === "/sitemap.xml/") && request.method === "GET") {
      const locs = [HOST + "/", HOST + "/download", HOST + "/install.sh", HOST + "/v1/skill", HOST + "/v1/jeeves", HOST + "/openapi.json", GITHUB_REPO];
      const xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + locs.map((u) => "  <url><loc>" + u + "</loc></url>").join("\n")
        + "\n</urlset>\n";
      return new Response(xml, {
        status: 200,
        headers: { "Content-Type": "application/xml; charset=utf-8", ...corsHeaders() },
      });
    }
    if ((url.pathname === "/cite.json" || url.pathname === "/cite.json/") && request.method === "GET") {
      return json({"author": "Aziel Eliab", "title": "AZAI", "github": "https://github.com/AzielEliab/azai", "download": "https://azai-download-tracker.vibelock.workers.dev/download", "doi": null, "license": "Apache-2.0", "catalog": "https://aziel-runtime.vibelock.workers.dev/"});
    }
    // /gitbaby-seo-routes
    return json({ error: "not found" }, 404);
  },
};
