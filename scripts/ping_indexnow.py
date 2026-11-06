#!/usr/bin/env python3
"""
Techdim IndexNow Ping Automator
Envia notificações instantâneas para a API do IndexNow (Bing, Copilot, Yandex)
para que as páginas e o manifesto para IAs sejam rastreados e indexados em minutos.
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"

INDEXNOW_KEY = "a7e1f48b9c2d3e4f5a6b7c8d9e0f1a2b"
HOST = "techdimbr.github.io"
BASE_URL = f"https://{HOST}/daily-engineering-lab"

URLS_TO_INDEX = [
    f"{BASE_URL}/",
    f"{BASE_URL}/llms.txt",
    f"{BASE_URL}/sitemap.xml",
    f"{BASE_URL}/robots.txt",
    f"{BASE_URL}/.well-known/ai-plugin.json"
]

def ensure_key_file():
    key_file = DOCS_DIR / f"{INDEXNOW_KEY}.txt"
    with open(key_file, "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")
    print(f"🔑 Arquivo de chave IndexNow gerado: {key_file.name}")
    return key_file

def ping_indexnow():
    endpoint = "https://api.indexnow.org/indexnow"
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": URLS_TO_INDEX
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=req_data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

    print(f"📡 Enviando ping de indexação instantânea para {endpoint}...")
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.getcode()
            print(f"✅ Sucesso IndexNow! Status HTTP: {status} (URLs submetidas para indexação imediata)")
            return True
    except urllib.error.HTTPError as e:
        print(f"ℹ️ Resposta HTTP IndexNow ({e.code}): {e.read().decode('utf-8', errors='ignore')}")
        # 200 or 202 are success, even 422 if host is pending key resolution
        return e.code in [200, 202]
    except Exception as e:
        print(f"⚠️ Erro de conexão com IndexNow: {e}")
        return False

def main():
    ensure_key_file()
    print("🚀 Disparando notificação aos motores de busca...")
    ping_indexnow()

if __name__ == "__main__":
    main()
