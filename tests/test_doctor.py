"""azai doctor: Lamb fixtures, loopback, receipts, no Worker keys."""

from azai.cli import main
from azai.doctor import run


def test_doctor_run_ok(tmp_path) -> None:
    payload = run(data_dir=str(tmp_path / "AZAI_DATA"))
    assert payload["ok"] is True
    ids = {c["id"]: c for c in payload["checks"]}
    for needed in (
        "version",
        "python",
        "lamb_pass",
        "lamb_fail",
        "lamb_check",
        "loopback",
        "max_body",
        "no_telemetry",
        "worker_no_keys",
        "worker_not_proxy",
        "tarball",
        "receipts",
        "jeeves_layer",
        "ollama",
        "skill_true_local",
        "install_ollama",
    ):
        assert ids[needed]["ok"] is True, needed + " " + str(ids[needed])
    assert payload["version"] == "0.3.0"
    assert payload["jeeves_sovereign"] is False
    assert payload["local_ai"] == "ollama-base"
    assert payload["hosted_v1"] == "lamb-check-only"


def test_cli_doctor(capsys) -> None:
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert "PASS" in out
    assert "lamb_pass" in out
    assert main(["doctor", "--json"]) == 0
    jout = capsys.readouterr().out
    assert '"ok": true' in jout.replace(" ", "") or '"ok": true' in jout
