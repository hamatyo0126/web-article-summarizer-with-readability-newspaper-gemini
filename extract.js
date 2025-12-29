const fs = require("fs");
const { Readability } = require("@mozilla/readability");
const { JSDOM } = require("jsdom");

const html = fs.readFileSync(0, "utf8"); // receive from stdin 
const dom = new JSDOM(html, { url: "https://example.com" });
const reader = new Readability(dom.window.document);
const article = reader.parse();

console.log(JSON.stringify(article));
