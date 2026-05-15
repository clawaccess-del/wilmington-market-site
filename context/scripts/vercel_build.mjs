import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const root = process.cwd();
const out = join(root, 'public');

rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });

const entries = [
  'index.html',
  'contact.html',
  'app.js',
  'styles.css',
  'favicon.svg',
  'robots.txt',
  'sitemap.xml',
  'vercel.json',
  'assets',
  'services',
  'areas'
];

for (const entry of entries) {
  const from = join(root, entry);
  const to = join(out, entry);
  if (!existsSync(from)) {
    throw new Error(`Missing build entry: ${entry}`);
  }
  cpSync(from, to, { recursive: true });
}

console.log('Built static site into public/');
