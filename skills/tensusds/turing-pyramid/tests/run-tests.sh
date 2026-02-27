#!/bin/bash
# run-tests.sh — Test runner for Turing Pyramid
# Usage: ./run-tests.sh [unit|integration|regression|all]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

run_test() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .sh)
    
    chmod +x "$test_file" 2>/dev/null
    
    printf "  %-40s " "$test_name"
    
    if output=$(bash "$test_file" 2>&1); then
        echo -e "${GREEN}PASS${NC}"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        [[ -n "$output" ]] && echo "    $output"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

run_suite() {
    local suite="$1"
    local suite_dir="$SCRIPT_DIR/$suite"
    
    if [[ ! -d "$suite_dir" ]]; then
        echo -e "${YELLOW}Suite '$suite' not found${NC}"
        return
    fi
    
    local found=0
    for test_file in "$suite_dir"/test_*.sh; do
        [[ -f "$test_file" ]] || continue
        found=1
        run_test "$test_file"
    done
    
    [[ $found -eq 0 ]] && echo -e "${YELLOW}  (no tests)${NC}"
}

echo "========================================"
echo "🔺 Turing Pyramid Test Suite"
echo "========================================"
echo ""

case "${1:-all}" in
    unit)
        echo "📦 Unit Tests"
        run_suite "unit"
        ;;
    integration)
        echo "🔗 Integration Tests"
        run_suite "integration"
        ;;
    regression)
        echo "🐛 Regression Tests"
        run_suite "regression"
        ;;
    all)
        echo "📦 Unit Tests"
        run_suite "unit"
        echo ""
        echo "🔗 Integration Tests"
        run_suite "integration"
        echo ""
        echo "🐛 Regression Tests"
        run_suite "regression"
        ;;
    *)
        echo "Usage: $0 [unit|integration|regression|all]"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo -e "Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}"
echo "========================================"

[[ $FAILED -gt 0 ]] && exit 1
exit 0
