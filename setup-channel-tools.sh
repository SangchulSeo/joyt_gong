#!/bin/sh
set -eu

cd "$(dirname "$0")"
: "${JOYTI_TOOL_PYTHON:=3.13}"
npm_cache="${JOYTI_NPM_CACHE:-$PWD/.local/npm-cache}"
npm install --prefix .local/n8n-runtime --cache "$npm_cache" --no-audit --no-fund --save-exact n8n@2.49.7 n8n-mcp@2.104.0
npm install --prefix .local/taisly-runtime --cache "$npm_cache" --no-audit --no-fund --save-exact @taisly/agent@0.2.10
export UV_CACHE_DIR="${UV_CACHE_DIR:-$PWD/.local/uv-cache}"
export UV_TOOL_DIR="$PWD/.local/skill-tools"
export UV_TOOL_BIN_DIR="$PWD/.local/skill-bin"
uv tool install --no-python-downloads --python "$JOYTI_TOOL_PYTHON" \
    'git+https://github.com/Johnhyeon/naver-blog-mcp.git@c3d71df47073f78061a066222e799ebee7001466'
.local/n8n-runtime/node_modules/.bin/n8n --version
.local/taisly-runtime/node_modules/.bin/taisly help
