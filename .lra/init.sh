#!/bin/bash
# Long-Running Agent - Environment Initialization Script
# Project: CSES Analyses - System Design Content Improvement

echo "Starting Long-Running Agent Environment..."

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

# Check Jekyll is available
if command -v bundle &> /dev/null; then
    echo "Ruby/Bundler detected"
else
    echo "Warning: Ruby/Bundler not found - Jekyll preview won't work"
fi

# Start Jekyll development server (optional - for previewing changes)
# Uncomment to auto-start:
# bundle exec jekyll serve --livereload &

echo ""
echo "=== LRA Status ==="
echo "Feature list: .lra/feature-list.json"
echo "Progress log: .lra/progress.txt"
echo ""
echo "To check status: cat .lra/feature-list.json | jq '.features[] | select(.status==\"pending\") | {id, description, priority}'"
echo "To preview site: bundle exec jekyll serve --livereload"
echo ""
echo "Environment ready!"
