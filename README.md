# 轻舟分流 · DailyRoute v1.6

**已识别的国内服务直连，海外和未识别的流量走代理。** Muse 和 ChatGPT 各用一个美国节点组，OKX 使用台湾节点组。Shadowrocket 可以从固定地址更新主配置和规则集。

## 固定配置入口

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-OriginalPlus.conf
```

从此地址导入后，配置内的 `update-url` 会指向同一份文件。主配置和引用的 `rules/*.list` 都可更新。

## APNs 双入口：按通知连接选择

这里的苹果共享推送是 **Apple Push Notification service（APNs）**。两份模板共用同一套远程规则，区别是苹果推送组的默认选项。

| 入口 | 苹果推送默认 | 建议 |
|---|---|---|
| DailyRoute-OriginalPlus.conf | DIRECT | 常规先用，沿用原固定 URL |
| DailyRoute-APNs-Proxy.conf | PROXY，跟随首页节点 | 直连异常时对照，也可在苹果推送组选择稳定手动节点 |

**APNs 默认直连版：**

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-OriginalPlus.conf
```

**APNs 默认代理版：**

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-APNs-Proxy.conf
```

选择其中一份导入并启用。两版各有自己的更新地址，分别拉取对应配置。

这是**可被规则处理的 APNs 连接的默认策略**，不是强制接管所有 iOS 系统连接。原 bypass-system 等网络参数未改，系统旁路连接可能不受组选择影响。Apple 允许可达且不解密的代理承载其 443 回退连接；不能承诺代理比直连快，也不能因此保证通知即时送达。见 [Apple 官方说明](https://support.apple.com/en-vn/102266)。不要对 APNs 开启 HTTPS 解密。

## 导入和自动更新

旧版曾建议删除更新地址。此前照做的用户，需要重新导入一次对应链接并启用新版，或在当前配置的 `[General]` 恢复对应的 `update-url` 后执行「更新配置」。

1. 在 Shadowrocket 的「配置」页用右上角「＋」下载对应链接，点击「使用配置」。首页全局路由选「配置」。
2. 检查「规则集 URL」下载成功 12/12，在 Muse美国、ChatGPT美国和 OKX台湾分别选相应地区的节点。
3. 在 Shadowrocket「设置 → 配置」开启「自动后台更新」，选择更新间隔。在 iPhone「设置 → 通用 → 后台 App 刷新」允许 Shadowrocket 后台刷新。
4. 需要立即拉取时，点配置文件名，再选「更新配置」。整份更新可能覆盖本地编辑和分组选项。若地区组回到 REJECT，重新选择节点。

需要优先保留手机上的自定义配置时，可以使用不含 `update-url` 的本地副本，继续按原方式刷新规则集。

**[完整迁移与使用步骤](OriginalPlus-Guide.md) · [自动同步和共同维护](AUTOMATION.md) · [通知指南](Notifications-Guide.md)**

## 两级同步

| 环节 | 实现 |
|---|---|
| 你和朋友维护配置 | 编辑 `DailyRoute-OriginalPlus.conf` 或对应的 `rules/*.list`，提交到 main |
| APNs 代理版 | GitHub Actions 校验后从直连版生成并发布 |
| GitHub 定时同步 | 每天北京时间 11:17 尝试同步 Telegram 官方 IP，校验通过才提交，有变更才产生提交 |
| 手机定期更新 | Shadowrocket 从所选版本的 `update-url` 拉取主配置，再刷新规则集 |
| 个人节点设置 | 整份更新后核对分组。只刷新规则集时继续使用本地副本 |

GitHub 定时任务可能延迟；iOS 后台任务也不是准点保证。定时同步目前只自动拉取 Telegram 官方地址，其他服务域名由维护者审核修改；没有重新引入旧大规则合集。

## 默认策略

| 服务 | 策略 |
|---|---|
| Muse | Muse美国，首次选择美国节点 |
| ChatGPT/OpenAI | ChatGPT美国，首次选择美国节点 |
| OKX | OKX台湾，首次选择台湾节点，覆盖 `okx.com` 及其子域名 |
| YouTube | PROXY，优先沿用原来流畅的首页节点，可切自动低延迟 |
| App Store 下载 | PROXY，可选择其他代理节点 |
| Telegram | 独立 Telegram 组，默认 PROXY |
| X 等海外社交 / 流媒体 | 独立组，默认 PROXY，可切自动低延迟 |
| Apple 共享推送 | 苹果推送，默认取决于所选入口；系统连接可能旁路 |
| 已识别的国内服务、局域网 | DIRECT，使用当前 Wi-Fi 或蜂窝网络 |
| 海外服务、未识别的流量 | 使用对应代理组，未匹配请求走「海外通用」 |

名称筛选不证明实际出口国家；低延迟不代表视频吞吐量最高。地区组不提供其他地区回退，但未收录的新接口仍需检查连接记录。通知还依赖系统权限、专注模式和 App 内开关。

Shadowrocket 根据连接的目标域名和 IP 匹配规则。国内 App 调用未收录的服务器时，该连接会进入代理兜底。APNs 是系统共用的通知连接，按所选模板中的苹果推送策略处理。[Shadowrocket 分流说明](https://github.com/LOWERTOP/Shadowrocket#app分流)

微信视频期间如果国内网站可访问，只有代理 App 卡住，请按使用说明在通话前、通话中、挂断后对比同一代理 App 和节点。[微信视频通话排查](OriginalPlus-Guide.md#8-微信视频通话期间代理-app-卡住)

## 验证和目录

- [original-plus-validation.json](original-plus-validation.json) 记录 669 条规则、12 个本地分组、12 个远程规则集和 61 项域名/IP 检查。校验同时检查腾讯 QQ/微信网络的直连规则是否存在。
- [GitHub Actions](https://github.com/oyyj11/shadowrocket-daily-route/actions)：push/PR 校验，定时和手动同步。
- [规则脚本](scripts/)：Python 标准库；同步失败或校验不通过时不发布新的 Telegram 数据。
- [通知官方数据来源](notification-sources.json) · [更新记录](CHANGELOG.md)

仓库提供 APNs 默认直连与默认代理两份可更新配置。规则分类参考用户提供的 default.conf。更新设置参考 Shadowrocket 社区手册，具体菜单及后台更新时间以手机为准。[自动更新说明](https://github.com/LOWERTOP/Shadowrocket#自动更新)
