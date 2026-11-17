const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(__dirname + '/OpenAI-Google-US.js', 'utf8');
function apply(config) { return JSON.parse(JSON.stringify(vm.runInNewContext(source + ';main(config)', {config}, {timeout: 1000}))); }
const original = {proxies:[{name:'美国 US 01'}, {name:'日本 JP 01'}, {name:'🇺🇸 US 02'}], 'proxy-groups':[{name:'Original',type:'select',proxies:['日本 JP 01']}],rules:['DOMAIN-SUFFIX,qq.com,DIRECT','GEOIP,CN,DIRECT','MATCH,Original']};
const out = apply(structuredClone(original));
assert.deepEqual(out['proxy-groups'][0].proxies, ['美国 US 01','🇺🇸 US 02']);
assert.equal(out['proxy-groups'][0].type,'fallback');
assert.equal(out.rules[0],'PROCESS-NAME,ChatGPT.exe,OpenAI-Google-US');
assert(out.rules.includes('GEOSITE,google,OpenAI-Google-US'));
assert(out.rules.includes('GEOSITE,openai,OpenAI-Google-US'));
assert(!out.rules.some(r => r.startsWith('PROCESS-NAME,chrome.exe,')));
assert.deepEqual(out.rules.slice(-3),original.rules);
assert.deepEqual(apply(structuredClone(out)),out);
assert.throws(()=>apply({proxies:[{name:'日本 JP 01'}]}), /No US nodes/);
console.log('PASS: US-only selection, rule priority, original routing, idempotency, no-US rejection');
