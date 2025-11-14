#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script untuk meng-update semua file .m3u / .m3u8
di SEMUA repository GitHub milik user tertentu.

- Target user : maywho5454
- Auth        : Personal Access Token melalui env var GITHUB_TOKEN

Cara pakai singkat:
1. pip install PyGithub
2. export/set GITHUB_TOKEN=TOKEN_KAMU
3. python update_all_playlists.py
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


# ==============================
# FUNGSI BANTUAN
# ==============================

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


# ==============================
# MAIN
# ==============================

def main():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
