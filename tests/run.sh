#!/bin/bash
# 双向验证：正例必须每条都报，反例必须 0 命中（误报是安全工具的头号杀手）
set -uo pipefail
cd "$(dirname "$0")/.."
PASS=0; FAIL=0
ok(){ echo "  ✅ $1"; PASS=$((PASS+1)); }
bad(){ echo "  ❌ $1"; FAIL=$((FAIL+1)); }

RULES=(
  LR-SH-23
  LR-SZ-26
  LR-SZ-29
  LR-SZ-73
  LR-SZ-75
  LR-SZ-79
  LR-SZ-80
)

echo ""; echo "  $(node -p "require('./package.json').name") · 双向验证"
echo "  ────────────────────────────────────────────────"

echo ""; echo "  【正例】demo-project（7 条判据必须逐条报出）"
J=$(node bin/cli.mjs --root tests/fixtures/fail/demo-project --json 2>&1)
N=$(echo "$J" | python3 -c "import json,sys; print(json.load(sys.stdin)['stats']['findings'])" 2>/dev/null || echo 0)
[ "${N:-0}" -eq 7 ] && ok "命中 7 条（每条判据各 1 处）" || bad "命中了 ${N} 条，预期 7 条"

for rid in "${RULES[@]}"; do
  c=$(echo "$J" | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    print(len([f for f in d.get('findings',[]) if f.get('ruleId')=='$rid']))
except Exception: print(0)" 2>/dev/null)
  [ "${c:-0}" -gt 0 ] && ok "$rid 报出（$c 处）" || bad "$rid 未报出（死规则）"
done

echo ""; echo "  【反例】clean-project（必须 0 命中）"
M=$(node bin/cli.mjs --root tests/fixtures/pass/clean-project --quiet 2>&1 | grep -oE '^[0-9]+' | head -1)
[ "${M:-1}" = "0" ] && ok "0 命中（含 /me/export、mask 调用、migrations DROP、缓存清理等边界写法）" || bad "误报 ${M} 条"

echo ""; echo "  【溯源】每条规则必须有 source、advice ≥ 40 字、且带 when 限定适用场景"
python3 - <<'PY' && ok "7 条规则溯源信息完整" || bad "有规则溯源信息不完整"
import json, glob, sys
bad = []
files = sorted(glob.glob('rules/*.json'))
if len(files) != 7:
    print('规则条数不是 7:', len(files), file=sys.stderr); sys.exit(1)
for f in files:
    r = json.load(open(f, encoding='utf-8'))
    rid = r.get('id') or f
    if not r.get('source'): bad.append(rid + ': 缺 source')
    if not r.get('advice') or len(r['advice']) < 40: bad.append(rid + ': advice 太短')
    if not (r.get('check') or {}).get('when'): bad.append(rid + ': 缺 check.when')
if bad:
    print('\n'.join(bad), file=sys.stderr)
    sys.exit(1)
PY

echo ""; echo "  【适用范围】报告头与页脚必须提示「需人工确认」"
H=$(node bin/cli.mjs --root tests/fixtures/fail/demo-project 2>&1 | head -4)
echo "$H" | grep -q "适用范围需人工确认" && ok "报告头含「适用范围需人工确认」" || bad "报告头缺适用范围提示"
F=$(node bin/cli.mjs --root tests/fixtures/fail/demo-project 2>&1 | tail -5)
echo "$F" | grep -q "只覆盖上海、深圳两市条例" && ok "报告页脚含地域覆盖范围声明" || bad "报告页脚缺地域覆盖范围声明"

echo ""; echo "  【规则清单】--list-rules 必须列出 7 条"
L=$(node bin/cli.mjs --list-rules 2>&1 | grep -cE '^\s+\[(high|medium|low)\] LR-')
[ "${L:-0}" -eq 7 ] && ok "--list-rules 列出 7 条" || bad "--list-rules 列出 ${L} 条，预期 7 条"

echo ""; echo "  ────────────────────────────────────────────────"
echo "  通过 $PASS · 失败 $FAIL"; echo ""
[ "$FAIL" -eq 0 ] || exit 1
