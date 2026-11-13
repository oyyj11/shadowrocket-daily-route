# 自动同步与共同维护

## 两条自动流程

1. **GitHub 端**每日北京时间 11:17（UTC 03:17）同步 Telegram 官方 IP。也可在 Actions 页面选「Validate, publish and sync configuration → Run workflow」手动运行。
2. **手机端**启用含 `update-url` 的对应版本，并开启 Shadowrocket 的配置后台更新，定期拉取主配置和规则集。iOS 决定实际调度时间。

这两条都需要配置，GitHub 自动更新不会直接操作手机。具体手机步骤见 [使用说明](OriginalPlus-Guide.md)。

## 修改哪个文件

| 内容 | 文件 |
|---|---|
| Muse 美国请求 | rules/muse-us.list |
| ChatGPT 美国请求 | rules/chatgpt-jp.list（沿用旧文件名，实际策略由本地分组决定） |
| OKX 台湾请求 | rules/okx.list |
| YouTube | rules/youtube.list |
| App Store 下载 | rules/appstore.list |
| Telegram | rules/telegram.list（IP 部分由官方同步，域名手工维护） |
| X / 其他海外社交 | rules/social.list |
| 海外流媒体 | rules/streaming.list |
| 国内直连 | rules/direct.list |
| Apple 系统推送 | rules/apple-push.list |
| 必须优先于国内规则的海外例外 | rules/overseas-exceptions.list |
| 其他海外匹配 | rules/overseas.list |

规则集中**不写代理策略或节点名**，策略由手机模板的 RULE-SET 行指定。例如给社交分类添加域名，只写：

```ini
DOMAIN-SUFFIX,example.com
```

以上是教学占位域名，不要直接添加。IP 格式示例为 `IP-CIDR,实际网段,no-resolve`。不要往公共规则文件加入个人订阅、服务器密码或 Token。

## 共同维护流程

1. 各自使用自己的 GitHub 账号；仓库协作者权限用于修改本仓库，不需要共用登录密码。
2. 修改对应规则文件或基础配置 `DailyRoute-OriginalPlus.conf`，在新分支提交 Pull Request。
3. 等待 validate 检查通过，再合并 main。GitHub Actions 校验后生成并发布 APNs 代理版和验证报告。
4. 手机下次执行配置更新时从各自的固定 URL 获得改动。

本仓库没有强制分支保护，直接提交 main 会先改变公开规则，然后触发 CI；因此共同维护时应走 PR。定时机器人则在本地完整校验成功后才推送更新。

新增分组或调整通用参数时，修改基础配置。使用整份更新的手机可以拉取这类改动。继续使用本地副本的用户只会收到已有规则集的变化。

## 脚本与失败处理

在仓库根目录运行：

```text
python scripts/validate.py
python scripts/validate.py --write-report
python scripts/sync_telegram.py
```

脚本使用 Python 标准库。定时同步从 Telegram 官方地址拉取 IP，验证网段、数量、公网属性及回归检查。有实际变更且通过校验才提交。

自动同步目前仅涵盖 Telegram 官方地址；Muse、ChatGPT、YouTube、X、国内域名和 Apple 地址由维护者核查后更新。不能把它理解为自动发现全部 App 新接口。

若 GitHub Actions 因账号/仓库设置禁用或计划调度暂停，查看 Actions 页面启用工作流。若机器人 push 被保护规则拦截，需改为审核发布流程；不要通过扩大账号 Token 权限解决。这里仅使用当前仓库的 GITHUB_TOKEN，不需要个人密码或长期 Token。

## 规则优先级与本地设置

苹果推送、Telegram、Muse、ChatGPT、OKX、YouTube、App Store、流媒体、社交、海外优先例外、国内、其余海外按模板顺序匹配。直连集收录明确的国内服务和局域网地址。未匹配的连接由 FINAL 交给「海外通用」。

本地副本的 RULE-SET 顺序不要随意调整。公共列表没有分组默认值，因此日常列表更新不会把 Muse/ChatGPT 改回 REJECT；节点订阅删除或改名、用户手动覆盖整个模板仍可能需要重新选择。

## 验证局限

首次在手机导入后，确认规则集下载成功 12/12，再检查节点选择和服务访问。后台更新时间由手机系统调度。

参考：[Shadowrocket 社区手册：自动更新与本地资源刷新](https://github.com/LOWERTOP/Shadowrocket#自动更新)。


## APNs 变体维护

维护入口是 `DailyRoute-OriginalPlus.conf`。合并到 main 后，GitHub Actions 自动生成代理版，设置其专用更新地址，并在内容变化时提交。需要在本地查看生成结果时，运行 `python scripts/build_variants.py`，再运行 `python scripts/validate.py`。两份配置共用 `rules/*.list`。
