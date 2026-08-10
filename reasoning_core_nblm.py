#!/usr/bin/env python3
"""Create a NotebookLM synthesis notebook for the Reasoning Core project.

Sources: epiplexity full paper, Sophontic interview transcript, EILT brief.
Fires an Audio Overview synthesis (fast, effectively unlimited on Ultra) and
polls for completion. Reuses the auth-heal-on-failure pattern from
dream_video_pipeline.py.

Usage:
    python reasoning_core_nblm.py init     # create notebook + add sources
    python reasoning_core_nblm.py synth    # fire Audio Overview on existing nb
    python reasoning_core_nblm.py status   # poll artifacts
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS = Path.home() / "AppData/Local/hermes/scripts"
VENV_PY = Path(os.environ["LOCALAPPDATA"]) / "hermes/hermes-agent/venv/Scripts/python.exe"
REFS = Path.home() / "dev/reasoning-core/references/sources"

NOTEBOOK_NAME = "Reasoning Core: Epiplexity x Geometry x EILT"
STATE_FILE = REFS.parent / "nblm_notebook_state.json"

SOURCES = [
    REFS / "epiplexity_paper_full.md",
    REFS / "sophontic_interview_transcript.md",
    REFS / "EILT_brief.md",
]


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(s):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, indent=2))


def heal_auth():
    h = SCRIPTS / "nblm_auth_healer.py"
    if h.exists():
        subprocess.run([str(VENV_PY), str(h)], capture_output=True, timeout=120)


async def get_client():
    from notebooklm import NotebookLMClient
    try:
        # Enter the async context so the kernel/http client initializes
        return await NotebookLMClient.from_storage().__aenter__()
    except Exception as e:
        if "Authentication" in str(e) or "expired" in str(e):
            print("[AUTH] expired — healing", file=sys.stderr)
            heal_auth()
            return await NotebookLMClient.from_storage().__aenter__()
        raise


def nid_of(created):
    if isinstance(created, str):
        return created
    if isinstance(created, dict):
        return created.get("id") or created.get("notebook_id")
    return getattr(created, "id", None) or created


async def cmd_init():
    client = await get_client()
    st = load_state()
    nid = st.get("notebook_id")
    if not nid:
        # find existing by name
        try:
            for nb in await client.notebooks.list():
                nm = nb.get("name") if isinstance(nb, dict) else getattr(nb, "name", "")
                if nm == NOTEBOOK_NAME:
                    nid = nb.get("id") if isinstance(nb, dict) else getattr(nb, "id", None)
                    break
        except Exception:
            pass
    if not nid:
        created = await client.notebooks.create(title=NOTEBOOK_NAME)
        nid = nid_of(created)
        save_state({"notebook_id": nid})
        print(f"[INIT] created notebook {NOTEBOOK_NAME}: {nid}")
    else:
        save_state({"notebook_id": nid})
        print(f"[INIT] using existing notebook: {nid}")

    # add sources not already present
    try:
        existing = await client.sources.list(nid)
    except Exception:
        existing = []
    have = set()
    for s in existing:
        nm = s.get("name") if isinstance(s, dict) else getattr(s, "name", None)
        if nm:
            have.add(Path(nm).name)
    for f in SOURCES:
        if f.name in have:
            print(f"[INIT] source present: {f.name}")
            continue
        try:
            await client.sources.add_file(nid, str(f), wait=True, wait_timeout=120)
            print(f"[INIT] added source: {f.name}")
        except Exception as e:
            print(f"[INIT] ERROR adding {f.name}: {type(e).__name__}: {str(e)[:160]}")
    await client.close()


async def cmd_synth():
    client = await get_client()
    st = load_state()
    nid = st.get("notebook_id")
    if not nid:
        print("[SYNTH] no notebook — run init first")
        return
    # confirm sources loaded
    try:
        existing = await client.sources.list(nid)
        print(f"[SYNTH] notebook has {len(existing)} sources")
    except Exception as e:
        print(f"[SYNTH] source check failed: {e}")
    a = await client.artifacts.generate_audio(
        nid,
        instructions=("Synthesize the relationship between epiplexity "
                      "(structural information extractable by bounded observers), "
                      "the geometric-reasoning perturbation paradigm from Sophontic, "
                      "and EILT's substrate-agnostic functionalist claim of an "
                      "'amnesia brain with memory' — the judge/witness/router "
                      "architecture. Focus on what unifies them and what testable "
                      "predictions follow."),
    )
    tid = getattr(a, "task_id", None) or (a.get("task_id") if isinstance(a, dict) else None)
    st = load_state()
    st["task_id"] = tid
    save_state(st)
    print(f"[SYNTH] audio queued: {a}")
    await client.close()


async def cmd_status():
    client = await get_client()
    st = load_state()
    nid = st.get("notebook_id")
    if not nid:
        print("[STATUS] no notebook")
        return
    try:
        arts = await client.artifacts.list(nid)
        print(f"[STATUS] artifacts for {nid}:")
        for x in arts:
            print(f"  - {x}")
    except Exception as e:
        print(f"[STATUS] error: {type(e).__name__}: {str(e)[:160]}")
    await client.close()


async def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "init":
        await cmd_init()
    elif cmd == "synth":
        await cmd_synth()
    elif cmd == "status":
        await cmd_status()
    else:
        print("usage: init|synth|status")


if __name__ == "__main__":
    asyncio.run(main())
