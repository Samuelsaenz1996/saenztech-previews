// Usage: node shot.js <site_dir> [chromium_path]
// Writes preview.png (phone, home first screen), preview-full.png (phone, home full page),
// desktop.png (desktop, home full page) and shots/<page>-phone.png + shots/<page>-desktop.png for every page.
// Prints JSON with fonts loaded and any page that overflows horizontally.
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');
(async () => {
  const dir = path.resolve(process.argv[2]);
  const exe = process.argv[3] || process.env.CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? undefined : undefined);
  let pages = [''];
  try { pages = JSON.parse(fs.readFileSync(path.join(dir, 'pages.json'), 'utf8')); } catch (e) {}
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const ctxP = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const ctxD = await b.newContext({ viewport: { width: 1440, height: 900 } });
  // map embeds need the network; never let them block a screenshot
  for (const c of [ctxP, ctxD]) await c.route(/google\.com\/maps/, r => r.abort());
  fs.mkdirSync(path.join(dir, 'shots'), { recursive: true });
  const overflow = [];
  let fonts = [];
  for (const pg of pages) {
    const url = 'file://' + path.join(dir, pg, 'index.html');
    const name = pg || 'home';
    const phone = await ctxP.newPage();
    await phone.goto(url, { waitUntil: 'load' });
    await phone.evaluate(() => document.fonts.ready);
    if (!pg) {
      await phone.screenshot({ path: path.join(dir, 'preview.png') });
      fonts = await phone.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))]);
    }
    await phone.addStyleTag({ content: '.callbar{display:none!important}.top{position:static!important}' });
    if (!pg) await phone.screenshot({ path: path.join(dir, 'preview-full.png'), fullPage: true });
    await phone.screenshot({ path: path.join(dir, 'shots', name + '-phone.png'), fullPage: true });
    if (await phone.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)) overflow.push(name);
    await phone.close();
    const desk = await ctxD.newPage();
    await desk.goto(url, { waitUntil: 'load' });
    await desk.evaluate(() => document.fonts.ready);
    await desk.addStyleTag({ content: '.top{position:static!important}' });
    if (!pg) await desk.screenshot({ path: path.join(dir, 'desktop.png'), fullPage: true });
    await desk.screenshot({ path: path.join(dir, 'shots', name + '-desktop.png'), fullPage: true });
    await desk.close();
  }
  await b.close();
  console.log(JSON.stringify({ dir, pages: pages.map(p => p || '/'), fonts, horizontalOverflow: overflow.length > 0, overflowPages: overflow }));
})();
