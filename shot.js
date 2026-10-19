// Usage: node shot.js <site_dir> [chromium_path]
// Writes preview.png (phone first screen), preview-full.png (phone full page), desktop.png
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const dir = path.resolve(process.argv[2]);
  const exe = process.argv[3] || process.env.CHROME || undefined;
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const url = 'file://' + dir + '/index.html';
  const phone = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await phone.goto(url, { waitUntil: 'load' });
  await phone.evaluate(() => document.fonts.ready);
  await phone.screenshot({ path: dir + '/preview.png' });
  await phone.addStyleTag({ content: '.callbar{display:none!important}' });
  await phone.screenshot({ path: dir + '/preview-full.png', fullPage: true });
  const fams = await phone.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))]);
  const overflow = await phone.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  const desk = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await desk.goto(url, { waitUntil: 'load' });
  await desk.evaluate(() => document.fonts.ready);
  await desk.screenshot({ path: dir + '/desktop.png', fullPage: true });
  await b.close();
  console.log(JSON.stringify({ dir, fonts: fams, horizontalOverflow: overflow }));
})();
