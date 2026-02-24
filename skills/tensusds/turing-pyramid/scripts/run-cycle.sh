#!/bin/bash
# Turing Pyramid — Main Cycle Runner
# Called on each heartbeat to evaluate and act on needs

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/assets/needs-config.json"
STATE_FILE="$SKILL_DIR/assets/needs-state.json"
SCRIPTS_DIR="$SKILL_DIR/scripts"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"

# Check initialization
if [[ ! -f "$STATE_FILE" ]]; then
    echo "❌ Turing Pyramid not initialized. Run: $SCRIPTS_DIR/init.sh"
    exit 1
fi

NOW=$(date +%s)
NOW_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TODAY=$(date +%Y-%m-%d)

# Bootstrap mode: process ALL needs
if [[ "$1" == "--bootstrap" ]]; then
    MAX_ACTIONS=10
    echo "🚀 BOOTSTRAP MODE — processing all needs"
else
    MAX_ACTIONS=$(jq -r '.settings.max_actions_per_cycle // 3' "$CONFIG_FILE")
fi

# Calculate tension for all needs
declare -A TENSIONS
declare -A SATISFACTIONS
declare -A DEPRIVATIONS

calculate_tensions() {
    local needs=$(jq -r '.needs | keys[]' "$CONFIG_FILE")
    
    for need in $needs; do
        local importance=$(jq -r ".needs.\"$need\".importance" "$CONFIG_FILE")
        local decay_rate=$(jq -r ".needs.\"$need\".decay_rate_hours" "$CONFIG_FILE")
        local last_sat=$(jq -r ".needs.\"$need\".last_satisfied" "$STATE_FILE")
        
        # Calculate time-based satisfaction
        local time_satisfaction=3
        if [[ "$last_sat" != "null" && -n "$last_sat" ]]; then
            local last_sat_epoch=$(date -d "$last_sat" +%s 2>/dev/null || echo $NOW)
            local hours_since=$(( (NOW - last_sat_epoch) / 3600 ))
            local decay_steps=$(( hours_since / decay_rate ))
            time_satisfaction=$(( 3 - decay_steps ))
            [[ $time_satisfaction -lt 0 ]] && time_satisfaction=0
        else
            time_satisfaction=0  # Never satisfied = critical
        fi
        
        # Run event scan if exists (can only worsen)
        local scan_script="$SCRIPTS_DIR/scan_${need}.sh"
        local event_satisfaction=""
        if [[ -x "$scan_script" ]]; then
            event_satisfaction=$("$scan_script" 2>/dev/null)
        fi
        
        # Merge: take worst
        local satisfaction=$time_satisfaction
        if [[ -n "$event_satisfaction" && "$event_satisfaction" =~ ^[0-3]$ ]]; then
            if [[ $event_satisfaction -lt $satisfaction ]]; then
                satisfaction=$event_satisfaction
            fi
        fi
        
        local deprivation=$(( 3 - satisfaction ))
        local tension=$(( importance * deprivation ))
        
        TENSIONS[$need]=$tension
        SATISFACTIONS[$need]=$satisfaction
        DEPRIVATIONS[$need]=$deprivation
    done
}

# Get top N needs by tension
get_top_needs() {
    local n=$1
    for need in "${!TENSIONS[@]}"; do
        echo "${TENSIONS[$need]} $need"
    done | sort -rn | head -n "$n" | awk '{print $2}'
}

# Probability-based action decision
# Returns 0 (true) if should take action, 1 (false) for non-action
# v1.5.0: Added tension bonus — higher importance needs are more "impatient"
roll_action() {
    local sat=$1
    local tension=$2
    
    # Base chance by satisfaction level
    local base_chance
    case $sat in
        3) base_chance=5 ;;   # 5% base
        2) base_chance=20 ;;  # 20% base
        1) base_chance=75 ;;  # 75% base
        0) base_chance=100 ;; # 100% base
        *) base_chance=0 ;;
    esac
    
    # Tension bonus: scales 0-50% based on tension
    # Global max_tension = max_importance(10) × max_deprivation(3) = 30
    # This preserves importance weighting: higher importance = bigger bonus at same sat
    local max_tension=30
    local max_bonus=50
    local bonus=$(( (tension * max_bonus) / max_tension ))
    
    # Final chance (capped at 100)
    local final_chance=$((base_chance + bonus))
    [[ $final_chance -gt 100 ]] && final_chance=100
    
    local roll=$((RANDOM % 100))
    [[ $roll -lt $final_chance ]]
}

# Roll for impact level based on satisfaction
# Uses impact_matrix from config (default or per-need)
roll_impact() {
    local need=$1
    local sat=$2
    local roll=$((RANDOM % 100))
    
    # Get impact matrix (per-need or default)
    local matrix_key="sat_$sat"
    local p1 p2 p3
    
    # Try per-need matrix first, fall back to default
    p1=$(jq -r ".needs.\"$need\".impact_matrix.\"$matrix_key\".\"1\" // .impact_matrix_default.\"$matrix_key\".\"1\" // 70" "$CONFIG_FILE")
    p2=$(jq -r ".needs.\"$need\".impact_matrix.\"$matrix_key\".\"2\" // .impact_matrix_default.\"$matrix_key\".\"2\" // 25" "$CONFIG_FILE")
    p3=$(jq -r ".needs.\"$need\".impact_matrix.\"$matrix_key\".\"3\" // .impact_matrix_default.\"$matrix_key\".\"3\" // 5" "$CONFIG_FILE")
    
    # Roll: 0-p1 = impact1, p1-(p1+p2) = impact2, rest = impact3
    if [[ $roll -lt $p1 ]]; then
        echo 1
    elif [[ $roll -lt $((p1 + p2)) ]]; then
        echo 2
    else
        echo 3
    fi
}

# Get actions filtered by impact level (simple list)
get_actions_by_impact() {
    local need=$1
    local impact=$2
    
    jq -r ".needs.\"$need\".actions[] | select(.impact == $impact) | .name" "$CONFIG_FILE"
}

# Weighted random selection of action by impact
select_weighted_action() {
    local need=$1
    local impact=$2
    
    # Get actions with weights for this impact
    local actions_json=$(jq -c "[.needs.\"$need\".actions[] | select(.impact == $impact)]" "$CONFIG_FILE")
    local count=$(echo "$actions_json" | jq 'length')
    
    if [[ $count -eq 0 ]]; then
        echo ""
        return
    fi
    
    if [[ $count -eq 1 ]]; then
        echo "$actions_json" | jq -r '.[0].name'
        return
    fi
    
    # Calculate total weight
    local total_weight=$(echo "$actions_json" | jq '[.[].weight // 100] | add')
    local roll=$((RANDOM % total_weight))
    
    # Select based on cumulative weights
    local cumulative=0
    local selected=""
    
    for i in $(seq 0 $((count - 1))); do
        local weight=$(echo "$actions_json" | jq -r ".[$i].weight // 100")
        local name=$(echo "$actions_json" | jq -r ".[$i].name")
        cumulative=$((cumulative + weight))
        
        if [[ $roll -lt $cumulative ]]; then
            selected="$name"
            break
        fi
    done
    
    echo "$selected"
}

# Log non-action (noticed but deferred)
log_noticed() {
    local need=$1
    local sat=$2
    local tension=$3
    local timestamp=$(date +"%H:%M")
    
    # Append to today's memory with timestamp
    if [[ -d "$MEMORY_DIR" ]]; then
        echo "- [$timestamp] ○ noticed: $need (sat=$sat, tension=$tension) — non-action" >> "$MEMORY_DIR/$TODAY.md"
    fi
}

# Log action taken
log_action() {
    local need=$1
    local sat=$2
    local tension=$3
    local timestamp=$(date +"%H:%M")
    
    # Append to today's memory with timestamp
    if [[ -d "$MEMORY_DIR" ]]; then
        echo "- [$timestamp] ▶ action: $need (sat=$sat, tension=$tension) — requires action" >> "$MEMORY_DIR/$TODAY.md"
    fi
}

# Main execution
echo "🔺 Turing Pyramid — Cycle at $(date)"
echo "======================================"

calculate_tensions

# Check if all satisfied
all_satisfied=true
for need in "${!TENSIONS[@]}"; do
    if [[ ${TENSIONS[$need]} -gt 0 ]]; then
        all_satisfied=false
        break
    fi
done

if $all_satisfied; then
    echo "✅ All needs satisfied. HEARTBEAT_OK"
    exit 0
fi

# Show current tensions
echo ""
echo "Current tensions:"
for need in "${!TENSIONS[@]}"; do
    if [[ ${TENSIONS[$need]} -gt 0 ]]; then
        echo "  $need: tension=${TENSIONS[$need]} (sat=${SATISFACTIONS[$need]}, dep=${DEPRIVATIONS[$need]})"
    fi
done | sort -t'=' -k2 -rn

# Select top needs
echo ""
echo "Selecting top $MAX_ACTIONS needs..."
top_needs=$(get_top_needs $MAX_ACTIONS)

echo ""
echo "📋 Decisions:"

action_count=0
noticed_count=0

for need in $top_needs; do
    if [[ ${TENSIONS[$need]} -gt 0 ]]; then
        sat=${SATISFACTIONS[$need]}
        tension=${TENSIONS[$need]}
        
        if roll_action $sat $tension; then
            # ACTION - roll for impact level, then weighted action selection
            ((action_count++))
            impact=$(roll_impact "$need" "$sat")
            
            # Select specific action using weights
            selected_action=$(select_weighted_action "$need" "$impact")
            
            echo ""
            echo "▶ ACTION: $need (tension=$tension, sat=$sat)"
            echo "  Impact $impact rolled → selected:"
            
            if [[ -n "$selected_action" ]]; then
                echo "    ★ $selected_action"
            else
                # Fallback: show all actions if no weighted selection
                echo "  (no impact-$impact actions, showing all):"
                jq -r ".needs.\"$need\".actions[] | \"    • \" + .name + \" (impact \" + (.impact|tostring) + \")\"" "$CONFIG_FILE"
            fi
            
            echo "  Then: mark-satisfied.sh $need $impact"
            
            # Log to memory with selected action
            log_action "$need" "$sat" "$tension"
        else
            # NON-ACTION - noticed but deferred
            ((noticed_count++))
            echo ""
            echo "○ NOTICED: $need (tension=$tension, sat=$sat) — deferred"
            log_noticed "$need" "$sat" "$tension"
        fi
    fi
done

echo ""
echo "======================================"
echo "Summary: $action_count action(s), $noticed_count noticed"

if [[ $action_count -gt 0 ]]; then
    echo ""
    echo "After completing actions, update state with:"
    echo "  ./scripts/mark-satisfied.sh <need> [impact]"
fi
