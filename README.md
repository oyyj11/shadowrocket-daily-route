# 轻舟分流 · DailyRoute

面向日常使用的 Shadowrocket 配置。推荐最新的原配置增强版：Muse 指定美国、ChatGPT 指定日本，国内服务直连，其他海外服务独立选路。



## 最新：基于用户原配置的增强版

原配置只有 612 条规则，使用系统 DNS。本版保留原网络参数与规则顺序，增加 Muse 美国、ChatGPT 日本、YouTube 和 App Store 等分组，共 744 条规则。

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-OriginalPlus.conf
```

**首次导入必须在 Muse美国、ChatGPT日本组各选择一个对应地区的实际节点。两个组默认 REJECT，防止误走首页其他地区节点。** 其他海外服务默认沿用首页节点，需要自动调节时在对应组选择自动低延迟。

[完整说明与首次设置](OriginalPlus-Guide.md) · [静态验证](original-plus-validation.json)

下方大规则版及兼容版属于旧方案，与本版相互独立；不要同时当模块叠加。

## 加载慢时的兼容版

如果原版 YouTube 或 App Store 下载缓慢，可用新文件与同一具体节点对比：

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-Compatibility.conf
```

兼容版移除了自动测速组，海外默认跟随首页所选节点；苹果服务默认跟随海外默认，也可切 DIRECT 对比；代理连接阻断 QUIC，使支持回退的客户端使用 TCP/TLS。国内域名及中国大陆 IP 直连规则保持不变。

这是针对选路和协议兼容性的调整，不是已验证的速度修复。未在用户手机上实测；节点吞吐量、拥堵、运营商线路和目标服务器仍影响速度。若效果变差，可切回原版，或删除兼容版 `block-quic = all-proxy` 后再测试。

首次导入后，确认选中的是新文件，首页选具体节点、全局路由选“配置”，暂时关闭旧模块并重新连接。Muse/AI 的资格不受本配置保证。原版默认行为及来源说明见下方。

## 原版 URL 导入

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
