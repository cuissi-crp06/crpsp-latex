#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor de lançamentos CTAN para pacotes do pipeline latex-dev (CRP-SP)
Autor: Goose (automatizado)
Uso: python monitor_ctan.py [--check] [--notify]

Pacotes monitorados:
  - latex-base-dev  (núcleo; contém latex-lab)
  - latex-lab       (módulos de tagging phase-III, sec-template, toc)
  - tagpdf          (motor de geração de tags PDF estruturais)
"""

import json
import os
import re
import sys
import ssl
import urllib.request
import urllib.error
from datetime import datetime

# ──────────────────────────── Configuração ────────────────────────────

MONITORED_PACKAGES = [
    "latex-base-dev",
    "latex-lab",
    "tagpdf",
]

CTAN_JSON_BASE = "https://ctan.org/json/1.2/pkg/{pkg}"
STATE_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".ctan_state.json")
README_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")

README_MARKER_START = "<!-- CTAN-VERSION-START -->"
README_MARKER_END   = "<!-- CTAN-VERSION-END -->"

# ──────────────────────────── Proxy ────────────────────────────

def get_windows_proxy():
    """Lê configuração de proxy do Internet Explorer (WinHTTP)."""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        )
        proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
        proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
        winreg.CloseKey(key)
        if proxy_enable and proxy_server:
            if "=" in proxy_server:
                for part in proxy_server.split(";"):
                    if part.lower().startswith("https="):
                        return "http://" + part.split("=", 1)[1]
                    if part.lower().startswith("http="):
                        return "http://" + part.split("=", 1)[1]
                return None
            return f"http://{proxy_server}"
    except Exception:
        return None
    return None

PROXY_URL = os.environ.get("CTAN_PROXY") or get_windows_proxy() or ""

# ──────────────────────────── HTTP ────────────────────────────

def build_opener():
    https_handler = urllib.request.HTTPSHandler(context=ssl.create_default_context())
    handlers = [https_handler]
    if PROXY_URL and PROXY_URL.lower() not in ("none", "", "direct"):
        handlers.insert(0, urllib.request.ProxyHandler({
            "http": PROXY_URL, "https": PROXY_URL,
        }))
    return urllib.request.build_opener(*handlers)

def fetch_ctan_data(pkg_name):
    """Consulta o endpoint JSON do CTAN para o pacote informado."""
    url = CTAN_JSON_BASE.format(pkg=pkg_name)
    req = urllib.request.Request(url, headers={
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    })
    opener = build_opener()
    conn_label = f"proxy ({PROXY_URL})" if PROXY_URL else "direta"
    try:
        with opener.open(req, timeout=30) as resp:
            if resp.status != 200:
                raise RuntimeError(f"HTTP {resp.status}")
            return json.loads(resp.read().decode("utf-8")), conn_label
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Erro HTTP ao consultar CTAN [{pkg_name}]: {e.code} {e.reason}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Resposta inválida do CTAN [{pkg_name}]: {e}")
    except Exception as e:
        raise RuntimeError(f"Falha na requisição [{pkg_name}]: {e}")

# ──────────────────────────── Estado ────────────────────────────

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"packages": {}, "last_checked": None}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# ──────────────────────────── README ────────────────────────────

def update_readme(results):
    """Atualiza a seção de versão no README.md com dados de todos os pacotes."""
    if not os.path.exists(README_FILE):
        print(f"[AVISO] README.md não encontrado em {README_FILE}")
        return False

    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if README_MARKER_START not in content or README_MARKER_END not in content:
        print("[AVISO] Marcadores <!-- CTAN-VERSION-START/END --> não encontrados no README.md")
        return False

    lines = [
        f"{README_MARKER_START}",
        f"**Última verificação CTAN:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]
    for pkg, info in results.items():
        status = "⚠️ NOVA VERSÃO" if info.get("changed") else "✅"
        lines.append(
            f"- `{pkg}`: **`{info['version']}`** ({info['date']}) {status}"
        )
    lines.append(README_MARKER_END)

    new_block = "\n".join(lines)
    pattern = re.compile(
        re.escape(README_MARKER_START) + ".*?" + re.escape(README_MARKER_END),
        re.DOTALL,
    )
    new_content = pattern.sub(new_block, content)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] README.md atualizado.")
    return True

# ──────────────────────────── Fluxo principal ────────────────────────────

def main():
    print(f"[{datetime.now().isoformat()}] Monitor CTAN iniciado")
    print(f"Pacotes: {', '.join(MONITORED_PACKAGES)}")
    print(f"Proxy:   {PROXY_URL or '(nenhum)'}")
    print("-" * 50)

    state = load_state()
    if "packages" not in state:
        # Migração de estado antigo (monitorava apenas latex-base-dev)
        old_version = state.get("last_known_version")
        old_date    = state.get("last_known_date")
        state = {"packages": {}, "last_checked": state.get("last_checked")}
        if old_version:
            state["packages"]["latex-base-dev"] = {
                "last_known_version": old_version,
                "last_known_date": old_date,
                "history": [],
            }
            print("[INFO] Estado antigo migrado para formato multi-pacote.")

    results = {}
    any_new  = False

    for pkg in MONITORED_PACKAGES:
        print(f"\n[{pkg}]")
        try:
            data, conn_label = fetch_ctan_data(pkg)
            print(f"  Conectado via: {conn_label}")
        except RuntimeError as e:
            print(f"  [ERRO] {e}")
            results[pkg] = {"version": "erro", "date": "-", "changed": False}
            continue

        version = data.get("version", {}).get("number")
        date    = data.get("version", {}).get("date", "")

        if not version:
            print(f"  [ERRO] Versão não encontrada na resposta CTAN.")
            results[pkg] = {"version": "erro", "date": "-", "changed": False}
            continue

        pkg_state = state["packages"].get(pkg, {
            "last_known_version": None,
            "last_known_date": None,
            "history": [],
        })

        current = {
            "version": version,
            "date": date,
            "checked_at": datetime.now().isoformat(),
        }

        pkg_state["history"] = (pkg_state.get("history", []) + [current])[-20:]
        last = pkg_state.get("last_known_version")

        changed = (last is not None) and (last != version)

        if last == version:
            print(f"  OK — versão atual: {version} ({date})")
        elif last is None:
            print(f"  INFO — primeira execução. Versão registrada: {version} ({date})")
        else:
            print(f"  *** NOVA VERSÃO: {last} → {version} ({date}) ***")
            any_new = True

        pkg_state["last_known_version"] = version
        pkg_state["last_known_date"]    = date
        state["packages"][pkg]          = pkg_state

        results[pkg] = {"version": version, "date": date, "changed": changed}

    state["last_checked"] = datetime.now().isoformat()
    save_state(state)

    update_readme(results)

    if any_new:
        print("\n" + "=" * 50)
        print(" ATENÇÃO: Novas versões detectadas.")
        print(" Revisar workarounds antes de modificar o .sty.")
        print(" Ver references/workarounds.md na skill latex-dev.")
        print("=" * 50)

    print(f"\n[OK] Verificação concluída.")

if __name__ == "__main__":
    main()
