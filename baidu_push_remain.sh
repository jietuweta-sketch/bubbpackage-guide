#!/bin/bash
# 兼容旧入口：统一调用不含明文凭据的完整推送脚本。
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "${SCRIPT_DIR}/baidu_push_guide.sh"
