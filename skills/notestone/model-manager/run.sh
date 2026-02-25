#!/bin/bash
# Wrapper for Model Manager Skill
# Usage: ./run.sh <list|enable> [target]

python3 skills/model-manager/manage_models.py "$@"
