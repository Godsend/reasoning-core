#!/usr/bin/env python3
"""Poll ALL reasoning-core generations, download completed artifacts,
transcribe audio (critique/debate) when they land.

Run in background; notify on completion. Exits when all tasks are done
or after ~55 min (cinematic is slow). Idempotent: skips already-downloaded.
"""
import asyncio, json, os, subprocess, sys, time
from pathlib import Path
from notebooklm import NotebookLMClient

SCRIPTS = Path.home() / "AppData/Local/hermes/scripts"
VENV_PY = Path(os.environ["LOCALAPPDATA"]) / "hermes/hermes-agent/venv/Scripts/python.exe"
REFS = Path.home() / "dev/reasoning-core/references"
STATE_FILE = REFS / "nblm_notebook_state.json"
OUT = REFS / "artifacts"
OUT.mkdir(exist_ok=True)

STATUS = {1: "processing", 2: "pending", 3: "completed", 4: "failed"}

def heal_auth():
    h = SCRIPTS / "nblm_auth_healer.py"
    if h.exists():
        subprocess.run([str(VENV_PY), str(h)], capture_output=True, timeout=120)

def transcribe(path: Path):
    """Transcribe an m4a/mp3 via faster-whisper (already installed)."""
    txt = path.with_suffix(".txt")
    if txt.exists() and txt.stat().st_size > 0:
        return txt
    code = (
        "from faster_whisper import WhisperModel\n"
        "import sys\n"
        f"m = WhisperModel('small', device='cpu', compute_type='int8')\n"
        f"segs, info = m.transcribe({str(path)!r}, language='en', beam_size=3)\n"
        f"lines=[s.text.strip() for s in segs if s.text.strip()]\n"
        f"open({str(txt)!r},'w',encoding='utf-8').write('\\n'.join(lines))\n"
        f"print('transcribed', len(lines), 'segs', flush=True)\n"
    )
    r = subprocess.run([str(VENV_PY), "-c", code], capture_output=True, text=True, timeout=1800)
    if r.returncode == 0 and txt.exists():
        return txt
    return None

async def main():
    try:
        c = await NotebookLMClient.from_storage().__aenter__()
    except Exception as e:
        heal_auth()
        c = await NotebookLMClient.from_storage().__aenter__()
    st = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    nid = st["notebook_id"]
    gens = st.get("generations", {})  # name -> task_id

    done = set()
    deadline = time.time() + 55 * 60
    while time.time() < deadline:
        try:
            arts = await c.artifacts.list(nid)
        except Exception as e:
            print(f"[poll] list error: {e}", flush=True)
            await asyncio.sleep(30); continue

        by_id = {}
        for a in arts:
            aid = a.id if hasattr(a, "id") else a.get("id")
            by_id[aid] = a

        all_finished = True
        for name, tid in gens.items():
            if tid in done:
                continue
            a = by_id.get(tid)
            if not a:
                all_finished = False
                continue
            stt = getattr(a, "status", None) if not isinstance(a, dict) else a.get("status")
            kind = getattr(a, "kind", None) if not isinstance(a, dict) else a.get("kind")
            title = getattr(a, "title", None) if not isinstance(a, dict) else a.get("title")
            print(f"[poll] {name} status={stt}({STATUS.get(stt, stt)}) kind={kind} title={title}", flush=True)
            if stt in (3, "completed", "COMPLETED"):
                # determine extension by kind
                ext = ".mp4"
                if kind and ("AUDIO" in str(kind) or name.startswith("audio")):
                    ext = ".m4a"
                out = OUT / f"{name}{ext}"
                try:
                    if ext == ".m4a":
                        saved = await c.artifacts.download_audio(nid, str(out), tid)
                    else:
                        saved = await c.artifacts.download_video(nid, str(out), tid)
                    print(f"[poll] DOWNLOADED {name} -> {saved} ({Path(saved).stat().st_size} bytes)", flush=True)
                    if ext == ".m4a":
                        tr = transcribe(Path(saved))
                        if tr:
                            print(f"[poll] TRANSCRIBED {name} -> {tr.name}", flush=True)
                        else:
                            print(f"[poll] transcription failed for {name}", flush=True)
                except Exception as e:
                    print(f"[poll] DOWNLOAD ERROR {name}: {type(e).__name__}: {str(e)[:200]}", flush=True)
                done.add(tid)
            elif stt in (4, "failed", "FAILED"):
                print(f"[poll] FAILED {name} ({tid})", flush=True)
                done.add(tid)
            else:
                all_finished = False
        if len(done) >= len(gens):
            print("[poll] ALL DONE", flush=True)
            break
        await asyncio.sleep(60)
    await c.close()
    pending = [n for n, t in gens.items() if t not in done]
    if pending:
        print(f"[poll] TIMEOUT — still pending: {pending}. Re-run this script to continue.", flush=True)
    sys.exit(0 if not pending else 2)

sys.exit(asyncio.run(main()))
