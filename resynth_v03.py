#!/usr/bin/env python3
"""Re-synthesis pass on paper v0.3:
Adds v0.3 as a source, fires Critique + Deep Dive fresh, focused on the
new adversarial content (latency falsifier, purge test, scarred-tissue).
"""
import asyncio, json, os, subprocess, sys
from pathlib import Path
from notebooklm import NotebookLMClient
from notebooklm.rpc.types import AudioFormat, AudioLength

SCRIPTS = Path.home() / "AppData/Local/hermes/scripts"
VENV_PY = Path(os.environ["LOCALAPPDATA"]) / "hermes/hermes-agent/venv/Scripts/python.exe"
REFS = Path.home() / "dev/reasoning-core/references"
STATE_FILE = REFS / "nblm_notebook_state.json"
PAPER_V03 = REFS.parent / "paper/paper_v0.3.md"

def heal_auth():
    h = SCRIPTS / "nblm_auth_healer.py"
    if h.exists():
        subprocess.run([str(VENV_PY), str(h)], capture_output=True, timeout=120)

async def main():
    try:
        c = await NotebookLMClient.from_storage().__aenter__()
    except Exception as e:
        heal_auth()
        c = await NotebookLMClient.from_storage().__aenter__()
    st = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    nid = st["notebook_id"]

    # Add v0.3 paper as a source if not present
    existing = await c.sources.list(nid)
    have = set()
    for s in existing:
        nm = s.get("name") if isinstance(s, dict) else getattr(s, "name", None)
        if nm:
            have.add(Path(nm).name)
    if "paper_v0.3.md" not in have:
        await c.sources.add_file(nid, str(PAPER_V03), wait=True, wait_timeout=120)
        print("[re-synth] added paper_v0.3.md as source")
    else:
        print("[re-synth] paper_v0.3.md already a source")

    # Fire a fresh Critique focused on the v0.3 adversarial additions
    g = st.get("generations", {})
    g["re_critique_v03"] = (await c.artifacts.generate_audio(
        nid, audio_format=AudioFormat.CRITIQUE, audio_length=AudioLength.LONG,
        instructions=(
            "Critique paper v0.3. This revision added TWO falsifiers: "
            "(1) a latency falsifier — measure rerouting cost on load-bearing "
            "edge deletion, expected to scale geometrically and be independent "
            "of output correctness; (2) an epiplexity-after-purge test — purge "
            "the witness, measure weight epiplexity stability. And a new §5 "
            "confronting the Scarred Tissue objection (weights-as-compressed-data). "
            "Do the falsifiers actually break the circularity? Is §5's "
            "formation-vs-operation response sound, or does the honest "
            "regime-boundary admission undermine SH? Find what's still wrong."
        ),
    )).task_id
    g["re_deepdive_v03"] = (await c.artifacts.generate_audio(
        nid, audio_format=AudioFormat.DEEP_DIVE, audio_length=AudioLength.DEFAULT,
        instructions=(
            "Synthesize paper v0.3 in full. Focus on the strongest surviving "
            "claim after adversarial hardening: is the latency falsifier + "
            "purge test enough to make the Separation Hypothesis empirically "
            "testable rather than vapor? What does the Scarred Tissue "
            "objection really concede? What is the defensible core?"
        ),
    )).task_id

    st["generations"] = g
    STATE_FILE.write_text(json.dumps(st, indent=2))
    print(f"QUEUED re_critique_v03: {g['re_critique_v03']}")
    print(f"QUEUED re_deepdive_v03: {g['re_deepdive_v03']}")
    await c.close()

sys.exit(asyncio.run(main()))
