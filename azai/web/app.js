/* AZAI loopback UI. No CDN. No telemetry. */
const $ = (id) => document.getElementById(id);

function badge(el, key, label, value) {
  const node = el.querySelector(`[data-k="${key}"]`);
  if (!node) return;
  node.textContent = `${label} ${value}`;
  node.className = String(value || "").split(/[\s/]/)[0];
  node.setAttribute("data-k", key);
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

function renderReceipts(rows) {
  const ol = $("receipts");
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
  const lamb = integ.lamb || integ;
  box.innerHTML = `
    <p class="${lamb.peace}">Peace ${lamb.peace}</p>
    <p class="${lamb.clarity}">Clarity ${lamb.clarity}</p>
    <p class="${lamb.service}">Service ${lamb.service}</p>
    <p>Runtime ${integ.runtime || "—"}</p>
    <p>Receipts ${integ.receipts && integ.receipts.ok ? "HEALTHY" : "CHECK"} (${integ.receipts ? integ.receipts.count : 0})</p>
    <p class="muted">${lamb.honest || ""}</p>
  `;
}

function addTurn(who, text) {
  const t = $("transcript");
  const div = document.createElement("div");
  div.className = "turn";
  const w = document.createElement("div");
  w.className = "who";
  w.textContent = who;
  const b = document.createElement("div");
  b.textContent = text;
  div.appendChild(w);
  div.appendChild(b);
  t.appendChild(div);
  t.scrollTop = t.scrollHeight;
}

async function refresh() {
  const status = await jget("/v1/health");
  const bar = $("status");
  const lamb = (status.lamb && status.lamb.overall) || "—";
  badge(bar, "lamb", "Lamb", lamb);
  badge(bar, "integrity", "Integrity", status.integrity || lamb);
  badge(bar, "runtime", "Runtime", status.runtime || "—");
  badge(bar, "jeeves", "Jeeves", status.jeeves || "—");
  const prov = status.providers || {};
  const present = Object.entries(prov)
    .filter(([k, v]) => k !== "local" && v && v.present)
    .map(([k]) => k);
  const ptxt = present.length ? present.join("+") : "local only";
  badge(bar, "providers", "Providers", ptxt);
  const rec = await jget("/v1/receipts");
  renderReceipts(rec.receipts);
  const integ = await jget("/v1/integrity");
  renderIntegrity(integ);
}

$("prompt-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const message = $("prompt").value.trim();
  if (!message) return;
  const model = $("model").value;
  addTurn("operator", message);
  $("prompt").value = "";
  const { data } = await jpost("/v1/chat/completions", {
    model,
    messages: [{ role: "user", content: message }],
  });
  if (data.error) {
    addTurn("AZAI", data.error.message || JSON.stringify(data.error));
  } else {
    const content = data.choices && data.choices[0] && data.choices[0].message
      ? data.choices[0].message.content
      : JSON.stringify(data);
    addTurn("Jeeves / " + (data.model || model), content);
  }
  await refresh();
});

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

refresh().catch((err) => addTurn("AZAI", String(err)));
