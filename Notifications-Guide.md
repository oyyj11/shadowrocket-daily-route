# Telegram、X 等应用：通知设置与验证

适用：v1.2 模板复制后的本地配置 `DailyRoute-Local.conf`。更新日期：2026-11-05。

## 这次补充了什么

| 内容 | 默认策略 | 目的 |
|---|---|---|
| Telegram 域名及官方公布的 14 个 IPv4/IPv6 地址段 | Telegram → PROXY | 覆盖原生客户端直接连接 IP 的情况 |
| X / Twitter 已有域名及新增 t.co | 海外社交 → PROXY | 保持业务请求、短链可达 |
| push.apple.com 及 Apple 公布的较窄 APNs 网段 | 苹果推送 → DIRECT | 为匹配到的共享系统推送连接提供独立策略 |

Muse 美国、ChatGPT 日本、YouTube 默认出口、国内直连和原网络参数保持。数据来源和快照见 [notification-sources.json](notification-sources.json)。

## 一、先理解两条连接

在 iPhone 上，App 的业务连接与 Apple 系统推送连接不是同一回事：

```text
Telegram / X 业务请求 → 对应应用策略组 → 平台服务器
平台发送的系统推送   → Apple APNs    → iPhone 通知
```

系统推送连接为多个 App 共用，不能按“只给 Telegram 的 APNs 走美国、只给 X 的 APNs 走日本”拆成独立线路。规则分类不等于打开系统通知权限，也不能让平台生成本来没有订阅的通知。

APNs 通道正常，有时能先收到通知，但打开 App 加载详情、下载媒体或回复消息仍需要业务连接。不能把“收到通知”当成 App 所有接口已连通的证据。

## 二、更新并检查两个新分组

继续使用相同下载地址：

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-OriginalPlus.conf
```

已迁移到 v1.2 的用户，只需对本地副本使用“使用配置/编译配置”刷新远程规则，不要重新用整份模板覆盖个人副本。首次迁移按 [完整说明](OriginalPlus-Guide.md) 复制本地配置、移除 update-url 并选择美国/日本节点。规则集应成功 11/11。

在代理分组中确认：

- **Telegram**：默认 PROXY。首页选一个实际可用且较稳定的节点；也可在本组改用手动节点。自动低延迟是可选项，不保证后台长连接更稳定。
- **海外社交**：X 等默认 PROXY，确认首页节点可正常打开对应 App。
- **苹果推送**：先保持 DIRECT。若直连异常、业务请求正常且其他通知设置无误，可切 PROXY 或“手动节点”对照；不要未经测试就让所有系统推送绕路。

切换后保存，重新连接，打开相应 App 一次，再回主屏幕进行测试。

### 为什么推送分组可能没有连接记录

本配置沿用 `bypass-system = true` 和原来的系统网络设置。iOS 的系统连接可能不经过 Shadowrocket 可控制的规则路径，因此苹果推送组只对实际被处理的连接生效；没有记录不代表 APNs 已被拦截，切组也未必改变系统旁路连接。

不要仅为了让日志出现而盲目修改所有系统旁路参数。若收不到通知，先完成下方系统设置和 Wi-Fi/蜂窝对照。Apple 的说明要求 APNs 保持可用网络连接；设备常用 TCP 5223，无法连接时可能回退到 TCP 443。受限 Wi-Fi、防火墙和系统网络状态也可能影响连接。

**不需要开放手机入站端口，不需要把全部 17.0.0.0/8 或所有 5223 端口请求强制代理，也不需要开启 HTTPS 解密。** Apple 明确要求代理不能解密 APNs 连接。

## 三、iPhone 系统通知权限

按你的 iOS 界面进入「设置 → 通知 → Telegram / X」，或「设置 → App → 对应应用 → 通知」：

1. 开启 **允许通知**。
2. 按需开启锁定屏幕、通知中心、横幅、声音和标记。
3. 希望及时提示时，检查是否将该 App 放进 **定时推送摘要**；需要即时收到的应用不要被摘要延后。
4. 检查 **专注模式 / 勿扰模式** 是否允许该 App 或联系人通知。测试时可先关闭专注模式。
5. 确认 Wi-Fi 或蜂窝实际联网，且 App 未被禁止使用蜂窝数据。

如果佩戴 Apple Watch，也检查通知是否显示在手表而不是手机。通知不显示内容还可能是“显示预览”的设置，不代表连接失败。

普通可见系统推送不是靠把 App 一直放在前台实现，也不应把“后台 App 刷新已开启”当成唯一条件。不要为了测试反复注销账号或清除数据。

## 四、Telegram 内设置

进入 Telegram **Settings → Notifications and Sounds（设置 → 通知和声音）**：

- 开启需要的私人聊天、群组、频道通知。
- 检查目标聊天、群组或频道是否单独静音。
- 检查特殊通知例外设置；全局开启不代表某个已静音群组也会通知。

先验证 App 打开时能正常收发消息，再测试后台通知。不要用一个已静音群组判断整个配置失效。

## 五、X / Twitter 内设置

进入 **Settings and privacy → Notifications → Preferences → Push notifications**，开启需要的私信、提及、回复等类型。

如果希望某个账号每次发帖都提醒，进入该账号主页点击铃铛，并选择相应发帖通知类型。检查通知过滤器和静音设置。

分流不能强制平台为每条时间线内容发送通知。X 是否生成某类推送还取决于你启用的类别、关注账号铃铛和平台策略。

## 六、如何实际测试

1. 更新配置、选择地区节点，保持 Shadowrocket 连接且全局路由为配置。
2. 打开 Telegram / X，确认业务请求可正常访问。
3. 返回主屏幕并锁屏，不需要将 App 从后台反复划掉。
4. 让另一账号发一条未静音聊天消息/私信，记录发送与收到提示的时间。
5. 对 Wi-Fi 和蜂窝分别测试。若仅某个 Wi-Fi 失败，优先排查该网络对 APNs 的连通性。
6. APNs 直连与代理的对照每次只改一个选项，并给连接重新建立和新的测试消息留出时间；不要一边换节点一边改多个权限。

也可先在“测试规则”中检查：

| 输入 | 预期策略 |
|---|---|
| courier.push.apple.com | 苹果推送 |
| 17.249.0.1 | 苹果推送 |
| api.telegram.org / t.me / telegram.me | Telegram |
| 149.154.160.1 | Telegram |
| api.x.com / api.twitter.com / t.co | 海外社交 |

以上只是分类示例，不代表每个主机都必须存在或接受测试请求。规则测试通过不等于通知实测送达。

## 七、按现象定位

| 现象 | 检查方向 |
|---|---|
| App 在前台也收不到消息、一直连接中 | 业务节点、Telegram IP/域名分流、平台状态 |
| 前台正常，锁屏后无横幅 | 系统通知、App 内开关、静音、专注、摘要、APNs 网络 |
| 有通知，打开 App 却加载失败 | 业务连接与推送连接分别检查 |
| 只有一个群或账号没有提醒 | 群/频道静音、X 铃铛、通知过滤 |
| 多个 App 都不推送 | 共享 APNs 连通性和系统设置 |
| 换蜂窝恢复，Wi-Fi 不行 | Wi-Fi 网络的防火墙和端口可达性 |
| 改苹果推送组无变化 | 系统连接可能旁路；不要认定设置已控制 APNs |

这次更新是连通性补充，尚未在用户手机验证通知送达率；不能承诺所有平台每条消息都即时到达。

## 官方参考

- [Apple：设备无法收到推送通知时的连接要求](https://support.apple.com/en-nz/102266)
- [Apple：调整 iPhone 通知、专注与摘要](https://support.apple.com/guide/iphone/change-notification-settings-iph7c3d96bab/ios)
- [Telegram：通知问题排查](https://telegram.org/faq#notification-problems)
- [Telegram 官方服务器地址段](https://core.telegram.org/resources/cidr.txt)
- [X：移动端推送通知设置](https://help.x.com/en/managing-your-account/notifications-on-mobile-devices)
