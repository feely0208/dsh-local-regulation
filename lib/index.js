import { createPlugin, pkgRootFrom } from '@deepwhale-cn/dsh-guard-core/plugin';

export const { name, inject, apply } = createPlugin({
  name: 'local-regulation',
  pkgRoot: pkgRootFrom(import.meta.url),
  skillFile: 'skill/local-regulation.md',
  binFile: 'bin/cli.mjs',
  description: '上海、深圳的额外要求，国家法之外那一层',
  whenToUse:
    '项目需要核对上海、深圳两市地方数据条例的额外要求时使用。用户会说：' +
    '「上海的数据条例有没有踩」「深圳对用户画像 / 数据销毁有什么额外要求」' +
    '「这个项目在深圳运营合不合规」「人脸识别标识、去标识化、数据安全责任人查一下」。' +
    '注意：本插件不判断实际运营地，报告头会提示「适用范围需人工确认」。',
});
