#!/usr/bin/env python3
"""Fire ALL reasoning-core NBLM generations:
   3 videos (cinematic, explainer, brief) + 2 audios (critique, debate).
Queues them, saves task ids, then reports. Slow; run in background.
"""
import asyncio, json, os, subprocess, sys
from pathlib import Path
from notebooklm import NotebookLMClient
from notebooklm.rpc.types import AudioFormat, AudioLength, VideoFormat, VideoStyle

SCRIPTS = Path.home() / "AppData/Local/hermes/scripts"
VENV_PY = Path(os.environ["LOCALAPPDATA"]) / "hermes/hermes-agent/venv/Scripts/python.exe"
REFS = Path.home() / "dev/reasoning-core/references"
STATE_FILE = REFS / "nblm_notebook_state.json"

def heal_auth():
    h = SCRIPTS / "nblm_auth_healer.py"
    if h.exists():
        subprocess.run([str(VENV_PY), str(h)], capture_output=True, timeout=120)

BASE_INSTR = (
    "Ground the argument in the hypergraph ledger framing: reasoning as "
    "constraint-satisfaction over an expanding relational hypergraph; "
    "epiplexity as the structural information a bounded observer extracts; "
    "the judge/witness/router split; perturbation = edge rewiring; flip rate = "
    "does the inference path survive edge deletion; the BS-detector function. "
)

async def main():
    try:
        c = await NotebookLMClient.from_storage().__aenter__()
    except Exception as e:
        heal_auth()
        c = await NotebookLMClient.from_storage().__aenter__()
    st = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    nid = st["notebook_id"]
    jobs = {}

    # -- Cinematic video (scare resource: ~10/day on Ultra) --
    jobs["cinematic"] = (await c.artifacts.generate_cinematic_video(
        nid,
        instructions=BASE_INSTR + "Cinematic documentary: the Separation Hypothesis — why intelligence may be separable from memory. A brain with amnesia, provided with memory.",
    )).task_id

    # -- Videos --
    jobs["explainer"] = (await c.artifacts.generate_video(
        nid, video_format=VideoFormat.EXPLAINER,
        instructions=BASE_INSTR + "Explain the judge/witness/router architecture and why flip-rate distinguishes reasoning from recall.",
    )).task_id
    jobs["brief"] = (await c.artifacts.generate_video(
        nid, video_format=VideoFormat.BRIEF,
        instructions=BASE_INSTR + "60-second brief: intelligence as geometry, memory as swappable content.",
    )).task_id

    # -- Audios (Critique + Debate) --
    jobs["audio_critique"] = (await c.artifacts.generate_audio(
        nid, audio_format=AudioFormat.CRITIQUE, audio_length=AudioLength.DEFAULT,
        instructions=BASE_INSTR + "Adversarial critique: steelman AND attack the Separation Hypothesis. What breaks? Circularity of flip-rate? Is the geometry claim testable or vapor?",
    )).task_id
    jobs["audio_debate"] = (await c.artifacts.generate_audio(
        nid, audio_format=AudioFormat.DEBATE, audio_length=AudioLength.DEFAULT,
        instructions=BASE_INSTR + "Debate both sides: 'Intelligence is a separable geometric core + swappable memory' vs 'Intelligence is inseparable from embodied data.' Argue to a verdict.",
    )).task_id

    st["generations"] = st.get("generations", {})
    st["generations"].update(jobs)
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(st, indent=2))
    for k, v in jobs.items():
        print(f"QUEUED {k}: {v}")
    print("All queued. Poll with poll_artifacts.py")
    await c.close()

sys.exit(asyncio.run(main()))
