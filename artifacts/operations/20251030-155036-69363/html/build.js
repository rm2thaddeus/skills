const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require('../../../../Code/anthropic-skills/document-skills/pptx/scripts/html2pptx');

const IMAGE_MAP = {
  'yearly.html': ['applications_by_year_bar.png'],
  'monthly.html': ['applications_by_month_line.png'],
  'heatmap.html': ['year_month_heatmap.png'],
  'overlay.html': ['compare_2022_vs_2025_monthly.png'],
  'cumulative.html': ['compare_2022_vs_2025_cumulative.png'],
  'weekday.html': ['compare_2022_vs_2025_weekday.png'],
  'topcompanies.html': ['top_companies_2022.png', 'top_companies_2025.png'],
  'periods.html': ['applications_by_week_line.png']
};

async function main() {
  const root = __dirname;
  const slidesDir = path.join(root, 'slides');
  const slidesList = JSON.parse(fs.readFileSync(path.join(slidesDir, 'slides.json'), 'utf8'));
  const outFile = path.join(path.dirname(root), 'output', 'applications_2022_vs_2025_html2pptx.pptx');

  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Aitor';
  pptx.title = 'Applications 2022 vs 2025';

  for (const item of slidesList) {
    const htmlPath = path.join(slidesDir, item.file);
    const { slide, placeholders } = await html2pptx(htmlPath, pptx);

    const imgs = IMAGE_MAP[item.file] || [];
    if (imgs.length && placeholders && placeholders.length) {
      if (item.file === 'topcompanies.html' && placeholders.length >= 2) {
        const left = placeholders.find(p => p.id === 'left') || placeholders[0];
        const right = placeholders.find(p => p.id === 'right') || placeholders[1];
        slide.addImage({ path: path.join(slidesDir, imgs[0]), x: left.x, y: left.y, w: left.w, h: left.h });
        slide.addImage({ path: path.join(slidesDir, imgs[1]), x: right.x, y: right.y, w: right.w, h: right.h });
      } else {
        const ph = placeholders[0];
        slide.addImage({ path: path.join(slidesDir, imgs[0]), x: ph.x, y: ph.y, w: ph.w, h: ph.h });
      }
    }
  }

  await pptx.writeFile({ fileName: outFile });
  console.log(outFile);
}

main().catch(err => { console.error(err); process.exit(1); });
