#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script untuk meng-update semua file .m3u / .m3u8
di SEMUA repository GitHub milik user tertentu.

- Target user : maywho5454
- Auth        : Personal Access Token melalui env var GITHUB_PAT
               (di-set lewat GitHub Actions secret MAGELIFE_GH_PAT)
"""

import os
from github import Github, GithubException

# ==============================
# KONFIGURASI
# ==============================

# Username GitHub yang mau diproses
GITHUB_USERNAME = "maywho5454"

# DRY_RUN = True  -> cuma simulasi (tidak ada file yang diubah)
# DRY_RUN = False -> beneran update file di GitHub
DRY_RUN = False

# Kalau kamu mau batasi hanya repo tertentu, isi keyword di sini.
# Contoh: ["CD", "OA"] -> hanya repo yang namanya mengandung "CD" atau "OA".
# Kalau kosong [], akan memproses semua repo milik user.
REPO_NAME_KEYWORDS = []  # biarkan kosong untuk semua repo


# Konten playlist baru yang akan MENIMPA isi file .m3u / .m3u8
PLAYLIST_CONTENT = """#EXTINF:-1 group-logo="https://i.imgur.com/aVBedkE.jpeg",🔰 MAGELIFE OFFICIAL

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/aVBedkE.jpeg" group-title="🔰 CHAT ADMIN", CHAT ADMIN
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/XXQ2pQ3.jpeg", ✅ CEK EMAIL KAMU 

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/DUIDZUC.jpeg" group-title="✅ CEK EMAIL KAMU", Kalau ga ada chat admni
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/XXQ2pQ3.jpeg", ✅ KALAU GA ADA 

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/DUIDZUC.jpeg" group-title="✅ KALAU GA ADA ", Kalau ga ada chat admni
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/XXQ2pQ3.jpeg", ✅ CHAT ADMIN KAMU

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/bxkCZST.jpeg" group-title="✅ CHAT ADMIN KAMU ", Kalau ga ada chat admni
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/bjfYe6g.jpegg", ✅ SILAHKAN RE ORDER

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/bjfYe6g.jpeg" group-title="✅ SILAHKAN RE ORDER", SILAHKAN RE ORDER
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/bjfYe6g.jpegg", ✅SILAHKAN RE ORDER OM

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/bjfYe6g.jpeg" group-title="✅ SILAHKAN RE ORDER OM", SILAHKAN RE ORDER
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/bjfYe6g.jpegg", ✅SILAHKAN RE ORDER TANTE

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/bjfYe6g.jpeg" group-title="✅SILAHKAN RE ORDER TANTE", SILAHKAN RE ORDER
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/bjfYe6g.jpegg", 📲 Wa 082219213334

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/bjfYe6g.jpeg" group-title="📲 Wa 082219213334", SILAHKAN RE ORDER
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/bjfYe6g.jpegg", 📲 Wa 082219213334 order

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/bjfYe6g.jpeg" group-title="📲 Wa 082219213334 order", SILAHKAN RE ORDER
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/PJ9tRpK.jpeg",✅ ORDER LYNK

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/PJ9tRpK.jpeg" group-title="✅ ORDER LYNK", ORDER LYNK
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/PJ9tRpK.jpeg",✅ https://lynk.id/magelife

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/PJ9tRpK.jpeg" group-title="✅ https://lynk.id/magelife", ORDER SHOPEE
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/PJ9tRpK.jpeg", ✅ORDER SHOPEE 

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/EWttwBZ.jpeg" group-title="✅ ORDER SHOPEE", ORDER LYNK
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8

#EXTINF:-1 group-logo="https://i.imgur.com/PJ9tRpK.jpeg", ✅ https://shorturl.at/1r9BB

#EXTINF:-1 tvg-id="Iheart80s" tvg-name="Iheart80s" tvg-logo="https://i.imgur.com/EWttwBZ.jpeg" group-title="✅ https://shorturl.at/1r9BB", ORDER LYNK
https://iheart-iheart80s-1-us.roku.wurl.tv/playlist.m3u8








#EXTM3U billed-msg="😢CHAT ADMIN 082219213334| lynk.id/magelife😎"
"""


def should_process_repo(repo_name: str) -> bool:
    """
    Cek apakah repo ini mau diproses, berdasarkan REPO_NAME_KEYWORDS.
    Kalau REPO_NAME_KEYWORDS kosong -> semua repo diproses.
    """
    if not REPO_NAME_KEYWORDS:
        return True
    lower = repo_name.lower()
    return any(keyword.lower() in lower for keyword in REPO_NAME_KEYWORDS)


def is_playlist_file(path: str) -> bool:
    """True kalau path berakhiran .m3u atau .m3u8."""
    lower = path.lower()
    return lower.endswith(".m3u") or lower.endswith(".m3u8")


def main():
    # Di workflow nanti kita set env GITHUB_PAT dari secret MAGELIFE_GH_PAT
    token = os.getenv("GITHUB_PAT")
    if not token:
        # fallback ke GITHUB_TOKEN kalau mau dipakai lokal
        token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise SystemExit(
            "ERROR: Env GITHUB_PAT / GITHUB_TOKEN belum diset.\n"
            "Kalau jalan di GitHub Actions, pastikan secret MAGELIFE_GH_PAT sudah di-set."
        )

    gh = Github(token)

    try:
        user = gh.get_user(GITHUB_USERNAME)
    except GithubException as e:
        raise SystemExit(f"Gagal mengambil user {GITHUB_USERNAME}: {e}")

    print(f"Login sebagai: {user.login}")
    print(f"DRY_RUN              : {DRY_RUN}")
    if REPO_NAME_KEYWORDS:
        print(f"Filter repo keywords : {REPO_NAME_KEYWORDS}")
    else:
        print("Filter repo keywords : (SEMUA repo user akan diproses)")
    print("-" * 60)

    # Loop semua repo milik user
    for repo in user.get_repos():
        if not should_process_repo(repo.name):
            continue

        print(f"\n▶ Repo: {repo.full_name}")
        default_branch = repo.default_branch or "main"
        print(f"   Default branch: {default_branch}")

        # Ambil isi root repo
        try:
            contents = repo.get_contents("", ref=default_branch)
        except GithubException as e:
            print(f"   Gagal membaca isi repo: {e}")
            continue

        files_touched = 0

        # DFS manual untuk jalanin semua folder & file
        while contents:
            item = contents.pop(0)

            if item.type == "dir":
                # Tambahkan isi folder ke antrian
                try:
                    contents.extend(
                        repo.get_contents(item.path, ref=default_branch)
                    )
                except GithubException as e:
                    print(f"   Gagal baca folder {item.path}: {e}")
                continue

            path = item.path

            if not is_playlist_file(path):
                continue

            files_touched += 1
            print(f"   - Target file: {path}")

            if DRY_RUN:
                # Hanya simulasi: tidak mengupdate
                continue

            try:
                repo.update_file(
                    path,
                    "Update playlist MAGELIFE footer via script",
                    PLAYLIST_CONTENT,
                    item.sha,
                    branch=default_branch,
                )
                print(f"     ✅ Berhasil update {path}")
            except GithubException as e:
                print(f"     ❌ Gagal update {path}: {e}")

        if files_touched == 0:
            print("   (Tidak ada file .m3u / .m3u8 ditemukan di repo ini.)")

    print("\nSelesai proses semua repo.")


if __name__ == "__main__":
    main()
