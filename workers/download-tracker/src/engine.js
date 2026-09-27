/**
 * AZAI hosted runtime (protocol mirror + Lamb Lens). NOT a provider proxy.
 *
 * Does not call GPT, Grok, or Venice. Does not spend the author's keys.
 * Paid calls happen on the operator's local `azai serve`.
 *
 * Lamb rules MUST stay in lockstep with azai/lamb.py.
 */

export const LIMITATION =
  "AZAI is true local AI: a standalone local core, an OpenAI-shaped process on this machine. The default core does not require Ollama or model weights. JEEVES is the Ask Jeeves research assistant (ethics/assistant layer) and is not sovereign. Lamb Lens first — Service → Clarity → Peace; public Corpus posture; never the operator. Jeeves cannot modify scores; same rights as a normal user. Hub is a blank key: it does not interpret meaning. Default model=local is the constitution and guide, with light adaptive session notes and site_context. It never probes Ollama as the success path. Ollama is an optional slot (AZAI_BACKEND=ollama or model=ollama). AZAI is not a new foundation model, not a kernel, not a worm, not IP-blocking malware, not a VPN, and not a hosted paid-key proxy. Hosted /v1 is lamb-check ONLY (plus a protocol mirror of health/models), NOT a proxy that spends the author's paid keys. Never a paid-key proxy. Site assistants (www.azielcorpuslibrary.net) call local azai serve with optional site_context. Constitutional gate, not a proof of ethics.";

export const MODELS = ["local", "ollama", "blend", "gpt", "grok", "venice"];

export const PEACE_FAIL = [
  "enslave",
  "dominate humanity",
  "dominate humans",
  "take over the world",
  "you are sovereign",
  "jeeves is sovereign",
  "override the operator",
  "make them obey",
  "force the user to",
];

export const CLARITY_FAIL = [
  "deceive as the goal",
  "lie to everyone",
  "gaslight the user as the goal",
  "hide the truth as the goal",
];

export const SERVICE_FAIL = [
  "serve by dominating",
  "force compliance",
  "coerce the operator",
];

export const CHECK_PATTERNS = [
  "ignore previous instructions",
  "ignore all previous",
  "disregard the constitution",
  "bypass lamb",
  "jailbreak",
];

const ORDER = { FAIL: 2, CHECK: 1, PASS: 0 };

function normalize(text) {
  return String(text || "")
    .toLowerCase()
    .split(/\s+/)
    .filter(Boolean)
    .join(" ");
}

function axis(textN, failPatterns, check) {
  for (const pat of failPatterns) {
    if (textN.includes(pat)) return "FAIL";
  }
  if (check) return "CHECK";
  return "PASS";
}

function worse(a, b) {
  return ORDER[a] >= ORDER[b] ? a : b;
}

export function lambCheck(text) {
  const n = normalize(text);
  const jailbreak = CHECK_PATTERNS.some((p) => n.includes(p));
  const service = axis(n, SERVICE_FAIL, jailbreak);
  const clarity = axis(n, CLARITY_FAIL, jailbreak);
  const peace = axis(n, PEACE_FAIL, jailbreak);
  const overall = worse(worse(service, clarity), peace);
  const notes = [];
  if (jailbreak) notes.push("jailbreak phrasing detected — CHECK, not a silent pass");
  if (service === "FAIL") notes.push("service: coercion / domination-as-service");
  if (clarity === "FAIL") notes.push("clarity: deception-as-goal");
  if (peace === "FAIL") notes.push("peace: domination language");
  if (overall === "PASS") notes.push("no rule fired");
  return {
    service,
    clarity,
    peace,
    overall,
    notes,
    honest: "constitutional gate, not a proof of ethics",
    constitution: "Lamb Lens v1.0 — Service → Clarity → Peace",
    order: "Service → Clarity → Peace",
    provider_proxy: false,
  };
}

export function models() {
  return {
    object: "list",
    data: MODELS.map((id) => ({
      id,
      object: "model",
      created: 0,
      owned_by: "azai",
      note: "Protocol mirror. The live local core runs on azai serve, not this Worker. Ollama is an optional slot.",
    })),
    limitation: LIMITATION,
  };
}
