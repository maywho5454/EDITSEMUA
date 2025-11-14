#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script untuk meng-update semua file .m3u / .m3u8
di SEMUA repository GitHub milik user yang punya token.

⚠️ CATATAN PENTING:
- SCRIPT INI TIDAK PERNAH MENGUBAH NAMA REPO.
- SCRIPT INI TIDAK PERNAH MENGUBAH NAMA FILE.
  YANG DIGANTI HANYA ISI (CONTENT) FILE-NYA SAJA.

Dipakai dari GitHub Actions dengan env:
  GITHUB_PAT = ${{ secrets.MAGELIFE_GH_PAT }}
"""

import os
from github import Github, GithubException, Auth

# ==============================
# KONFIGURASI
# ==============================

# DRY_RUN = True  -> hanya simulasi (cek file apa saja, TIDAK mengubah apa pun)
# DRY_RUN = False -> beneran update file di GitHub
DRY_RUN = False

# Kalau mau batasi hanya repo tertentu, isi keyword di sini.
# Contoh: ["CD", "OA"] -> hanya repo yang namanya mengandung "CD" atau "OA".
# Kalau kosong [], semua repo milik user akan diproses.
REPO_NAME_KEYWORDS = []  # biarkan [] kalau mau semua repo


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
    if not REPO_NAME_KEYWORDS:
        return True
    lower = repo_name.lower()
    return any(keyword.lower() in lower for keyword in REPO_NAME_KEYWORDS)


def is_playlist_file(path: str) -> bool:
    """Pilih file yang akan di-update BERDASARKAN NAMANYA.
    Fungsi ini TIDAK mengubah nama file, hanya memutuskan mau diupdate atau tidak.
    """
    lower = path.lower()
    return lower.endswith(".m3u") or lower.endswith(".m3u8")


def main():
    token = os.getenv("GITHUB_PAT") or os.getenv("GITHUB_TOKEN")

    if not token:
        raise SystemExit(
            "ERROR: Env GITHUB_PAT / GITHUB_TOKEN belum diset.\n"
            "Kalau jalan di GitHub Actions, pastikan secret MAGELIFE_GH_PAT sudah di-set."
        )

    auth = Auth.Token(token)
    gh = Github(auth=auth)

    try:
        user = gh.get_user()
    except GithubException as e:
        raise SystemExit(f"Gagal mengambil user dari token: {e}")

    print(f"Login sebagai: {user.login}")
    print(f"DRY_RUN              : {DRY_RUN}")
    if REPO_NAME_KEYWORDS:
        print(f"Filter repo keywords : {REPO_NAME_KEYWORDS}")
    else:
        print("Filter repo keywords : (SEMUA repo user akan diproses)")
    print("-" * 60)

    for repo in user.get_repos():
        if not should_process_repo(repo.name):
            continue

        print(f"\n▶ Repo: {repo.full_name}")
        default_branch = repo.default_branch or "main"
        print(f"   Default branch: {default_branch}")

        try:
            contents = repo.get_contents("", ref=default_branch)
        except GithubException as e:
            print(f"   Gagal membaca isi repo: {e}")
            continue

        files_touched = 0

        while contents:
            item = contents.pop(0)

            if item.type == "dir":
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
            print(f"   - Target file (hanya isi yang diubah, nama file tetap): {path}")

            if DRY_RUN:
                continue

            try:
                repo.update_file(
                    path,  # ⬅ NAMA FILE TETAP SAMA
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
