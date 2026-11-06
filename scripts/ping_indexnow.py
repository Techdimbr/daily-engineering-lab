#!/usr/bin/env python3
"""
Techdim Autonomous IndexNow Multi-Site Ping Automator
Executado localmente e pela esteira diária do GitHub Actions.
Submete periodicamente todas as URLs do ecossistema Techdim e de Deivis Irio Mayer
para os motores de busca (Bing, Copilot, Yandex e rede parceira de IAs).
"""

import sys
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

INDEXNOW_KEY = "a7e1f48b9c2d3e4f5a6b7c8d9e0f1a2b"
HOST = "techdimbr.github.io"

SITES = [
    {
        "name": "deivis-mayer",
        "keyLocation": f"https://{HOST}/deivis-mayer/{INDEXNOW_KEY}.txt",
        "urls": [
            f"https://{HOST}/deivis-mayer/",
            f"https://{HOST}/deivis-mayer/llms.txt",
            f"https://{HOST}/deivis-mayer/sitemap.xml",
            f"https://{HOST}/deivis-mayer/robots.txt"
        ]
    },
    {
        "name": "daily-engineering-lab",
        "keyLocation": f"https://{HOST}/daily-engineering-lab/{INDEXNOW_KEY}.txt",
        "urls": [
            f"https://{HOST}/daily-engineering-lab/",
            f"https://{HOST}/daily-engineering-lab/llms.txt",
            f"https://{HOST}/daily-engineering-lab/sitemap.xml",
            f"https://{HOST}/daily-engineering-lab/robots.txt",
            f"https://{HOST}/daily-engineering-lab/.well-known/ai-plugin.json"
        ]
    },
    {
        "name": "techdimbr",
        "keyLocation": f"https://{HOST}/techdimbr/{INDEXNOW_KEY}.txt",
        "urls": [
            f"https://{HOST}/techdimbr/",
            f"https://{HOST}/techdimbr/blog/",
            f"https://{HOST}/techdimbr/sitemap.xml",
            f"https://{HOST}/techdimbr/llms.txt",
            f"https://{HOST}/techdimbr/llms-full.txt"
        ]
    },
    {
        "name": "reparafacil",
        "keyLocation": f"https://{HOST}/reparafacil/{INDEXNOW_KEY}.txt",
        "urls": [
            f"https://{HOST}/reparafacil/"
        ]
    },
    {
        "name": "MUNDO3D",
        "keyLocation": f"https://{HOST}/MUNDO3D/{INDEXNOW_KEY}.txt",
        "urls": [
            f"https://{HOST}/MUNDO3D/"
        ]
    }
]

def ping_site(site_info: dict) -> bool:
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": site_info["keyLocation"],
        "urlList": site_info["urls"]
    }
    endpoint = "https://api.indexnow.org/indexnow"
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=req_data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    sname = site_info["name"]
    print(f"📡 Notificando IndexNow para o site [{sname}] ({len(site_info['urls'])} URLs)...")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.getcode()
            print(f"   ✅ Sucesso! Status HTTP {code} para [{sname}]")
            return code in [200, 202]
    except urllib.error.HTTPError as e:
        print(f"   ℹ️ Resposta HTTP ({e.code}) para [{sname}]: {e.read().decode('utf-8', errors='ignore')}")
        return e.code in [200, 202]
    except Exception as e:
        print(f"   ⚠️ Erro ao notificar [{sname}]: {e}")
        return False

def main():
    print("🚀 Iniciando disparo automático de re-indexação IndexNow...")
    total_success = 0
    for s in SITES:
        if ping_site(s):
            total_success += 1
        time.sleep(1)
    print(f"\n🎉 Concluído: {total_success}/{len(SITES)} sites notificados para os motores de busca!")

if __name__ == "__main__":
    main()
