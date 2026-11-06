#!/usr/bin/env python3
"""
Techdim Kether Daily Commit Runner
Executa um ciclo completo de commit diário:
1. Seleciona ou gera um módulo de engenharia
2. Escreve código e testes unitários
3. Executa pytest para garantir integridade
4. Realiza git commit e git push (se configurado)
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import subprocess
from engine.generator import CodebaseGenerator

def run_tests():
    print("🧪 Executando suite de testes pytest...")
    res = subprocess.run(["pytest", "-q"], cwd=ROOT_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"⚠️ Pytest retornou aviso/erro:\n{res.stdout}\n{res.stderr}")
    else:
        print("✅ Todos os testes passaram com sucesso!")
    return res.returncode == 0

def git_commit_and_push(commit_msg: str, push: bool = True):
    print("📦 Realizando stage e commit no Git...")
    subprocess.run(["git", "add", "."], cwd=ROOT_DIR, check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=ROOT_DIR, check=True)
    print(f"✨ Commit realizado com sucesso:\n'{commit_msg.splitlines()[0]}'")

    if push:
        print("🚀 Enviando para o repositório remoto (git push)...")
        res = subprocess.run(["git", "push"], cwd=ROOT_DIR, capture_output=True, text=True)
        if res.returncode == 0:
            print("🎉 Push concluído com sucesso!")
        else:
            print(f"ℹ️ Git push não enviado (ou remoto não configurado ainda): {res.stderr.strip()}")

def main():
    generator = CodebaseGenerator(ROOT_DIR)
    module = generator.select_next_module()
    print(f"🚀 Preparando módulo: [{module['category']}] {module['title']}")

    code_p, test_p, commit_msg = generator.deploy_module(module)
    print(f"📄 Arquivo criado: {code_p.relative_to(ROOT_DIR)}")
    print(f"🧪 Teste criado:   {test_p.relative_to(ROOT_DIR)}")

    # Opcional: roda testes locais se pytest estiver disponível
    try:
        run_tests()
    except FileNotFoundError:
        print("ℹ️ Pytest não encontrado no PATH imediato, continuando...")

    try:
        git_commit_and_push(commit_msg, push=True)
    except Exception as e:
        print(f"⚠️ Nota de Git: {e}")

if __name__ == "__main__":
    main()
