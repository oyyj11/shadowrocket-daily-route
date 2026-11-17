// DailyRoute-FlClash v1.0.0
// FlClash 0.8.92 per-subscription overwrite. No credentials.
const main = (config) => {
  const group = 'OpenAI-Google-US';
  const us = (config.proxies || []).map(p => p.name).filter(n => /美国|美國|🇺🇸|\bUSA?\b|United States/i.test(n) && !/到期|流量|剩余|官网/.test(n));
  if (!us.length) throw new Error('No US nodes found; refusing to route OpenAI/Google through another country');
  config['proxy-groups'] = (config['proxy-groups'] || []).filter(g => g.name !== group);
  config['proxy-groups'].unshift({name: group, type:'fallback', proxies:us, url:'https://www.gstatic.com/generate_204', interval:300, lazy:true});
  const processes = ['ChatGPT.exe','Codex.exe','codex.exe','codex-code-mode-host.exe','codex-computer-use-swift.exe','codex-windows-sandbox-service.exe','GoogleDriveFS.exe'];
  const domains = ['openai.com','chatgpt.com','chat.com','oaistatic.com','oaiusercontent.com','sora.com','openaiapi-site.azureedge.net','openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net','production-openaicom-storage.azureedge.net','chatgpt.livekit.cloud','google.com','googleapis.com','gstatic.com','googleusercontent.com','googlevideo.com','youtube.com','youtu.be','ytimg.com','ggpht.com','gmail.com','googlemail.com','googlesyndication.com','doubleclick.net','googleadservices.com','googletagmanager.com','googletagservices.com','google-analytics.com','g.co','google.cn','google.com.hk','android.com','android.googleapis.com','firebaseio.com','firebaseapp.com','firebase.google.com','appspot.com','withgoogle.com','withyoutube.com','recaptcha.net'];
  const prefix = [...processes.map(n => `PROCESS-NAME,${n},${group}`), ...domains.map(n => `DOMAIN-SUFFIX,${n},${group}`), `GEOSITE,openai,${group}`, `GEOSITE,google,${group}`, `GEOSITE,youtube,${group}`];
  config.rules = [...prefix, ...(config.rules || []).filter(r => !r.endsWith(',' + group))];
  config.mode='rule';
  config['find-process-mode']='always';
  return config;
};
