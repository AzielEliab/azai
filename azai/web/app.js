/* AZAI loopback UI. No CDN. No telemetry. */
const $ = (id) => document.getElementById(id);
const SAMPLE = "Explain receipts in one sentence, please.";

let view = "simple";

function setView(next) {
  view = next === "advanced" ? "advanced" : "simple";
  document.body.setAttribute("data-view", view);
  const simple = $("view-simple");
  const advanced = $("view-advanced");
  if (simple) simple.classList.toggle("on", view === "simple");
  if (advanced) advanced.classList.toggle("on", view === "advanced");
  try { localStorage.setItem("azai-view", view); } catch (e) { /* ignore */ }
}

function badge(el, key, label, value) {
  if (!el) return;
  const node = el.querySelector(`[data-k="${key}"]`);
  if (!node) return;
  node.textContent = `${label} ${value}`;
  node.className = String(value || "").split(/[\s/]/)[0];
  node.setAttribute("data-k", key);
}

function setChips(lamb) {
  const box = $("chips");
  if (!box || !lamb) return;
  for (const axis of ["service", "clarity", "peace"]) {
    const node = box.querySelector(`[data-axis="${axis}"]`);
    if (!node) continue;
    const val = lamb[axis] || "—";
    const label = axis.charAt(0).toUpperCase() + axis.slice(1);
    node.textContent = `${label} ${val}`;
    node.className = "chip " + val;
  }
}

function plainStatus(status) {
  const runtime = status.runtime || "";
  const ol = status.ollama || {};
  let base;
  if (ol.reachable && ol.model_present) base = "Ollama is ready";
  else if (ol.reachable) base = "Ollama is up. Pull the model, then ask again";
  else base = "Ollama is not running yet, so Jeeves uses the local stub";
  if (runtime === "SEALED") return `Chat is locked. Use Open under Advanced. ${base}.`;
  return `Ready to chat. ${base}.`;
}

async function jget(path) {
  const res = await fetch(path, { headers: { Accept: "application/json" } });
  return res.json();
}

async function jpost(path, body) {
  const res = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  const data = await res.json();
  return { status: res.status, data };
}

function downloadBlob(filename, mime, text) {
  const blob = new Blob([text], { type: mime });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
}

function renderReceipts(rows) {
  const ol = $("receipts");
  if (!ol) return;
  ol.innerHTML = "";
  const list = (rows || []).slice(-40).reverse();
  if (!list.length) {
    const li = document.createElement("li");
    li.textContent = "No receipts yet.";
    ol.appendChild(li);
    return;
  }
  for (const rec of list) {
    const li = document.createElement("li");
    const h = String(rec.hash || "").slice(0, 10);
    li.textContent = `${rec.timestamp} · ${rec.action} · ${rec.result} · ${h}`;
    ol.appendChild(li);
  }
}

function renderIntegrity(integ) {
  const box = $("integrity");
  if (!box) return;
  const lamb = integ.lamb || integ;
  const chain = integ.receipts && integ.receipts.ok ? "healthy" : "needs a look";
  const count = integ.receipts ? integ.receipts.count : 0;
  box.innerHTML = `
    <p class="${lamb.service}">Service ${lamb.service}</p>
    <p class="${lamb.clarity}">Clarity ${lamb.clarity}</p>
    <p class="${lamb.peace}">Peace ${lamb.peace}</p>
    <p>Runtime ${integ.runtime || "—"}</p>
    <p>Receipts ${chain} (${count})</p>
    <p class="hint">${lamb.honest || ""}</p>
  `;
  setChips(lamb);
}

function syncEmpty() {
  const t = $("transcript");
  const empty = $("empty-state");
  if (!t || !empty) return;
  empty.hidden = t.childElementCount > 0;
}

function addTurn(who, text) {
  const t = $("transcript");
  if (!t) return;
  const div = document.createElement("div");
  div.className = "turn";
  const w = document.createElement("div");
  w.className = "who";
  w.textContent = who;
  const b = document.createElement("div");
  b.className = "body";
  b.textContent = text;
  div.appendChild(w);
  div.appendChild(b);
  t.appendChild(div);
  t.scrollTop = t.scrollHeight;
  syncEmpty();
}

function clearTranscript() {
  const t = $("transcript");
  if (t) t.innerHTML = "";
  syncEmpty();
}

function displayContent(data) {
  if (view === "simple" && data.azai && data.azai.simple) return data.azai.simple;
  const content = data.choices && data.choices[0] && data.choices[0].message
    ? data.choices[0].message.content
    : JSON.stringify(data);
  return content;
}

function errorText(data) {
  const err = data.error || {};
  const msg = err.message || "That message did not go through.";
  if (err.type === "sealed") return `${msg} Next: use Open under Advanced.`;
  if (err.type === "lamb_fail") return `${msg} Next: rephrase, or use Check this text.`;
  return msg;
}

async function refresh() {
  const status = await jget("/v1/health");
  const line = $("status-line");
  if (line) line.textContent = plainStatus(status);
  const bar = $("status");
  const lamb = (status.lamb && status.lamb.overall) || "—";
  badge(bar, "lamb", "Lamb", lamb);
  badge(bar, "integrity", "Integrity", status.integrity || lamb);
  badge(bar, "runtime", "Runtime", status.runtime || "—");
  badge(bar, "jeeves", "Jeeves", status.jeeves || "—");
  const ol = status.ollama || {};
  const olabel = ol.reachable ? (ol.model_present ? "READY" : "PULL") : "SETUP";
  badge(bar, "ollama", "Ollama", olabel);
  const prov = status.providers || {};
  const present = Object.entries(prov)
    .filter(([k, v]) => k !== "local" && k !== "ollama" && v && v.present)
    .map(([k]) => k);
  const ptxt = present.length ? present.join("+") : "local only";
  badge(bar, "providers", "Providers", ptxt);
  setChips(status.lamb || {});
  const rec = await jget("/v1/receipts");
  renderReceipts(rec.receipts);
  const integ = await jget("/v1/integrity");
  renderIntegrity(integ);
  const dbg = $("debug-strip");
  if (dbg) {
    if (status.debug) {
      dbg.hidden = false;
      dbg.textContent = "Debug traces are on. Body limit " + (status.max_body || "") + " bytes.";
    } else {
      dbg.hidden = true;
    }
  }
}

async function restoreSession() {
  try {
    const sess = await jget("/v1/session");
    const msgs = sess.messages || [];
    if (!msgs.length) return;
    clearTranscript();
    for (const m of msgs) {
      const who = m.role === "user" ? "you" : (m.role === "assistant" ? "Jeeves" : m.role);
      const text = view === "simple" && m.role === "assistant"
        ? (m.content || "").replace(/\[gpt\][\s\S]*?(?=\[grok\]|\[venice\]|\[local \/ Jeeves\]|\[synthesis\]|$)/g, "")
            .replace(/\[grok\][\s\S]*?(?=\[venice\]|\[local \/ Jeeves\]|\[synthesis\]|$)/g, "")
            .replace(/\[venice\][\s\S]*?(?=\[local \/ Jeeves\]|\[synthesis\]|$)/g, "")
            .replace("[synthesis]", "")
            .trim() || m.content
        : m.content;
      addTurn(who, text);
    }
  } catch (e) {
    /* first load */
  }
}

$("prompt-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const message = $("prompt").value.trim();
  if (!message) {
    addTurn("AZAI", "Type a question first, then press Send.");
    $("prompt").focus();
    return;
  }
  const model = $("model").value;
  addTurn("you", message);
  $("prompt").value = "";
  const { data } = await jpost("/v1/chat/completions", {
    model,
    messages: [{ role: "user", content: message }],
  });
  if (data.error) {
    addTurn("AZAI", errorText(data));
    if (data.error.lamb) setChips(data.error.lamb);
  } else {
    addTurn("Jeeves", displayContent(data));
    if (data.azai && data.azai.lamb_out) setChips(data.azai.lamb_out);
  }
  await refresh();
});

$("lamb-btn").addEventListener("click", async () => {
  const text = $("prompt").value.trim();
  if (!text) {
    addTurn("Lamb", "Type something in the box, then press Check this text.");
    $("prompt").focus();
    return;
  }
  const { data } = await jpost("/v1/lamb-check", { text });
  setChips(data);
  addTurn(
    "Lamb",
    `Service ${data.service} · Clarity ${data.clarity} · Peace ${data.peace} → ${data.overall}. `
      + (data.honest || "")
  );
  await refresh();
});

$("sample-btn").addEventListener("click", () => {
  $("prompt").value = SAMPLE;
  $("prompt").focus();
});

$("view-simple").addEventListener("click", () => setView("simple"));
$("view-advanced").addEventListener("click", () => setView("advanced"));

$("seal").addEventListener("click", async () => {
  await jpost("/v1/seal", { reason: "ui" });
  addTurn("runtime", "Chat is locked. Receipts stay readable. Use Open under Advanced to unlock.");
  await refresh();
});

$("open").addEventListener("click", async () => {
  await jpost("/v1/open", { reason: "ui" });
  addTurn("runtime", "Chat is open again.");
  await refresh();
});

$("integrity-btn").addEventListener("click", async () => {
  await refresh();
  addTurn("integrity", "Service, Clarity, and Peace were refreshed.");
});

$("import-btn").addEventListener("click", () => $("import-file").click());
$("import-file").addEventListener("change", async (ev) => {
  const file = ev.target.files && ev.target.files[0];
  ev.target.value = "";
  if (!file) return;
  const content = await file.text();
  const { data } = await jpost("/v1/import", { content, filename: file.name });
  if (!data.ok) {
    addTurn("AZAI", (data.error || "That file could not be imported.") + " Try a .txt or .json conversation.");
    return;
  }
  clearTranscript();
  for (const m of data.messages || []) {
    const who = m.role === "user" ? "you" : "Jeeves";
    addTurn(who, m.content);
  }
  addTurn("AZAI", `Imported ${data.count} messages from ${file.name}.`);
  await refresh();
});

async function exportFormat(fmt) {
  const res = await fetch("/v1/export?format=" + fmt);
  const text = await res.text();
  if (fmt === "md") downloadBlob("azai-chat.md", "text/markdown", text);
  else downloadBlob("azai-chat.json", "application/json", text);
}

$("export-json").addEventListener("click", () => exportFormat("json"));
$("export-md").addEventListener("click", () => exportFormat("md"));

try {
  const saved = localStorage.getItem("azai-view");
  if (saved === "advanced" || saved === "simple") setView(saved);
} catch (e) { /* ignore */ }

syncEmpty();
refresh()
  .then(restoreSession)
  .catch(() => {
    const line = $("status-line");
    if (line) line.textContent = "Could not read status. You can still type a question and press Send.";
  });
