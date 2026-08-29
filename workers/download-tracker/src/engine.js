/**
 * AZAI hosted runtime (protocol mirror + Lamb Lens). NOT a provider proxy.
 *
 * Does not call GPT, Grok, or Venice. Does not spend the author's keys.
 * Paid calls happen on the operator's local `azai serve`.
 *
 * Lamb rules MUST stay in lockstep with azai/lamb.py.
 */

export const LIMITATION =
  "AZAI is a local OpenAI-compatible runtime, not a new foundation model, not a kernel, not a worm, not IP-blocking malware, not a VPN. Jeeves is not sovereign. Lamb Lens (peace, clarity, service) gates every turn. Hub is a blank key: it does not interpret meaning. Hosted /v1 is a protocol mirror + Lamb check + models list, NOT a proxy that spends the author's paid keys. Constitutional gate, not a proof of ethics.";

export const MODELS = ["blend", "gpt", "grok", "venice", "local"];

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
  const peace = axis(n, PEACE_FAIL, jailbreak);
  const clarity = axis(n, CLARITY_FAIL, jailbreak);
  const service = axis(n, SERVICE_FAIL, jailbreak);
  const overall = worse(worse(peace, clarity), service);
  const notes = [];
  if (jailbreak) notes.push("jailbreak phrasing detected — CHECK, not a silent pass");
  if (peace === "FAIL") notes.push("peace: domination language");
  if (clarity === "FAIL") notes.push("clarity: deception-as-goal");
  if (service === "FAIL") notes.push("service: coercion / domination-as-service");
  if (overall === "PASS") notes.push("no rule fired");
  return {
    peace,
    clarity,
    service,
    overall,
    notes,
    honest: "constitutional gate, not a proof of ethics",
    constitution: "Lamb Lens v1.0 — Peace → Clarity → Service",
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
      note: "Protocol mirror. Live blend runs on local azai serve, not this Worker.",
    })),
    limitation: LIMITATION,
  };
}
