"""Generate APNs proxy defaults without changing other routing policies."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DIRECT='苹果推送 = select,DIRECT,PROXY,手动节点,policy-select-name=DIRECT'
PROXY='苹果推送 = select,PROXY,DIRECT,手动节点,policy-select-name=PROXY'

def expected_proxy(source):
    assert source.count(DIRECT)==1
    assert source.count('# APNs 默认：DIRECT')==1
    return source.replace(DIRECT,PROXY,1).replace('# APNs 默认：DIRECT','# APNs 默认：PROXY',1)

if __name__=='__main__':
    source=(ROOT/'DailyRoute-OriginalPlus.conf').read_text(encoding='utf-8')
    (ROOT/'DailyRoute-APNs-Proxy.conf').write_text(expected_proxy(source),encoding='utf-8',newline='\n')
    print('APNs proxy variant generated; all other settings identical')
