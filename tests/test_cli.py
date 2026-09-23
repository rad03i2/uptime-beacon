import json
from unittest.mock import patch
from uptime_beacon.cli import main
from uptime_beacon.core import CheckResult

OK = CheckResult("https://example.com", True, 200, 12.3, "2026-01-01T00:00:00+00:00")
DOWN = CheckResult("https://down.example", False, None, 10.0, "2026-01-01T00:00:00+00:00", "offline")

def test_cli_json(capsys):
    with patch("uptime_beacon.cli.check_many", return_value=[OK]):
        assert main(["https://example.com", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)[0]["status"] == 200

def test_cli_failure_exit():
    with patch("uptime_beacon.cli.check_many", return_value=[DOWN]):
        assert main(["https://down.example"]) == 1

def test_cli_requires_target(capsys):
    assert main([]) == 2
    assert "Provide at least one" in capsys.readouterr().err

def test_target_file(tmp_path):
    f = tmp_path / "targets.txt"
    f.write_text("# comment\nhttps://example.com\nhttps://example.com\n", encoding="utf-8")
    with patch("uptime_beacon.cli.check_many", return_value=[OK]) as mocked:
        assert main(["--file", str(f)]) == 0
    assert mocked.call_args.args[0] == ["https://example.com"]
