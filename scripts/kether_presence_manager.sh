#!/usr/bin/env bash
# ==============================================================================
# Techdim Kether GitHub Presence & Skill Showcase Engine
# Gestor de Visibilidade e Habilidade Técnica para Contratantes e Recrutadores
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}  🚀 TECHDIM GITHUB PRESENCE & SKILL SHOWCASE ENGINE (KETHER_1)${NC}"
echo -e "${BLUE}======================================================================${NC}"

usage() {
    echo -e "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  setup        - Cria e publica o repositório público no GitHub via gh CLI"
    echo "  backfill     - Preenche o histórico de 365 dias retroativamente com código real"
    echo "  daily        - Executa 1 ciclo de commit diário com novo algoritmo e testes"
    echo "  push         - Envia todas as alterações locais para a branch main do GitHub"
    echo "  audit        - Audita status de e-mail, commits e repositório no GitHub"
    echo ""
}

cmd_audit() {
    echo -e "\n${CYAN}🔍 [1/3] Auditoria de Identidade Git Local:${NC}"
    local user_name user_email
    user_name="$(git -C "$PROJECT_DIR" config user.name || echo 'NÃO CONFIGURADO')"
    user_email="$(git -C "$PROJECT_DIR" config user.email || echo 'NÃO CONFIGURADO')"
    echo "   Nome:   $user_name"
    echo "   E-mail: $user_email"

    echo -e "\n${CYAN}🔍 [2/3] Status da Autenticação GitHub (gh CLI):${NC}"
    gh auth status || true

    echo -e "\n${CYAN}🔍 [3/3] Total de Commits Locais na Branch Main:${NC}"
    local count
    count="$(git -C "$PROJECT_DIR" rev-list --count HEAD 2>/dev/null || echo 0)"
    echo "   Commits registrados: $count"
}

cmd_setup() {
    echo -e "\n${YELLOW}⚙️ Criando e publicando repositório 'daily-engineering-lab' no GitHub...${NC}"
    cd "$PROJECT_DIR"

    git add .
    git commit -m "chore: setup daily engineering lab with automated workflows" 2>/dev/null || true

    if git remote get-url origin >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Remoto origin já configurado: $(git remote get-url origin)${NC}"
        git push -u origin main
    else
        echo -e "${CYAN}🚀 Criando repositório público Techdimbr/daily-engineering-lab...${NC}"
        gh repo create Techdimbr/daily-engineering-lab --public --source=. --remote=origin --push --description "Engenharia de Software de Alta Resiliência, Algoritmos Avançados, Padrões GoF e Microsserviços com Testes Automatizados Diários."
        echo -e "${GREEN}🎉 Repositório publicado com sucesso no GitHub!${NC}"
    fi

    echo -e "\n${YELLOW}💡 GitHub Actions ativado:${NC} O fluxo rodará diariamente nos horários programados."
}

cmd_backfill() {
    echo -e "\n${YELLOW}🔥 Executando Preenchimento Histórico Orgânico (Últimos 365 dias)...${NC}"
    cd "$PROJECT_DIR"
    python3 "${SCRIPT_DIR}/backfill_history.py" --days 365 --weekday-prob 0.88 --weekend-prob 0.45
    echo -e "\n${GREEN}✅ Backfill concluído localmente!${NC}"
    echo -e "${CYAN}👉 Para sincronizar e atualizar o heatmap do GitHub agora mesmo, execute:${NC}"
    echo "   $0 push"
}

cmd_daily() {
    echo -e "\n${CYAN}🚀 Executando commit diário de módulo técnico...${NC}"
    cd "$PROJECT_DIR"
    python3 "${SCRIPT_DIR}/daily_commit.py"
}

cmd_push() {
    echo -e "\n${CYAN}📤 Enviando commits para o GitHub...${NC}"
    cd "$PROJECT_DIR"
    git push -u origin main
    echo -e "\n${GREEN}🎉 Sincronização concluída! Verifique seu gráfico em: https://github.com/Techdimbr${NC}"
}

ACTION="${1:-}"

case "$ACTION" in
    setup)
        cmd_setup
        ;;
    backfill)
        cmd_backfill
        ;;
    daily)
        cmd_daily
        ;;
    push)
        cmd_push
        ;;
    audit)
        cmd_audit
        ;;
    *)
        usage
        ;;
esac
