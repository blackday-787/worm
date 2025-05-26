#!/bin/bash
# This script stages all changes, commits them, and pushes to the current branch.

# Use the first argument as the commit message or default to "auto commit"
MESSAGE=${1:-"auto commit"}

git add .
git commit -m "$MESSAGE"
git push
