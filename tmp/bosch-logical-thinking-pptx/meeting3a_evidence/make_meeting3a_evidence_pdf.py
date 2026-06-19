from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from pypdf import PdfReader, PdfWriter

src = Path(r"\\prod-fs-gen01\WorkFile\04_在宅勤務\★グローバルビジネス推進部（在宅）\ランゲージサービス課\Dobson（在宅）\02. Clients\Bosch\Logical Thinking & Discussion\Activities\Meeting 3a - Bosch EV Dilemma Simulation_r20251112.pdf")
out_dir = Path(r"\\prod-fs-gen01\WorkFile\04_在宅勤務\★グローバルビジネス推進部（在宅）\ランゲージサービス課\Dobson（在宅）\04. Projects\code\textmaker\tmp\bosch-logical-thinking-pptx\meeting3a_evidence")
summary_pdf = out_dir / "evidence_summary_revised_pages.pdf"
out_pdf = out_dir / "Meeting 3a - Bosch EV Dilemma Simulation_r20251112_evidence-holders.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.2, leading=8.5, spaceAfter=0))
styles.add(ParagraphStyle(name="Tiny", parent=styles["BodyText"], fontName="Helvetica", fontSize=6.6, leading=7.8, spaceAfter=0))
styles.add(ParagraphStyle(name="Head", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=colors.HexColor("#1F4E79"), spaceAfter=4))
styles.add(ParagraphStyle(name="Sub", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=10, textColor=colors.HexColor("#333333"), spaceAfter=6))
styles.add(ParagraphStyle(name="TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.2, leading=8.5, textColor=colors.white, alignment=1))
styles.add(ParagraphStyle(name="Role", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.0, leading=8.2, textColor=colors.HexColor("#1F4E79")))

role_rows = [
    ["Profit target", "Bosch's 2024 Annual Report shows a 9% profit margin goal for its EV division.", "Bosch Corporate Report 2024", "Role A: Managing Director (Chair)"],
    ["Cost comparison", "European supplier: JPY 40,000 per unit; Southeast Asian supplier: JPY 27,000 per unit (33% cheaper).", "Purchasing Department estimates", "Role B: Purchasing Manager"],
    ["Annual savings", "Potential JPY 1.2 billion cost reduction per year if switching supplier.", "Purchasing Manager data", "Role B: Purchasing Manager"],
    ["Global battery prices", "Lithium-ion battery prices fell 14% globally in 2024.", "Bloomberg 2024 Energy Market Data", "Role B: Purchasing Manager"],
    ["Consumer ethics", "78% of Japanese consumers would stop buying from unethical companies.", "Nikkei Survey 2023", "Role A: Managing Director (Chair)"],
    ["ESG investor trends", "65% of global investors prioritize ESG performance.", "Deloitte ESG Survey 2023", "Role C: Sustainability Officer"],
    ["Emissions concern", "Southeast Asian supplier emits 30% more CO2 per unit than standard.", "NGO Environmental Report 2024", "Role C: Sustainability Officer"],
    ["Bosch sustainability goals", "Bosch aims for carbon neutrality (Scope 1 & 2) by 2030 and 15% Scope 3 reduction by 2027.", "Bosch Sustainability Policy", "Role C: Sustainability Officer"],
    ["Legal risk", "EU CSDDD to require full supply-chain transparency by 2026.", "European Commission Directive Summary", "Role D: Legal Counsel"],
    ["Legal penalties", "Fines up to 5% of global annual turnover for ESG violations.", "EU Compliance Guidelines", "Role D: Legal Counsel"],
]

additional_rows = [
    ["Technical / logistics fit", "Southeast Asian supplier can meet technical and logistical requirements and deliver on time.", "Purchasing verification", "Role B: Purchasing Manager"],
    ["ESG risk control plan", "ESG risks could be managed through regular audits, supplier contracts, penalties, and a draft 12-month monitoring plan.", "Purchasing planning note", "Role B: Purchasing Manager"],
    ["Verification gap", "Southeast Asian supplier emissions reports lack third-party verification.", "Legal compliance review", "Role D: Legal Counsel"],
    ["Due diligence liability", "Bosch may be liable later if it fails to perform adequate due diligence before contracting.", "Legal risk assessment", "Role D: Legal Counsel"],
    ["Customer ESG expectations", "72% of automotive buyers say ESG factors influence their decisions; customers also demand stability and quality.", "Dentsu Research 2024", "Role E: Customer Sales Manager"],
    ["Customer approval", "Customers will likely need formal documentation and testing approval before accepting a new supplier.", "Customer account knowledge", "Role E: Customer Sales Manager"],
    ["Supplier reliability", "European supplier has a 12-year partnership record and a 99.2% on-time delivery rate.", "R&D / supplier history", "Role F: Head of R&D"],
    ["Quality failure rates", "European supplier failure rate is below 0.3%; Southeast Asian supplier trial rate is 2.1%.", "Technical trial data", "Role F: Head of R&D"],
    ["Warranty / recall risk", "Delays or quality issues could add JPY 300 million in warranty and recall costs.", "Technical risk estimate", "Role F: Head of R&D"],
    ["Future emissions improvement", "European supplier is testing a recycling process that could reduce production emissions by 10% by 2026.", "R&D technical update", "Role F: Head of R&D"],
]

def p(txt, style="Small"):
    return Paragraph(str(txt), styles[style])

def make_table(rows):
    data = [[p("Category", "TableHead"), p("Fact / Statistic", "TableHead"), p("Source or Context", "TableHead"), p("Held by before meeting", "TableHead")]]
    for cat, fact, source, role in rows:
        data.append([p(cat, "Small"), p(fact, "Tiny"), p(source, "Tiny"), p(role, "Role")])
    table = Table(data, colWidths=[31*mm, 80*mm, 43*mm, 40*mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1F4E79")),
        ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#A6A6A6")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 3),
        ("RIGHTPADDING", (0,0), (-1,-1), 3),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F7F9FC")]),
    ]))
    return table

story = []
story.append(p("Evidence Summary Sheet", "Head"))
story.append(p("Use this sheet after the simulation to review factual evidence, evaluate how it was applied in discussion, and connect data points to the final decision. The final column identifies which role had the information before the meeting began.", "Sub"))
story.append(make_table(role_rows))
story.append(PageBreak())
story.append(p("Additional Role Evidence", "Head"))
story.append(p("The original summary table did not include several role-specific data points. These items may be useful when checking whether the meeting discussion used the available evidence fully.", "Sub"))
story.append(make_table(additional_rows))
story.append(Spacer(1, 4*mm))
story.append(p("Note: The simulation states that facts, figures, and sources are fictionalized for educational purposes.", "Sub"))

doc = SimpleDocTemplate(str(summary_pdf), pagesize=A4, leftMargin=8*mm, rightMargin=8*mm, topMargin=10*mm, bottomMargin=10*mm)
doc.build(story)

writer = PdfWriter()
reader = PdfReader(str(src))
for i in range(5):
    writer.add_page(reader.pages[i])
summary_reader = PdfReader(str(summary_pdf))
for page in summary_reader.pages:
    writer.add_page(page)
with out_pdf.open("wb") as f:
    writer.write(f)
print(out_pdf)
