#!/bin/bash
# Long-Running Agent - Environment Initialization Script
# Project: CSES Problem Set Analyses
# This script prepares the environment for analysis work

echo "Starting Long-Running Agent Environment..."

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

# Display current status
echo ""
echo "=== Project Status ==="
echo "Categories found:"
for dir in */; do
    if [ -d "$dir" ]; then
        count=$(ls "$dir" | grep -c "analysis.md" 2>/dev/null || echo "0")
        echo "  - ${dir%/}: $count analyses"
    fi
done

echo ""
echo "=== LRA Status ==="
if [ -f ".lra/feature-list.json" ]; then
    pending=$(grep -c '"status": "pending"' .lra/feature-list.json 2>/dev/null || echo "0")
    completed=$(grep -c '"status": "completed"' .lra/feature-list.json 2>/dev/null || echo "0")
    echo "  Features pending: $pending"
    echo "  Features completed: $completed"
else
    echo "  Feature list not found!"
fi

echo ""
echo "=== Git Status ==="
git status --short

echo ""
echo "Environment ready!"
echo "Run 'cat .lra/progress.txt' to see session history"
echo "Run 'cat .lra/feature-list.json | jq' to see feature list"
