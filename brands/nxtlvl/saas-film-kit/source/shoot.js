const {chromium}=require('playwright');const jobs=require('./jobs.json');
(async()=>{const b=await chromium.launch();for(const [src,out,w,h,transparent] of jobs){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
await p.goto('file://'+src);await p.waitForTimeout(700);await p.screenshot({path:out,omitBackground:transparent});await p.close();console.log('ok',out.split('/').slice(-2).join('/'));}await b.close();})();
