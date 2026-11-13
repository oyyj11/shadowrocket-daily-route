"""Generate the APNs proxy profile and its matching update URL."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE_URL = 'https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/'
DIRECT_FILENAME = 'DailyRoute-OriginalPlus.conf'
PROXY_FILENAME = 'DailyRoute-APNs-Proxy.conf'
DIRECT='苹果推送 = select,DIRECT,PROXY,手动节点,policy-select-name=DIRECT'
PROXY='苹果推送 = select,PROXY,DIRECT,手动节点,policy-select-name=PROXY'

def expected_proxy(source):
    assert source.count(DIRECT)==1
    assert source.count('# APNs 默认：DIRECT')==1
    direct_update = f'update-url = {BASE_URL}{DIRECT_FILENAME}\n'
    proxy_update = f'update-url = {BASE_URL}{PROXY_FILENAME}\n'
    assert source.splitlines().count(direct_update.rstrip('\n')) == 1, 'Incorrect base profile update URL'
    return (
        source.replace(DIRECT, PROXY, 1)
        .replace('# APNs 默认：DIRECT', '# APNs 默认：PROXY', 1)
        .replace(direct_update, proxy_update, 1)
    )

if __name__=='__main__':
    source=(ROOT/DIRECT_FILENAME).read_text(encoding='utf-8')
    (ROOT/PROXY_FILENAME).write_text(expected_proxy(source),encoding='utf-8',newline='\n')
    print('Generated APNs proxy profile with its own update URL')
