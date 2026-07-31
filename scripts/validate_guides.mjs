import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const expected = [
  "beauty-skincare",
  "3c-digital",
  "electronics-packaging",
  "food-beverage",
  "coffee-bean-packaging",
  "ecommerce-retail",
  "tea-packaging",
  "apparel-packaging",
  "gift-box-custom",
  "health-supplement-packaging",
  "carton-customization",
  "individual-packaging",
  "xiaopiliang-baozhuang-dingzhi"
];
const upgraded = expected.filter((slug) => slug !== "coffee-bean-packaging");
const errors = [];
const titles = new Map();
const descriptions = new Map();

const fail = (message) => errors.push(message);
const match = (html, pattern, label, slug) => {
  const result = html.match(pattern);
  if (!result) {
    fail(`${slug}: missing ${label}`);
    return "";
  }
  return result[1].trim();
};

for (const slug of expected) {
  const file = resolve(root, slug, "index.html");
  if (!existsSync(file)) {
    fail(`${slug}: index.html does not exist`);
    continue;
  }
  const html = readFileSync(file, "utf8");
  const title = match(html, /<title>([^<]+)<\/title>/, "title", slug);
  const description = match(html, /<meta name="description" content="([^"]+)"/, "meta description", slug);
  const canonical = match(html, /<link rel="canonical" href="([^"]+)"/, "canonical", slug);
  const expectedCanonical = `https://guide.bubbpackage.com/${slug}/`;

  if (canonical && canonical !== expectedCanonical) {
    fail(`${slug}: canonical is ${canonical}`);
  }
  if (titles.has(title)) fail(`${slug}: duplicate title with ${titles.get(title)}`);
  if (descriptions.has(description)) fail(`${slug}: duplicate description with ${descriptions.get(description)}`);
  titles.set(title, slug);
  descriptions.set(description, slug);

  const jsonBlocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
  for (const [, raw] of jsonBlocks) {
    try {
      JSON.parse(raw);
    } catch (error) {
      fail(`${slug}: invalid JSON-LD (${error.message})`);
    }
  }

  for (const [, source] of html.matchAll(/(?:src|href)="\.\.\/([^"#?]+)"/g)) {
    if (!existsSync(resolve(root, source))) fail(`${slug}: missing local asset ../${source}`);
  }

  if (upgraded.includes(slug)) {
    for (const required of [
      "../css/article.css",
      "../assets/ai-packaging-demo.mp4",
      '"@type": "Article"',
      '"@type": "FAQPage"',
      'class="decision-table"',
      'class="article-hero"',
      'class="related-grid"'
    ]) {
      if (!html.includes(required)) fail(`${slug}: missing ${required}`);
    }
    for (const claim of ["10,000+", "7 天无理由退换", "100% 可回收", "成本比传统方案降低约 20%"]) {
      if (html.includes(claim)) fail(`${slug}: contains unsupported templated claim "${claim}"`);
    }
  }
}

const sitemap = readFileSync(resolve(root, "sitemap.xml"), "utf8");
for (const slug of expected) {
  const url = `https://guide.bubbpackage.com/${slug}/`;
  if (!sitemap.includes(`<loc>${url}</loc>`)) fail(`sitemap: missing ${url}`);
}

const generatedAssets = readdirSync(resolve(root, "assets")).filter((name) => name.endsWith(".webp"));
if (generatedAssets.length < 13) fail(`assets: expected at least 13 webp files, found ${generatedAssets.length}`);

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log(`Validated ${expected.length} guides, ${titles.size} unique titles, ${descriptions.size} unique descriptions.`);
console.log(`Parsed JSON-LD, checked local assets, sitemap entries, shared guide structure, and unsupported claims.`);
