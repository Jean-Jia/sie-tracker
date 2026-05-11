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
        '【考试权重】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n所在考纲：Section 1 – Knowledge of Capital Markets\n本节总题量：12题（含第 1、2、11、19 章）\n本章预计题量：约 2–3 题\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n\n══════════════════════════════════════\n一、什么是发行人（What\'s an Issuer?）\n══════════════════════════════════════\n\n📄 原文：\n"An issuer is any legal entity that issues and sells securities to raise capital. Issuers can raise capital by issuing both debt securities (i.e., bonds) and equity securities (i.e., stocks)."\n\n"Examples of issuers include the U.S. Treasury, foreign governments, state and local governments, corporations, and banks."\n\n【考点解析】\n发行人（Issuer）= 发行证券来筹集资金的法律实体\n\n▸ 两类证券：\n  ① 债务证券（Debt Securities）→ 债券（Bonds）\n     • 发行人向投资者借钱，承诺还本付息\n     • 投资者是"债权人"，不拥有公司\n  ② 权益证券（Equity Securities）→ 股票（Stocks）\n     • 投资者成为公司股东，持有所有权\n     • 风险更高，但潜在回报更高\n\n▸ 五类常见发行人（SIE 高频考点）：\n  ① U.S. Treasury（美国财政部）→ 发行国债（T-Bills / Notes / Bonds）\n  ② 外国政府（Foreign Governments）→ 发行主权债券\n  ③ 州及地方政府（State / Local Governments）→ 发行市政债券（Municipal Bonds）\n  ④ 企业（Corporations）→ 发行公司债券和股票\n  ⑤ 银行（Banks）→ 发行银行债券及股票\n\n⚠️ 考试提示：\n  "Primary market"（一级市场）= 发行人直接向投资者出售新证券的场所\n  发行人在一级市场募集资金；在二级市场（Secondary Market）交易时，发行人不再收取资金\n\n\n══════════════════════════════════════\n二、什么是券商（What\'s a Broker-Dealer?）\n══════════════════════════════════════\n\n📄 原文：\n"A broker-dealer (BD) is a firm that is in the business of buying and selling securities. A broker-dealer can act as either a broker (agent) or a dealer (principal)."\n\n"When acting as a broker, the firm acts as an agent on behalf of a customer and charges a commission for the service."\n\n"When acting as a dealer, the firm acts as a principal, buying securities for its own inventory or selling securities from its own inventory. In a principal transaction, the firm earns a markup (when selling to a customer) or markdown (when buying from a customer)."\n\n【考点解析】\n券商（Broker-Dealer / BD）= 从事证券买卖业务的公司\n\n▸ 双重角色核心区分（高频考点！）：\n\n  ① Broker（经纪人）= Agent（代理人）\n     • 代客户买卖，不持有自己的仓位\n     • 赚取：佣金（Commission）\n\n  ② Dealer（自营商）= Principal（主体 / 本金方）\n     • 用自己的账户（inventory）买卖\n     • 赚取：Markup（卖给客户时加价）或 Markdown（从客户买入时压价）\n\n▸ 券商五大内部部门：\n\n  ① Investment Banking（投资银行部）— IPO、债券发行、并购顾问\n  ② Research（研究部）— 买入 / 卖出 / 持有评级；与 IB 部有"信息墙"隔离\n  ③ Sales（销售部）— 注册代表（RRs）直接服务客户\n  ④ Trading（交易部）— 自营交易 + 客户委托交易\n  ⑤ Operations（运营部 / 后台）— 确认书、账单、转账、记录保存\n\n⚠️ BD 在同一笔交易中只能以 Broker 或 Dealer 身份之一出现\n\n\n══════════════════════════════════════\n三、什么是做市商（What\'s a Market Maker?）\n══════════════════════════════════════\n\n📄 原文：\n"A market maker is a broker-dealer that is required to display, and to regularly make, firm bids and offers on a particular security. Market makers help ensure liquidity in the market."\n\n"A two-sided quote includes both a bid price (the price the market maker will buy) and an ask price (the price the market maker will sell), as well as the size of the quote."\n\n"Example: Bid 17.05 × Ask 17.08 / Size 1,000 × 2,000"\n\n【考点解析】\n做市商（Market Maker）= 必须持续为特定证券提供双向报价的自营商\n\n▸ 双向报价（Two-Sided Quote）：\n  • Bid Price = 做市商买入价（较低）\n  • Ask / Offer Price = 做市商卖出价（较高）\n  • Spread（价差）= Ask − Bid = 做市商利润来源\n\n▸ 报价示例：Bid 17.05 / Ask 17.08 / Size 1,000 × 2,000\n  • 做市商愿意以 $17.05 买入最多 1,000 股\n  • 做市商愿意以 $17.08 卖出最多 2,000 股\n\n▸ 做市商 vs. 交易员：\n  • Market Maker：必须持续报价（义务）\n  • Trader：只执行交易，无持续报价义务\n\n\n══════════════════════════════════════\n四、什么是交易员（What\'s a Trader?）\n══════════════════════════════════════\n\n📄 原文：\n"A trader is a person that is employed by a broker-dealer to execute securities transactions. A trader does not have an obligation to post bids and offers as a market maker does. A trader may trade on behalf of the firm in its proprietary account or on behalf of its clients."\n\n【考点解析】\n交易员（Trader）= 券商雇用的、执行买卖交易的专业人员\n\n▸ 两类职责：\n  ① 自营交易（Proprietary Trading）：动用公司自有资金\n  ② 客户委托交易（Client Trading）：代表客户执行订单\n\n⚠️ 交易员 ≠ 做市商，两者的"报价义务"不同是常考区分点\n\n\n══════════════════════════════════════\n五、什么是投资顾问（What\'s an Investment Adviser?）\n══════════════════════════════════════\n\n📄 原文：\n"An investment adviser (IA) is any person or firm that: (1) provides advice about securities; (2) is in the business of providing such advice; and (3) receives compensation for the advice."\n\n"Investment advisers typically charge fees, often calculated as a percentage of assets under management (AUM)."\n\n"Investment adviser registration requirements based on AUM:\n• Less than $100 million → register with the state\n• Between $100 million and $110 million → may register with either the state or SEC\n• Greater than $110 million → must register with the SEC"\n\n【考点解析】\n投资顾问（IA）= 提供证券建议并收取费用的个人或机构\n\n▸ IA 认定的三要素（同时满足）：\n  ① 提供证券建议  ② 以此为业  ③ 收取报酬\n\n▸ IA 注册门槛（三档必背）：\n  • AUM < $1 亿 → 向各州注册\n  • AUM $1 亿–$1.1 亿 → 可向州或 SEC 注册\n  • AUM > $1.1 亿 → 必须向 SEC 注册（RIA）\n\n▸ IA vs. BD：IA 收费（Fee / % of AUM）；BD 收佣金（Commission）或利差（Markup）\n\n\n══════════════════════════════════════\n六、市政顾问（Municipal Advisors）\n══════════════════════════════════════\n\n📄 原文：\n"A municipal advisor is a firm or individual that provides advice to municipal entities on the structure, timing, and terms of municipal finance offerings."\n\n"Municipal advisors must register with the SEC and are regulated by the MSRB."\n\n【考点解析】\n市政顾问 = 为市政实体提供融资结构、时机及条款建议的专业顾问\n• 注册：向 SEC 注册\n• 监管：MSRB（制定规则但无执法权）\n\n\n══════════════════════════════════════\n七、投资者类型（Types of Investors）\n══════════════════════════════════════\n\n📄 原文（合格投资者）：\n"An accredited investor is an individual or entity that meets one of the following criteria:\n• Individual net worth (or joint net worth with spouse) exceeds $1 million, excluding the value of the primary residence; OR\n• Individual income in each of the two most recent years exceeded $200,000 (or $300,000 with spouse)."\n\n"Certain professional certifications and designations also qualify, including holders of Series 7, Series 65, Series 82, and CFP."\n\n📄 原文（QIB）：\n"A Qualified Institutional Buyer (QIB) must meet a three-part test:\n1. The entity must be an eligible entity type.\n2. The entity must be buying for its own account or for the account of another QIB.\n3. The entity must own and invest, on a discretionary basis, at least $100 million of non-affiliated securities."\n\n"Individuals CANNOT be QIBs, regardless of their wealth."\n\n【考点解析】\n▸ 四类投资者层级：\n\n  ① Retail Investors（零售投资者）\n     • 普通个人，资产有限，受到最多监管保护\n\n  ② Accredited Investors（合格投资者）（高频考点！）\n     • 净资产 > $100 万（不含主要住宅）\n     • 或：个人年收入 > $20 万 / 夫妻联合 > $30 万（近两年）\n     • 或：持有 CFP、Series 7、Series 65、Series 82 等认证\n     • 或：金融机构、公司董事 / 高管 / 普通合伙人\n\n  ③ Institutional Investors（机构投资者）\n     • 银行、保险公司、养老基金、捐赠基金、对冲基金\n     • FINRA 定义：总资产 ≥ $5,000 万\n\n  ④ QIBs（合格机构买家）（高频考点！）\n     三条件同时满足：\n     ① 符合资格的实体类型\n     ② 为自己或其他 QIB 账户购买\n     ③ 自主管理 ≥ $1 亿 的非关联发行人证券\n     ⚠️ 个人无论多有钱都不能成为 QIB！\n\n\n══════════════════════════════════════\n八、市场结构（Market Structure）\n══════════════════════════════════════\n\n📄 原文（一级 vs. 二级市场）：\n"In the primary market, issuers sell new securities to investors for the first time. The issuer receives the proceeds from the sale."\n\n"In the secondary market, investors buy and sell previously issued securities among themselves. The issuer does NOT receive proceeds."\n\n"The primary market is regulated by the Securities Act of 1933. The secondary market is regulated by the Securities Exchange Act of 1934."\n\n📄 原文（OTC 市场）：\n"The OTC equity markets have four tiers:\n• OTCQX Best Market: the highest tier\n• OTCQB Venture Market: early-stage companies\n• OTC Pink Open Market: least regulated; highest risk\n• OTC Expert Market (OTCID): restricted to professional traders"\n\n【考点解析】\n▸ 一级市场（Primary）vs. 二级市场（Secondary）：\n  • 一级：发行人 → 投资者，发行人收资金，受 1933 年证券法监管\n  • 二级：投资者 ↔ 投资者，发行人不收资金，受 1934 年证券交易法监管\n\n▸ 交易所市场：NYSE（物理 + 电子混合）、Nasdaq（纯电子）\n  • 上市证券 = NMS Securities\n\n▸ OTC 市场四层（高到低）：OTCQX > OTCQB > Pink > Expert\n\n⚠️ Nasdaq 是交易所，不是 OTC！\n⚠️ 债券主要在 OTC 市场交易，不在交易所\n\n\n══════════════════════════════════════\n九、其他交易执行方式（Other Execution Methods）\n══════════════════════════════════════\n\n📄 原文：\n"The third market consists of exchange-listed securities that are traded OTC, away from the exchanges. Third market trading can occur after regular market hours."\n\n"The fourth market consists of direct institution-to-institution trading using proprietary trading systems (PTSs). No broker-dealer intermediary is used."\n\n"Electronic Communications Networks (ECNs) are automated systems that electronically match buy and sell orders. ECNs act as agents only, allow after-hours trading, and charge fees per transaction."\n\n"Dark pools are private trading platforms that do not display publicly available quotes. They are used for large block orders and provide anonymity."\n\n【考点解析】\n▸ 第三市场：交易所上市证券在场外（OTC）交易；可盘前盘后交易\n▸ 第四市场：机构直接互相交易，无中间商，用专有交易系统（PTSs）\n▸ ECN：自动撮合 + 仅代理（Agent Only）+ 允许盘后交易 + 收手续费\n▸ 暗池：不公开报价 + 大宗交易 + 机构 / HFT 参与 + 交易后才报告 + 匿名\n\n⚠️ ECN = Agent Only（不是主体）\n⚠️ 第三市场（有券商）vs. 第四市场（无中间商）\n\n\n══════════════════════════════════════\n十、清算与结算体系（Clearing and Settlement）\n══════════════════════════════════════\n\n📄 原文：\n"The DTCC is the central clearinghouse for U.S. financial markets, processing clearing and settlement of equities, bonds, MBS, money market instruments, and OTC derivatives. It is a non-profit, industry-owned organization regulated by the SEC."\n\n"DTCC subsidiaries:\n• NSCC: clears equity trades\n• FICC: clears bond and fixed income trades"\n\n"Clearing firms are full-service broker-dealers that execute, clear, and settle trades, interfacing directly with DTCC."\n\n"Introducing firms contract out clearing to clearing firms. Customer assets are held at the clearing firm."\n\n"Two clearing arrangements:\n• Fully disclosed: clearing firm knows each individual customer; sends statements/confirms directly\n• Omnibus: clearing firm sees only one account; introducing firm handles recordkeeping"\n\n【考点解析】\n▸ DTCC：非营利、行业自有、受 SEC 监管、美联储系统成员\n  • NSCC → 清算股票；FICC → 清算债券\n\n▸ 清算公司 vs. 介绍公司：\n  • 清算公司：全服务，直接对接 DTCC，持有客户资产\n  • 介绍公司：只执行交易，外包清算，客户资产在清算公司\n\n▸ Fully Disclosed vs. Omnibus：\n  • 完全披露：清算公司认识每个最终客户，直接发账单\n  • 综合账户：清算公司只看到一个总账户，不知道最终客户\n\n\n══════════════════════════════════════\n十一、主经纪商（Prime Brokerage）\n══════════════════════════════════════\n\n📄 原文：\n"Prime brokerage allows a hedge fund to trade through multiple executing brokers while centralizing clearing and settlement at one prime broker. The prime broker holds the hedge fund\'s assets and provides financing, risk reporting, and securities lending."\n\n【考点解析】\n主经纪商（Prime Broker）服务对冲基金：\n• 集中清算结算（多家执行经纪商 → 一家主经纪商）\n• 持有资产 + 融资借贷 + 风险报告 + 证券借贷（支持卖空）\n\n\n══════════════════════════════════════\n十二、期权清算（Clearing Options Contracts）\n══════════════════════════════════════\n\n📄 原文：\n"Unlike equity and bond trades cleared through DTCC, options are cleared through the Options Clearing Corporation (OCC)."\n\n"The OCC acts as the counterparty in all options transactions, guaranteeing performance of both buyer and seller."\n\n"Options exchanges: CBOE, BOX, NYSE Arca, Nasdaq PHLX, and ISE."\n\n"Options settle T+1."\n\n【考点解析】\n▸ OCC = 期权的中央清算所；充当所有期权交易的对手方\n\n▸ 期权交易所（5个）：CBOE、BOX、NYSE Arca、Nasdaq PHLX、ISE\n\n▸ 结算周期：T+1\n\n⚠️ 股票 / 债券 → DTCC；期权 → OCC（绝对不能混淆！）\n\n\n══════════════════════════════════════\n十三、其他市场实体（Other Entities）\n══════════════════════════════════════\n\n📄 原文：\n"Custodians hold customers\' securities for safekeeping and may collect income on their behalf."\n\n"A registrar maintains the ownership register to ensure the corporation does not issue more shares than authorized."\n\n"A transfer agent issues and cancels stock certificates, maintains the shareholder list, acts as paying agent for dividends and interest, acts as proxy agent, and handles lost certificates."\n\n"Securities trustees hold security interests for bondholders, enforce trust indenture covenants, and represent investors in default or bankruptcy."\n\n【考点解析】\n▸ 托管人（Custodian）：保管证券 + 代收股息 / 利息\n▸ 注册登记机构（Registrar）：维护股东登记册，防止超发\n▸ 过户代理（Transfer Agent）（多功能，常考）：\n  发行 / 注销证书 + 维护股东名单 + 支付股息 / 利息 + 代理投票 + 处理丢失证书\n▸ 证券受托人（Securities Trustee）：代表债券持有人，执行契约条款，违约时代表投资者\n\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n【本章核心考点速记】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n✦ Broker = Agent = 佣金；Dealer = Principal = Markup / Markdown\n✦ 做市商必须持续双向报价；交易员无此义务\n✦ 一级市场（1933 年）→ 发行人收资金；二级市场（1934 年）→ 发行人不收资金\n✦ Nasdaq = 交易所（不是 OTC！）；OTC 四层：OTCQX > OTCQB > Pink > Expert\n✦ Accredited Investor：$100 万净资产（不含主宅）或 $20 万 / $30 万年收入\n✦ QIB：$1 亿 + 机构实体；个人永远不能成为 QIB\n✦ DTCC 清算股票 / 债券；OCC 清算期权（绝对不混淆）\n✦ 过户代理 = 发行 / 注销证书 + 支付股息 + 代理投票\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
    ),
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
    8: None,
    9: None,
    10: None,
    11: None,
    12: None,
    13: None,
    14: None,
    15: None,
    16: None,
    17: None,
    18: None,
    19: None,
    20: None,
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
