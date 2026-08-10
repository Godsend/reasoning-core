#!/usr/bin/env python3
"""Poll the Reasoning Core NotebookLM audio overview until it completes and download it."""
import asyncio, json, os, subprocess, sys
from pathlib import Path

SCRIPTS = Path.home() / "AppData/Local/hermes/scripts"
VENV_PY = Path(os.environ["LOCALAPPDATA"]) / "hermes/hermes-agent/venv/Scripts/python.exe"
REFS = Path.home() / "dev/reasoning-core/references"
STATE_FILE = REFS / "nblm_notebook_state.json"

def heal_auth():
    h = SCRIPTS / "nblm_auth_healer.py"
    if h.exists():
        subprocess.run([str(VENV_PY), str(h)], capture_output=True, timeout=120)

async def main():
    from notebooklm import NotebookLMClient
    st = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    nid = st.get("notebook_id")
    task_id = st.get("task_id")
    if not task_id:
        # try latest artifact
        pass
    try:
        client = await NotebookLMClient.from_storage().__aenter__()
    except Exception as e:
        if "Authentication" in str(e) or "expired" in str(e):
            heal_auth()
            client = await NotebookLMClient.from_storage().__aenter__()
        else:
            raise
    for i in range(30):
        try:
            arts = await client.artifacts.list(nid)
        except Exception as e:
            print(f"[poll] list error {i}: {e}")
            await asyncio.sleep(20); continue
        for a in arts:
            sid = a.id if hasattr(a, "id") else a.get("id")
            stt = getattr(a, "status", None) if not isinstance(a, dict) else a.get("status")
            url = getattr(a, "url", None) if not isinstance(a, dict) else a.get("url")
            print(f"[poll] task {sid} status={stt} url={'yes' if url else 'no'}")
            # status: 3=COMPLETED, 4=FAILED
            if stt in (3, "completed", "COMPLETED"):
                print(f"COMPLETED {sid} url={url}")
                # Download via the client's auth-aware method (NOT urllib:
                # raw Google storage URLs wall to sign-in for naive clients).
                out = REFS / f"synthesis_overview_{sid[:8]}.m4a"
                try:
                    saved = await client.artifacts.download_audio(nid, str(out), sid)
                    print(f"DOWNLOADED {saved} ({Path(saved).stat().st_size} bytes)")
                except Exception as e:
                    print(f"DOWNLOAD ERROR {type(e).__name__}: {str(e)[:200]}")
                await client.close(); return 0
            if stt in (4, "failed", "FAILED"):
                print(f"FAILED {sid}")
                await client.close(); return 1
        await asyncio.sleep(20)
    await client.close()
    print("TIMEOUT after 10 min — still rendering")
    return 2

sys.exit(asyncio.run(main()))
