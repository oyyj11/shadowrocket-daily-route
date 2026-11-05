from pathlib import Path
import concurrent.futures as cf
import urllib.request, hashlib, json, re, ipaddress, zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
CACHE = ROOT / 'work' / 'rules'
CACHE.mkdir(exist_ok=True)
BASE = 'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/'
SOURCES = [
 ('Lan','DIRECT'),
 ('OpenAI','AI服务'), ('Claude','AI服务'), ('Gemini','AI服务'),
 ('YouTube','YouTube'), ('Netflix','Netflix'), ('Disney','Disney'),
 ('Spotify','Spotify'), ('TikTok','TikTok'),
 ('Facebook','Muse与Meta'), ('Instagram','Muse与Meta'), ('Whatsapp','Muse与Meta'),
 ('Telegram','海外社交'), ('Twitter','海外社交'), ('Discord','海外社交'), ('Line','海外社交'),
 ('GitHub','开发工具'), ('Google','谷歌服务'),
 ('Apple','苹果服务'), ('Microsoft','微软服务'),
 ('Steam','游戏平台'), ('Epic','游戏平台'),
 ('ChinaMaxNoIP','DIRECT'),
]

def fetch(item):
    name, policy = item
    url = BASE + name + '/' + name + '.list'
    path = CACHE / (name + '.list')
    data = urllib.request.urlopen(url, timeout=45).read()
    body = data.decode('utf-8-sig')
    assert not body.lstrip().startswith('<'), name
    path.write_bytes(data)
    # 上游部分大集合把 DOMAIN / DOMAIN-SUFFIX 拆入配套 _Domain 文件。
    declared = sum(int(n) for n in re.findall(r'^# DOMAIN(?:-SUFFIX)?: (\d+)$', body, re.M))
    actual = sum(line.startswith(('DOMAIN,','DOMAIN-SUFFIX,')) for line in body.splitlines())
    companion = None
    if actual < declared:
        domain_url = BASE + name + '/' + name + '_Domain.list'
        domain_data = urllib.request.urlopen(domain_url, timeout=45).read()
        (CACHE / (name + '_Domain.list')).write_bytes(domain_data)
        converted=[]
        for line in domain_data.decode('utf-8-sig').splitlines():
            line=line.strip()
            if not line or line.startswith('#'): continue
            assert ',' not in line and ' ' not in line, (name,line)
            converted.append(('DOMAIN-SUFFIX,'+line[1:]) if line.startswith('.') else ('DOMAIN,'+line))
        assert len(converted)>0, name
        body += '\n# Companion source: '+domain_url+'\n'+'\n'.join(converted)+'\n'
        companion=dict(url=domain_url, sha256=hashlib.sha256(domain_data).hexdigest(), rules=len(converted))
    return name, policy, url, body, hashlib.sha256(data).hexdigest(), companion

with cf.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch, SOURCES))
print('Downloaded:', ', '.join(x[0] for x in results))

license_data = urllib.request.urlopen('https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/LICENSE', timeout=30).read()
(OUT / 'LICENSE-GPL-2.0.txt').write_bytes(license_data)

header = '''# Shadowrocket 日常分流配置 / 2026-11-05
# 本文件由 Codex 整理；内置规则来自 blackmatrix7/ios_rule_script，GPL-2.0。
# 上游：https://github.com/blackmatrix7/ios_rule_script
# 本地修改：合并分组、补充 Muse 和 AI 核心域名、国内仅保留域名规则、去重。
# 完整许可证及来源见随附文件。无担保；未在你的 iPhone 上运行验证。
# 这是完整主配置，不是模块。已有节点订阅继续在首页管理，本文件不提供节点。
# 国内直连使用手机当前 Wi-Fi/蜂窝网络，不代表强制切到蜂窝。
# 主配置内置规则为日期快照，不自动更新；不包含远程脚本或 HTTPS 解密。
# 先备份旧配置、暂时关闭旧模块，再导入本文件，首页全局路由选“配置”。

[General]
skip-proxy = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,localhost,*.local
tun-excluded-routes = 10.0.0.0/8,127.0.0.0/8,169.254.0.0/16,172.16.0.0/12,192.168.0.0/16,224.0.0.0/4
dns-server = https://dns.alidns.com/dns-query,https://doh.pub/dns-query
fallback-dns-server = system
ipv6 = true
prefer-ipv6 = false
dns-direct-system = false
private-ip-answer = true
dns-direct-fallback-proxy = false
udp-policy-not-supported-behaviour = REJECT

[Proxy Group]
# PROXY 是首页选择的节点；“手动节点”可从现有节点中选择。
# AI/Muse 默认使用 PROXY，请在首次使用时选定一个实际可用的稳定节点。
'''
groups = []
groups.append('手动节点 = select,PROXY,policy-regex-filter=^(?!(.*(剩余|到期|过期|流量|官网|套餐|重置))).*$,policy-select-name=PROXY')
auto = dict(自动测速='^(?!(.*(剩余|到期|过期|流量|官网|套餐|重置))).*$',
            香港测速='香港|🇭🇰|(?i:hong|\\bhk\\b)',
            台湾测速='台湾|台灣|🇹🇼|(?i:taiwan|taipei|\\btw\\b)',
            日本测速='日本|东京|大阪|🇯🇵|(?i:japan|tokyo|\\bjp\\b)',
            新加坡测速='新加坡|狮城|🇸🇬|(?i:singapore|\\bsg\\b)',
            美国测速='美国|美國|洛杉矶|西雅图|纽约|🇺🇸|(?i:united states|america|\\bus\\b|\\busa\\b)')
for name, pattern in auto.items():
    groups.append(f'{name} = url-test,policy-regex-filter={pattern},url=https://www.gstatic.com/generate_204,interval=900,tolerance=100,timeout=5')
choices = '自动测速,手动节点,香港测速,台湾测速,日本测速,新加坡测速,美国测速,PROXY'
groups.append(f'海外默认 = select,{choices},policy-select-name=自动测速')
for name in ['AI服务','Muse与Meta','Netflix','Disney','Spotify','TikTok']:
    groups.append(f'{name} = select,PROXY,手动节点,美国测速,日本测速,新加坡测速,香港测速,台湾测速,海外默认,policy-select-name=PROXY')
for name in ['YouTube','海外社交','开发工具','谷歌服务']:
    groups.append(f'{name} = select,海外默认,手动节点,香港测速,台湾测速,日本测速,新加坡测速,美国测速,PROXY,policy-select-name=海外默认')
for name in ['苹果服务','微软服务','游戏平台']:
    groups.append(f'{name} = select,DIRECT,海外默认,手动节点,PROXY,policy-select-name=DIRECT')

lines = [header, '\n'.join(groups), '\n[Rule]', '# 自定义规则请加在这里，位于下方内置规则之前。']
custom = []
def suffix(domain, policy):
    custom.append(f'DOMAIN-SUFFIX,{domain},{policy}')
for domain in ['muse.ai','meta.ai','meta.com','facebook.com','facebook.net','fbcdn.net','fbsbx.com','fb.com','instagram.com','cdninstagram.com','whatsapp.com','whatsapp.net']:
    suffix(domain,'Muse与Meta')
for domain in ['chatgpt.com','chat.com','openai.com','oaistatic.com','oaiusercontent.com','sora.com','claude.ai','anthropic.com','gemini.google.com','generativelanguage.googleapis.com','aistudio.google.com','ai.google.dev','notebooklm.google','notebooklm.google.com','grok.com','x.ai','perplexity.ai','pplx.ai','openrouter.ai']:
    suffix(domain,'AI服务')
for domain in ['qq.com','weixin.qq.com','wechat.com','tenpay.com','alipay.com','alipayobjects.com','taobao.com','tmall.com','alicdn.com','jd.com','360buyimg.com','pinduoduo.com','yangkeduo.com','meituan.com','dianping.com','ele.me','bilibili.com','bilivideo.com','biliapi.net','hdslb.com','douyin.com','douyincdn.com','snssdk.com','xiaohongshu.com','xhscdn.com','zhihu.com','zhimg.com','baidu.com','bdstatic.com','amap.com','gaode.com','163.com','126.com','music.163.com','iqiyi.com','youku.com','deepseek.com','kimi.com','moonshot.cn','doubao.com','qianwen.com','ccb.com','icbc.com.cn','abchina.com','boc.cn','cmbchina.com']:
    suffix(domain,'DIRECT')
lines += ['# Muse 与 Meta 登录相关域名共用出口；其他接口仍需按实际连接记录补充。'] + custom
seen = set()
for item in custom:
    p=item.split(','); seen.add(tuple(p[:2]))
manifest = []
allowed = {'DOMAIN','DOMAIN-SUFFIX','DOMAIN-KEYWORD','IP-CIDR','IP-CIDR6','IP-ASN'}
rule_records = []
for name, policy, url, body, digest, companion in results:
    lines += ['', f'# --- {name} | author: blackmatrix7 | {url} ---']
    lines += [s for s in body.splitlines() if s.startswith('#')]
    count = 0
    skipped = 0
    for raw in body.splitlines():
        raw = raw.strip()
        if not raw or raw.startswith('#'): continue
        p = [v.strip() for v in raw.split(',')]
        if p[0] not in allowed:
            skipped += 1; continue
        # 国内集合只用明确域名，避免 UA 和“stripe”等宽泛关键词误直连。
        if name == 'ChinaMaxNoIP' and p[0] not in {'DOMAIN','DOMAIN-SUFFIX'}:
            skipped += 1; continue
        assert len(p) >= 2 and p[1], (name, raw)
        key = tuple(p[:2])
        if key in seen:
            skipped += 1; continue
        seen.add(key)
        opts = p[2:]
        assert all(v == 'no-resolve' for v in opts), (name, raw)
        # IP 条目不主动触发 DNS；域名优先，国内 GEOIP 在最后兜底。
        if p[0].startswith('IP-') and 'no-resolve' not in opts: opts += ['no-resolve']
        compiled = ','.join(p[:2] + [policy] + opts)
        lines.append(compiled); rule_records.append((p[0],p[1],policy)); count += 1
    manifest.append(dict(name=name, url=url, sha256=digest, companion=companion, imported=count, skipped=skipped))
lines += ['', '# 国内 IP 直连，其余请求走海外默认。', 'GEOIP,CN,DIRECT', 'FINAL,海外默认', '']
config = '\n'.join(lines)
path=OUT/'Shadowrocket-Daily.conf'
path.write_text(config, encoding='utf-8')
(OUT/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

# 静态检查：组引用、循环、规则语法、示例域名的首条域名匹配。
names = {g.split(' = ')[0] for g in groups}
builtins = {'DIRECT','PROXY','REJECT'}
edges={}
for g in groups:
    name,rest=g.split(' = ',1)
    members=[p for p in rest.split(',')[1:] if '=' not in p]
    assert all(x in names|builtins for x in members),(name,members)
    edges[name]=[m for m in members if m in names]
def cycle(node,stack):
    assert node not in stack, stack+[node]
    for child in edges[node]: cycle(child,stack+[node])
for name in names: cycle(name,[])
section=''; parsed=[]
for line in config.splitlines():
    if line.startswith('['): section=line
    if section!='[Rule]' or not line or line.startswith(('#','[')): continue
    p=line.split(',')
    target=p[1] if p[0]=='FINAL' else p[2]
    assert target in names|builtins, line
    if p[0] in {'IP-CIDR','IP-CIDR6'}: ipaddress.ip_network(p[1],strict=False)
    parsed.append(p)
assert sum(x[0]=='FINAL' for x in parsed)==1 and parsed[-1][0]=='FINAL'
def match(domain):
    for p in parsed:
        kind=p[0]
        if kind=='DOMAIN' and domain==p[1] or kind=='DOMAIN-SUFFIX' and (domain==p[1] or domain.endswith('.'+p[1])) or kind=='DOMAIN-KEYWORD' and p[1] in domain:
            return p[2]
    return '海外默认'
examples={'muse.ai':'Muse与Meta','www.facebook.com':'Muse与Meta','chatgpt.com':'AI服务','gemini.google.com':'AI服务','www.youtube.com':'YouTube','www.netflix.com':'Netflix','www.disneyplus.com':'Disney','open.spotify.com':'Spotify','www.tiktok.com':'TikTok','api.telegram.org':'海外社交','github.com':'开发工具','www.google.com':'谷歌服务','www.apple.com':'苹果服务','www.microsoft.com':'微软服务','store.steampowered.com':'游戏平台','www.taobao.com':'DIRECT','www.jd.com':'DIRECT','www.bilibili.com':'DIRECT','www.douyin.com':'DIRECT','www.xiaohongshu.com':'DIRECT','www.deepseek.com':'DIRECT','www.icbc.com.cn':'DIRECT'}
checks={}
for domain,expected in examples.items():
    got=match(domain); assert got==expected,(domain,got,expected)
    checks[domain]=got
report={'rules':len(parsed),'groups':len(names),'bytes':path.stat().st_size,'domain_checks':checks,'notes':'静态检查通过；并非 Shadowrocket 客户端运行或节点测速。'}
(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
