"""Validate the local-template/remote-rule boundary and routing regressions."""
from pathlib import Path
import hashlib, ipaddress, json, re, sys
from build_variants import expected_proxy

ROOT=Path(__file__).resolve().parents[1]
BASE='https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/'

def validate(write=False):
    source=(ROOT/'DailyRoute-OriginalPlus.conf').read_text(encoding='utf-8')
    variant=(ROOT/'DailyRoute-APNs-Proxy.conf').read_text(encoding='utf-8')
    assert variant==expected_proxy(source), 'APNs variant drifted: rebuild with scripts/build_variants.py'
    assert not re.search(r'^\s*update-url\s*=',source,re.M), 'Main template must not have a full-update URL'
    assert not any(x in source for x in ['[Script]','[MITM]','[Proxy]\n']), 'No credentials or interception in shared template'
    groupbody=source.split('[Proxy Group]\n',1)[1].split('[Rule]\n',1)[0]
    definitions=[l for l in groupbody.splitlines() if l and not l.startswith('#')]
    names={l.split(' = ')[0] for l in definitions}
    edges={}
    for definition in definitions:
        name,body=definition.split(' = ',1)
        fields=body.split(',')
        members=[p for p in fields[1:] if '=' not in p]
        assert all(p in names|{'PROXY','DIRECT','REJECT'} for p in members),(name,members)
        edges[name]=[m for m in members if m in names]
        if name in {'Muse美国','ChatGPT日本'}:
            assert fields[0]=='select' and members==['REJECT'] and 'policy-regex-filter=' in body, 'Country groups cannot fall back to home node'
    def visit(node,stack):
        assert node not in stack,stack+[node]
        for child in edges[node]: visit(child,stack+[node])
    for node in names: visit(node,[])
    main=[l.split(',') for l in source.split('[Rule]\n',1)[1].split('[Host]\n',1)[0].splitlines() if l and not l.startswith('#')]
    assert main[-2:]==[['GEOIP','CN','DIRECT'],['FINAL','海外通用']]
    compiled=[]; stats=[]; checked=set()
    for p in main[:-2]:
        assert len(p)==3 and p[0]=='RULE-SET' and p[1].startswith(BASE+'rules/') and p[2] in names|{'DIRECT'},p
        relative=p[1][len(BASE):]
        assert re.fullmatch(r'rules/[a-z-]+\.list',relative),relative
        file=ROOT/relative; assert file.exists(),relative
        checked.add(relative)
        data=file.read_text(encoding='utf-8').encode('utf-8'); lines=data.decode('utf-8').splitlines(); count=0
        for line in lines:
            if not line or line.startswith('#'): continue
            v=line.split(','); kind=v[0]
            assert kind in {'DOMAIN','DOMAIN-SUFFIX','DOMAIN-KEYWORD','IP-CIDR','IP-ASN','USER-AGENT'},(relative,line)
            assert len(v) in {2,3} and v[1] and not any(c.isspace() for c in v[1]),line
            if len(v)==3: assert v[2]=='no-resolve' and kind in {'IP-CIDR','IP-ASN'},line
            if kind=='IP-CIDR': ipaddress.ip_network(v[1],strict=True)
            if kind=='IP-ASN': assert v[1].isdigit(),line
            compiled.append(v[:2]+[p[2]]+v[2:]); count+=1
        assert count>0,relative
        stats.append({'file':relative,'policy':p[2],'rules':count,'sha256':hashlib.sha256(data).hexdigest()})
    assert checked=={str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/'rules').glob('*.list')},'Unreferenced or missing rule set'
    def match(host):
        try: addr=ipaddress.ip_address(host)
        except ValueError: addr=None
        for p in compiled:
            k=p[0]
            if addr is None:
                if k=='DOMAIN' and host==p[1] or k=='DOMAIN-SUFFIX' and (host==p[1] or host.endswith('.'+p[1])) or k=='DOMAIN-KEYWORD' and p[1] in host: return p[2]
            elif k=='IP-CIDR':
                n=ipaddress.ip_network(p[1])
                if addr.version==n.version and addr in n: return p[2]
        return '海外通用'
    reportpath=ROOT/'original-plus-validation.json'
    report=json.loads(reportpath.read_text(encoding='utf-8'))
    tests=report['domain_tests']
    # Preserve higher-priority Apple Intelligence / Copilot exceptions as well.
    tests.update({'apple-relay.apple.com':'海外通用','copilot.microsoft.com':'海外通用'})
    for host,expected in tests.items(): assert match(host)==expected,(host,match(host),expected)
    report.update(release='v1.3',rules=len(compiled)+2,groups=len(names),rule_sets=stats,domain_tests=tests,scope='Static rule/priority checks only; no Shadowrocket runtime, node geolocation, throughput or notification-delivery verification.',config_sha256=hashlib.sha256(source.encode()).hexdigest(),apns_proxy_variant_sha256=hashlib.sha256(variant.encode()).hexdigest(),variant_only_changes_apns_default=True)
    if write: reportpath.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'OK: {len(stats)} remote sets, {len(compiled)+2} rules, {len(names)} local groups, {len(tests)} regression cases')
    return report

if __name__=='__main__': validate('--write-report' in sys.argv)
