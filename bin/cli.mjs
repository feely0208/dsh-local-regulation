#!/usr/bin/env node
import { runCli } from '@deepwhale-cn/dsh-guard-core/cli';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const pkgRoot = join(dirname(fileURLToPath(import.meta.url)), '..');

runCli({
  pkgRoot,
  meta: {
    // 地域适用性是这个插件的第一前提：报告头必须写明「需人工确认」。
    // 我们不知道、也不替用户猜实际运营地；上海 / 深圳的规则不能默认套到全国。
    name: '深鲸守护 · 地方数据条例检查（仅上海 / 深圳）· 适用范围需人工确认',
    desc: '上海、深圳两市的额外数据要求（国家法之外那一层）；本插件不判断你的实际运营地。',
    footer: '本插件只覆盖上海、深圳两市条例；是否适用取决于实际运营地，需人工确认。命中是提示确认，不是违规判定。',
  },
});
