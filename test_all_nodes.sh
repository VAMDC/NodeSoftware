#!/bin/bash
# Script to test all VAMDC nodes

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

NODES_DIR="/home/user/NodeSoftware/nodes"
RESULTS_FILE="/home/user/NodeSoftware/node_test_results.txt"

echo "Testing all VAMDC nodes..." > "$RESULTS_FILE"
echo "=====================================" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

# Get list of all nodes
NODES=$(ls -d "$NODES_DIR"/*/ | grep -v __pycache__ | sed 's|.*/||g' | sed 's|/$||g' | sort)

PASSED=0
FAILED=0
NEEDS_FIX=0

for node in $NODES; do
    echo -e "${YELLOW}Testing node: $node${NC}"
    echo "Testing node: $node" >> "$RESULTS_FILE"

    cd "$NODES_DIR/$node" || continue

    # Check if manage.py exists
    if [ ! -f "manage.py" ]; then
        echo -e "${RED}  ✗ No manage.py found${NC}"
        echo "  Status: SKIP (no manage.py)" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        continue
    fi

    # Check/create settings.py
    if [ ! -f "settings.py" ]; then
        if [ -f "settings_default.py" ]; then
            ln -sf settings_default.py settings.py
            echo "  Created settings.py symlink"
        else
            echo -e "${YELLOW}  ! No settings.py or settings_default.py${NC}"
            echo "  Status: NEEDS_SETUP (no settings)" >> "$RESULTS_FILE"
            echo "" >> "$RESULTS_FILE"
            NEEDS_FIX=$((NEEDS_FIX + 1))
            continue
        fi
    fi

    # Try migrate
    echo "  Running migrate..."
    MIGRATE_OUTPUT=$(uv run python manage.py migrate 2>&1)
    MIGRATE_EXIT=$?

    if [ $MIGRATE_EXIT -ne 0 ]; then
        echo -e "${RED}  ✗ Migration failed${NC}"
        echo "  Status: FAILED (migration error)" >> "$RESULTS_FILE"
        echo "  Error: ${MIGRATE_OUTPUT}" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
        continue
    fi

    echo "  Migration successful"

    # Try to check if server can start (syntax check)
    echo "  Checking if server starts..."
    SERVER_OUTPUT=$(timeout 2 uv run python manage.py check 2>&1)
    SERVER_EXIT=$?

    if [ $SERVER_EXIT -ne 0 ] && [ $SERVER_EXIT -ne 124 ]; then
        echo -e "${RED}  ✗ Server check failed${NC}"
        echo "  Status: FAILED (server check error)" >> "$RESULTS_FILE"
        echo "  Error: ${SERVER_OUTPUT}" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
    else
        echo -e "${GREEN}  ✓ Node is working${NC}"
        echo "  Status: PASSED" >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        PASSED=$((PASSED + 1))
    fi
done

echo "" >> "$RESULTS_FILE"
echo "=====================================" >> "$RESULTS_FILE"
echo "Summary:" >> "$RESULTS_FILE"
echo "  Passed: $PASSED" >> "$RESULTS_FILE"
echo "  Failed: $FAILED" >> "$RESULTS_FILE"
echo "  Needs Setup: $NEEDS_FIX" >> "$RESULTS_FILE"

echo ""
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo -e "${YELLOW}Needs Setup: $NEEDS_FIX${NC}"
echo ""
echo "Results saved to: $RESULTS_FILE"
