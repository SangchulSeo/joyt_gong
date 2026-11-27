#!/bin/sh
set -eu

cd "$(dirname "$0")"
: "${JOYTI_TOOL_PYTHON:=3.13}"
npm install --prefix .local/social-mcp-node --cache "${JOYTI_NPM_CACHE:-$PWD/.local/npm-cache}" \
    --no-audit --no-fund --ignore-scripts --save-exact \
    @upload-post/mcp@0.28.0 @isnow890/naver-search-mcp@1.1.1

export UV_CACHE_DIR="${UV_CACHE_DIR:-$PWD/.local/uv-cache}"
export UV_TOOL_DIR="$PWD/.local/skill-tools"
export UV_TOOL_BIN_DIR="$PWD/.local/skill-bin"
uv tool install --no-python-downloads --python "$JOYTI_TOOL_PYTHON" --with 'mcp==1.30.0' \
    'git+https://github.com/William-Gao/instagram-mcp.git@d8e1adf7ae1cb071c490d0fca379386d020b6cd0'
uv tool install --no-python-downloads --python "$JOYTI_TOOL_PYTHON" \
    'git+https://github.com/pauling-ai/youtube-mcp-server.git@611f98782774d2468abafd69c4d30cfee30f00ba'

python3 - <<'PY'
import json
from pathlib import Path
root = Path.cwd()
source = Path("config/codex-social-mcp.example.toml").read_text(encoding="utf-8")
lines = []
for line in source.splitlines():
    if line.startswith('command = ".local/'):
        executable = line.removeprefix('command = "').removesuffix('"')
        line = 'command = ' + json.dumps(str(root / executable), ensure_ascii=False)
    lines.append(line)
output = Path(".local/codex-social-mcp.toml")
if output.exists():
    print(f"기존 설정 유지: {output}")
else:
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"생성: {output}")
PY
