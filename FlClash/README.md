# FlClash：OpenAI / Google 美国分流

适用于已核对源码和本机运行配置的 FlClash 0.8.92。新版客户端的入口可能不同。

## 两种更新，各管一件事

- **原机场订阅 → 同步**：更新节点、额度、原有规则。不要把订阅 URL 改成这里的 JS 地址。
- **运行一键更新 → 退出并重开 FlClash**：从本仓库更新美国分流覆写脚本。以后修改规则，只需继续用同一更新入口。

公开仓库只放规则代码。机场链接、令牌、节点密码及完整私人 YAML 不应上传。

## 本次电脑已安装

脚本绑定在原订阅 `gw树洞.yaml` 上，脚本 ID 为 `202611170001`。首页使用**规则**模式。
本机已生成的配置包含 `OpenAI-Google-US` 分组和置顶进程规则，但未据此验证每个节点的真实美国出口或所有服务可用性。

下载 [更新器](./Update-FlClash-Rules.ps1)，用 PowerShell 运行。此更新器只替换已有绑定脚本，不修改订阅，也不自动关闭应用。下载失败时保留旧脚本，旧版本备份在 FlClash 的 `scripts/dailyroute-backups` 下。

本次电脑另有本地双击入口。更新成功后，从 FlClash 托盘菜单退出，再重新打开，确认仍为规则模式。

## 其他电脑手动安装

1. 下载 [覆写脚本](https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/FlClash/OpenAI-Google-US.js)。
2. 在 FlClash 的脚本管理中导入或新建脚本，把此文件内容完整保存。
3. 当前订阅卡片的「更多」中找到覆写设置，选择脚本方式并绑定该脚本。不同版本菜单名称可能不同。
4. 使用规则模式，在代理列表确认出现 `OpenAI-Google-US`。如使用更新器，需要将 `-ScriptId` 改成实际绑定脚本文件名中的数字。

## 路由行为与边界

- OpenAI、ChatGPT、Sora、Codex 已知域名及进程规则优先走美国组。
- Google、YouTube、Gmail、Gemini 等使用显式域名和内核 `GEOSITE,google/youtube` 覆盖，Google Drive 桌面进程也进入美国组。
- 仅筛选订阅中名称含美国、US 等标识的节点。美国组使用 fallback，优先保持节点，故障时换另一个美国节点；不回落到日本、香港或 DIRECT。
- 无美国节点时脚本报错。客户端可能保留上一次已加载配置，不能把脚本失败视为全机断网保护。
- 节点名称不是出口地区证明。Google 的连通性测试也不是 OpenAI 解锁验证，仍需实际使用核对。
- 保留原机场其余分流规则。规则模式不等于匿名或自动消除账户、Cookie、浏览器位置等影响。
- 不把整个 Chrome/Edge、node.exe/python.exe 等通用进程送去美国。Codex 启动的这些子进程按目标域名匹配；未来新增程序名和域名需要补充。
- 显式进程规则需要流量进入内核并能识别进程。TUN/系统代理设置和程序自设代理也会影响接管范围，不承诺捕获所有 EXE 流量。
- 更换客户端、开启全局/直连模式、同时启用另一套 TUN，都会影响这些规则。不要同时开启两套代理客户端的 TUN/系统代理。

## 维护与校验

修改 `OpenAI-Google-US.js` 后运行 `node FlClash/test.cjs`，提交到 main。GitHub Actions 自动检查规则逻辑。该检查不包含真实节点地区、网速或账户服务可用性测试。

脚本模式在加载订阅后、生成运行配置前应用，依据 [FlClash v0.8.92 源码](https://github.com/chen08209/FlClash/blob/v0.8.92/lib/controller.dart)。本版数据库中的脚本没有远程 URL 字段，因此订阅卡片「同步」不会从 GitHub 同步此脚本，本更新器负责这一步。
