#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script untuk meng-update SEMUA file di SEMUA repository
GitHub milik user yang punya token.

⚠️ PENTING:
- Tidak mengubah nama repo.
- Tidak mengubah nama file.
- HANYA mengubah isi (content) file.
- file ini sendiri "update_all_playlists.py" TIDAK akan di-update.

Dipakai dari GitHub Actions dengan env:
  GITHUB_PAT = ${{ secrets.MAGELIFE_GH_PAT }}
"""

import os
from github import Github, GithubException, Auth

# ==============================
# KONFIGURASI
# ==============================

DRY_RUN = False   # True = test mode, False = update sungguhan
REPO_NAME_KEYWORDS = []  # kosong = semua repo milik user

# Nama file yang TIDAK BOLEH di-update
EXCLUDED_FILES = [
    "update_all_playlists.py",
    ".github/workflows/update_all_playlists.yml"
]

# Isi playlist baru (akan menimpa semua file lain)
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
    """Filter nama repo (opsional)."""
    if not REPO_NAME_KEYWORDS:
        return True
    lower = repo_name.lower()
    return any(k.lower() in lower for k in REPO_NAME_KEYWORDS)


def should_update_file(path: str) -> bool:
    """SEMUA file di-update kecuali file yang dikecualikan."""
    filename = os.path.basename(path).lower()
    for skip in EXCLUDED_FILES:
        if filename == skip.lower():
            return False
    return True


def main():
    token = os.getenv("GITHUB_PAT") or os.getenv("GITHUB_TOKEN")
    if not token:
        raise SystemExit("ERROR: token tidak ditemukan. Set secret MAGELIFE_GH_PAT.")

    gh = Github(auth=Auth.Token(token))

    try:
        user = gh.get_user()
    except GithubException as e:
        raise SystemExit(f"Gagal login dengan token: {e}")

    print(f"Login sebagai: {user.login}")
    print(f"DRY_RUN = {DRY_RUN}")
    print("-" * 60)

    for repo in user.get_repos():
        if not should_process_repo(repo.name):
            continue

        print(f"\n▶ Repo: {repo.full_name}")

        default_branch = repo.default_branch or "main"

        try:
            contents = repo.get_contents("", ref=default_branch)
        except Exception as e:
            print(f"   Tidak bisa load repo: {e}")
            continue

        files_touched = 0

        while contents:
            item = contents.pop(0)

            # Folder → scan isinya
            if item.type == "dir":
                try:
                    contents.extend(
                        repo.get_contents(item.path, ref=default_branch)
                    )
                except Exception:
                    pass
                continue

            path = item.path

            if not should_update_file(path):
                print(f"   - SKIP (file dikecualikan): {path}")
                continue

            files_touched += 1
            print(f"   - Update isi file: {path}")

            if not DRY_RUN:
                try:
                    repo.update_file(
                        path,
                        "Auto-update playlist Magelife",
                        PLAYLIST_CONTENT,
                        item.sha,
                        branch=default_branch,
                    )
                    print("     ✔ Berhasil")
                except Exception as e:
                    print(f"     ✖ Gagal update: {e}")

        print(f"   Total file diupdate: {files_touched}")

    print("\nSelesai semua repo.")

if __name__ == "__main__":
    main()
