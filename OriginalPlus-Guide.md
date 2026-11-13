# DailyRoute v1.5 迁移和使用说明

v1.5 将直连范围收紧到已识别的国内服务和局域网。海外及未识别的流量走代理，App Store 下载组仅提供代理选项。使用旧本地副本的用户需下载新模板并重新选择节点，才能更新本地兜底和组定义。后续规则集刷新会沿用本地分组。

## 0. 先选择 APNs 默认直连或默认代理

APNs 即 Apple Push Notification service。常规入口 DailyRoute-OriginalPlus.conf 默认 DIRECT；新入口 DailyRoute-APNs-Proxy.conf 默认 PROXY。代理版 URL：

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-APNs-Proxy.conf
```

两份 v1.5 模板共用规则集，安装步骤相同。此前代理版导入时遇到中断的用户，可以先使用已能正常导入的 APNs 默认直连版。

## 1. 下载模板并复制成本地配置

备份现在能用的配置，记下 Muse、YouTube、App Store 等组的节点选择。继续使用已有的节点订阅。

在 Shadowrocket 底部「配置」点右上角 ＋，在 URL 框粘贴：

```text
https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/DailyRoute-OriginalPlus.conf
```

下载后，在「本地文件」找到 DailyRoute-OriginalPlus.conf。点击文件名进入菜单，按版本提供的「编辑配置 → 复制」复制为本地文件（复制通常生成 -copy.conf）；再重命名为 **DailyRoute-Local.conf**。

这里要的是独立本地副本，不能只改远程文件名，也不要误点“扩展配置”建立继承关系。

进入副本的「编辑纯文本」，检查 `[General]`：

```ini
# 如果应用自动加了下面这种行，删除整行：
# update-url = https://.../DailyRoute-OriginalPlus.conf
```

仓库模板没有主动设置 update-url，但应用导入远程文件可能记录更新地址。必须确认副本没有整份配置的更新地址。保留 `[Rule]` 中全部 RULE-SET 行，它们是日常同步入口。

## 2. 选中新配置在哪里

回底部「配置 → 本地文件」，点击 **DailyRoute-Local.conf 文件名 → 使用配置**（部分版本点击直接选中），确认 ✓ 在它旁边。

```text
本地文件
DailyRoute-OriginalPlus.conf           ⓘ  ← 初始化模板
DailyRoute-Local.conf             ✓   ⓘ  ← 日常启用本地副本
```

蓝色 ⓘ 是编辑入口，打开编辑不代表已经启用。首页「全局路由」设为 **配置**，不要日常设成全局代理，否则不能按这里的地区分组判断选路。

首次验证暂时关闭旧模块，避免模块规则覆盖。副本验证正常后，可以删除手机旧大规则版、兼容版和重复副本；个人 default.conf 备份可保留用于回退。

## 3. 选择美国和台湾节点

首页下拉，或点节点列表上方指示牌图标进入代理分组。查看/编辑定义的入口是「配置 → 本地副本右侧 ⓘ → 代理分组」。

- **Muse美国**：从筛选结果选一条真实美国节点。
- **ChatGPT美国** 从筛选结果选一条真实美国节点。
- **OKX台湾** 从筛选结果选一条真实台湾节点。OKX 的服务资格取决于真实居住地、账户和平台规则。[OKX 注册说明](https://www.okx.com/help/how-do-i-register-an-account-on-okx)

三个地区组初始为 REJECT。选择完成后保存并重新连接。日常更新通过刷新本地副本引用的规则集完成。

如果列表只有 REJECT，检查订阅是否有对应地区的线路，以及节点备注是否包含美国、US、🇺🇸、台湾、台灣、TW 或 🇹🇼 等标识。地区筛选根据备注匹配，选好后还需核对节点的实际出口。

所选节点失效、被订阅删除或改名时，需要重新选一个同地区节点。

## 4. 确认远程规则全部下载成功

在本地副本「编辑配置 → 规则集 URL」查看，首次应成功 **12/12**。缺失时重试下载，再点「使用配置」或「编译配置」。

本地副本通过 12 个 RULE-SET 引用公共规则，下载后在手机上匹配。首次下载和后台刷新需要能访问 GitHub Raw。

公共规则文件没有节点账号或 `[Proxy Group]`，只保存匹配条件。组名、组默认值和实际节点选择由本地副本提供，远程列表更新不能定义或重置这些组。

维护者如果新增全新策略组或修改 General，这属于主配置升级，仍需要单独迁移；日常新增域名/IP 使用现有分类即可，无需改主配置。

## 5. 开启规则后台更新

Shadowrocket **设置 → 配置 → 自动后台更新**，选择可用更新间隔，例如 1 天，并按需开更新提醒。iPhone **设置 → 通用 → 后台 App 刷新**，允许 Shadowrocket。

菜单以安装版本为准。“配置更新”和“服务器节点订阅更新”是不同设置。这里让当前没有整份更新地址的本地配置刷新其远程规则资源。

iOS 后台调度不保证准点；重启手机、强制结束 App 等可能影响后台任务。若怀疑没有刷新，手动对本地副本执行“使用配置/编译配置”，然后看规则集 URL 成功状态。

**不再对个人副本执行从服务器整份覆盖，也不要再次下载模板后直接替换个人副本。** 否则仍可能重新得到初始 REJECT。误覆盖时根据原记录恢复节点选择即可。

## 6. 其他应用、速度和自动选路

YouTube、App Store、Telegram、海外社交、海外流媒体、海外通用默认 PROXY，跟随首页具体节点。苹果推送默认值取决于所选模板（直连版 DIRECT，代理版 PROXY）。国内直连依据已收录的服务域名，局域网地址也走直连。其余流量默认走代理。

YouTube 先使用原配置下流畅的同一个首页节点；要试自动选择，在 YouTube 组单独选“自动低延迟”。海外通用、社交、流媒体也需要各自选择，并不互相跟随。自动组每 900 秒比较测试地址延迟，公差 150；它不检测视频带宽、解锁或账号资格。

“手动节点”是共用组，多个应用都选择它时，改它会同时影响这些应用。需要独立线路时，在相应应用组添加并选择具体节点。

YouTube 慢时，固定网络、视频和清晰度，比较 PROXY 和自动组，并查看 googlevideo.com 的实际命中、缓冲和连接速度。App Store 下载慢时，在 AppStore下载 组换一个代理节点，暂停再继续同一个下载，观察进度。

若短时全局代理也慢，优先检查节点吞吐量、拥堵、Wi-Fi/蜂窝和目标服务器。全局代理对照只用于测速，结束后切回配置，再使用 Muse/ChatGPT。

没有配置能保证所有应用永远最快；手机节点供应商、网络、平台资格和实际出口都要实测。

## 7. 验证地区与直连

在「测试规则」选 DailyRoute-Local.conf，输入域名：

| 域名/IP | 预期策略 |
|---|---|
| muse.ai / auth.meta.com | Muse美国 |
| chatgpt.com / api.openai.com | ChatGPT美国 |
| www.okx.com / openapi.okx.com / ws.okx.com | OKX台湾 |
| weixin.qq.com / weixinbridge.com / wechatos.net | DIRECT |
| www.youtube.com / r1.googlevideo.com | YouTube |
| apps.apple.com | AppStore下载 |
| api.telegram.org / 149.154.160.1 | Telegram |
| api.x.com / t.co | 海外社交 |
| courier.push.apple.com | 苹果推送 |
| www.jd.com / www.bilibili.com / www.douyin.com | DIRECT |
| store.steampowered.com / www.paypal.com / www.icloud.com | 海外通用 |

测试显示的是组名，实际节点要在组里看。再打开 App，在数据连接记录核对真实请求。未知新接口可能仍走海外通用，应提供失败域名补充；不能只测主页就认为所有接口都覆盖。

国内直连使用手机当前的 Wi-Fi 或蜂窝。连接按域名和 IP 匹配。同一个 App 使用第三方服务或未知域名时，个别连接可能命中其他策略。用连接记录查看实际出口。[Shadowrocket 分流说明](https://github.com/LOWERTOP/Shadowrocket#app分流)

## 8. 微信视频通话期间代理 App 卡住

如果微信语音消息发送慢，先刷新当前配置的规则集，确认 `direct.list` 下载成功，再用同一网络重发一条语音。补丁恢复了腾讯 QQ/微信网络 AS132203 的 IP 直连规则。若仍然慢，查看发送当时的「数据 → 代理日志」，记录目标域名或 IP、命中策略和错误。若已命中 DIRECT，可在同一网络断开 VPN 再发一条语音，比较耗时。[腾讯网络登记](https://www.peeringdb.com/asn/132203)

已报告的现象是在 Wi-Fi 和蜂窝下，微信视频期间国内网页能打开，代理 App 卡住。排查优先看节点、隧道和通话流量的实际走向。直连和代理共用手机的网络上行，国内网页可打开时，仍可能有排队延迟或丢包。[IETF RFC 9743](https://datatracker.ietf.org/doc/html/rfc9743#section-5.1.2)

1. 保持「全局路由 → 配置」，在发生问题的 App 对应组选择一个已验证可用的固定节点。ChatGPT 选择美国节点，OKX 选择台湾节点。测试期间让 APNs 策略、网络和其他设置保持一致。
2. 用同一网络对比通话前、通话中、挂断后。在每个阶段刷新同一个代理 App 和同一个国内页面。通话中可以暂时关闭摄像头并保持通话，观察代理连接是否恢复。
3. 在「数据 → 代理日志」查看发起通话时出现的连接和故障 App 的失败记录，核对域名或目标 IP、命中策略、协议和错误。微信已知域名应命中 DIRECT。若确认某个通话地址误走海外通用，先核实地址归属，再添加针对该地址的直连规则。
4. 如果只在一个固定节点上复现，换同地区的另一个节点重测。如果多个固定节点都失败，观察 Shadowrocket 是否仍连接，并查看日志是否出现 DNS 超时、TCP 连接失败、UDP 转发拒绝或隧道重连。不同错误对应不同的排查方向。

| 对照结果 | 接下来查什么 |
|---|---|
| 通话中关闭摄像头后恢复，或延迟明显下降 | 上行拥塞或排队。用更稳定的网络，必要时降低视频上行负载。 |
| 只换节点就恢复 | 原节点或协议链路。使用同地区可稳定复现的节点。 |
| 日志确认只有 UDP 请求失败，而 TCP 请求正常 | 核对节点的 UDP 转发能力，以及订阅或节点是否开启 UDP。保留全局 `udp-policy-not-supported-behaviour = REJECT`，避免地区流量改走直连。 |
| 多个节点均失败，日志显示隧道重连 | 记录 iOS、Shadowrocket 版本和重连时间，再排查客户端或隧道问题。 |

本版把缺失的 `weixinbridge.com` 和 `wechatos.net` 加入直连规则。已知的微信登录及 NAT 域名此前已被 `tencent-cloud.net` 直连覆盖，实际通话仍可能使用其他地址。缺少故障时的代理日志，目前无法确认断连根因。可提供失败条目的域名或目标 IP、策略和错误，隐去节点凭据。

## 9. 推送、共同维护和回退

- [通知推送指南](Notifications-Guide.md)：Apple APNs、Telegram、X 的权限和锁屏检查，系统连接可能旁路。
- [自动同步与共同维护](AUTOMATION.md)：日程、修改规则、校验及失败处理。
- 回退：选原 default.conf 备份 → 使用配置 → 首页全局路由配置 → 原节点 → 重新连接。回退后重新检查敏感服务的出口。

分享问题时提供配置名、App、网络类型、组内选择、失败域名和命中结果。不要公开订阅链接、密码、令牌或证书私钥。

## 10. 本版验证范围

CI 检查格式、网段、策略引用和组循环，并验证美国及台湾节点名称筛选和 61 项域名/IP 分类。每天同步 Telegram 官方 IP 前后均执行校验。[验证报告](original-plus-validation.json)

尚未在用户手机验证完整接口、速度、推送送达、出口国家，以及所有客户端版本的后台行为。完成首次本地迁移后，仍要实际测试一次刷新前后的节点选择。
