// gate G5: open deck.html in a real browser and check every slide.
// usage: node pipeline/render_check.js topic-pronunciation
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const topic = path.resolve(process.argv[2]);
const drafts = fs.readdirSync(path.join(topic, 'drafts')).filter(f => f.endsWith('.md')).sort();

(async () => {
  const browser = await chromium.launch();
  const problems = [];

  for (const [label, viewport] of [['desktop', { width: 1280, height: 720 }], ['phone', { width: 390, height: 844 }]]) {
    const page = await browser.newPage({ viewport });
    await page.goto('file://' + path.join(topic, 'deck.html'));
    await page.waitForTimeout(400);

    const count = await page.locator('.slide').count();
    if (count !== drafts.length) problems.push(`${label}: ${count} slides but ${drafts.length} drafts`);

    for (let i = 0; i < count; i++) {
      await page.keyboard.press(i === 0 ? 'Home' : 'ArrowRight');  // use the real keyboard nav so we test it too
      const info = await page.evaluate(() => {
        const s = document.querySelector('.slide.on');
        return {
          n: s ? Number(s.dataset.n) : -1,
          // content taller than the box = text cut off on a projector
          overflowY: s ? s.scrollHeight - s.clientHeight : 0,
          overflowX: s ? s.scrollWidth - s.clientWidth : 0,
          pageX: document.documentElement.scrollWidth - window.innerWidth,
          sources: s ? s.querySelectorAll('.src a').length : 0,
          buttons: s ? s.querySelectorAll('.say').length : 0,
        };
      });
      const want = (fs.readFileSync(path.join(topic, 'drafts', drafts[i]), 'utf8').match(/^\s*-?\s*🔊/gm) || []).length;
      const tag = `${label} slide ${String(i + 1).padStart(2, '0')}`;
      if (info.n !== i + 1) problems.push(`${tag}: arrow key showed slide ${info.n}`);
      // on phones a slide may scroll inside itself, but it must never scroll sideways
      if (label === 'desktop' && info.overflowY > 1) problems.push(`${tag}: content overflows by ${info.overflowY}px`);
      if (info.overflowX > 1 || info.pageX > 1) problems.push(`${tag}: sideways overflow`);
      if (info.sources < 1) problems.push(`${tag}: no source links in footer`);
      if (info.buttons !== want) problems.push(`${tag}: ${info.buttons} 🔊 buttons but draft has ${want} examples`);
    }

    // a script can't hear the 🔊, but it can check we never fail silently:
    // if this browser has no french voice, clicking 🔊 must show the warning
    if (label === 'desktop') {
      await page.evaluate(() => show(2));  // jump to slide 3, it has 🔊 buttons (home key isn't wired up)
      await page.locator('.slide.on .say').first().click();
      await page.waitForTimeout(300);
      const v = await page.evaluate(() => ({
        fr: speechSynthesis.getVoices().filter(x => x.lang.startsWith('fr')).length,
        warned: getComputedStyle(document.getElementById('voiceMsg')).display !== 'none',
      }));
      if (v.fr === 0 && !v.warned) problems.push('🔊 clicked with no french voice on this device, but no warning shown (silent button)');
    }
    await page.close();
  }
  await browser.close();

  if (problems.length) {
    console.log(`FAIL G5 render: ${problems.length} problem(s)`);
    problems.forEach(p => console.log('  - ' + p));
    process.exit(1);
  }
  console.log('PASS G5 render');
})();
