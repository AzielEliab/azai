/* AZAI loopback UI. No CDN. No telemetry. */
const $ = (id) => document.getElementById(id);
const SAMPLE = "Explain receipts in one sentence, please.";

let view = "simple";

function setView(next) {
  view = next === "advanced" ? "advanced" : "simple";
  document.body.setAttribute("data-view", view);
  $("view-simple").classList.toggle("on", view === "simple");
  $("view-advanced").classList.toggle("on", view === "advanced");
  try { localStorage.setItem("azai-view", view); } catch (e) { /* ignore */ }
}

function badge(el, key, label, value) {
  const node = el.querySelector(`[data-k="${key}"]`);
  if (!node) return;
  node.textContent = `${label} ${value}`;
  node.className = String(value || "").split(/[\s/]/)[0];
  node.setAttribute("data-k", key);
}

function setChips(lamb) {
  const box = $("chips");
  if (!box || !lamb) return;
  for (const axis of ["peace", "clarity", "service"]) {
    const node = box.querySelector(`[data-axis="${axis}"]`);
    if (!node) continue;
    const val = lamb[axis] || "—";
    const label = axis.charAt(0).toUpperCase() + axis.slice(1);
    node.textContent = `${label} ${val}`;
    node.className = "chip " + val;
  }
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
  for (const rec of list) {
    const li = document.createElement("li");
    const h = String(rec.hash || "").slice(0, 10);
    li.textContent = `${rec.timestamp} | ${rec.action} | ${rec.result} | ${h}`;
    ol.appendChild(li);
  }
}

function renderIntegrity(integ) {
  const box = $("integrity");
  if (!box) return;
  const lamb = integ.lamb || integ;
  box.innerHTML = `
    <p class="${lamb.peace}">Peace ${lamb.peace}</p>
    <p class="${lamb.clarity}">Clarity ${lamb.clarity}</p>
    <p class="${lamb.service}">Service ${lamb.service}</p>
    <p>Runtime ${integ.runtime || "—"}</p>
    <p>Receipts ${integ.receipts && integ.receipts.ok ? "HEALTHY" : "CHECK"} (${integ.receipts ? integ.receipts.count : 0})</p>
    <p class="muted">${lamb.honest || ""}</p>
  `;
  setChips(lamb);
}

function addTurn(who, text) {
  const t = $("transcript");
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
}

function clearTranscript() {
  $("transcript").innerHTML = "";
}

function displayContent(data, model) {
  if (view === "simple" && data.azai && data.azai.simple) return data.azai.simple;
  const content = data.choices && data.choices[0] && data.choices[0].message
    ? data.choices[0].message.content
    : JSON.stringify(data);
  return content;
}

async function refresh() {
  const status = await jget("/v1/health");
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
  const ptxt = present.length ? present.join("+") : "ollama base";
  badge(bar, "providers", "Providers", ptxt);
  setChips(status.lamb || {});
  const rec = await jget("/v1/receipts");
  renderReceipts(rec.receipts);
  const integ = await jget("/v1/integrity");
  renderIntegrity(integ);
  const dbg = $("debug-strip");
  if (status.debug) {
    dbg.hidden = false;
    dbg.textContent = "AZAI_DEBUG=1  max_body=" + (status.max_body || "") + "  hosted /v1=lamb-check-only  no telemetry";
  } else {
    dbg.hidden = true;
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
  if (!message) return;
  const model = $("model").value;
  addTurn("you", message);
  $("prompt").value = "";
  const { data } = await jpost("/v1/chat/completions", {
    model,
    messages: [{ role: "user", content: message }],
  });
  if (data.error) {
    addTurn("AZAI", data.error.message || JSON.stringify(data.error));
    if (data.error.lamb) setChips(data.error.lamb);
  } else {
    addTurn("Jeeves / " + (data.model || model), displayContent(data, model));
    if (data.azai && data.azai.lamb_out) setChips(data.azai.lamb_out);
  }
  await refresh();
});

$("lamb-btn").addEventListener("click", async () => {
  const text = $("prompt").value.trim();
  if (!text) {
    addTurn("Lamb", "Type something in the box, then press Check this text.");
    return;
  }
  const { data } = await jpost("/v1/lamb-check", { text });
  setChips(data);
  addTurn(
    "Lamb",
    `Peace ${data.peace} · Clarity ${data.clarity} · Service ${data.service} → ${data.overall}. `
      + (data.honest || "") + " No provider call."
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
  addTurn("runtime", "SEALED — Jeeves locked. Receipts remain readable.");
  await refresh();
});

$("open").addEventListener("click", async () => {
  await jpost("/v1/open", { reason: "ui" });
  addTurn("runtime", "OPEN — Jeeves ready.");
  await refresh();
});

$("integrity-btn").addEventListener("click", async () => {
  await refresh();
  addTurn("integrity", "Peace / Clarity / Service refreshed. Constitutional gate, not a proof of ethics.");
});

$("import-btn").addEventListener("click", () => $("import-file").click());
$("import-file").addEventListener("change", async (ev) => {
  const file = ev.target.files && ev.target.files[0];
  ev.target.value = "";
  if (!file) return;
  const content = await file.text();
  const { data } = await jpost("/v1/import", { content, filename: file.name });
  if (!data.ok) {
    addTurn("AZAI", data.error || "import failed");
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

refresh()
  .then(restoreSession)
  .catch((err) => addTurn("AZAI", String(err)));
