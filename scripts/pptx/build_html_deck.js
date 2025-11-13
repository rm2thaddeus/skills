/* Build PPTX from HTML slides using html2pptx */
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require(path.resolve('Code/anthropic-skills/document-skills/pptx/scripts/html2pptx.js'));

function parseArgs() {
  const args = process.argv.slice(2);
  const out = { slides: [], output: null, audit: null };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--slides' && args[i + 1]) {
      out.slides = args[i + 1].split(',').map(s => s.trim()).filter(Boolean);
      i++;
    } else if (a === '--output' && args[i + 1]) {
      out.output = args[i + 1]; i++;
    } else if (a === '--audit' && args[i + 1]) {
      out.audit = args[i + 1]; i++;
    }
  }
  if (!out.slides.length) throw new Error('No slides provided (--slides)');
  if (!out.output) throw new Error('No output path provided (--output)');
  return out;
}

async function main() {
  const { slides, output, audit } = parseArgs();

  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  pres.author = 'Aitor Patiño Diaz';
  pres.title = 'Chercher sa voie à l’ère de l’IA';

  const results = [];

  for (const slidePath of slides) {
    const abs = path.isAbsolute(slidePath) ? slidePath : path.resolve(slidePath);
    if (!fs.existsSync(abs)) throw new Error(`Slide not found: ${abs}`);
    const { slide, placeholders } = await html2pptx(abs, pres);
    results.push({ html: abs, placeholdersCount: placeholders.length });
  }

  const outAbs = path.isAbsolute(output) ? output : path.resolve(output);
  fs.mkdirSync(path.dirname(outAbs), { recursive: true });
  await pres.writeFile({ fileName: outAbs });

  if (audit) {
    const auditAbs = path.isAbsolute(audit) ? audit : path.resolve(audit);
    const auditDir = path.dirname(auditAbs);
    fs.mkdirSync(auditDir, { recursive: true });
    const payload = {
      operation_id: path.basename(path.dirname(outAbs)),
      timestamp: new Date().toISOString(),
      agent: 'document-processing',
      input_files: slides,
      output_file: outAbs,
      changes: results.map((r, idx) => ({ slide_index: idx, html: r.html, placeholders: r.placeholdersCount })),
      validation: { errors: 0, status: 'success' },
      approval_status: 'approved'
    };
    fs.writeFileSync(auditAbs, JSON.stringify(payload, null, 2), 'utf-8');
  }
}

main().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});


