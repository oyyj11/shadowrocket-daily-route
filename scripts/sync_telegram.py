"""Fetch official Telegram CIDRs; publish only after all validations pass."""
from pathlib import Path
import hashlib, ipaddress, json, urllib.request
from validate import validate

ROOT=Path(__file__).resolve().parents[1]
URL='https://core.telegram.org/resources/cidr.txt'

def main():
    data=urllib.request.urlopen(URL,timeout=45).read()
    lines=[l.strip() for l in data.decode('utf-8').splitlines() if l.strip()]
    assert 5<=len(lines)<=256,'Unexpected Telegram list size; retain last published rules'
    networks=[ipaddress.ip_network(l,strict=True) for l in lines]
    assert any(n.version==4 for n in networks) and any(n.version==6 for n in networks)
    assert all(n.is_global and n.prefixlen>0 for n in networks),'Non-global or default-route entry'
    assert len(set(networks))==len(networks),'Duplicate networks'
    p=ROOT/'rules'/'telegram.list'; prior_bytes=p.read_bytes(); prior=p.read_text(encoding='utf-8')
    retained=[l for l in prior.splitlines() if not l.startswith('IP-CIDR,') and not l.startswith('# Telegram CIDR source:')]
    updated='\n'.join(retained).rstrip()+'\n# Telegram CIDR source: '+URL+'\n'+'\n'.join(f'IP-CIDR,{n},no-resolve' for n in networks)+'\n'
    manifestpath=ROOT/'notification-sources.json'; oldmanifest_bytes=manifestpath.read_bytes(); oldmanifest=oldmanifest_bytes.decode('utf-8')
    reportpath=ROOT/'original-plus-validation.json'; oldreport_bytes=reportpath.read_bytes()
    try:
        p.write_text(updated,encoding='utf-8',newline='\n')
        manifest=json.loads(oldmanifest)
        manifest['telegram']={'url':URL,'sha256':hashlib.sha256(data).hexdigest(),'cidrs':[str(n) for n in networks]}
        manifestpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        validate(write=True)
    except Exception:
        p.write_bytes(prior_bytes)
        manifestpath.write_bytes(oldmanifest_bytes)
        reportpath.write_bytes(oldreport_bytes)
        raise
    print('Official Telegram addresses synchronized; local template/groups were not touched')

if __name__=='__main__': main()
