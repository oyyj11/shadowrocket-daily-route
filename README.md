# 轻舟分流 · DailyRoute

面向中国大陆日常网络环境的 Shadowrocket 主配置：国内服务直连，海外服务按类别选择节点，Muse 与 Meta 使用共同策略组。

## URL 导入

在 Shadowrocket → 配置 → 右上角 ＋ 的 URL 下载框中粘贴：

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/Shadowrocket-Daily.conf
```

下载后选中配置，首页全局路由设为“配置”，重新连接。首次使用先备份旧配置、暂时关闭旧模块，并在首页选一个可用节点。AI服务 / Muse与Meta / 流媒体默认跟随首页节点（PROXY）；请按实际服务可用性选择稳定出口。地区测速组可能因订阅节点命名而为空，空组改用手动节点或 PROXY。

URL 必须返回配置纯文本；不要将仓库网页或带 blob 的页面地址填入 URL 框。如果下载失败，可先用现有可用代理重新下载，或从仓库下载文件后本地导入。

## 分流概览

| 类别 | 默认行为 |
|---|---|
| 微信、支付宝、淘宝、京东、抖音、小红书、B站、国内银行、国内 AI | 域名直连，加中国大陆 IP 兜底 |
| 未分类海外流量 | 自动测速 |
| Muse、Meta、Facebook、Instagram、WhatsApp | Muse与Meta 组 |
| ChatGPT、Claude、Gemini、Grok、Perplexity 等 | AI服务组 |
| YouTube、Netflix、Disney、Spotify、TikTok | 独立服务组 |
| Telegram、X、Discord、LINE | 海外社交组 |
| GitHub / Google | 开发工具 / 谷歌服务组 |
| Apple / Microsoft / Steam / Epic | 默认直连，可切代理 |

不提供节点或订阅，不需要 HTTPS 解密、证书或脚本。国内直连使用手机当前的 Wi-Fi 或蜂窝网络，不强制切换蜂窝，不提供运营商流量减免。

自动测速比较测试地址连通延迟，不代表带宽最优或地区解锁。Muse 等账号资格、服务开放地区和平台风控不由分流配置决定。规则按域名/IP 匹配，不能保证整 App 所有接口均由同一策略处理。

## 来源和更新

规则快照：2026-11-05。主要来源：[blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)，许可证 GPL-2.0；本项目是修改整合版。分组语法参考：[LOWERTOP/Shadowrocket](https://github.com/LOWERTOP/Shadowrocket)。

本地修改包括服务分组、Muse/AI 和国内常用域名补充、去重、跳过 User-Agent、国内集合排除宽泛关键词，以及 no-resolve 的 IP 策略。大型集合已同时合入配套的 _Domain.list。

规则内置到单个配置文件，无需手机下载远程规则；本项目未设置定时更新任务，上游变化不会自动合入。重新下载 URL 只获取本仓库当前版本。

- [完整使用说明](使用说明.md)
- [规则来源与 SHA-256](sources.json)
- [静态验证结果](validation.json)
- [许可证](LICENSE)
- [可编辑生成脚本](work/build_config.py)：电脑安装 Python 后，在仓库根目录运行 `python work/build_config.py`，联网获取上游规则，结果写入 outputs/；审核后再更新仓库根目录的发布文件。

已检查分组引用、循环、IP 格式和 22 个代表域名的匹配结果。未经过 Shadowrocket 官方解析器或用户 iPhone 真机验证，也未实测节点速度。无担保。
