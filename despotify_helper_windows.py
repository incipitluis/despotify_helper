"""Descarga en MP3 una playlist exportada de Spotify (formato Exportify CSV) en Windows.

Uso:
    python despotify_helper_windows.py <playlist.csv>

Estructura de salida: %USERPROFILE%\\Music\\despotify_helper\\<Artista>\\<Album>\\<Cancion>.mp3
Resumible: si el .mp3 ya existe, salta.
Requiere: yt-dlp y ffmpeg en el PATH.
    winget install yt-dlp.yt-dlp
    winget install Gyan.FFmpeg
  (o con Chocolatey: choco install yt-dlp ffmpeg)
"""
from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

OUTPUT_ROOT = Path.home() / "Music" / "despotify_helper"
INVALID_CHARS = re.compile(r'[/\\:*?"<>|\x00]')
RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
DOWNLOAD_TIMEOUT_S = 300
CREATE_NO_WINDOW = 0x08000000


def sanitize(name: str) -> str:
    cleaned = INVALID_CHARS.sub("_", name).strip()
    cleaned = cleaned.rstrip(". ")
    if not cleaned:
        return "_"
    if cleaned.split(".")[0].upper() in RESERVED_NAMES:
        cleaned = f"_{cleaned}"
    return cleaned


def first_artist(artists: str) -> str:
    return artists.split(",")[0].strip()


def download(query: str, out_path: Path) -> tuple[bool, str]:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    template = str(out_path.with_suffix("")) + ".%(ext)s"
    cmd = [
        "yt-dlp",
        f"ytsearch1:{query}",
        "--no-playlist",
        "--quiet",
        "--no-warnings",
        "--no-progress",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "192K",
        "-o", template,
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=DOWNLOAD_TIMEOUT_S,
            creationflags=CREATE_NO_WINDOW,
        )
    except subprocess.TimeoutExpired:
        return False, "timeout (>5min)"
    if proc.returncode != 0:
        err_lines = (proc.stderr or proc.stdout).strip().splitlines()
        return False, err_lines[-1] if err_lines else f"exit {proc.returncode}"
    if not out_path.exists():
        return False, "yt-dlp terminó OK pero no apareció el .mp3"
    return True, ""


def main(csv_path: Path) -> int:
    if sys.platform != "win32":
        print("Este script está pensado para Windows. En macOS/Linux usa despotify_helper.py.", file=sys.stderr)
        return 1
    if not csv_path.exists():
        print(f"No existe el fichero: {csv_path}", file=sys.stderr)
        return 1
    for tool in ("yt-dlp", "ffmpeg"):
        if not shutil.which(tool):
            print(
                f"{tool} no está en el PATH "
                f"(winget install {'yt-dlp.yt-dlp' if tool == 'yt-dlp' else 'Gyan.FFmpeg'})",
                file=sys.stderr,
            )
            return 1

    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("El CSV está vacío.", file=sys.stderr)
        return 1
    required = {"Track Name", "Album Name", "Artist Name(s)"}
    missing = required - set(rows[0].keys())
    if missing:
        print(f"Faltan columnas en el CSV: {missing}", file=sys.stderr)
        return 1

    total = len(rows)
    skipped = downloaded = failed = 0
    failures: list[str] = []

    print(f"Procesando {total} canciones. Salida: {OUTPUT_ROOT}\n")

    for i, row in enumerate(rows, 1):
        track = (row.get("Track Name") or "").strip()
        album = (row.get("Album Name") or "").strip()
        artists = (row.get("Artist Name(s)") or "").strip()

        if not (track and album and artists):
            print(f"[{i}/{total}] SALTADA (datos incompletos)")
            failed += 1
            failures.append(f"fila {i}: datos incompletos")
            continue

        artist_folder = first_artist(artists)
        out_path = (
            OUTPUT_ROOT
            / sanitize(artist_folder)
            / sanitize(album)
            / f"{sanitize(track)}.mp3"
        )

        label = f"[{i}/{total}] {artist_folder} - {album} - {track}"

        if out_path.exists():
            print(f"{label}\n    ya existe, salto")
            skipped += 1
            continue

        print(f"{label}\n    descargando...")
        ok, err = download(f"{artists} - {track}", out_path)
        if ok:
            downloaded += 1
        else:
            failed += 1
            failures.append(f"{artist_folder} - {track}  ({err})")
            print(f"    fallo: {err}")

    print(
        f"\nResumen: {downloaded} descargadas, {skipped} ya existían, "
        f"{failed} fallidas de {total} totales."
    )
    if failures:
        print("\nFallidas:")
        for item in failures:
            print(f"  - {item}")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python despotify_helper_windows.py <playlist.csv>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(Path(sys.argv[1]).expanduser()))
