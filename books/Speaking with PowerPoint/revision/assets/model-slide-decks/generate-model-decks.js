const pptxgen = require('pptxgenjs');
const {
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require('./pptxgenjs_helpers');

const OUT = __dirname;
const pptxgenjs = pptxgen;
const SH = (new pptxgenjs()).ShapeType;
const COLORS = {
  ink: '243133',
  muted: '5F7272',
  rule: 'CBD6D6',
  bg: 'F7F8F6',
  white: 'FFFFFF',
  charcoal: '334044',
  blue: '2E6F95',
  bluePale: 'E5F1F6',
  teal: '0097B2',
  tealPale: 'DEF3F7',
  green: '3C7964',
  greenPale: 'E4F2EA',
  amber: 'D1A624',
  amberPale: 'FFF3D1',
  red: 'A63B52',
  redPale: 'F8E8EC',
  grayPale: 'EEF2F2',
  gray: '6C7F7F',
};
const SLIDE_W = 13.333;
const SLIDE_H = 7.5;
const FONT = 'Aptos';

function makeDeck(meta) {
  const ppt = new pptxgenjs();
  ppt.layout = 'LAYOUT_WIDE';
  ppt.author = 'Language Services';
  ppt.company = 'BR2e / Presentation Skills 2026';
  ppt.subject = meta.subject;
  ppt.title = meta.title;
  ppt.lang = 'en-US';
  ppt.theme = {
    headFontFace: FONT,
    bodyFontFace: FONT,
    lang: 'en-US'
  };
  ppt.defineLayout({ name: 'LAYOUT_WIDE', width: SLIDE_W, height: SLIDE_H });
  ppt.layout = 'LAYOUT_WIDE';
  return ppt;
}

function addBase(slide, meta, idx, total, backup=false) {
  slide.background = { color: COLORS.bg };
  slide.addShape(SH.rect, { x:0, y:0, w:0.11, h:7.5, fill:{color:meta.accent}, line:{color:meta.accent} });
  slide.addText(meta.family, { x:0.38, y:6.95, w:7.2, h:0.22, fontFace:FONT, fontSize:7.2, color:COLORS.muted, margin:0, breakLine:false });
  slide.addText(`${idx}/${total}${backup ? ' Backup' : ''}`, { x:11.85, y:0.22, w:1.0, h:0.24, fontFace:FONT, fontSize:8.5, bold:true, color:meta.accent, align:'right', margin:0 });
}

function addTitle(slide, title, subtitle, meta) {
  slide.addText(title, { x:0.55, y:0.36, w:11.4, h:0.42, fontFace:FONT, fontSize:22, bold:true, color:COLORS.ink, margin:0.02, breakLine:false, fit:'shrink' });
  if (subtitle) slide.addText(subtitle, { x:0.58, y:1.02, w:10.6, h:0.28, fontFace:FONT, fontSize:10, color:COLORS.muted, margin:0, breakLine:false, fit:'shrink' });
  slide.addShape(SH.line, { x:0.55, y:1.34, w:12.15, h:0, line:{color:COLORS.rule, width:1.1} });
}

function cleanDecisionItem(s) {
  return s.replace(/^Decision today:\s*/i, '').trim();
}

function addDecision(slide, title, items, meta, idx, total, backup=false) {
  addBase(slide, meta, idx, total, backup); addTitle(slide, title, meta.subtitle, meta);
  slide.addText('Decision today', { x:0.92, y:1.9, w:2.3, h:0.28, fontFace:FONT, fontSize:11, bold:true, color:meta.accent, margin:0 });
  const n = items.length;
  if (n <= 1) {
    slide.addShape(SH.roundRect, { x:1.2, y:2.55, w:10.9, h:2.2, rectRadius:0.07, fill:{color:COLORS.white}, line:{color:meta.accent, width:1.4} });
    slide.addText(items.map(cleanDecisionItem).join('\n'), { x:1.75, y:3.05, w:9.8, h:1.1, fontFace:FONT, fontSize:24, bold:true, color:COLORS.ink, margin:0.04, align:'center', valign:'mid', fit:'shrink' });
  } else {
    const gap = 0.35;
    const cardW = (11.1 - gap*(n-1))/n;
    let x = 1.1;
    items.forEach((item, i) => {
      slide.addShape(SH.roundRect, { x, y:2.55, w:cardW, h:2.25, rectRadius:0.07, fill:{color:COLORS.white}, line:{color:meta.accent, width:1.35} });
      slide.addText(String(i+1).padStart(2,'0'), { x:x+0.18, y:2.78, w:0.45, h:0.24, fontFace:FONT, fontSize:9.5, bold:true, color:meta.accent, margin:0 });
      slide.addText(cleanDecisionItem(item), { x:x+0.32, y:3.18, w:cardW-0.64, h:0.85, fontFace:FONT, fontSize:15.5, bold:true, color:COLORS.ink, margin:0.03, align:'center', valign:'mid', fit:'shrink' });
      x += cardW + gap;
    });
  }
}
function textItems(text) {
  return text.split('/').map(s=>s.trim()).filter(Boolean);
}

function addCards(slide, title, text, meta, idx, total, opts={}) {
  addBase(slide, meta, idx, total, opts.backup); addTitle(slide, title, opts.subtitle || meta.subtitle, meta);
  const items = Array.isArray(text) ? text : textItems(text);
  const n = items.length;
  const startX = n <= 3 ? 1.05 : 0.75;
  const gap = 0.32;
  const w = (11.85 - gap*(n-1) - (startX-0.75)*2) / n;
  items.forEach((it,i)=>{
    const x=startX+i*(w+gap);
    slide.addShape(SH.roundRect,{x,y:2.35,w,h:2.2,rectRadius:0.06,fill:{color:opts.fill || COLORS.white},line:{color:meta.accent,width:1.2}});
    const parts = it.split(':').map(s=>s.trim());
    if(parts.length>1){
      slide.addText(parts[0],{x:x+0.18,y:2.62,w:w-0.36,h:0.35,fontFace:FONT,fontSize:11,bold:true,color:COLORS.muted,margin:0,fit:'shrink'});
      slide.addText(parts.slice(1).join(':').trim(),{x:x+0.18,y:3.0,w:w-0.36,h:1.0,fontFace:FONT,fontSize:19,bold:true,color:meta.accent,margin:0.03,align:'center',valign:'mid',fit:'shrink'});
    } else {
      slide.addText(it,{x:x+0.22,y:2.75,w:w-0.44,h:1.25,fontFace:FONT,fontSize:18,bold:true,color:COLORS.ink,margin:0.03,align:'center',valign:'mid',fit:'shrink'});
    }
  });
  if (opts.note) slide.addText(opts.note, {x:1.1,y:5.35,w:11.0,h:0.45,fontFace:FONT,fontSize:10,color:COLORS.muted,margin:0,align:'center'});
}

function addFlow(slide, title, labels, meta, idx, total, opts={}) {
  addBase(slide, meta, idx, total, opts.backup); addTitle(slide, title, opts.subtitle || meta.subtitle, meta);
  const n=labels.length;
  const gap=0.28; const w=(11.7-gap*(n-1))/n; let x=0.82; const y=3.05;
  labels.forEach((lab,i)=>{
    const [h,b] = lab.includes(':') ? lab.split(':').map(s=>s.trim()) : [lab.trim(), ''];
    slide.addShape(SH.roundRect,{x,y,w,h:1.2,rectRadius:0.04,fill:{color:opts.fill || COLORS.white},line:{color:meta.accent,width:1.1}});
    slide.addText(h,{x:x+0.1,y:y+0.26,w:w-0.2,h:0.25,fontFace:FONT,fontSize:11.5,bold:true,color:meta.accent,align:'center',margin:0,fit:'shrink'});
    if(b) slide.addText(b,{x:x+0.1,y:y+0.62,w:w-0.2,h:0.25,fontFace:FONT,fontSize:9,color:COLORS.muted,align:'center',margin:0,fit:'shrink'});
    if(i<n-1){ slide.addShape(SH.rightArrow,{x:x+w+0.04,y:y+0.39,w:gap-0.08,h:0.38,fill:{color:meta.accent,transparency:10},line:{color:meta.accent,transparency:100}}); }
    x += w+gap;
  });
  if (opts.headline) slide.addText(opts.headline,{x:1.0,y:1.95,w:11.0,h:0.55,fontFace:FONT,fontSize:18,bold:true,color:COLORS.ink,align:'center',margin:0,fit:'shrink'});
}

function addBeforeAfter(slide,title,before,after,meta,idx,total,opts={}){
  addBase(slide,meta,idx,total,opts.backup); addTitle(slide,title,opts.subtitle||meta.subtitle,meta);
  const rows=[['Current',before,COLORS.red,COLORS.redPale],['Pilot',after,meta.accent,meta.pale]];
  rows.forEach((row,ri)=>{
    const [label,items,color,pale]=row; const y=1.98+ri*2.18;
    slide.addShape(SH.roundRect,{x:0.72,y:y+0.15,w:1.05,h:0.52,rectRadius:0.04,fill:{color:pale},line:{color,width:1}});
    slide.addText(label,{x:0.82,y:y+0.29,w:0.85,h:0.18,fontFace:FONT,fontSize:10.5,bold:true,color,align:'center',margin:0});
    const n=items.length, gap=0.18, w=(10.45-gap*(n-1))/n; let x=2.0;
    items.forEach((it,i)=>{
      const [h,b]=it.includes(':')?it.split(':').map(s=>s.trim()):[it.trim(),''];
      slide.addShape(SH.roundRect,{x,y:y,w,h:1.05,rectRadius:0.04,fill:{color:pale},line:{color,width:1}});
      slide.addText(h,{x:x+0.12,y:y+0.22,w:w-0.24,h:0.26,fontFace:FONT,fontSize:11.5,bold:true,color,align:'center',margin:0,fit:'shrink'});
      if(b) slide.addText(b,{x:x+0.12,y:y+0.58,w:w-0.24,h:0.24,fontFace:FONT,fontSize:9.2,color:COLORS.ink,align:'center',margin:0,fit:'shrink'});
      if(i<n-1) slide.addShape(SH.rightArrow,{x:x+w+0.04,y:y+0.34,w:gap-0.08,h:0.34,fill:{color,transparency:5},line:{color,transparency:100}});
      x+=w+gap;
    });
  });
}

function addTimeline(slide,title,steps,meta,idx,total,opts={}){
  addBase(slide,meta,idx,total,opts.backup); addTitle(slide,title,opts.subtitle||meta.subtitle,meta);
  const y=3.05; const n=steps.length; const gap=0.32; const w=(11.5-gap*(n-1))/n; let x=0.92;
  slide.addShape(SH.line,{x:1.1,y:y+0.65,w:11.0,h:0,line:{color:meta.accent,width:2.2}});
  steps.forEach((s,i)=>{
    const [h,b]=s.split(':').map(v=>v.trim());
    slide.addShape(SH.ellipse,{x:x+w/2-0.16,y:y+0.49,w:0.32,h:0.32,fill:{color:COLORS.white},line:{color:meta.accent,width:2}});
    slide.addShape(SH.roundRect,{x,y:y+1.05,w,h:1.05,rectRadius:0.05,fill:{color:COLORS.white},line:{color:COLORS.rule,width:1}});
    slide.addText(h,{x:x+0.12,y:y+1.22,w:w-0.24,h:0.24,fontFace:FONT,fontSize:11,bold:true,color:meta.accent,align:'center',margin:0,fit:'shrink'});
    slide.addText(b||'',{x:x+0.12,y:y+1.55,w:w-0.24,h:0.24,fontFace:FONT,fontSize:10,color:COLORS.muted,align:'center',margin:0,fit:'shrink'});
    x+=w+gap;
  });
}

function addSimpleBars(slide,title,items,meta,idx,total,opts={}){
  addBase(slide,meta,idx,total,opts.backup); addTitle(slide,title,opts.subtitle||meta.subtitle,meta);
  const max=Math.max(...items.flatMap(i=>[i.before,i.after]));
  const baseY=5.35, topY=2.35, scale=(baseY-topY)/max;
  const groupGap=1.1; const groupW=(10.4-groupGap*(items.length-1))/items.length; let x=1.3;
  items.forEach((it)=>{
    const bw=0.45;
    [['Before',it.before,COLORS.blue],['After',it.after,meta.accent]].forEach((b,j)=>{
      const h=b[1]*scale; const bx=x+groupW/2-0.55+j*0.65; const by=baseY-h;
      slide.addShape(SH.rect,{x:bx,y:by,w:bw,h,fill:{color:b[2]},line:{color:b[2]}});
      slide.addText(String(b[1]),{x:bx-0.05,y:by-0.32,w:bw+0.1,h:0.22,fontFace:FONT,fontSize:10,bold:true,color:b[2],align:'center',margin:0});
      
    });
    slide.addText(it.label,{x:x,y:baseY+0.5,w:groupW,h:0.38,fontFace:FONT,fontSize:9.5,bold:true,color:COLORS.ink,align:'center',margin:0,fit:'shrink'});
    x+=groupW+groupGap;
  });
  slide.addText('Fictional practice data', {x:1.3,y:1.78,w:3.0,h:0.22,fontFace:FONT,fontSize:9.5,color:COLORS.muted,margin:0});
  slide.addShape(SH.rect,{x:9.7,y:1.76,w:0.13,h:0.13,fill:{color:COLORS.blue},line:{color:COLORS.blue}});
  slide.addText('Before',{x:9.9,y:1.72,w:0.55,h:0.2,fontFace:FONT,fontSize:8.5,color:COLORS.muted,margin:0});
  slide.addShape(SH.rect,{x:10.65,y:1.76,w:0.13,h:0.13,fill:{color:meta.accent},line:{color:meta.accent}});
  slide.addText('After',{x:10.85,y:1.72,w:0.55,h:0.2,fontFace:FONT,fontSize:8.5,color:COLORS.muted,margin:0});
}

function addTwoColumn(slide,title,leftTitle,leftItems,rightTitle,rightItems,meta,idx,total,opts={}){
  addBase(slide,meta,idx,total,opts.backup); addTitle(slide,title,opts.subtitle||meta.subtitle,meta);
  [[1.0,leftTitle,leftItems,meta.pale,meta.accent],[6.9,rightTitle,rightItems,COLORS.amberPale,COLORS.amber]].forEach(([x,h,items,fill,color])=>{
    slide.addShape(SH.roundRect,{x,y:2.05,w:5.0,h:3.6,rectRadius:0.06,fill:{color:fill},line:{color,width:1.2}});
    slide.addText(h,{x:x+0.25,y:2.35,w:4.5,h:0.35,fontFace:FONT,fontSize:15,bold:true,color,align:'center',margin:0,fit:'shrink'});
    slide.addText(items.map(cleanDecisionItem).join('\n'),{x:x+0.5,y:3.05,w:4.0,h:1.8,fontFace:FONT,fontSize:14,bold:true,color:COLORS.ink,align:'center',margin:0.03,fit:'shrink',paraSpaceAfterPt:8});
  });
}

const decks = [
  {file:'process-business',title:'Process Improvement: Business Client',subject:'Reducing Import Document Handoff Delays',accent:COLORS.blue,pale:COLORS.bluePale,subtitle:'Reducing import document handoff delays',family:'Process Improvement Briefing | Business-client sample slide set',slides:[
    ['decision','Approve a Four-Week Workflow Pilot','Decision today: pilot the shared exception log. / Confirm the checkpoint owner. / Review delay and rework after four weeks.'],
    ['flow','Handoff Notes Are Spread Across Three Places','Email: messages split / Spreadsheet: copied details / Short messages: owner unclear'],
    ['cards','Most Delays Involve Unclear Handoff Notes','Late handoffs: 38 / Unclear notes: 61% / Average rework: 22 minutes'],
    ['beforeAfter','One Shared Log Makes Ownership Visible Earlier',{before:['Email check: messages split','Manual note: copied details','Handoff: owner unclear','Deadline risk: late handoff'],after:['Exception log: one shared list','Checkpoint: fixed time','Owner: next action visible','Control: unchanged']}],
    ['timeline','The Pilot Is Limited and Controlled','Week 0: review fields / Weeks 1-4: daily checkpoint / End: review delay / Review: rework and feedback'],
    ['decision','The Request Is Approval, Ownership, and Review Criteria','Approve the pilot. / Confirm the documentation lead. / Agree the review measures.'],
  ]},
  {file:'process-government',title:'Process Improvement: Government Agency',subject:'Reducing Returned Application Forms',accent:COLORS.green,pale:COLORS.greenPale,subtitle:'Reducing returned application forms',family:'Process Improvement Briefing | Government-agency sample slide set',slides:[
    ['decision','Approve a One-Month Intake Checklist Trial','Decision today: trial the checklist. / Agree first fields. / Assign the FAQ owner.'],
    ['flow','Errors Are Found Too Late in the Process','Submit: form received / Formal review: error found / Returned form: user contacted / Repeat inquiry: delay grows'],
    ['cards','Most Returns Come from Common Preventable Errors','Returned applications: 142 / Missing one attachment: 54% / Incomplete contact or ID field: 31%'],
    ['flow','A Short Intake Check Catches Errors Earlier','Quick intake check: first contact / Shared FAQ: common answers / Formal review: unchanged'],
    ['timeline','The Trial Measures Service Benefit and Counter Time','Scope: one application type / Time: one month / Review: returns and reasons / Feedback: inquiries and staff comments'],
    ['decision','The Request Is Trial Approval and FAQ Ownership','Approve the trial. / Confirm checklist fields. / Assign one FAQ owner.'],
  ]},
  {file:'launch-business',title:'Launch: Business Client',subject:'Supplier-Status Dashboard Pilot',accent:COLORS.teal,pale:COLORS.tealPale,subtitle:'Supplier-status dashboard pilot',family:'Launch Briefing | Business-client sample slide set',slides:[
    ['decision','Approve a Four-Week Dashboard Pilot','Decision today: confirm pilot teams, launch date, and feedback owner'],
    ['cards','Repeated Status Checks Are Taking Time','Status-check messages: 74 last cycle / Staff time: about 9 hours per week / Source: spread across teams'],
    ['cards','The Dashboard Shows What Needs Attention First','Status / Deadline / Owner / Next action'],
    ['cards','The Pilot Creates Three Practical Benefits','Earlier view / Fewer repeated messages / Clearer ownership'],
    ['timeline','The Rollout Tests Adoption Before Expansion','Week 0: prepare / Week 1: launch / Weeks 2-3: adjust / Week 4: review'],
    ['decision','The Next Step Is to Confirm the Pilot Users','Today: nominate two teams / Friday: send access plan / Monday: start pilot'],
  ]},
  {file:'launch-government',title:'Launch: Government Agency',subject:'Application Support Desk Pilot',accent:COLORS.green,pale:COLORS.greenPale,subtitle:'Application support desk pilot',family:'Launch Briefing | Government-agency sample slide set',slides:[
    ['decision','Approve a Three-Month Support Desk Pilot','Decision today: schedule, staffing, and review measures'],
    ['cards','Many Online Form Questions Happen Before Submission','Online form inquiries: 312 / Attachments or fields: 47% / Repeat contact: 28%'],
    ['flow','The Support Desk Helps Before Submission','User starts form / Support point / User submits / Staff review'],
    ['cards','The Desk Reduces Preventable Repeat Work','Fewer incomplete forms / Fewer repeat contacts / Clearer guidance'],
    ['timeline','The Pilot Starts Limited and Reviews Evidence','Prepare: staff guide / Month 1: limited hours / Month 2: improve guidance / Month 3: review'],
    ['decision','The Next Step Is Pilot Approval','Approve schedule / Confirm staffing / Agree review measures'],
  ]},
  {file:'results-business',title:'Results Briefing: Business Client',subject:'Exception Resolution Pilot',accent:COLORS.blue,pale:COLORS.bluePale,subtitle:'Exception resolution pilot results',family:'Results Briefing | Business-client sample slide set',slides:[
    ['decision','Approve a Controlled Expansion of the Exception Resolution Pilot','Decision today: expand to two more desks for six weeks / Controls: morning log check + duplicate-entry owner'],
    ['beforeAfter','The Pilot Targeted Unclear Exception Ownership',{before:['Problem: separate messages','Ownership: unclear','Rework: repeated clarification'],after:['Shared log: one place','Checkpoint: fixed daily time','Goal: fewer late handoffs']}],
    ['bars','Late Handoffs Fell from 38 to 27',[{label:'Late document handoffs',before:38,after:27},{label:'Rework time (min)',before:22,after:16},{label:'Ownership clearer (%)',before:48,after:82}]],
    ['twoColumn','The Result Is Positive, but Two Controls Are Needed',{leftTitle:'What improved',leftItems:['Clearer ownership','Fewer repeated messages'],rightTitle:'What remains',rightItems:['Morning updates','Duplicate entries: 9 cases']}],
    ['cards','Expand, but Do Not Move to Full Rollout Yet','Recommendation: two more desks / Period: six weeks / Review: same measures + volume-adjusted view'],
    ['cards','Volume Check: Improvement Remained Visible','Backup question: Was volume lower? / Check: compare result against average daily volume / Use only if asked',{backup:true}],
  ]},
  {file:'results-government',title:'Results Briefing: Government Agency',subject:'Intake Checklist Trial',accent:COLORS.green,pale:COLORS.greenPale,subtitle:'Intake checklist trial results',family:'Results Briefing | Government-agency sample slide set',slides:[
    ['decision','Approve Limited Expansion of the Intake Checklist','Decision today: expand to two more application types / Add: one update owner / Review again after one month'],
    ['flow','The Checklist Catches Preventable Errors Earlier','Before: errors found after formal review / Trial: front-counter checklist + shared FAQ / Aim: fewer returns and repeat inquiries'],
    ['flow','The Checklist Fits Before Formal Review','Check: attachment / Check: contact field / Check: ID field / Check: signature'],
    ['bars','Returned Applications Fell from 142 to 111',[{label:'Returned applications',before:142,after:111},{label:'Repeat inquiries',before:86,after:68},{label:'Attachment returns',before:77,after:58}]],
    ['cards','Expand with One Owner and Monitor Waiting Time','Next: two high-volume application types / Owner: document-review team / Monitor: returns, repeat inquiries, waiting time'],
    ['cards','Staff Feedback: The Checklist Added About 40 Seconds','Backup question: Will the counter line get longer? / Staff feedback: about 40 seconds per intake / Monitor during expansion',{backup:true}],
  ]},
];

function addSlideByType(ppt, meta, spec, idx){
  const slide=ppt.addSlide();
  const [type,title,data,extra]=spec;
  if(type==='decision') addDecision(slide,title,textItems(data),meta,idx,6,extra && extra.backup);
  else if(type==='cards') addCards(slide,title,data,meta,idx,6,extra||{});
  else if(type==='flow') addFlow(slide,title,textItems(data),meta,idx,6,extra||{});
  else if(type==='timeline') addTimeline(slide,title,textItems(data),meta,idx,6,extra||{});
  else if(type==='beforeAfter') addBeforeAfter(slide,title,data.before,data.after,meta,idx,6,extra||{});
  else if(type==='bars') addSimpleBars(slide,title,data,meta,idx,6,extra||{});
  else if(type==='twoColumn') addTwoColumn(slide,title,data.leftTitle,data.leftItems,data.rightTitle,data.rightItems,meta,idx,6,extra||{});
  warnIfSlideHasOverlaps(slide,ppt,{muteContainment:true,ignoreLines:true,ignoreDecorativeShapes:true});
  warnIfSlideElementsOutOfBounds(slide,ppt);
}

(async()=>{
  for (const deck of decks) {
    const ppt = makeDeck(deck);
    deck.slides.forEach((s,i)=>addSlideByType(ppt,deck,s,i+1));
    await ppt.writeFile({ fileName: `${OUT}/${deck.file}.pptx` });
    console.log(`wrote ${deck.file}.pptx`);
  }
})();



