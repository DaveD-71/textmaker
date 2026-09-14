"""
Merge each LTF book's 20 per-topic article files into a single
student-edition markdown file: front matter, then all 20 topics in
Part.Topic order, with a `\\pagebreak` marker and a two-paragraph Part
description inserted before each Part's first topic.

The two-paragraph Part descriptions match the depth of the IR project's
own Part dividers (confirmed by direct inspection of
`Investor Relations Resource - Articles.docx`): one paragraph introducing
the Part's theme and its first 2-3 topics by name, a second paragraph
covering the remaining topics and closing on a unifying point.

This is the Phase 6 "assemble" step for the student edition; the output
feeds `build_ltf_student_edition_md.py` (Vocabulary Focus / hyperlink
transform) and then the DOCX build pipeline.

Usage: python build_ltf_student_edition_merge.py
(no arguments; paths and Part descriptions are defined below)
"""
import re
import os

PART_DESC_A = {
    1: """Money, Payments and Financial Technology looks at what happens when a payment system changes faster than the rules built to govern it. Cryptocurrency moved from a niche curiosity to a market large enough that governments in Japan, the European Union and the United States each felt compelled to write dedicated rules, though they chose very different approaches. Central bank digital currencies raise a related but distinct question: not whether private money needs supervision, but whether central banks should offer a public digital alternative at all, and almost every country studying one has so far chosen not to launch.

The same tension between innovation and oversight runs through fintech regulation, where regulatory sandboxes let new payment models prove themselves under supervision before rules are finalised. It also runs through data privacy, where the same personal information that makes a service convenient becomes a liability the moment it crosses a border without adequate protection, and through financial inclusion, where mobile money and agent banking have brought hundreds of millions of previously unbanked adults into the formal financial system while a fully banked country like Japan faces a very different inclusion problem: keeping cash and branch access available as both quietly disappear. Across all five topics, the same question recurs: does a new technology need its own new rulebook, or can it be supervised inside the old one?""",
    2: """Markets, Institutions and Financial Stability turns to the machinery that is supposed to catch trouble before it spreads. Circuit breakers and daily price limits exist to slow a market panic down long enough for information, not fear, to set prices again, while credit rating agencies translate a borrower's complex financial position into a single letter grade that investors around the world rely on, sometimes too heavily. Insurance regulation asks a related question over a much longer time horizon: whether an insurer holds enough capital today to make good on promises it will not have to pay out for decades.

Stress testing brings these ideas together directly, deliberately imagining a bank's worst plausible future to check whether its capital buffer would survive it, a test that only measures the risk it is designed to measure, as Signature Bank's failure showed. Sovereign debt management closes the part by moving from private institutions to governments themselves, examining how a country manages, restructures and, when necessary, defaults on debt owed not to one lender but to thousands of bondholders. Each of these five topics is really the same argument told through a different institution: a financial system is only as stable as the assumptions behind the safeguards nobody hopes to actually use.""",
    3: """Capital, Investment and Public Policy examines how governments direct large, long-lived flows of money toward public goals rather than private returns alone. Green finance channels capital toward environmental projects through green bonds and an increasingly strict taxonomy of what counts as genuinely sustainable, while infrastructure investment asks a more basic question: how a country pays for the roads, ports and power grids that no single investor would build alone, often through public-private partnerships that split the risk between them. Trade policy and tariffs cover a third form of government intervention, one that raises prices for consumers as a deliberate tool of economic or political strategy rather than a market failure to correct.

Pension reform and the post-COVID economic recovery close the part by looking at how public policy manages long-run demographic and economic shocks: an ageing population that slowly outgrows a pension system designed for a younger one, and a global pandemic recovery that left some economies richer than before and others permanently behind. These five topics share a common thread: each is a case where markets alone would produce an outcome society has decided not to accept, and government policy is the tool used to change it.""",
    4: """Finance, Fairness and Global Cooperation asks who bears the cost when the financial system is misused, and how far countries are willing to cooperate to stop it. Anti-money-laundering rules make banks the front line against criminals who try to disguise illegal money as legitimate, a system that only works if every country enforces it, since a gap in one jurisdiction can undermine strict rules everywhere else. Financial literacy programmes tackle a quieter version of the same fairness question: whether ordinary people have the knowledge to make sound financial decisions, or whether the system's complexity itself is a source of disadvantage.

Wealth inequality and corporate governance examine fairness from two more angles, one asking whether the very richest bear a fair share of the tax burden when their income is taxed differently from wages, the other asking whether a company's board genuinely represents shareholders or quietly serves management instead. Economic diplomacy closes the resource by taking the same fairness question to the level of nations, where sanctions and coordinated financial pressure are used as tools of foreign policy. Across all five topics, the resource ends where finance ultimately answers to something outside itself: not just markets, but law, ethics and international cooperation.""",
}

PART_DESC_B = {
    1: """Personal Finance and Household Money starts where finance is most immediately felt: in a household's own budget. Inflation and the cost of living set the backdrop for everything else in this part, since a sustained rise in prices quietly erodes savings and wages alike unless a central bank's target keeps it in check, as Japan's decades of near-zero inflation and Argentina's 211% crisis show from opposite extremes. Debt follows naturally, from the everyday compounding on an unpaid credit-card balance to the newer, less regulated pull of buy-now-pay-later, while saving and investing for the long term asks the flip side of the same question: how compounding, given enough time, works in a saver's favour instead.

Housing markets and affordability bring these threads together in the single largest purchase most households ever make, where interest rates, supply constraints and local policy all interact to decide whether a place to live is treated as shelter or as an investment. The part closes with scams, fraud and financial self-defence, a reminder that every one of these systems, credit, savings, housing, depends on trust, and that trust is exactly what organised fraud is designed to exploit. Across all five topics, the same lesson recurs: household financial wellbeing depends on forces, like inflation and interest rates, that no individual controls, and skills, like recognising a scam, that every individual can still learn.""",
    2: """Companies, Work and Money moves from the household to the organisations that employ people and raise capital. How companies raise money lays the foundation, contrasting the public discipline of an IPO with the private flexibility that has let firms like SpaceX stay unlisted for years while still raising billions, and startups and venture capital extends the same theme into the highest-risk end of that spectrum, where most funded companies still fail and a rare few become unicorns. The gig economy and income security shifts from how companies raise money to how they organise work itself, asking what happens to benefits, pensions and job security when employment becomes platform-based and irregular.

Executive pay and inequality inside firms turns to a different fault line, the growing gap between what a top executive earns and what a median employee does, and how shareholders can vote, even if only symbolically, on whether that gap is justified. The part ends with banks: what they do and how they fail, using cases from Silicon Valley Bank to the broader mechanics of deposit insurance to explain why a bank run can turn a solvent institution into a failed one within hours. These five topics together describe modern work and enterprise as a set of trade-offs between risk and reward, control and flexibility, that plays out differently for founders, workers and executives alike.""",
    3: """Markets, Risk and the Global Economy zooms out to the forces that move prices and capital across entire economies. What moves stock markets opens by naming the four real drivers behind any market move, earnings, interest rates, sentiment and index concentration, correcting the common habit of assigning a single tidy cause to what is usually several forces acting together. Bubbles, crashes and manias traces the same pattern across four centuries, from Dutch tulip bulbs to Japan's late-1980s property bubble to a 2022 cryptocurrency collapse, showing that cheap money, herd behaviour and the belief that "this time is different" recur in every era.

Commodities, currencies and emerging markets close the part by looking at risk that crosses borders directly: a bakery in Tokyo paying more for flour because of a war fought thousands of kilometres away, a currency's value shifting because of a decision made by a foreign central bank, and a developing economy's access to capital drying up the moment global interest rates rise. These five topics share a single insight: in a genuinely global financial system, a shock rarely stays confined to the market or country where it started.""",
    4: """Money, Society and the Future closes the resource by asking what money is for beyond markets and firms. Tax and government debt open the part together, examining how governments raise the money that pays for public services and what happens when spending consistently outruns revenue, a tension that toppled a British prime minister in 2022 and that Japan has so far managed without a crisis for reasons that are still debated. The business of sport, art and culture turns to a less obvious kind of finance, where a single painting can sell for more than an orchestra's annual budget and Saudi Arabia's sovereign wealth fund buys football clubs partly for "soft power" rather than financial return alone.

Philanthropy, foundations and impact examines how large-scale giving is structured, taxed and increasingly judged by measurable outcomes rather than good intentions alone, while the future of money closes the resource by asking where money itself is heading, from Sweden's now-reversing retreat from cash to central bank digital currencies still stuck at the pilot stage almost everywhere. Across all five topics, the resource ends on the same note it began: money is not only a tool for individual households or companies, but a shared system that societies continually choose, and re-choose, how to run.""",
}

BOOKS = [
    {
        "name": "Let's Talk Finance",
        "title": "Let's Talk Finance",
        "dir": r"books/Let's Talk Finance/drafts/articles",
        "out": r"books/Let's Talk Finance/drafts/output/Let's Talk Finance - Student Edition.md",
        "parts": {
            1: ("Money, Payments and Financial Technology", PART_DESC_A[1]),
            2: ("Markets, Institutions and Financial Stability", PART_DESC_A[2]),
            3: ("Capital, Investment and Public Policy", PART_DESC_A[3]),
            4: ("Finance, Fairness and Global Cooperation", PART_DESC_A[4]),
        },
    },
    {
        "name": "Let's Talk Finance 2",
        "title": "Let's Talk Finance 2",
        "dir": r"books/Let's Talk Finance 2/drafts/articles",
        "out": r"books/Let's Talk Finance 2/drafts/output/Let's Talk Finance 2 - Student Edition.md",
        "parts": {
            1: ("Personal Finance and Household Money", PART_DESC_B[1]),
            2: ("Companies, Work and Money", PART_DESC_B[2]),
            3: ("Markets, Risk and the Global Economy", PART_DESC_B[3]),
            4: ("Money, Society and the Future", PART_DESC_B[4]),
        },
    },
]


def sort_key(fname):
    m = re.match(r"(\d+)-(\d+)_", fname)
    return (int(m.group(1)), int(m.group(2)))


def main():
    for book in BOOKS:
        d = book["dir"]
        files = [f for f in os.listdir(d) if f.endswith(".md") and not f.startswith("00_")]
        files.sort(key=sort_key)

        front_matter_path = os.path.join(d, "00_How_This_Resource_Is_Organized.md")
        front_matter = open(front_matter_path, encoding="utf-8").read().strip()
        front_matter_body = front_matter.split("\n", 1)[1].strip()

        out_parts = []
        out_parts.append(f"# {book['title']}\n")
        out_parts.append("## How This Resource Is Organized\n\n" + front_matter_body)

        current_part = None
        for fname in files:
            part_num, topic_num = sort_key(fname)
            if part_num != current_part:
                current_part = part_num
                title, desc = book["parts"][part_num]
                out_parts.append(f"\n\n\\pagebreak\n\n# Part {part_num}: {title}\n\n{desc}")
            content = open(os.path.join(d, fname), encoding="utf-8").read().strip()
            out_parts.append("\n\n" + content)

        final_text = "\n".join(out_parts).rstrip() + "\n"

        os.makedirs(os.path.dirname(book["out"]), exist_ok=True)
        with open(book["out"], "w", encoding="utf-8", newline="\n") as f:
            f.write(final_text)

        word_count = len(re.findall(r"\S+", final_text))
        topic_count = len(files)
        print(f"{book['name']}: wrote {book['out']} - {topic_count} topics, {word_count} words total")


if __name__ == "__main__":
    main()
