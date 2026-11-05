# 轻舟分流 · DailyRoute

公开的 Shadowrocket 配置仓库。当前推荐 **原配置增强版 DailyRoute-OriginalPlus.conf**：以原来速度较好的 default.conf 为基础，保留系统 DNS 等网络参数，补充 Muse 美国、ChatGPT 日本及常用服务分流。

**首次导入后，必须为「Muse美国」「ChatGPT日本」各选择一个对应地区的实际节点。两个组初始为 REJECT，未选择时无法连接。** 本仓库不提供节点或订阅。

## 复制 URL 下载

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-OriginalPlus.conf
```

这是返回配置纯文本的地址，可以填入 Shadowrocket URL 框。仓库首页或带 /blob/ 的文件预览地址不能代替它。

## 首次启用：六步

1. 备份当前配置，保留已有节点订阅。
2. 底部 **配置 → 右上角 ＋ → URL 粘贴上方地址 → 下载**。
3. **本地文件 → 点击 DailyRoute-OriginalPlus.conf 文件名 → 使用配置**（若出现菜单），确认文件旁有 **✓**。
4. 首页 **全局路由 → 配置**。首次验证暂时关闭旧模块，避免覆盖规则。
5. 首页下拉，或点击节点列表上方的指示牌图标进入分组，分别选择 **Muse美国 → 美国节点、ChatGPT日本 → 日本节点**。
6. 首页选原来播放 YouTube 流畅的节点，断开再连接，重新打开目标 App。

不同版本菜单可能变化。下载、选中配置、选择地区节点、开启连接是四件事。**[完整使用说明：从入口定位到故障排查](OriginalPlus-Guide.md)**

## 默认选路

| 服务 | 默认策略 |
|---|---|
| Muse 核心域名及指定认证域名 | Muse美国，首次需选实际美国节点 |
| ChatGPT / OpenAI 已知接口和静态资源 | ChatGPT日本，首次需选实际日本节点 |
| YouTube | PROXY，跟随首页节点，可切自动低延迟 |
| App Store 已知下载资源 | PROXY，可切 DIRECT 对比 |
| 常见海外社交、流媒体 | 独立组，默认 PROXY，可切自动低延迟 |
| 其他代理流量 | 海外通用，默认 PROXY，可切自动低延迟 |
| 国内常用服务及中国大陆 IP | DIRECT，使用当前 Wi-Fi / 蜂窝网络 |

PROXY 是首页所选节点；DIRECT 是直连；REJECT 是拒绝。自动低延迟比较连通延迟，不保证视频带宽最高。节点名称筛选也不证明真实出口国家。

## 版本列表

| 文件 | 用途 | 建议 |
|---|---|---|
| **DailyRoute-OriginalPlus.conf** | 原 default.conf 增强版，744 条规则、9 个分组 | **当前推荐** |
| DailyRoute-Compatibility.conf | 旧大规则版的固定出口及 QUIC 兼容性尝试 | 历史对照 |
| Shadowrocket-Daily.conf | 初期约 11.6 万条规则合集 | 历史对照 |

三份是独立主配置，只选一份使用，不需要全部导入或当模块叠加。旧 [使用说明.md](使用说明.md)、[sources.json](sources.json)、[validation.json](validation.json) 对应历史大规则版，不代表推荐版的默认行为。

## 来源与验证

推荐版基于用户提供的 Shadowrocket 默认配置，保留原 612 条规则的匹配条件和顺序，调整代理策略引用并前置新增 132 条规则。操作和语法参考 [LOWERTOP/Shadowrocket 非官方社区手册](https://github.com/LOWERTOP/Shadowrocket)。

旧大规则版使用 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) 的规则，GPL-2.0 许可证和来源记录保存在仓库。它不是当前推荐版的完整基线。

- [完整使用说明](OriginalPlus-Guide.md)
- [推荐版静态验证记录](original-plus-validation.json)
- [仓库更新记录](CHANGELOG.md)

规则为日期快照，没有定时生成或自动发布任务。重新下载 URL 只获取本仓库已发布内容，不会自动合入上游变化。没有新增解密、证书或脚本。

已做静态检查和下载链接核验，未在用户手机完成真机测速，不保证完整 App 接口覆盖、平台资格、真实节点国家或速度。
