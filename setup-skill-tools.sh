#!/bin/sh
set -eu

cd "$(dirname "$0")"
command -v uv >/dev/null 2>&1 || {
    printf '%s\n' 'SkillSpector를 설치하려면 uv가 필요합니다.' >&2
    exit 1
}

export UV_CACHE_DIR="${UV_CACHE_DIR:-$PWD/.local/uv-cache}"
export UV_TOOL_DIR="$PWD/.local/skill-tools"
export UV_TOOL_BIN_DIR="$PWD/.local/skill-bin"

uv tool install --no-python-downloads --python "${JOYTI_SKILL_PYTHON:-3.13}" \
    'git+https://github.com/NVIDIA/SkillSpector.git@02894ec5b8a0a70637df5a6b45763de92940cedd'
"$UV_TOOL_BIN_DIR/skillspector" --version
