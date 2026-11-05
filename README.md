# 轻舟分流 · DailyRoute v1.3

**本地保存节点选择，远程同步规则。** Muse 已知请求走美国，ChatGPT 已知请求走日本；国内常用服务直连，普通海外可手动或自动选路。保留原系统 DNS、IPv6、QUIC 参数。

## 固定配置入口

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-OriginalPlus.conf
```

此地址是初始化模板，保持不变。日常同步的是模板引用的 `rules/*.list`，不是反复用整份模板覆盖手机个人设置。

## APNs 双入口：按通知连接选择

这里的苹果共享推送是 **Apple Push Notification service（APNs）**。两份模板共用同一套远程规则；差异仅是苹果推送组的默认选项和对应标识。Muse 美国、ChatGPT 日本、国内直连、YouTube 和更新流程一致。

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

选择其中一份下载，复制成本地配置并移除整份 update-url；想保留两个本地副本对照时，分别命名 APNs-Direct-Local.conf 和 APNs-Proxy-Local.conf，且各自确认美国/日本节点选择。已有本地副本也可直接切换“苹果推送”组，无需重新导入。

这是**可被规则处理的 APNs 连接的默认策略**，不是强制接管所有 iOS 系统连接。原 bypass-system 等网络参数未改，系统旁路连接可能不受组选择影响。Apple 允许可达且不解密的代理承载其 443 回退连接；不能承诺代理比直连快，也不能因此保证通知即时送达。见 [Apple 官方说明](https://support.apple.com/en-vn/102266)。不要对 APNs 开启 HTTPS 解密。

## 必须做一次的迁移

1. 记录当前 Muse、ChatGPT 和其他组的节点选择，备份个人配置。
2. Shadowrocket → 配置 → ＋ → URL 填上方链接 → 下载。
3. 点击下载的文件 → 编辑配置 → 复制（具体菜单随版本变化），将副本命名为 **DailyRoute-Local.conf**。这里使用“复制”，不选“扩展配置”。
4. 编辑副本的纯文本，在 `[General]` 中删除应用自动添加的 `update-url = ...`（若没有就不用删）；保留所有 RULE-SET 行。确认副本不再有整份配置更新地址。
5. 点击 **DailyRoute-Local.conf → 使用配置**，确认 ✓ 在副本旁，首页全局路由选 **配置**。
6. Muse美国 选实际美国节点、ChatGPT日本 选实际日本节点。初始 REJECT 只用于首次待配置状态。
7. 配置的“规则集 URL”应下载成功 **11/11**。先测试基本连接，再开启后台更新。
8. Shadowrocket 设置 → 配置 → 自动后台更新，选择可用间隔（例如 1 天）；iPhone 设置 → 通用 → 后台 App 刷新，允许 Shadowrocket。不要把“节点订阅更新”当作规则更新。

以后只刷新远程规则集，本地组定义、节点选择和网络参数不在公共规则文件里，不会被远程规则覆盖。不要再对已经设置好的本地副本执行“从服务器整份更新配置”。

**[完整迁移与使用步骤](OriginalPlus-Guide.md) · [自动同步和共同维护](AUTOMATION.md) · [通知指南](Notifications-Guide.md)**

## 两级同步

| 环节 | 实现 |
|---|---|
| 你和朋友维护规则 | 编辑对应 rules/*.list，合并到 main，固定规则 URL 即更新 |
| GitHub 定时同步 | 每天北京时间 11:17 尝试同步 Telegram 官方 IP，校验通过才提交，有变更才产生提交 |
| 手机定期更新 | Shadowrocket 配置后台更新，刷新当前本地主配置引用的规则集 |
| 个人节点设置 | 只留在各自手机本地副本，首次选择后无需因公共规则更新反复重选 |

GitHub 定时任务可能延迟；iOS 后台任务也不是准点保证。定时同步目前只自动拉取 Telegram 官方地址，其他服务域名由维护者审核修改；没有重新引入旧大规则合集。

## 默认策略

| 服务 | 策略 |
|---|---|
| Muse | Muse美国，首次选择美国节点 |
| ChatGPT/OpenAI | ChatGPT日本，首次选择日本节点 |
| YouTube | PROXY，优先沿用原来流畅的首页节点，可切自动低延迟 |
| App Store 下载 | PROXY，可切 DIRECT 比较 |
| Telegram | 独立 Telegram 组，默认 PROXY |
| X 等海外社交 / 流媒体 | 独立组，默认 PROXY，可切自动低延迟 |
| Apple 共享推送 | 苹果推送，默认取决于所选入口；系统连接可能旁路 |
| 国内常用服务和中国大陆 IP | DIRECT，使用当前 Wi-Fi/蜂窝网络 |

名称筛选不证明实际出口国家；低延迟不代表视频吞吐量最高。地区组不提供其他地区回退，但未收录的新接口仍需检查连接记录。通知还依赖系统权限、专注模式和 App 内开关。

## 验证和目录

- [original-plus-validation.json](original-plus-validation.json)：728 条去重后规则、11 个本地分组、11 个远程集、43 项回归检查；迁移时 1375 个样本的路由结果与前版相同。
- [GitHub Actions](https://github.com/oyyj11/shadowrocket-daily-route/actions)：push/PR 校验，定时和手动同步。
- [规则脚本](scripts/)：Python 标准库；同步失败或校验不通过时不发布新的 Telegram 数据。
- [通知官方数据来源](notification-sources.json) · [更新记录](CHANGELOG.md)

当前 main 保留 APNs 默认直连与默认代理两份初始化 .conf；不包含节点账号、订阅密钥、证书或解密脚本。规则分类参考用户提供的 default.conf，操作语法参考 [LOWERTOP/Shadowrocket 非官方社区手册](https://github.com/LOWERTOP/Shadowrocket)。静态和服务器 CI 校验不能代替手机实测、速度测试和平台资格核验。
