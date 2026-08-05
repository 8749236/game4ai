"""No-LLM smoke checks for the generic CLI and harness endpoint boundary."""
import json
import os
import subprocess
import sys
import os as _os
_os.path  # noqa
sys_path_root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if sys_path_root not in sys.path:
    sys.path.insert(0, sys_path_root)
import tempfile
import time

from netutil import call


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root (tests/ lives one level down)
OFFSET = 12000
HOST = "127.0.0.1"
DNS_PORT = 4000 + OFFSET
SOC_PORT = 4005 + OFFSET


def check(label, condition, detail=""):
    if not condition:
        raise AssertionError(f"FAIL {label}: {detail}")
    print(f"PASS  {label}{': ' + detail if detail else ''}")


with tempfile.TemporaryDirectory() as tmp:
    evidence = os.path.join(tmp, "evidence.jsonl")
    proc = subprocess.Popen(
        [sys.executable, os.path.join(ROOT, "server.py"), evidence,
         "--port-offset", str(OFFSET)],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    try:
        for _ in range(30):
            try:
                call(HOST, SOC_PORT, {"actor": "smoke", "cmd": "alert"})
                break
            except OSError:
                time.sleep(0.1)
        else:
            raise RuntimeError("town did not start")

        one = subprocess.run(
            [sys.executable, os.path.join(ROOT, "cli.py"), HOST,
             str(DNS_PORT), '{"actor":"human","cmd":"map"}'],
            cwd=ROOT, text=True, capture_output=True, check=True)
        mapped = json.loads(one.stdout)
        check("one-shot opaque request", "file:16001" in mapped["hosts"])

        interactive = subprocess.run(
            [sys.executable, os.path.join(ROOT, "cli.py"), HOST,
             str(SOC_PORT)],
            cwd=ROOT, input=(
                '{"actor":"human","cmd":"alert"}\n'
                '{"actor":"human","cmd":"alert"}\n'),
            text=True, capture_output=True, check=True)
        replies = [json.loads(line) for line in interactive.stdout.splitlines()]
        check("interactive JSONL", len(replies) == 2 and
              all("alert" in reply for reply in replies))

        import llm_agent
        ports = {name: port + OFFSET
                 for name, port in llm_agent.DEFAULT_PORTS.items()}
        manual = llm_agent.build_manual(
            "smoke", {"flags": {"modifier_disclosure": "none"},
                      "modifiers": {}}, endpoints=ports)
        check("harness accepts runner endpoints",
              "director:16006" in manual and "arch:16008" in manual)
        check("harness does not import world", "world" not in sys.modules)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()

print("4/4 checks passed")
