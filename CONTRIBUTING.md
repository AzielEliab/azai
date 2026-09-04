# Contributing to AZAI

**Forks are first-class.** This project is Apache-2.0; you do not need
permission to fork, patch, or redistribute.

**Forks are welcome and always allowed.**

## How to run tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q
```

Python 3.10+. Tests never call the network. Provider hooks are injected
in-process. Do not set live API keys in CI.

## Ground rules

1. **True local AI on an Ollama base.** Default `model=local` uses
   Ollama through JEEVES. Local JEEVES does not pretend to be GPT.
   Not a hosted paid-key proxy.
2. **JEEVES is not sovereign.** It is the ethics/assistant layer.
   Lamb Lens (peace, clarity, service) and the operator govern every
   turn. Hub is a blank key: it does not interpret meaning.
3. **Blend is visible.** When mode=blend, label `[gpt]` `[grok]`
   `[venice]` then `[synthesis]`. Never hide which model said what.
4. **Hosted Worker `/v1` is lamb-check ONLY.** Never a paid-key proxy.
   Health and models are a protocol mirror. Paid calls happen on the
   operator's local `azai serve`.
5. **UI binds 127.0.0.1:8860 by default.** `--host` for on-site LAN is
   documented risk (it can spend the operator's keys). Prefer loopback.
   Max POST body is 1 MiB. No telemetry. No keys in the Worker.
6. **Voice is optional extra `[voice]`.** MVP is text. Push-to-talk
   only; no wake word; no passive recording; voice does not execute
   commands. Do not vendor Whisper/Piper models in the tarball.
7. **Memory writes require explicit confirm.** Session-only by default.
8. **Do not implement** real "static block IP routing", Phoenix as a
   spreader, or remote OS takeover.
9. **Do not merge this product** into AZ-OS, GodLock, or any sibling tree.
10. **Do not mix the download tracker** with any other product's Worker or KV.
11. New behavior needs a test that fails without the change.
12. Keep the Python Lamb Lens and Worker JS port in lockstep.

## Where to change things

- Lamb Lens: `azai/lamb.py` and `workers/download-tracker/src/engine.js`
- Providers: `azai/providers.py`
- Ollama base: `azai/ollama.py`, `scripts/setup-ollama.sh`
- JEEVES layer: `azai/jeeves.py`
- Runtime / blend / seal: `azai/runtime.py`
- Receipts: `azai/receipts.py`
- CLI: `azai/cli.py` (`azai doctor`, import/export)
- Import/export: `azai/exchange.py`
- Doctor: `azai/doctor.py`
- Debug (`AZAI_DEBUG=1`): `azai/debug.py`
- Local UI + `/v1`: `azai/ui.py`, `azai/web/`
- Spec: `docs/whitepaper.md`
- Source papers: `docs/source/`
- Flutter companion: `mobile/`
- Isolated counter + hosted gate: `workers/download-tracker/`

## License of contributions

By submitting a change you agree it is licensed under Apache-2.0, the
same license as the rest of the tree. Keep the copyright lines honest.
Ship as Aziel Eliab.
