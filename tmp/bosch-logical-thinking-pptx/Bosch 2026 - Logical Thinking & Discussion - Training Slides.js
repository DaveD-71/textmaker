const pptxgen = require("pptxgenjs");
const {
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require("./pptxgenjs_helpers/layout");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Avanti Staff Corporation";
pptx.company = "Avanti Staff Corporation";
pptx.subject = "Bosch Logical Thinking & Discussion intensive training";
pptx.title = "Bosch 2026 - Logical Thinking & Discussion - Training Slides";
pptx.lang = "en-US";
pptx.theme = {
  headFontFace: "Gill Sans Nova Cond",
  bodyFontFace: "Noto Serif",
  lang: "en-US",
};
pptx.defineLayout({ name: "CUSTOM_WIDE", width: 13.333, height: 7.5 });
pptx.layout = "CUSTOM_WIDE";
pptx.margin = 0;

const COURSE_ROOT =
  "\\\\prod-fs-gen01\\WorkFile\\04_在宅勤務\\★グローバルビジネス推進部（在宅）\\ランゲージサービス課\\Dobson（在宅）\\02. Clients\\Bosch\\Logical Thinking & Discussion";
const OUT = `${COURSE_ROOT}\\Bosch 2026 - Logical Thinking & Discussion - Training Slides.pptx`;

const C = {
  deepBlue: "002060",
  headingBlue: "2F5496",
  brightBlue: "0070C0",
  paleBlue: "D9E2F3",
  paleBlue2: "DEEAF6",
  grayFill: "E1DFDD",
  paleOrange: "FBE4D5",
  gold: "BF8F00",
  text: "000000",
  muted: "605E5C",
  white: "FFFFFF",
  line: "9EADBD",
};

const FONT = {
  head: "Gill Sans Nova Cond",
  headFallback: "Arial Narrow",
  body: "Noto Serif",
  bodyFallback: "Georgia",
  sans: "Arial",
};

const SLIDE_W = 13.333;
const SLIDE_H = 7.5;
const M = 0.55;

function addFooter(slide, section = "") {
  slide.addShape(pptx.ShapeType.line, {
    x: M,
    y: 7.05,
    w: SLIDE_W - M * 2,
    h: 0,
    line: { color: C.line, width: 0.6 },
  });
  slide.addText(section, {
    x: M,
    y: 7.12,
    w: 8.8,
    h: 0.22,
    fontFace: FONT.sans,
    fontSize: 6.8,
    color: C.muted,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
}

function addTopRule(slide, label = "") {
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: SLIDE_W,
    h: 0.13,
    fill: { color: C.deepBlue },
    line: { color: C.deepBlue },
  });
  if (label) {
    slide.addText(label.toUpperCase(), {
      x: M,
      y: 0.23,
      w: 5.5,
      h: 0.2,
      margin: 0,
      fontFace: FONT.sans,
      fontSize: 7.5,
      color: C.brightBlue,
      bold: true,
    });
  }
}

function titleSlide(title, subtitle, details = []) {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addTopRule(slide);
  slide.addText("LOGICAL THINKING & DISCUSSION", {
    x: 0.7,
    y: 0.75,
    w: 7.2,
    h: 0.35,
    margin: 0,
    fontFace: FONT.sans,
    fontSize: 11,
    color: C.brightBlue,
    bold: true,
    charSpace: 1,
  });
  slide.addText(title, {
    x: 0.7,
    y: 1.35,
    w: 8.8,
    h: 1.3,
    margin: 0,
    fontFace: FONT.head,
    fontSize: 38,
    bold: true,
    color: C.headingBlue,
    fit: "shrink",
    breakLine: false,
  });
  slide.addText(subtitle, {
    x: 0.74,
    y: 2.76,
    w: 7.6,
    h: 0.55,
    margin: 0,
    fontFace: FONT.body,
    fontSize: 14,
    color: C.text,
    italic: true,
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 9.8,
    y: 1.0,
    w: 2.55,
    h: 4.7,
    fill: { color: C.paleBlue2 },
    line: { color: C.headingBlue, width: 1.2 },
  });
  slide.addText("Opinion", boxText(10.02, 1.45, 2.1, 0.45, 18, C.headingBlue, true));
  slide.addText("Reason", boxText(10.02, 2.45, 2.1, 0.45, 18, C.headingBlue, true));
  slide.addText("Evidence", boxText(10.02, 3.45, 2.1, 0.45, 18, C.headingBlue, true));
  slide.addShape(pptx.ShapeType.line, { x: 10.05, y: 2.15, w: 2.0, h: 0, line: { color: C.brightBlue, width: 1 } });
  slide.addShape(pptx.ShapeType.line, { x: 10.05, y: 3.15, w: 2.0, h: 0, line: { color: C.brightBlue, width: 1 } });
  slide.addShape(pptx.ShapeType.line, { x: 10.05, y: 4.15, w: 2.0, h: 0, line: { color: C.brightBlue, width: 1 } });
  slide.addText("A clear answer is useful.\nA clear explanation is persuasive.", {
    x: 10.0,
    y: 4.65,
    w: 2.15,
    h: 0.72,
    margin: 0,
    fontFace: FONT.body,
    fontSize: 10.8,
    italic: true,
    color: C.text,
    align: "center",
    fit: "shrink",
  });
  details.forEach((d, i) => {
    slide.addText(d, {
      x: 0.75,
      y: 4.35 + i * 0.34,
      w: 7.7,
      h: 0.26,
      margin: 0,
      fontFace: FONT.sans,
      fontSize: 10.5,
      color: C.muted,
    });
  });
  addFooter(slide, "Bosch Corporation 2026 | Business Skills Training in English");
  check(slide);
}

function boxText(x, y, w, h, fontSize, color = C.text, bold = false) {
  return {
    x,
    y,
    w,
    h,
    margin: 0,
    fontFace: FONT.head,
    fontSize,
    bold,
    color,
    align: "center",
    valign: "mid",
    fit: "shrink",
  };
}

function baseSlide(title, section = "") {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addTopRule(slide, section);
  slide.addText(title, {
    x: M,
    y: 0.56,
    w: 10.3,
    h: 0.5,
    margin: 0,
    fontFace: FONT.head,
    fontSize: 26,
    bold: true,
    color: C.headingBlue,
    fit: "shrink",
  });
  slide.addShape(pptx.ShapeType.line, {
    x: M,
    y: 1.18,
    w: SLIDE_W - M * 2,
    h: 0,
    line: { color: C.brightBlue, width: 1 },
  });
  addFooter(slide, section);
  return slide;
}

function addBullets(slide, items, x, y, w, h, opts = {}) {
  const runs = [];
  items.forEach((item) => {
    runs.push({
      text: item,
      options: {
        bullet: { type: "ul" },
        hanging: 4,
        breakLine: true,
      },
    });
  });
  slide.addText(runs, {
    x,
    y,
    w,
    h,
    margin: 0.07,
    fontFace: opts.fontFace || FONT.body,
    fontSize: opts.fontSize || 14,
    color: opts.color || C.text,
    breakLine: false,
    paraSpaceAfterPt: opts.paraSpaceAfterPt ?? 8,
    fit: "shrink",
  });
}

function addNumbered(slide, items, x, y, w, h, opts = {}) {
  const lineH = h / items.length;
  items.forEach((item, i) => {
    slide.addShape(pptx.ShapeType.rect, {
      x,
      y: y + i * lineH + 0.04,
      w: 0.38,
      h: 0.32,
      fill: { color: opts.fill || C.paleBlue },
      line: { color: opts.line || C.headingBlue, width: 0.6 },
    });
    slide.addText(String(i + 1), {
      x: x + 0.03,
      y: y + i * lineH + 0.085,
      w: 0.32,
      h: 0.22,
      margin: 0,
      fontFace: FONT.sans,
      fontSize: 8,
      bold: true,
      color: C.headingBlue,
      align: "center",
    });
    slide.addText(item, {
      x: x + 0.55,
      y: y + i * lineH,
      w,
      h: lineH - 0.03,
      margin: 0,
      fontFace: opts.fontFace || FONT.body,
      fontSize: opts.fontSize || 12.5,
      color: C.text,
      fit: "shrink",
    });
  });
}

function addTwoColumn(slide, leftTitle, leftItems, rightTitle, rightItems, section) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.7,
    y: 1.55,
    w: 5.7,
    h: 4.95,
    fill: { color: C.paleBlue2 },
    line: { color: C.headingBlue, width: 0.7 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 6.95,
    y: 1.55,
    w: 5.7,
    h: 4.95,
    fill: { color: C.grayFill },
    line: { color: C.line, width: 0.7 },
  });
  slide.addText(leftTitle, boxText(0.95, 1.82, 5.2, 0.35, 17, C.headingBlue, true));
  slide.addText(rightTitle, boxText(7.2, 1.82, 5.2, 0.35, 17, C.headingBlue, true));
  addBullets(slide, leftItems, 1.05, 2.45, 4.85, 3.5, { fontSize: 12.2, paraSpaceAfterPt: 7 });
  addBullets(slide, rightItems, 7.3, 2.45, 4.85, 3.5, { fontSize: 12.2, paraSpaceAfterPt: 7 });
}

function sectionSlide(title, subtitle, section, model = "") {
  const slide = pptx.addSlide();
  slide.background = { color: C.paleBlue2 };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: SLIDE_W,
    h: 0.2,
    fill: { color: C.deepBlue },
    line: { color: C.deepBlue },
  });
  slide.addText(section.toUpperCase(), {
    x: 0.75,
    y: 1.0,
    w: 5.7,
    h: 0.28,
    margin: 0,
    fontFace: FONT.sans,
    fontSize: 10,
    bold: true,
    color: C.brightBlue,
    charSpace: 1,
  });
  slide.addText(title, {
    x: 0.75,
    y: 1.48,
    w: 8.6,
    h: 1.15,
    margin: 0,
    fontFace: FONT.head,
    fontSize: 36,
    bold: true,
    color: C.headingBlue,
    fit: "shrink",
  });
  slide.addText(subtitle, {
    x: 0.78,
    y: 2.86,
    w: 7.8,
    h: 0.65,
    margin: 0,
    fontFace: FONT.body,
    fontSize: 15,
    italic: true,
    color: C.text,
    fit: "shrink",
  });
  if (model) {
    slide.addShape(pptx.ShapeType.rect, {
      x: 9.75,
      y: 1.45,
      w: 2.5,
      h: 2.75,
      fill: { color: C.white, transparency: 10 },
      line: { color: C.headingBlue, width: 1 },
    });
    slide.addText(model, {
      x: 9.96,
      y: 2.05,
      w: 2.1,
      h: 1.5,
      margin: 0,
      fontFace: FONT.head,
      fontSize: 31,
      bold: true,
      align: "center",
      valign: "mid",
      color: C.deepBlue,
      fit: "shrink",
    });
  }
  addFooter(slide, section);
  check(slide);
}

function simpleTable(slide, rows, x, y, w, h, opts = {}) {
  const colW = opts.colW || Array(rows[0].length).fill(w / rows[0].length);
  const rowH = h / rows.length;
  rows.forEach((row, r) => {
    let cx = x;
    row.forEach((raw, c) => {
      const cell = typeof raw === "object" && raw.text != null ? raw : { text: String(raw), options: {} };
      const options = cell.options || {};
      const fill = options.fill || (r === 0 ? C.headingBlue : C.white);
      const color = options.color || (r === 0 ? C.white : C.text);
      slide.addText(cell.text, {
        x: cx,
        y: y + r * rowH,
        w: colW[c],
        h: rowH,
        margin: 0.08,
        fontFace: options.fontFace || FONT.body,
        fontSize: options.fontSize || opts.fontSize || 10.5,
        bold: options.bold || r === 0,
        color,
        fill: { color: fill },
        line: { color: C.headingBlue, width: 0.45 },
        valign: "mid",
        fit: "shrink",
      });
      cx += colW[c];
    });
  });
}

function optionCell(slide, text, x, y, w, options = {}) {
  const struck = options.struck || [];
  const parts = text.split(" / ");
  const runs = [];
  parts.forEach((part, idx) => {
    const clean = part.trim();
    runs.push({
      text: clean,
      options: {
        strike: struck.includes(clean),
        color: struck.includes(clean) ? "9B9B9B" : C.text,
        breakLine: false,
      },
    });
    if (idx < parts.length - 1) {
      runs.push({ text: " / ", options: { color: C.muted, breakLine: false } });
    }
  });
  slide.addText(runs, {
    x,
    y,
    w,
    h: options.h || 0.45,
    margin: 0.04,
    fontFace: FONT.body,
    fontSize: options.fontSize || 10,
    color: C.text,
    fit: "shrink",
    breakLine: false,
  });
}

function puzzleGridSlide(title, section, note, eliminations = {}, claim = "") {
  const slide = baseSlide(title, section);
  const x = 0.7, y = 1.5;
  const col = [1.25, 5.25, 5.2];
  const rowH = 0.78;
  const headers = ["Person", "Possible divisions", "Possible meeting styles"];
  let cx = x;
  headers.forEach((h, i) => {
    slide.addText(h, {
      x: cx,
      y,
      w: col[i],
      h: 0.45,
      margin: 0.06,
      fontFace: FONT.body,
      fontSize: 10.8,
      bold: true,
      color: C.white,
      fill: { color: C.headingBlue },
      line: { color: C.headingBlue, width: 0.5 },
      valign: "mid",
    });
    cx += col[i];
  });
  const people = ["Aiko", "Ben", "Carlos", "Dita"];
  const divisions = "Manufacturing / Purchasing / R&D / Sales";
  const styles = "Email / Chat / Call / Face-to-face";
  people.forEach((person, r) => {
    const yy = y + 0.45 + r * rowH;
    slide.addText(person, {
      x,
      y: yy,
      w: col[0],
      h: rowH,
      margin: 0.06,
      fontFace: FONT.body,
      fontSize: 11.5,
      color: C.text,
      fill: { color: r % 2 ? C.white : "F7F9FC" },
      line: { color: C.headingBlue, width: 0.35 },
      valign: "mid",
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: x + col[0],
      y: yy,
      w: col[1],
      h: rowH,
      fill: { color: r % 2 ? C.white : "F7F9FC", transparency: 100 },
      line: { color: C.headingBlue, width: 0.35 },
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: x + col[0] + col[1],
      y: yy,
      w: col[2],
      h: rowH,
      fill: { color: r % 2 ? C.white : "F7F9FC", transparency: 100 },
      line: { color: C.headingBlue, width: 0.35 },
    });
    optionCell(slide, divisions, x + col[0] + 0.08, yy + 0.16, col[1] - 0.15, {
      struck: eliminations[`${person}:div`] || [],
      fontSize: 9.7,
      h: 0.42,
    });
    optionCell(slide, styles, x + col[0] + col[1] + 0.08, yy + 0.16, col[2] - 0.15, {
      struck: eliminations[`${person}:style`] || [],
      fontSize: 9.7,
      h: 0.42,
    });
  });
  slide.addText(note, {
    x: 0.82,
    y: 5.35,
    w: 11.6,
    h: 0.52,
    margin: 0.04,
    fontFace: FONT.body,
    fontSize: 11.2,
    color: C.text,
    fit: "shrink",
  });
  if (claim) addTakeaway(slide, claim, 6.15);
  check(slide);
}

function relationCell(slide, items, x, y, w, h, struck = [], opts = {}) {
  const runs = [];
  items.forEach((item, idx) => {
    runs.push({
      text: item,
      options: {
        strike: false,
        color: C.text,
        breakLine: false,
      },
    });
    if (idx < items.length - 1) runs.push({ text: " / ", options: { color: C.muted, breakLine: false } });
  });
  slide.addText(runs, {
    x,
    y,
    w,
    h,
    margin: 0.05,
    fontFace: FONT.body,
    fontSize: opts.fontSize || 8.8,
    color: C.text,
    fit: "shrink",
    breakLine: false,
    fill: { color: opts.fill || C.white },
    line: { color: C.headingBlue, width: 0.35 },
    valign: "mid",
  });
}

function relationGridSlide(title, section, note, rows, claim = "") {
  const slide = baseSlide(title, section);
  const x = 0.78, y = 1.52;
  const col = [1.2, 3.7, 3.3, 3.3];
  const rowH = 0.78;
  const headers = ["Link", "Possible person", "Division", "Meeting style"];
  let cx = x;
  headers.forEach((h, i) => {
    slide.addText(h, {
      x: cx,
      y,
      w: col[i],
      h: 0.45,
      margin: 0.06,
      fontFace: FONT.body,
      fontSize: 9.2,
      bold: true,
      color: C.white,
      fill: { color: C.headingBlue },
      line: { color: C.headingBlue, width: 0.45 },
      valign: "mid",
    });
    cx += col[i];
  });
  rows.forEach((row, r) => {
    const yy = y + 0.45 + r * rowH;
    const fill = r % 2 ? C.white : "F7F9FC";
    slide.addText(row.link, {
      x,
      y: yy,
      w: col[0],
      h: rowH,
      margin: 0.06,
      fontFace: FONT.body,
      fontSize: 9.2,
      color: C.text,
      fill: { color: fill },
      line: { color: C.headingBlue, width: 0.35 },
      valign: "mid",
      fit: "shrink",
    });
    relationCell(slide, row.people, x + col[0], yy, col[1], rowH, row.struckPeople || [], { fill });
    relationCell(slide, row.divisions, x + col[0] + col[1], yy, col[2], rowH, row.struckDivisions || [], { fill });
    relationCell(slide, row.styles, x + col[0] + col[1] + col[2], yy, col[3], rowH, row.struckStyles || [], { fill });
  });
  slide.addText(note, {
    x: 0.82,
    y: 5.28,
    w: 11.6,
    h: 0.48,
    margin: 0.04,
    fontFace: FONT.body,
    fontSize: 10.3,
    color: C.text,
    fit: "shrink",
  });
  if (claim) addTakeaway(slide, claim, 6.15);
  check(slide);
}

function statusCell(slide, items, status, x, y, w, h, opts = {}) {
  const runs = [];
  items.forEach((item, idx) => {
    const s = status[item] || "open";
    runs.push({
      text: item,
      options: {
        strike: s === "out",
        bold: s === "in",
        color: s === "in" ? C.deepBlue : s === "out" ? "9B9B9B" : C.text,
        breakLine: false,
      },
    });
    if (idx < items.length - 1) runs.push({ text: " / ", options: { color: C.muted, breakLine: false } });
  });
  slide.addText(runs, {
    x,
    y,
    w,
    h,
    margin: 0.05,
    fontFace: FONT.body,
    fontSize: opts.fontSize || 7.9,
    color: C.text,
    fill: { color: opts.fill || C.white },
    line: { color: C.headingBlue, width: 0.35 },
    valign: "mid",
    fit: "shrink",
    breakLine: false,
  });
}

function puzzleWorkingTableSlide() {
  const slide = baseSlide("Mini Logic Puzzle: Option Tags", "Pre-Course Follow-up");
  const x = 0.7;
  const y = 1.48;
  const colW = [1.35, 3.05, 4.0, 4.0];
  const colGap = 0.08;
  const headers = ["Person", "Facts", "Division", "Meeting Style"];
  const people = ["Aiko", "Ben", "Carlos", "Dita"];
  const facts = [
    ["Not Sales", "Not Call", "Not Manufacturing"],
    ["Works in Purchasing"],
    ["Prefers Face-to-face"],
    ["Not R&D"],
  ];
  const additionalFacts = ["The colleague in R&D prefers Chat", "The Sales colleague prefers Call"];
  const divisions = ["Manufacturing", "Purchasing", "R&D", "Sales"];
  const meetingStyles = ["Email", "Chat", "Call", "Face-to-face"];

  const tagStyles = {
    person: { fill: "DEEAF6", line: "2F5496" },
    fact: { fill: "E1DFDD", line: "808080" },
    division: { fill: "D9E2F3", line: "2F5496" },
    style: { fill: "FBE4D5", line: "BF8F00" },
  };

  function columnX(index) {
    return x + colW.slice(0, index).reduce((sum, w) => sum + w + colGap, 0);
  }

  headers.forEach((header, c) => {
    const hx = columnX(c);
    slide.addText(header, {
      x: hx,
      y,
      w: colW[c] - 0.1,
      h: 0.28,
      margin: 0,
      fontFace: FONT.sans,
      fontSize: 10.2,
      bold: true,
      color: C.headingBlue,
      align: "left",
      breakLine: false,
    });
    slide.addShape(pptx.ShapeType.line, {
      x: hx,
      y: y + 0.38,
      w: colW[c] - 0.16,
      h: 0,
      line: { color: C.brightBlue, width: 0.75 },
    });
  });

  function addTag(text, tx, ty, tw, th, style, fontSize = 8.4) {
    slide.addText(text, {
      shape: pptx.ShapeType.roundRect,
      x: tx,
      y: ty,
      w: tw,
      h: th,
      margin: 0.03,
      fill: { color: style.fill },
      line: { color: style.line, width: 0.7 },
      fontFace: FONT.sans,
      fontSize,
      color: C.text,
      align: "center",
      valign: "mid",
      breakLine: false,
      fit: "shrink",
    });
  }

  function addOptionTags(options, tx, ty, tw, style) {
    const gapX = 0.1;
    const gapY = 0.12;
    const itemW = (tw - gapX) / 2;
    const itemH = 0.3;
    options.forEach((option, i) => {
      const ox = tx + (i % 2) * (itemW + gapX);
      const oy = ty + Math.floor(i / 2) * (itemH + gapY);
      addTag(option, ox, oy, itemW, itemH, style, option.length > 12 ? 7.3 : 8.1);
    });
  }

  function addFactTags(options, tx, ty, tw) {
    const gapX = 0.1;
    const gapY = 0.1;
    const itemH = 0.3;
    const itemW = options.length === 1 ? Math.min(tw, 1.65) : (tw - gapX) / 2;
    options.forEach((option, i) => {
      const ox = tx + (i % 2) * (itemW + gapX);
      const oy = ty + Math.floor(i / 2) * (itemH + gapY);
      addTag(option, ox, oy, itemW, itemH, tagStyles.fact, option.length > 16 ? 7 : 8);
    });
  }

  const startY = y + 0.65;
  const rowGap = 0.98;
  people.forEach((person, r) => {
    const rowY = startY + r * rowGap;
    addTag(person, columnX(0), rowY + 0.22, 1.02, 0.34, tagStyles.person, 8.8);
    addFactTags(facts[r], columnX(1), rowY + 0.23, colW[1] - 0.1);
    addOptionTags(divisions, columnX(2), rowY, colW[2] - 0.1, tagStyles.division);
    addOptionTags(meetingStyles, columnX(3), rowY, colW[3] - 0.1, tagStyles.style);
  });

  const additionalY = 6.08;
  slide.addText("Additional Facts", {
    x,
    y: additionalY,
    w: 1.8,
    h: 0.24,
    margin: 0,
    fontFace: FONT.sans,
    fontSize: 10,
    bold: true,
    color: C.headingBlue,
    breakLine: false,
  });
  addTag(additionalFacts[0], x + 2.05, additionalY - 0.03, 3.25, 0.34, tagStyles.fact, 8);
  addTag(additionalFacts[1], x + 5.5, additionalY - 0.03, 2.95, 0.34, tagStyles.fact, 8);

  check(slide);
}

function check(slide) {
  warnIfSlideHasOverlaps(slide, pptx, { ignoreLines: true, tolerance: 0.05 });
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

function addTakeaway(slide, text, y = 6.25) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.78,
    y,
    w: 11.8,
    h: 0.55,
    fill: { color: C.paleBlue },
    line: { color: C.headingBlue, width: 0.7 },
  });
  slide.addText(text, {
    x: 1.05,
    y: y + 0.13,
    w: 11.2,
    h: 0.28,
    margin: 0,
    fontFace: FONT.body,
    fontSize: 12.5,
    italic: true,
    color: C.text,
    fit: "shrink",
  });
}

function contentSlide(title, section, bullets, takeaway = "") {
  const slide = baseSlide(title, section);
  addBullets(slide, bullets, 0.9, 1.6, 11.4, takeaway ? 4.3 : 5.0, {
    fontSize: 14,
    paraSpaceAfterPt: 11,
  });
  if (takeaway) addTakeaway(slide, takeaway);
  check(slide);
}

function modelSlide(title, section, steps, modelLabel, takeaway) {
  const slide = baseSlide(title, section);
  slide.addText(modelLabel, {
    x: 0.85,
    y: 1.55,
    w: 2.7,
    h: 4.1,
    margin: 0,
    fontFace: FONT.head,
    fontSize: 34,
    bold: true,
    align: "center",
    valign: "mid",
    color: C.deepBlue,
    fit: "shrink",
  });
  addNumbered(slide, steps, 4.05, 1.58, 7.8, 3.85, { fontSize: 12.2 });
  if (takeaway) addTakeaway(slide, takeaway, 6.05);
  check(slide);
}

function makeSlides() {
  titleSlide("Bosch Corporation 2026", "Logical Thinking & Discussion", [
    "Monday, June 29 and Tuesday, June 30, 2026",
    "Business Skills Training in English",
    "Avanti Staff Corporation",
  ]);

  contentSlide("Course Objectives", "Course Introduction", [
    "Express clear and persuasive opinions.",
    "Support ideas with strong reasoning and credible evidence.",
    "Identify bias and evaluate information critically.",
    "Apply logical speaking in realistic business situations.",
  ], "The course focus is business communication: English accuracy supports the message, but logic drives the result.");

  const agenda = baseSlide("Two-Day Roadmap", "Course Introduction");
  simpleTable(agenda, [
    [{ text: "Day 1 | Face-to-face", options: { bold: true, color: C.white, fill: C.headingBlue } }, { text: "Day 2 | Online", options: { bold: true, color: C.white, fill: C.headingBlue } }],
    ["ORE, opinions, reasoning, evidence, bias", "PBSR, full argument writing, PCAF"],
    ["Meeting 1: Bosch investment decision", "Meeting 2: automation and staffing"],
    ["Day 1 review and bridge", "Meeting 3: EV supply-chain dilemma"],
  ], 0.9, 1.65, 11.5, 3.5, { fontSize: 12, colW: [5.75, 5.75] });
  addTakeaway(agenda, "The schedule moves from short logical structures to full business decisions.", 5.75);
  check(agenda);

  contentSlide("Pre-Course Preparation Check", "Course Introduction", [
    "You read Logical Speaking Units 1-5 and 7-8.",
    "You checked unknown vocabulary and reviewed Activity 1A.",
    "You prepared to discuss Activity 1B.",
    "You solved the mini logic puzzle before class.",
  ], "Preparation lets us use class time for explaining, testing, and improving reasoning.");

  contentSlide("Mini Logic Puzzle: Evidence and Rules", "Pre-Course Follow-up", [
    "What is our evidence? The information in the task: four colleagues, four divisions, four meeting styles, and seven clues.",
    "What are our logic rules? Each colleague works in a different division, and each has a different preferred meeting style.",
    "Each person, division, and meeting style can be used only once.",
    "The clues are known facts. Reasoning is the connection between those facts and the claim we make.",
  ], "Eliminate what the evidence makes impossible before making a final claim.");

  contentSlide("Mini Logic Puzzle: Process", "Pre-Course Follow-up", [
    "First, check whether the clues connect the three variables: person, division, and meeting style.",
    "Note the links: Ben -> Purchasing; Carlos -> Face-to-face; the R&D colleague -> Chat; the Sales colleague -> Call.",
    "Then go through each variable column one by one and eliminate options based on the evidence.",
    "When only one option remains possible, that option must be the answer for that variable.",
  ], "Work from known facts to eliminated options, then from the last remaining option to the final answer.");

  puzzleWorkingTableSlide();

  const puzzle = baseSlide("Mini Logic Puzzle: Final Answer", "Pre-Course Follow-up");
  simpleTable(puzzle, [
    [{ text: "Person", options: { bold: true, color: C.white, fill: C.headingBlue } }, { text: "Division", options: { bold: true, color: C.white, fill: C.headingBlue } }, { text: "Meeting style", options: { bold: true, color: C.white, fill: C.headingBlue } }],
    ["Aiko", "R&D", "Chat"],
    ["Ben", "Purchasing", "Email"],
    ["Carlos", "Manufacturing", "Face-to-face"],
    ["Dita", "Sales", "Call"],
  ], 1.05, 1.55, 6.8, 3.95, { fontSize: 15, colW: [1.7, 2.4, 2.7] });
  slideText(puzzle, "Complete answer sentences", 8.45, 1.65, 3.5, 0.28, 17, C.headingBlue, true, FONT.head);
  addBullets(puzzle, [
    "Aiko works in R&D and prefers Chat.",
    "Ben works in Purchasing and prefers Email.",
    "Carlos works in Manufacturing and prefers Face-to-face meetings.",
    "Dita works in Sales and prefers Calls.",
  ], 8.28, 2.2, 3.8, 2.4, { fontSize: 11.2, paraSpaceAfterPt: 8 });
  addTakeaway(puzzle, "A correct answer is the result. Logical speaking explains how the evidence leads to that result.", 6.1);
  check(puzzle);

  contentSlide("Bridge: Clear Reasoning", "Pre-Course Follow-up", [
    "The textbook defines reasoning as the connection between evidence and the claim you make.",
    "In the puzzle, the evidence is the set of clues. The claims are absolute because only one answer is possible.",
    "In business discussion, claims may be less certain, but the same discipline applies: show how the evidence supports what you say.",
  ], "Logical speaking means making the evidence-to-claim connection clear.");

  sectionSlide("Day 1", "Build the core structures: ORE, reasoning language, evidence, and bias.", "Day 1 Objectives", "ORE");

  sectionSlide("Units 1-2", "From opinions to complete arguments.", "Logical Speaking", "ORE");
  modelSlide("ORE: A Simple Argument Structure", "Units 1-2", [
    "Opinion: state your position clearly.",
    "Reason: explain why you think this.",
    "Evidence: give information that makes the reason credible.",
  ], "O\nR\nE", "A strong argument connects the roof, columns, and foundation.");
  contentSlide("Units 1-2 Wrap-up", "Units 1-2", [
    "Opinion is not fact; it is your conclusion based on thinking and evidence.",
    "Opinion phrases can be weak, moderate, or strong.",
    "ORE helps listeners separate your answer, your logic, and your support.",
  ], "If the listener cannot identify O, R, and E, the argument is hard to evaluate.");

  sectionSlide("Units 3-4", "Make the connections between ideas easy to follow.", "Reasoning", "Logic");
  addReasonLanguageSlide();
  contentSlide("Units 3-4 Wrap-up", "Units 3-4", [
    "Conjunctions show cause, result, contrast, and purpose.",
    "Discourse markers organize the listener's attention.",
    "Sequence language helps explain processes and decisions in order.",
  ], "Logical speaking is not only what you think; it is how clearly you connect each idea.");

  sectionSlide("Practice 1", "Use ORE to present a short business argument.", "Practice", "ORE");

  sectionSlide("Unit 5", "Evidence makes persuasion credible.", "Supporting Evidence", "Evidence");
  const evidence = baseSlide("Evidence Quality", "Unit 5");
  simpleTable(evidence, [
    [{ text: "Evidence type", options: { bold: true, color: C.white, fill: C.headingBlue } }, { text: "Typical strength", options: { bold: true, color: C.white, fill: C.headingBlue } }, { text: "Use carefully when...", options: { bold: true, color: C.white, fill: C.headingBlue } }],
    ["Statistics and data", "Very strong", "Definitions or collection methods are unclear."],
    ["Research and case studies", "Strong", "The source, date, or method is weak."],
    ["Expert opinion", "Moderate", "The expert may not be neutral or relevant."],
    ["Experience / analogy", "Weak to moderate", "One case is treated like proof."],
  ], 0.82, 1.55, 11.75, 4.35, { fontSize: 10.7, colW: [3.1, 2.4, 6.25] });
  addTakeaway(evidence, "Evidence should be credible, current, relevant, objective, and accurate.", 6.15);
  check(evidence);

  contentSlide("Bias and Framing", "Unit 5", [
    "Bias can come from what is emphasized, omitted, or compared.",
    "Risk can be framed by severity or by base rate.",
    "Ask what the evidence actually measures before accepting the conclusion.",
  ], "A persuasive speaker should be skeptical before asking others to be persuaded.");
  contentSlide("Unit 5 Wrap-up", "Unit 5", [
    "Evidence is the foundation of logical speaking.",
    "Weak evidence can still be useful if you acknowledge its limits.",
    "Strong evidence can become misleading if it is framed unfairly.",
  ], "Before using evidence, test the source, method, relevance, and possible bias.");

  sectionSlide("Meeting 1", "Choose a Bosch investment opportunity using ORE.", "Meeting Simulation", "ORE");
  contentSlide("Meeting 1 Review", "Meeting 1", [
    "Was each project recommendation stated as a clear opinion?",
    "Were the reasons connected to Bosch's goals and constraints?",
    "Was the evidence credible enough to support the investment choice?",
    "Was the final decision rationale easy to explain?",
  ], "A meeting decision should leave a traceable line from evidence to conclusion.");

  sectionSlide("Unit 7", "Use PBSR for business problem solving and reporting.", "PBSR", "PBSR");
  modelSlide("PBSR: Problem to Result", "Unit 7", [
    "Problem: define what needs to be solved.",
    "Background: explain the context that matters.",
    "Solution: propose what should be done and why.",
    "Result: describe the expected outcome.",
  ], "P\nB\nS\nR", "Your opinion and evidence usually live inside the Solution.");
  contentSlide("Unit 7 Wrap-up", "Unit 7", [
    "A weak problem statement creates a weak solution.",
    "Background should include only context that changes the decision.",
    "Result should make the value of the solution clear.",
  ], "PBSR works well when the discussion starts with a shared problem.");

  contentSlide("Day 1 Review", "Day 1 Wrap-up", [
    "ORE helps you build a short argument.",
    "Reasoning language makes your logic visible.",
    "Evidence quality determines how persuasive your argument can be.",
    "Bias awareness helps you evaluate information before using it.",
  ], "Day 2 applies these skills to longer arguments and more complex decisions.");

  sectionSlide("Day 2", "Develop complete arguments and make balanced business decisions.", "Day 2 Objectives", "PBSR");

  sectionSlide("Unit 8", "Write and deliver a complete argument.", "Writing an Argument", "ORE");
  contentSlide("Unit 8 Wrap-up", "Unit 8", [
    "A complete argument needs a clear opinion, connected reasons, and evidence.",
    "Invented evidence can support practice, but real business decisions need real evidence.",
    "A strong argument is easy to repeat accurately after hearing it once.",
  ], "Aim for one persuasive argument, not a list of disconnected points.");

  sectionSlide("Meeting 2", "Balance automation and workforce retention using PBSR.", "Meeting Simulation", "PBSR");
  contentSlide("Meeting 2 Review", "Meeting 2", [
    "Did each group define the business problem in the same way?",
    "Was the background complete enough for a fair decision?",
    "Did the solution match the problem and evidence?",
    "Were the expected results realistic and measurable?",
  ], "PBSR helps compare proposals because each proposal must answer the same four questions.");

  sectionSlide("Unit 9", "Use PCAF to recommend one option while addressing alternatives.", "PCAF", "PCAF");
  modelSlide("PCAF: Balanced Recommendation", "Unit 9", [
    "Point: state your recommendation.",
    "Counterpoint: acknowledge another reasonable view.",
    "Against: explain why the counterpoint is weaker.",
    "For: explain why your point is stronger.",
  ], "P\nC\nA\nF", "PCAF is useful when the room already knows there are two sides.");
  contentSlide("Unit 9 Wrap-up", "Unit 9", [
    "Balanced reasoning can make a recommendation more credible.",
    "The counterpoint should be fair, not artificial.",
    "Against and For should compare business impact, risk, and evidence.",
  ], "Acknowledge the alternative, then justify the preferred choice.");

  sectionSlide("Meeting 3", "Decide how Bosch should handle the EV supply-chain dilemma.", "Meeting Simulation", "Decision");
  contentSlide("Meeting 3 Review", "Meeting 3", [
    "Did the group separate cost, ESG, compliance, and reputation risks?",
    "Which evidence was strongest, and which evidence needed more verification?",
    "Did the final decision balance short-term pressure and long-term consequences?",
    "Could the chair explain the decision clearly to senior management?",
  ], "Complex business decisions need both logical structure and responsible judgment.");

  contentSlide("Course Wrap-up", "Course Review", [
    "Use ORE when you need a quick persuasive argument.",
    "Use PBSR when you need to solve or report a business problem.",
    "Use PCAF when you need to recommend one option while addressing alternatives.",
    "Use evidence checks before relying on data, examples, or expert opinions.",
  ], "At work, clear reasoning is a communication skill and a decision-making skill.");

  const final = pptx.addSlide();
  final.background = { color: C.deepBlue };
  final.addText("Thank you", {
    x: 0.8,
    y: 1.8,
    w: 6.2,
    h: 0.9,
    margin: 0,
    fontFace: FONT.head,
    fontSize: 42,
    bold: true,
    color: C.white,
  });
  final.addText("Logical Thinking & Discussion", {
    x: 0.84,
    y: 2.9,
    w: 7.3,
    h: 0.45,
    margin: 0,
    fontFace: FONT.body,
    fontSize: 17,
    italic: true,
    color: C.white,
  });
  final.addText("Use clear structure. Test your evidence. Explain your reasoning.", {
    x: 0.84,
    y: 4.55,
    w: 7.2,
    h: 0.42,
    margin: 0,
    fontFace: FONT.sans,
    fontSize: 13.5,
    color: C.paleBlue,
  });
  final.addShape(pptx.ShapeType.rect, {
    x: 9.05,
    y: 1.45,
    w: 3.1,
    h: 3.1,
    fill: { color: C.white, transparency: 5 },
    line: { color: C.white, width: 1 },
  });
  final.addText("O R E\nP B S R\nP C A F", {
    x: 9.35,
    y: 2.0,
    w: 2.55,
    h: 2.1,
    margin: 0,
    fontFace: FONT.head,
    fontSize: 27,
    bold: true,
    color: C.deepBlue,
    align: "center",
    valign: "mid",
    breakLine: false,
    fit: "shrink",
  });
  check(final);
}

function addReasonLanguageSlide() {
  const slide = baseSlide("Reasoning Language", "Units 3-4");
  simpleTable(slide, [
    [{ text: "Function", options: { bold: true, color: C.white, fill: C.headingBlue } }, { text: "Useful language", options: { bold: true, color: C.white, fill: C.headingBlue } }, { text: "Business use", options: { bold: true, color: C.white, fill: C.headingBlue } }],
    ["Cause", "because / since / due to", "Explain why a situation happened."],
    ["Result", "so / therefore / as a result", "Show the consequence of a fact."],
    ["Contrast", "but / however / on the other hand", "Compare risk, cost, or options."],
    ["Order", "first / next / finally / to sum up", "Guide listeners through a process."],
  ], 0.8, 1.55, 11.75, 4.3, { fontSize: 10.8, colW: [2.35, 4.0, 5.4] });
  addTakeaway(slide, "Logical language helps listeners follow the connection between information and conclusion.", 6.15);
  check(slide);
}

function slideText(slide, text, x, y, w, h, fontSize, color, bold = false, fontFace = FONT.body) {
  slide.addText(text, {
    x,
    y,
    w,
    h,
    margin: 0,
    fontFace,
    fontSize,
    bold,
    color,
    fit: "shrink",
  });
}

async function main() {
  makeSlides();
  await pptx.writeFile({ fileName: OUT });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
