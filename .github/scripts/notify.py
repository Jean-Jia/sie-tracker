#!/usr/bin/env python3
"""SIE Exam Tracker — Feishu Notification Script
Usage: python notify.py <type> <supabase_key>
Types: daily-reminder | missed-checkin | weekly-report | behind-alert
"""
import sys
import json
import requests
from datetime import date, timedelta

# ── CONFIG ──────────────────────────────────────────────
SUPABASE_URL   = 'https://cupdvksfzqpjedibajus.supabase.co'
SUPABASE_KEY   = sys.argv[2] if len(sys.argv) > 2 else ''
SITE_URL       = 'https://jean-jia.github.io/sie-tracker/'
TRACKING_START = date(2026, 5, 8)
TOTAL_CHAPTERS = 20
TODAY          = date.today()
DRY_RUN        = '--dry-run' in sys.argv

USERS = {
    'jiannbinkhor': {'name':'Jiannbin Khor', 'startChapter':11, 'examDate':date(2026,6,5),  'weeklyHours':11.5, 'studyStart':date(2026,4,6)},
    'nicholasneoh': {'name':'Nicholas Neoh', 'startChapter':1,  'examDate':date(2026,7,5),  'weeklyHours':5,    'studyStart':date(2026,4,13)},
    'daisywang':    {'name':'Daisy Wang',    'startChapter':5,  'examDate':date(2026,6,25), 'weeklyHours':6,    'studyStart':date(2026,4,10)},
    'cindylin':     {'name':'Cindy Lin',     'startChapter':0,  'examDate':date(2026,7,5),  'weeklyHours':5,    'studyStart':date(2026,4,6)},
    'suqinng':      {'name':'Su Qin Ng',     'startChapter':0,  'examDate':date(2026,6,15), 'weeklyHours':9,    'studyStart':date(2026,4,20)},
    'jeremyzhang':  {'name':'Jeremy Zhang',  'startChapter':0,  'examDate':date(2026,6,15), 'weeklyHours':9,    'studyStart':date(2026,4,30)},
}

OFFICIAL_NOTES = {
    1: (
        "**Ch.1 Market Participants & Structure**\n"
        "• Broker-dealer roles: investment banker (primary mkt) vs market maker (secondary mkt)\n"
        "• Broker = agent (earns commission); Dealer = principal (earns markup)\n"
        "• Investor types: institutional / accredited / QIB / individual\n"
        "• Primary mkt (new issues) vs Secondary mkt (existing securities)\n"
        "• Market platforms: physical vs electronic; NMS vs OTC equities; Third & Fourth Market\n"
        "• DTCC: handles clearing, settlement, and custody electronically\n"
        "• Clearing firm (back-office) vs Introducing firm (client-facing)"
    ),
    2: (
        "**Ch.2 Overview of Regulation**\n"
        "• SEC: primary federal regulator; NASAA: state Blue Sky laws; FRB: monetary policy & margin\n"
        "• Act of 1933: primary market / new issuances / prospectus requirement\n"
        "• Act of 1934: secondary market / created the SEC\n"
        "• Investment Company Act 1940: mutual funds; Investment Advisers Act 1940: advisers\n"
        "• SIPC: protects customers if BD fails — up to $500K ($250K cash); NOT investment losses\n"
        "• FINRA: largest SRO; Code of Conduct + Code of Arbitration\n"
        "• MSRB: regulates municipal securities dealers; no enforcement power\n"
        "• WSP (Written Supervisory Procedures): every firm must maintain one"
    ),
    3: (
        "**Ch.3 Equity Securities**\n"
        "• Common stock: growth; highest bankruptcy risk; voting rights (board/mergers, NOT dividends)\n"
        "• Treasury shares: repurchased; no votes, no dividends, not outstanding\n"
        "• Preferred stock: income; interest rate risk; no voting; dividends before common\n"
        "• Cumulative preferred: unpaid dividends accumulate (arrears) → must pay before common\n"
        "• Convertible preferred: more price stability when rates fluctuate\n"
        "• Rights: short-term (30–45 days), below-market price; Warrants: long-term, above-market\n"
        "• ADRs: U.S. investors buy foreign stocks in USD; market risk + currency risk\n"
        "• Sponsored ADRs trade on exchanges; Unsponsored ADRs trade OTC"
    ),
    4: (
        "**Ch.4 Introduction to Debt Instruments**\n"
        "• Par = $1,000; Coupon/nominal yield; Current yield; YTM; YTC; Accrued interest\n"
        "• Accrued interest: corp/muni = 30/360; gov't = actual/365\n"
        "• Serial bonds: mature in installments; Term bonds: all mature same date\n"
        "• Interest rate risk: rates ↑ → bond prices ↓ (inverse relationship)\n"
        "• Bond ratings: investment grade ≥ Baa/BBB; junk < Ba/BB\n"
        "• Corp bonds trade in 1/8 point; Gov't bonds trade in 1/32 point\n"
        "• Call provision: issuer redeems early; Call protection period; Call premium above par\n"
        "• Put provision: bondholder sells back at par\n"
        "• Convertible bonds: convert to stock at conversion ratio; conversion is tax-free"
    ),
    5: (
        "**Ch.5 Types of Debt Instruments**\n"
        "• T-Bills (<1yr, discount); T-Notes (2–10yr); T-Bonds (>10yr); TIPS (inflation-adjusted)\n"
        "• Agency securities: GNMA (gov't backed) vs FNMA/FHLMC (gov't sponsored)\n"
        "• MBS prepayment risk: early payoff risk when interest rates fall\n"
        "• Municipal bonds — GO bonds: backed by taxes / Revenue bonds: backed by project revenue\n"
        "• Corporate bonds: secured (mortgage bonds) vs unsecured (debentures/income bonds)\n"
        "• Tax: U.S. gov't interest = federal taxable, state exempt\n"
        "• Municipal interest = federal exempt (may be state exempt)\n"
        "• Eurodollar bonds, Yankee bonds, Eurobonds: international debt distinctions"
    ),
    6: (
        "**Ch.6 Investment Returns**\n"
        "• Ex-dividend date: stock trades without dividend; price drops by dividend amount\n"
        "• Bond prices and yields move inversely: rates ↑ → prices ↓\n"
        "• Discount bond yields: nominal < current < YTM\n"
        "• Premium bond yields: nominal > current > YTM\n"
        "• Basis points: 1 bp = 0.01%; 100 bp = 1%\n"
        "• Cost basis: original purchase price; Sales proceeds − cost basis = capital gain/loss\n"
        "• Total return = income (dividends/interest) + capital gain/loss\n"
        "• Current yield = annual income ÷ current market price\n"
        "• DJIA: price-weighted, 30 stocks; S&P 500: market cap-weighted, 500 stocks"
    ),
    7: (
        "**Ch.7 Packaged Products (Mutual Funds)**\n"
        "• 3 types of investment companies: management cos (open/closed-end), UITs, face amount certs\n"
        "• Open-end (mutual fund): issue/redeem at NAV; NAV = (assets − liabilities) ÷ shares\n"
        "• POP = NAV ÷ (1 − sales charge %); Forward pricing: next calculated NAV\n"
        "• Share classes: A = front-end load (breakpoints); B = back-end CDSC; C = level 12b-1 fee\n"
        "• 12b-1 fee: distribution/marketing fee, max 1% annually\n"
        "• Sales charge reductions: breakpoints, letter of intent (13 months), rights of accumulation\n"
        "• Violations: breakpoint sales, large Class B purchases, unsuitable switching\n"
        "• Dollar cost averaging: fixed dollar invested regularly → buys more shares at lower prices\n"
        "• Closed-end funds: fixed shares, trade on exchanges, may trade at premium/discount to NAV"
    ),
    8: (
        "**Ch.8 Variable Contracts & Municipal Fund Securities**\n"
        "• Fixed annuity: guaranteed rate, general account; Variable annuity: separate account (SEC-registered)\n"
        "• Accumulation phase: tax-deferred growth; Annuity phase: periodic payments begin\n"
        "• Withdrawals: ordinary income tax on gains (LIFO) + 10% penalty if under 59½\n"
        "• Payout options: life only, life with period certain, joint & survivor, lump sum\n"
        "• Death benefit: greater of account value or total premiums paid\n"
        "• 1035 Exchange: tax-free exchange of one annuity/life policy for another\n"
        "• Qualified annuity: pre-tax funds; Non-qualified: after-tax (cost basis applies)\n"
        "• 529 plans: state-sponsored, tax-free growth for qualified education expenses\n"
        "• 529 ABLE: for individuals with disabilities; SECURE Act: 529 can roll to Roth IRA (max $35K)"
    ),
    9: (
        "**Ch.9 Alternative Investments**\n"
        "• ETFs: investment companies (NOT mutual funds); passively managed; trade on exchanges\n"
        "• Inverse ETF: opposite of benchmark; Leveraged ETF: amplified returns (2x/3x)\n"
        "• ETNs: unsecured bank debt; issuer credit risk is the key risk factor\n"
        "• Hedge funds: private, largely unregulated; accredited investors only\n"
        "• REITs: invest in real estate; distribute ≥90% of income; taxed as corporations\n"
        "  – Equity REIT (owns property), Mortgage REIT (holds mortgages), Hybrid (both)\n"
        "• DPPs: flow-through vehicles; income/losses pass directly to investors\n"
        "• Limited partnerships: GP = manages + unlimited liability; LP = passive + limited liability\n"
        "• LP liquidation order: secured creditors → unsecured creditors → limited partners → GP"
    ),
    10: (
        "**Ch.10 Options**\n"
        "• Call = right to buy; Put = right to sell; both have buyers (long) and sellers/writers (short)\n"
        "• Premium = Intrinsic Value + Time Value\n"
        "• ITM call: market > strike; ITM put: market < strike\n"
        "• Strategies: Long call / Short put = Bullish; Short call / Long put = Bearish\n"
        "• Breakeven: call = strike + premium; put = strike − premium\n"
        "• Long call: max gain = unlimited; max loss = premium paid\n"
        "• Short call: max gain = premium; max loss = unlimited\n"
        "• Covered call: writer owns the stock; Uncovered/naked: writer does not own stock\n"
        "• OCC: counterparty to every option; guarantees performance\n"
        "• Equity options: physical delivery of 100 shares; Index options: cash settlement"
    ),
    11: (
        "**Ch.11 Offerings**\n"
        "• IPO = company's first public stock sale; Split offering = new + existing shares\n"
        "• Underwriting types: Firm commitment / Best efforts / All-or-none / Mini-maxi / Stand-by\n"
        "• Shelf registration (Rule 415): register securities to sell over 2-year period\n"
        "• Red Herring = preliminary prospectus (no price); Statutory = final prospectus\n"
        "• Exempt securities: U.S. gov't, municipal bonds, nonprofits, commercial paper (<270 days)\n"
        "• Accredited investor: net worth >$1M (excl. primary home) OR income >$200K/$300K (joint)\n"
        "• Rule 144: resale of restricted/control stock (volume limits + holding period)\n"
        "• Rule 144A: restricted securities resold to QIBs without SEC registration\n"
        "• Rule 147/147A: intrastate offerings; QIB = institution with >$100M in securities\n"
        "• Official statement = municipal bond disclosure doc; EMMA = MSRB's public disclosure system"
    ),
    12: (
        "**Ch.12 Orders & Trading Strategies**\n"
        "• Broker = agent (commission); Dealer = principal (markup on buy, markdown on sell)\n"
        "• 5% policy: FINRA guideline for reasonable markups/commissions; not a firm rule\n"
        "• Short sale: sell borrowed shares expecting price drop; must be covered later\n"
        "• Order types:\n"
        "  – Market order: best available price immediately\n"
        "  – Limit order: execute at specified price or better\n"
        "  – Stop order: becomes market order when stop price hit\n"
        "  – Stop-limit order: becomes limit order (not market) when triggered\n"
        "• Day order: expires end of day; GTC: open until executed or cancelled\n"
        "• Margin account: borrow up to 50% of purchase (Reg T); minimum equity $2,000\n"
        "• Proceeds transaction: sell one security to buy another = considered one transaction for 5% policy"
    ),
    13: (
        "**Ch.13 Settlement & Corporate Actions**\n"
        "• Regular-way settlement: corporate/municipal + gov't/options = T+1\n"
        "• Reg T payment: T+2; failure to pay → securities sold out + 90-day account freeze\n"
        "• Cash settlement: same-day; must be agreed by both parties\n"
        "• Good delivery: securities in proper form (correct denomination, properly endorsed)\n"
        "• Stock power: separate endorsement form enabling transfer without signing the certificate\n"
        "• Tender offer: offer to buy shares at premium; oversubscribed → prorated; undersubscribed → fewer shares\n"
        "• Forward stock split (2-for-1): double shares, half price; total value unchanged; cost basis halved\n"
        "• Reverse stock split: fewer shares, higher price; same total value\n"
        "• Stock splits: NOT taxable; cost basis adjusted proportionally"
    ),
    14: (
        "**Ch.14 Customer Accounts**\n"
        "• Cash account: pay in full by settlement; Margin account: borrow 50% (Reg T), min equity $2,000\n"
        "• Discretionary account: rep trades without prior approval; requires written authorization\n"
        "• Full POA: complete control; Limited POA: specific transactions only\n"
        "• Not-held order: time/price discretion given to rep — NOT a discretionary account\n"
        "• Joint accounts: JTWROS (right of survivorship) or TIC (share passes to estate)\n"
        "• Custodial UGMA/UTMA: minor is beneficial owner; custodian manages until majority\n"
        "• Retirement accounts:\n"
        "  – Traditional IRA: pre-tax, tax-deferred growth, RMDs at age 73\n"
        "  – Roth IRA: after-tax, tax-free growth, NO RMDs\n"
        "  – 401(k)/403(b): employer-sponsored, pre-tax, RMDs apply\n"
        "• ERISA: federal law governing private employer plans (eligibility, vesting, fiduciary duty)\n"
        "• Coverdell ESA: education savings, $2,000/year limit, tax-free for qualified expenses"
    ),
    15: (
        "**Ch.15 Compliance Considerations**\n"
        "• KYC (Know Your Customer): name, address, DOB, SSN, employment, financial info required\n"
        "• Trusted contact person: should be requested (not required); used if exploitation suspected\n"
        "• FINRA 3 suitability obligations:\n"
        "  1. Reasonable Basis: suitable for some investors\n"
        "  2. Customer-Specific: suitable for THIS customer\n"
        "  3. Quantitative: not excessive trading (anti-churning)\n"
        "• 3 stages of money laundering: Placement → Layering → Integration\n"
        "• FinCEN CTR: cash >$10,000; SAR: suspicious activity >$5,000 (don't tell customer)\n"
        "• Reg S-P: protect customers' non-public personal info (privacy notice required)\n"
        "• Communications: Correspondence (≤25 retail) / Retail Comm (>25 retail) / Institutional\n"
        "• BCP (Business Continuity Plan): required for all member firms\n"
        "• Records: 3 years (trade tickets, confirms), 6 years (account statements, blotters), lifetime (corporate docs)"
    ),
    16: (
        "**Ch.16 Prohibited Activities**\n"
        "• Regulation M: prohibits price manipulation during a distribution\n"
        "• Front-running: trading ahead of large customer order to profit from anticipated move\n"
        "• Churning: excessive trading to generate commissions (quantitative suitability violation)\n"
        "• Reverse churning: excessive inactivity in a fee-based account\n"
        "• Marking the close/open: trades near market open/close to manipulate closing prices\n"
        "• Interpositioning: unnecessary middleman to increase markups\n"
        "• Insider trading: trading on material, non-public information\n"
        "• Freeriding: buying and selling securities before paying (Reg T violation)\n"
        "• FINRA New Issue Rule: 'restricted persons' (BD employees, FINRA associates, family) cannot buy IPOs at POP\n"
        "• Sharing in customer accounts: only with written consent + proportional to investment\n"
        "• Borrowing/lending to clients: generally prohibited; limited exceptions apply\n"
        "• Temporary hold: firms can hold disbursements if financial exploitation of senior/adult suspected"
    ),
    17: (
        "**Ch.17 SRO Requirements for Associated Persons**\n"
        "• SIE Exam: entry-level; does NOT grant registration rights; must pass a 'top-off' exam (Series 6, 7, etc.)\n"
        "• Associated person: anyone employed by or associated with a FINRA member firm\n"
        "• Non-registered persons: clerical/admin only; no public interaction on securities; no securities-based pay\n"
        "• Form U4: required for all registered persons; filed via CRD (Central Registration Depository)\n"
        "• Statutory disqualification: criminal convictions, regulatory sanctions bar registration\n"
        "• Eligibility proceeding: firm can request disqualified person associate under heightened supervision\n"
        "• Fingerprinting: required for registered persons and certain non-registered persons\n"
        "• Must satisfy both FINRA AND state (Blue Sky) registration requirements\n"
        "• CE requirements:\n"
        "  – Regulatory Element: FINRA computer-based training, annually\n"
        "  – Firm Element: firm-specific training, developed by each firm\n"
        "• Special Inactive Status: for registered persons on active military duty"
    ),
    18: (
        "**Ch.18 Employee Conduct & Reportable Events**\n"
        "• Form U4: personal info, employment history, disclosure questions (criminal, regulatory, financial)\n"
        "• Form U5: termination notice; filed within 30 days; reason for departure disclosed\n"
        "• Form U6: filed by regulators/firms to report disciplinary actions\n"
        "• BrokerCheck: FINRA's public database; available 10 years post-termination for most events\n"
        "• Must notify FINRA for: criminal charges, regulatory actions, civil judgments, bankruptcy, liens >$2,500, complaints >$15,000\n"
        "• Outside Business Activities (OBA): must disclose and get approval from employing firm\n"
        "• Selling Away: selling securities not offered through your firm; requires prior written approval\n"
        "• Gifts: cannot give/receive >$100/year per person connected with securities business\n"
        "• Political contributions (Pay-to-Play Rule): max $250 to officials who influence muni securities business\n"
        "• Customer complaints: recorded + quarterly reports to FINRA; records kept 4 years at OSJ"
    ),
    19: (
        "**Ch.19 Economic Factors**\n"
        "• GDP: value of all goods/services within a country's borders\n"
        "• GNP: value produced by a country's residents, regardless of location\n"
        "• Inflation measured by CPI; Deflation = falling prices; Stagflation = inflation + recession\n"
        "• Real interest rate = nominal rate − inflation rate\n"
        "• Business cycle: Expansion → Peak → Contraction/Recession → Trough\n"
        "  – Recession = 2+ consecutive quarters of declining GDP\n"
        "• Economic indicators: Leading (predict future), Coincident (current), Lagging (confirm past)\n"
        "• Key rates: Prime (best customers), Discount (Fed to banks), Fed Funds (bank-to-bank overnight), Broker Call (banks to BDs)\n"
        "• FRB tools: Open market ops (buy Treasuries → ↑ money supply), Discount rate, Reserve requirements\n"
        "• Yield curves: Normal (upward), Inverted (recession signal), Flat (transition)\n"
        "• Balance sheet: assets = liabilities + equity; Income statement: revenues − expenses = net income\n"
        "• EBIT / EBITDA: measures of profitability; bond coverage ratio = EBIT ÷ interest expense"
    ),
    20: (
        "**Ch.20 Investment Risks**\n"
        "• Systematic risk (non-diversifiable): affects entire market\n"
        "  – Market risk (equities), Interest rate risk (bonds), Inflation risk, Event risk\n"
        "• Non-systematic risk (diversifiable): specific to company/industry; reduced through diversification\n"
        "  – Business risk, Regulatory/legislative risk, Capital risk, Liquidity risk\n"
        "  – Currency risk, Political risk, Credit risk, Prepayment risk (MBS)\n"
        "• Alpha: excess return vs benchmark (manager skill); Beta: sensitivity to market movements\n"
        "  – Beta >1: more volatile; Beta <1: less volatile; Beta =1: moves with market\n"
        "• Duration: measure of interest rate sensitivity; longer duration = greater price change per rate move\n"
        "• Efficient Market Hypothesis (EMH): prices reflect all available info; active mgmt can't consistently beat market\n"
        "• Strategic (passive) allocation: buy-and-hold, indexing, rebalancing\n"
        "• Tactical (active) allocation: sector rotation, short-term adjustments\n"
        "• Options as hedges: buy puts to protect long stock; buy calls to hedge short positions"
    ),
}

def get_todays_chapter():
    delta = (TODAY - TRACKING_START).days
    return (delta % TOTAL_CHAPTERS) + 1

QUOTES = [
    "The secret of getting ahead is getting started.",
    "不是因为有希望才坚持，而是坚持了才会有希望。",
    "Small daily improvements lead to staggering long-term results.",
    "你现在的努力，是在为未来的自己铺路。",
    "It does not matter how slowly you go as long as you do not stop.",
    "每天进步一点点，考试就近了一点点。",
    "Success is the sum of small efforts repeated day in and day out.",
    "坚持不是因为相信结果，而是因为相信自己。",
    "Don't watch the clock; do what it does. Keep going.",
    "今天的你，正在成为未来更好的自己。",
    "The pain you feel today will be the strength you feel tomorrow.",
    "坚持下去，不是因为路的尽头有什么，而是走着走着就成了习惯。",
    "Fall seven times, stand up eight.",
    "没有捷径，只有脚踏实地。",
    "A river cuts through rock not because of its power, but its persistence.",
    "种一棵树最好的时间是十年前，其次是现在。",
    "One step at a time is good walking.",
    "慢慢来，比较快。",
    "Perseverance is not a long race; it is many short races one after another.",
    "坚持是一种习惯，也是一种态度。",
    "The harder you work, the luckier you get.",
    "距离终点越近，越不能放慢脚步。",
    "Push yourself, because no one else is going to do it for you.",
    "考试只是一个节点，你的努力才是真正的收获。",
    "Believe you can and you're halfway there.",
    "冲刺阶段最考验意志，也最能看出差距。",
    "You didn't come this far to only come this far.",
    "最后的坚持，往往是成功的开始。",
    "Champions keep playing until they get it right.",
    "不要让昨天的懈怠，成为今天的借口。",
    "Pressure makes diamonds.",
    "压力就是动力，挑战就是机遇。",
    "The last mile is always the hardest.",
    "越到最后越要稳住，胜负就在这里。",
    "Sprint, not stumble — the finish line is close.",
    "临考前的每一天，都是你拉开差距的机会。",
    "It always seems impossible until it's done.",
    "还没到最后一刻，就不要轻言放弃。",
    "The night is darkest just before the dawn.",
    "黎明前最黑暗，坚持就是胜利。",
    "Doubt kills more dreams than failure ever will.",
    "你比你想象的更有能力。",
    "The only person you should try to be better than is who you were yesterday.",
    "成功不是偶然的，它是日积月累的结果。",
    "Wake up with determination. Go to bed with satisfaction.",
    "每一次打开书本，都是对自己的一次投资。",
    "Your future self will thank you for what you do today.",
    "现在吃的苦，都会变成你的实力。",
    "Excellence is not a destination but a continuous journey.",
    "做到了才有资格说做不到，还没做就别放弃。",
    "You are stronger than you think.",
    "你比昨天的自己更强了，这就够了。",
    "Motivation gets you started. Habit keeps you going.",
    "自律是最高级的自由。",
    "The difference between ordinary and extraordinary is that little extra.",
    "普通人和优秀的人之间，差的就是每天多做一点。",
    "Hard work beats talent when talent doesn't work hard.",
    "努力不一定成功，但放弃一定失败。",
    "Every expert was once a beginner.",
    "每个高手都曾是初学者，你也一样。",
    "Coffee in hand, notes open, let's go! ☕",
    "学习使我快乐，不学习使我更快乐，但考试使我清醒。",
    "Studying now so you can flex later. 💪",
    "考过了就可以跟朋友吹牛了，加油！",
    "Your brain has more capacity than your phone. Use it.",
    "今天学的东西，明天就是你的竞争优势。",
    "Be the person your future self is proud of.",
    "考试不可怕，可怕的是没准备好。",
    "Study hard, flex harder.",
    "刷题一时爽，过关才是真的爽——所以现在就好好学！",
    "My brain is 90% finance facts and 10% song lyrics. Priorities. 🎵",
    "学习虽苦，但通过考试的那一刻是甜的。",
    "SIE won't study itself. Unfortunately.",
    "证书不会自己长脚跑来，但努力会。",
    "Plot twist: you actually enjoy studying. 📖",
    "打卡一分钟，良心安一天。",
    "Brain cells activated. Let's go! 🧠",
    "今天不想学，那就学一点。",
    "Sleep is good. Study is better. Passing is best.",
    "睡得好不如学得好，学得好不如考得好。",
    "Invest in your knowledge — the returns are guaranteed.",
    "知识是唯一一种投资，回报率永远是正的。",
    "In the market of life, education is the best asset.",
    "学好SIE，就是给自己最好的职业投资。",
    "The best investment you can make is in yourself. — Warren Buffett",
    "你的证书，就是你最硬核的简历。",
    "Risk comes from not knowing what you're doing. — Warren Buffett",
    "考出来的不只是证书，是对自己的证明。",
    "Financial knowledge is the foundation of financial freedom.",
    "今天多学一章，未来多一份底气。",
    "In investing, what is comfortable is rarely profitable.",
    "走出舒适区，才能看到更大的市场。",
    "The stock market rewards patience, so does studying.",
    "备考就像建立投资组合：每天积累，长期复利。",
    "Know what you own, and know why you own it. — Peter Lynch",
    "搞清楚每一个知识点，就是最好的备考策略。",
    "Compound interest is the eighth wonder of the world. — Einstein",
    "学习也有复利效应：今天多学一章，明天事半功倍。",
    "The four most dangerous words: 'this time it's different.'",
    "考试没有捷径，只有扎实准备。",
]

# ── SUPABASE ─────────────────────────────────────────────
def sb_get(table, params=''):
    headers = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
    url = f'{SUPABASE_URL}/rest/v1/{table}'
    if params:
        url += f'?{params}'
    return requests.get(url, headers=headers).json()

# ── CALCULATIONS ─────────────────────────────────────────
def fmt_date(d):
    return f'{d.month}月{d.day}日'

def days_between(d1, d2):
    return (d2 - d1).days

def planned_chapters_today(username):
    u = USERS[username]
    total_days = days_between(u['studyStart'], u['examDate'])
    if total_days <= 0:
        return TOTAL_CHAPTERS
    elapsed = max(0, days_between(u['studyStart'], TODAY))
    return min(TOTAL_CHAPTERS, (elapsed / total_days) * TOTAL_CHAPTERS)

def get_status(gap):
    if gap is None or gap >= -0.3:
        return ('🟢', 'On Track')
    if gap >= -2:
        return ('🟡', 'At Risk')
    return ('🔴', 'Off Track')

def get_quote():
    idx = days_between(date(2026, 1, 1), TODAY)
    return QUOTES[idx % len(QUOTES)]

# ── FEISHU ───────────────────────────────────────────────
def build_card(title, color, content, btn_label, btn_url):
    return {
        'msg_type': 'interactive',
        'card': {
            'config': {'wide_screen_mode': True},
            'header': {'title': {'tag': 'plain_text', 'content': title}, 'template': color},
            'elements': [
                {'tag': 'div', 'text': {'tag': 'lark_md', 'content': content}},
                {'tag': 'action', 'actions': [{
                    'tag': 'button',
                    'text': {'tag': 'plain_text', 'content': btn_label},
                    'type': 'primary', 'url': btn_url
                }]}
            ]
        }
    }

def send_feishu(url, payload):
    import json as _json
    content = payload.get('card', {}).get('elements', [{}])[0].get('text', {}).get('content', '')
    print(f'  Message preview:\n{content}\n')
    if DRY_RUN:
        print('  [DRY RUN] Skipping Feishu send.')
        return True
    r = requests.post(url, json=payload)
    print(f'  Feishu response: {r.text}')
    return r.ok

# ── MAIN ─────────────────────────────────────────────────
def main():
    ntype = sys.argv[1] if len(sys.argv) > 1 else 'daily-reminder'
    print(f'Running: {ntype} | Today: {TODAY}')

    # Load data
    prog_data = sb_get('chapter_progress')
    ci_data   = sb_get('checkins')
    wh_data   = sb_get('webhook_config', 'id=eq.1')

    webhook_url = wh_data[0]['group_webhook'] if wh_data else ''
    if not webhook_url and not DRY_RUN:
        print('ERROR: No group webhook configured in Supabase webhook_config')
        sys.exit(1)

    # Build per-user data
    users_data = {}
    for username in USERS:
        prog = next((p for p in prog_data if p['username'] == username), None)
        completed = prog['completed_chapters'] if prog else list(range(1, USERS[username]['startChapter']+1))
        checkins = {c['date']: c for c in ci_data if c['username'] == username}
        users_data[username] = {'completed': completed, 'checkins': checkins}

    def stats(username):
        d = users_data[username]
        actual  = len(d['completed'])
        planned = planned_chapters_today(username)
        gap     = actual - planned
        left    = days_between(TODAY, USERS[username]['examDate'])
        today_ci = d['checkins'].get(str(TODAY))
        # Consecutive missed days
        missed, cursor = 0, TODAY
        while str(cursor) not in d['checkins'] and cursor >= TRACKING_START:
            missed += 1
            cursor -= timedelta(days=1)
            if missed > 30: break
        return {'actual':actual, 'gap':gap, 'left':left, 'today_ci':today_ci, 'missed':missed}

    if DRY_RUN:
        print('─── Stats ───')
        for u in USERS:
            s = stats(u)
            st_icon, st_label = get_status(s['gap'])
            print(f"  {USERS[u]['name']:20s} actual={s['actual']:2d} planned={planned_chapters_today(u):.1f} gap={s['gap']:+.1f} {st_icon}{st_label}  study_start={USERS[u]['studyStart']}")
        print('─────────────')

    quote    = get_quote()
    today_str = fmt_date(TODAY)
    medals   = ['🥇','🥈','🥉']

    # ── Daily reminder ──
    if ntype == 'daily-reminder':
        ranked = sorted(USERS.keys(), key=lambda u: stats(u)['gap'], reverse=True)
        lines = [f'"{quote}"', '', '<at id=all></at> 今日学习任务来了，冲！💪', '',
                 '━━━━━━━━━━━━━━━', '🏆 进度排行榜', '━━━━━━━━━━━━━━━']
        for i, u in enumerate(ranked):
            s = stats(u)
            st_icon, st_label = get_status(s['gap'])
            row_icon = medals[i] if st_label == 'On Track' and i < 3 else ('⚠️' if st_label == 'At Risk' else '❌')
            gap_str = f"领先{s['gap']:.1f}章" if s['gap'] >= 0 else f"落后{abs(s['gap']):.1f}章"
            lines.append(f"{row_icon} **{USERS[u]['name']}**  {s['actual']}/{TOTAL_CHAPTERS}章  {st_icon} {st_label} · {gap_str} · 剩{s['left']}天")
        lines += ['━━━━━━━━━━━━━━━', '今日目标：完成打卡 ✅']
        card = build_card(f'📚 SIE备考提醒 · {today_str}', 'blue', '\n'.join(lines), '📎 打开备考工具 →', SITE_URL)
        send_feishu(webhook_url, card)

    # ── Missed check-in ──
    elif ntype == 'missed-checkin':
        yesterday = str(TODAY - timedelta(days=1))
        missed = [u for u in USERS if yesterday not in users_data[u]['checkins']]
        if not missed:
            print('Everyone checked in yesterday ✓')
            return
        names = '、'.join(f'**{USERS[u]["name"]}**' for u in missed)
        content = f'<at id=all></at>\n\n昨天（{fmt_date(TODAY - timedelta(days=1))}）以下同学没有打卡记录：\n{names}\n\n今天记得补上学习进度！加油 💪'
        card = build_card('⚠️ 昨日未打卡提醒', 'yellow', content, '📎 去打卡 →', SITE_URL)
        send_feishu(webhook_url, card)

    # ── Weekly report ──
    elif ntype == 'weekly-report':
        ranked = sorted(USERS.keys(), key=lambda u: stats(u)['gap'], reverse=True)
        on_track  = [u for u in ranked if get_status(stats(u)['gap'])[1] == 'On Track']
        at_risk   = [u for u in ranked if get_status(stats(u)['gap'])[1] == 'At Risk']
        off_track = [u for u in ranked if get_status(stats(u)['gap'])[1] == 'Off Track']
        lines = [f'"{quote}"', '']
        def row(u, icon):
            s = stats(u)
            gap_str = f"领先{s['gap']:.1f}章" if s['gap'] >= 0 else f"落后{abs(s['gap']):.1f}章"
            return f"{icon} **{USERS[u]['name']}** · {s['actual']}/{TOTAL_CHAPTERS}章 · {gap_str} · 剩{s['left']}天"
        if on_track:
            lines.append('🟢 **On Track**')
            for i, u in enumerate(on_track): lines.append(row(u, medals[i] if i < 3 else '🟢'))
            lines.append('')
        if at_risk:
            lines.append('🟡 **At Risk**')
            for u in at_risk: lines.append(row(u, '⚠️'))
            lines.append('')
        if off_track:
            lines.append('🔴 **Off Track**')
            for u in off_track: lines.append(row(u, '❌'))
            lines.append('')
        if at_risk or off_track:
            lines.append('💡 落后的同学加油，考试不等人！')
        card = build_card(f'📊 SIE考牌项目 · 本周进度播报 · {today_str}', 'green', '\n'.join(lines), '📎 打开备考工具 →', SITE_URL)
        send_feishu(webhook_url, card)

    # ── Chapter study push ──
    elif ntype == 'chapter-study':
        ch = get_todays_chapter()
        note = OFFICIAL_NOTES.get(ch)
        note_section = f'\n\n**📋 本章精读**\n{note}' if note else '\n\n📋 本章精读内容即将更新，敬请期待。'
        content = (
            f'<at id=all></at>\n\n'
            f'📖 **今日学习重点 · 第 {ch} 章**\n'
            f'━━━━━━━━━━━━━━━'
            f'{note_section}\n\n'
            f'━━━━━━━━━━━━━━━\n'
            f'💡 学完记得打卡，知识库里也可以添加你的笔记！'
        )
        card = build_card(f'📖 今日学习重点 · 第 {ch} 章', 'blue', content, '📎 打开知识库 →', SITE_URL)
        send_feishu(webhook_url, card)

    # ── Behind alert ──
    elif ntype == 'behind-alert':
        behind = [(u, stats(u)) for u in USERS if stats(u)['missed'] >= 3]
        if not behind:
            print('No one is 3+ days behind ✓')
            return
        blocks = []
        for u, s in behind:
            gap_str = f"落后计划{abs(s['gap']):.1f}章" if s['gap'] < 0 else "进度正常"
            blocks.append(
                f"👋 **{USERS[u]['name']}**，你已经连续 **{s['missed']}天** 没有打卡了\n"
                f"📊 当前进度：{s['actual']}/{TOTAL_CHAPTERS}章，{gap_str}\n"
                f"⏰ 距考试还有 {s['left']} 天\n"
                f"现在开始还来得及，今天学一章就是进步！"
            )
        content = '<at id=all></at>\n\n' + '\n\n─────────────────\n\n'.join(blocks)
        card = build_card('⚠️ 备考进度催促', 'red', content, '📎 打开备考工具 →', SITE_URL)
        send_feishu(webhook_url, card)

if __name__ == '__main__':
    main()
