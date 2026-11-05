# 轻舟分流 · DailyRoute v1.1

面向 iPhone Shadowrocket 的配置。**仓库当前只保留这一份配置：DailyRoute-OriginalPlus.conf。** 旧大规则版、兼容版和对应文件已从 main 分支移除，不需要再选择版本

## 唯一下载地址

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-OriginalPlus.conf
```

沿用此前的原配置增强版 URL，方便手机覆盖更新。配置头部显示 **DailyRoute v1.1**。本次统一版本与文档，分流行为与上一版相同，不是新的提速方案。

## 首次启用 / 覆盖更新

1. 先记录 Muse 的美国节点、ChatGPT 的日本节点及其他组的选择；备份本地修改。
2. Shadowrocket → 底部 **配置** → ＋ → URL 粘贴上方链接 → 下载。已有远程文件且菜单有“更新配置”时，也可直接更新。
3. 在 **本地文件** 找到 DailyRoute-OriginalPlus.conf，点击文件名 → **使用配置**（若弹出菜单），确认旁边有 **✓**。
4. 首页全局路由选 **配置**。首页下拉 / 节点列表上方指示牌图标进入分组。
5. **Muse美国** 选实际美国节点，**ChatGPT日本** 选实际日本节点。两个组首次默认 REJECT；更新后也应重新核对。
6. 首页选原来 YouTube 流畅的具体节点，保存后断开再连接，并重开目标 App。

仓库删文件不会自动删除 iPhone 已下载的旧文件。确认 v1.1 正常使用后，在配置列表中通过文件菜单或左滑删除旧大规则版、兼容版及重复副本；保留个人原配置备份即可。不要删除节点订阅。

## 分流与推送

| 服务 | 当前策略 |
|---|---|
| Muse 已知域名及指定认证域名 | Muse美国，需用户选择美国节点 |
| ChatGPT/OpenAI 已知接口和静态资源 | ChatGPT日本，需用户选择日本节点 |
| YouTube | PROXY，跟随首页节点，可切自动低延迟 |
| App Store 下载相关域名 | PROXY，可切 DIRECT 比较 |
| Telegram 域名及官方服务器 IP | Telegram，默认 PROXY |
| X 等海外社交、常见流媒体 | 独立组，默认 PROXY，可切自动低延迟 |
| Apple 共享推送连接 | 苹果推送，默认 DIRECT，可切代理排查 |
| 国内常用服务及中国大陆 IP | DIRECT，使用当前 Wi-Fi/蜂窝网络 |

PROXY 是首页节点；DIRECT 是直连；REJECT 是拒绝。名称筛选不证明真实出口国家，自动低延迟不保证视频带宽最高。Apple 系统连接可能不经过规则，通知还取决于系统和 App 的权限、静音、专注等设置。

## 文档与验证

- **[完整使用说明](OriginalPlus-Guide.md)**：下载、选中配置、地区节点、自动选择、速度排查、更新和回退。
- **[通知推送指南](Notifications-Guide.md)**：Telegram、X、苹果推送、权限和锁屏测试。
- [静态验证结果](original-plus-validation.json)：772 条规则、11 个分组、41 项域名/IP 匹配检查。
- [推送规则的官方数据来源](notification-sources.json)
- [更新记录](CHANGELOG.md)

基线是用户提供的 Shadowrocket default.conf，保留原网络参数与 612 条旧规则的匹配顺序，新增服务分类。操作语法参考 [LOWERTOP/Shadowrocket 非官方社区手册](https://github.com/LOWERTOP/Shadowrocket)，Telegram IP 来源于其官方列表，推送范围参考 Apple 官方说明。

不提供节点、订阅，不需要解密证书或脚本；未设置定时生成或自动发布。静态检查和公开 URL 下载核验不等于真机速度、完整接口覆盖、通知送达或平台资格保证。

仓库公开；文件及变更历史可查看。旧文件从当前 main 移除，Git 历史仍保留。
