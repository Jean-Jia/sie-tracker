#!/usr/bin/env python3
"""SIE Exam Tracker — Feishu Notification Script
Usage: python notify.py <type> <supabase_key>
Types: daily-reminder | missed-checkin | weekly-report | behind-alert | daily-notes
"""
import sys
import json
import requests
from datetime import date, timedelta

# ── CONFIG ──────────────────────────────────────────────
SUPABASE_URL   = 'https://cupdvksfzqpjedibajus.supabase.co'
SUPABASE_KEY   = sys.argv[2] if len(sys.argv) > 2 else ''
SITE_URL       = 'https://jean-jia.github.io/sie-tracker/'
TRACKING_START = date(2026, 5, 11)
TOTAL_CHAPTERS = 20
TODAY          = date.today()
DRY_RUN        = '--dry-run' in sys.argv
NOTES_WEBHOOK  = 'https://open.feishu.cn/open-apis/bot/v2/hook/bf8c9760-404e-4665-abe8-e680950dafbd'

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
    2: ('【考试权重】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n所在考纲：Section 1 – Knowledge of Capital Markets\n本节总题量：12题（含第 1、2、11、19 章）\n本章预计题量：约 2–3 题\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n══════════════════════════════════════\n一、监管体系四层级\n══════════════════════════════════════\n\n📄 原文：\n"The securities industry operates under a layered regulatory framework: federal regulation, state regulation, self-regulatory organizations (SROs), and firm-specific rules."\n\n【考点解析】\n美国证券监管分四层：\n1. 联邦监管（Federal）：SEC 主导，整体市场监督\n2. 州级监管（State）：各州 Blue-Sky Laws（蓝天法）\n3. 自律组织（SROs）：FINRA、MSRB、CBOE\n4. 公司内部规定：Written Supervisory Procedures（WSP）\n\n⚠️ 考试提示：SEC 负责民事执法；DOJ（司法部）处理刑事案件\n\n══════════════════════════════════════\n二、主要联邦监管机构\n══════════════════════════════════════\n\n📄 原文：\n"The SEC is an independent federal agency... The Federal Reserve Board (FRB) acts as the nation\'s central bank and is responsible for monetary policy... The FDIC insures bank deposits up to $250,000 per depositor per FDIC-insured bank."\n\n【考点解析】\n**SEC（证券交易委员会）**\n- 独立联邦机构，负责证券市场整体监管\n- Division of Enforcement 负责民事执法\n- 刑事案件由 DOJ 处理\n\n**FRB（联邦储备委员会）**\n- 美国中央银行，制定货币政策\n- 工具：贴现率（Discount Rate）、法定准备金率（Reserve Requirements）、Reg T（保证金）\n- 通过公开市场操作（Open Market Operations）影响联邦基金利率（Fed Funds Rate）\n- 注意：FRB 不直接"设定"联邦基金利率，而是"影响"\n\n**FDIC（联邦存款保险公司）**\n- 保险金额：每位储户每家银行最高 $250,000\n\n⚠️ 考试提示：Reg T 由 FRB 制定，管理保证金账户\n\n══════════════════════════════════════\n三、自律组织（SROs）\n══════════════════════════════════════\n\n📄 原文：\n"Self-regulatory organizations (SROs) are non-governmental organizations that have the power to create and enforce industry regulations and standards. The primary SRO for broker-dealers is FINRA."\n\n【考点解析】\n**FINRA（金融业监管局）**\n- 主要 SRO，监管经纪商和证券代表\n- 四项规则体系：\n  · Conduct Rules（行为规则）\n  · Uniform Practice Code（UPC，统一操作规范）\n  · Code of Procedure（纪律程序，FINRA 对会员）\n  · Code of Arbitration（仲裁规范，解决金钱纠纷，裁决不可上诉）\n\n**MSRB（市政证券规则制定委员会）**\n- 负责制定市政债券规则\n- 无执法权：BD 由 SEC/FINRA 执法，银行经销商由货币监理署/FRB/FDIC 执法\n\n**CBOE（芝加哥期权交易所）**\n- 最大的期权交易所，期权市场的 SRO\n\n**NASAA（北美证券管理协会）**\n- 协调各州 Blue-Sky Laws（统一证券法 USA）\n\n⚠️ 考试提示：MSRB 只制定规则不执法——是高频考点\n\n══════════════════════════════════════\n四、重要联邦证券立法（必考）\n══════════════════════════════════════\n\n📄 原文：\n"The Securities Act of 1933 requires full disclosure of all material information relating to a new securities offering... The Securities Exchange Act of 1934 created the SEC and governs secondary market transactions."\n\n【考点解析】\n\n**1933年证券法（Securities Act of 1933）**\n- 规范一级市场（Primary Market，新发行）\n- 核心要求：完整披露（Full and Fair Disclosure）\n- 要求发行招募说明书（Prospectus）\n\n**1934年证券交易法（Securities Exchange Act of 1934）**\n- 规范二级市场（Secondary Market）\n- 创建了 SEC\n- 制定了 Regulation T（保证金规定）\n- 反欺诈条款\n\n**1938年马洛尼法案（Maloney Act）**\n- 创建了 NASD（全国证券商协会）→ 2007年合并为 FINRA\n\n**1940年投资顾问法（Investment Advisers Act of 1940）**\n- ABC 测试：Advice（建议）、Business（业务）、Compensation（报酬）三者兼具则需注册\n- 豁免：律师、会计师、教师、工程师提供的附带性建议\n\n**1940年投资公司法（Investment Company Act of 1940）**\n- 规范 FACs、UITs、开放式/封闭式管理公司\n- 超过100名股东触发注册要求\n- 发行股份最低资产要求：$100,000\n- 要求提交半年报和年报\n\n**1970年SIPA / SIPC（证券投资者保护法/公司）**\n- 每个独立客户最高保障 $500,000，其中现金最高 $250,000\n- 由行业自筹资金，非政府保障\n- 覆盖：街名证券（Street-name securities）\n- 不覆盖：市场亏损、不当行为造成的损失\n- 现金账户+保证金账户合并计算；联名账户=独立客户\n- 不覆盖：大宗商品、其他BD账户、高管个人账户\n\n**1974年ERISA**\n- 规范私人合格退休计划（如401k）\n- 涵盖：归属条款、资金要求、资格要求、受托责任\n\n**1975年证券法修正案**\n- 正式创建了 MSRB\n\n**1988年内幕交易法（Insider Trading Act）**\n- 禁止使用重大非公开信息（Material Non-Public Information）\n- 知情者（Tippers）和受知者（Tippees）均承担责任\n- 刑事处罚：最高罚款 $5,000,000 / 最高监禁 20年\n- 民事处罚：SEC 可追诉三倍损害赔偿（Treble Damages = 3×）\n\n**1990年廉价股改革法案（Penny Stock Reform Act）**\n- 适用于场外股票 < $5/股\n- 要求买方签署风险披露声明\n\n**1991年TCPA**\n- 禁止打扰名单（Do Not Call）\n- 仅允许早8点至晚9点（当地时间）联系\n\n**2001年USA爱国者法案（USA PATRIOT Act）**\n- 反洗钱（AML）法规\n- CTR：现金交易 > $10,000 必须申报\n- SAR：可疑交易 ≥ $5,000 必须申报\n- CIP（客户身份识别程序）\n\n⚠️ 考试提示：1933法=一级市场+招募书；1934法=二级市场+创建SEC；SIPC保额必记\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n【本章核心考点速记】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n✦ SEC=民事执法；DOJ=刑事执法\n✦ FRB 通过公开市场操作影响（非直接设定）联邦基金利率\n✦ FDIC 保额=$250,000/储户/银行\n✦ MSRB=制定规则但无执法权\n✦ SIPC=$500K保障（$250K现金上限）；非政府资金；不保市场亏损\n✦ 1933法=一级市场+招募说明书；1934法=二级市场+创建SEC\n✦ 内幕交易：刑事 $5M罚款/20年监禁；民事=3倍赔偿\n✦ CTR>$10,000；SAR≥$5,000\n✦ ABC测试=判断是否需注册为投资顾问\n✦ ERISA=私人退休计划（401k等）的监管法律'),
    3: ('【考试权重】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n所在考纲：Section 2 – Understanding Products and Their Risks\n本节总题量：33题（含第 3、4、5、7、8、9、10、20 章）\n本章预计题量：约 4–6 题\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n══════════════════════════════════════\n一、公司与股权基础\n══════════════════════════════════════\n\n📄 原文：\n"A corporation is a separate legal entity... Shareholders of a corporation have limited liability, meaning that they can lose no more than the amount of their investment."\n\n【考点解析】\n- 公司是独立法人实体\n- 股东有有限责任（Limited Liability）：最多损失投资本金\n- 债券持有人 = 债权人：有权收取利息和本金，无投票权\n- 股东 = 所有者：有权获得股息、有投票权\n\n**破产清算顺序（Chapter 7，必背）：**\n1. 有担保债权人（Secured Creditors）\n2. 行政费用（Administrative Claims）：税款、工资、律师/会计师费\n3. 无担保债权人（Unsecured Creditors / Debenture holders）\n4. 次级债权人（Subordinated Creditors）\n5. 优先股股东（Preferred Stockholders）\n6. 普通股股东（Common Stockholders）\n\n⚠️ 考试提示：清算顺序是必考题，普通股股东排最后\n\n══════════════════════════════════════\n二、普通股（Common Stock）\n══════════════════════════════════════\n\n📄 原文：\n"Common stock represents the basic ownership unit of a corporation... The par value of common stock is an arbitrary amount that\'s used only for bookkeeping purposes."\n\n【考点解析】\n**股份状态术语（必考）：**\n- Authorized（授权股份）：公司章程允许发行的最大股份数\n- Issued（已发行）：已实际发行给投资者的股份\n- Treasury（库存股）：公司回购的自有股份；无投票权；不获股息\n- Outstanding（流通股）= Issued - Treasury：拥有投票权，获得股息\n\n**普通股股东权利：**\n1. 查阅财务记录权\n2. 投票权（选举董事会、股票分拆、合并/收购）\n3. 股息权（但董事会决定是否派息，股东不投票）\n4. 所有权证明\n5. 转让权\n\n⚠️ 考试提示：股东不对股息进行投票——这是董事会的权力（高频陷阱）\n\n══════════════════════════════════════\n三、投票方式\n══════════════════════════════════════\n\n📄 原文：\n"Statutory voting allows a shareholder to cast one vote per share for each issue to be decided... Cumulative voting allows shareholders to cast all of their votes for a single candidate."\n\n【考点解析】\n**法定投票（Statutory Voting）：**\n- 每股 × 每项议题 = 1票\n- 有利于大股东（多数派）\n\n**累积投票（Cumulative Voting）：**\n- 总票数 = 持股数 × 议题数\n- 可将所有票集中投给同一候选人\n- 有利于小股东（少数派）\n\n例题：持有1,000股，选举3名董事\n- 法定投票：每位候选人最多1,000票\n- 累积投票：共3,000票，可全部投给1人\n\n⚠️ 考试提示：累积投票保护少数股东是核心考点\n\n══════════════════════════════════════\n四、限制性证券与控制性证券（Rule 144）\n══════════════════════════════════════\n\n📄 原文：\n"Restricted securities are unregistered securities that are typically received from an issuer through a private placement... Control securities are registered securities that are held by affiliates of an issuing company."\n\n【考点解析】\n**限制性证券（Restricted Securities）：**\n- 未注册证券，通常来自私募发行\n- 报告公司：6个月持有期\n- 非报告公司：1年持有期\n\n**控制性证券（Control Securities）：**\n- 已注册，持有人为内部人士（高管、董事、>10%股东）\n- 无强制持有期，但受 Rule 144 成交量限制\n\n**Rule 144 规则（必考）：**\n- 出售时需提交 Form 144\n- 90天销售期内有效\n- 成交量限制 = 流通股的1% 或 过去4周平均周成交量，取较大值\n- 非附属人士（Non-affiliates）无成交量限制\n\n⚠️ 考试提示：Rule 144 同时适用限制性证券和控制性证券，但持有期起算点不同\n\n══════════════════════════════════════\n五、股票分类\n══════════════════════════════════════\n\n📄 原文：\n"Blue-chip stocks are shares of large, well-known companies with a long history of dividend payments... Cyclical stocks are stocks of companies whose earnings tend to fluctuate with the business cycle."\n\n【考点解析】\n蓝筹股（Blue-chip）：大型稳定公司，有股息历史（如道指成分股）\n成长股（Growth）：收益快速增长，低/无股息（如科技公司）\n防御股（Defensive）：抗经济衰退，需求稳定（公用事业、食品、制药）\n收益股（Income）：高股息支付（公用事业股）\n周期股（Cyclical）：收益随经济周期波动（汽车、钢铁、建筑）\n\n⚠️ 考试提示：公用事业股同时是防御股和收益股\n\n══════════════════════════════════════\n六、优先股（Preferred Stock）\n══════════════════════════════════════\n\n📄 原文：\n"Preferred stockholders have a senior claim on assets over common stockholders, but a junior claim compared to bondholders... Preferred stock typically pays a fixed dividend that\'s based on its par value ($100)."\n\n【考点解析】\n**优先股基本特征：**\n- 优先于普通股，次于债券持有人\n- 通常无投票权\n- 面值 $100（与普通股不同）\n- 固定股息率（基于面值计算）\n- 适合追求收入的投资者\n\n**优先股类型（必考）：**\n累积型（Cumulative）：欠发的股息（Dividends in Arrears）必须在支付普通股股息前全部补发\n非累积型（Non-cumulative）：未支付股息直接作废，无法追回\n参与型（Participating）：除固定股息外，可能获得额外股息\n可赎回型（Callable）：公司有权按指定价格赎回\n可转换型（Convertible）：可按固定比率转换为普通股\n\n**可转换优先股：**\n- 转换比率 = $100面值 ÷ 转换价格\n- 交易价格取赎回价值和转换价值中的较高者\n\n⚠️ 考试提示：累积型"积欠股息"是最常考知识点；优先股面值=$100（非$1,000）\n\n══════════════════════════════════════\n七、美国存托凭证（ADRs）\n══════════════════════════════════════\n\n📄 原文：\n"American Depositary Receipts (ADRs) allow investors to purchase the securities of foreign companies in U.S. markets... ADRs are priced and pay dividends in U.S. dollars."\n\n【考点解析】\n- 外国股票在美国市场交易的方式\n- 以美元计价和支付股息\n- Sponsored（有担保型）：在交易所上市，由发行公司支付费用\n- Unsponsored（无担保型）：在场外市场（OTC）交易，由银行发行\n- 享有股息权，无优先认购权（No Preemptive Rights）\n- 风险：市场风险 + 货币风险（汇率风险）\n\n⚠️ 考试提示：ADR 无优先认购权是易错点\n\n══════════════════════════════════════\n八、认购权（Rights）与认股权证（Warrants）\n══════════════════════════════════════\n\n📄 原文：\n"Rights are issued to existing common shareholders and allow them to purchase additional shares at a price that\'s below the current market price... Warrants are issued to purchasers of stocks or bonds and allow the holder to purchase shares at a price that\'s above the current market price."\n\n【考点解析】\n认购权（Rights）：\n- 发给现有普通股股东\n- 认购价格低于当前市场价\n- 有效期短：30–45天\n- 每股获得一份认购权，目的是维持持股比例\n\n认股权证（Warrants）：\n- 随股票/债券发行作为"甜头"（sweetener）\n- 认购价格高于当前市场价\n- 有效期长：数年\n- 可单独分离交易\n- 内在价值 = 市场价 - 认购价（正值时）\n\n对比总结：\n| 项目     | Rights       | Warrants     |\n|----------|--------------|--------------|\n| 认购价格  | 低于市价      | 高于市价      |\n| 有效期    | 短（30-45天） | 长（数年）    |\n| 发给谁    | 现有股东      | 新证券购买者  |\n\n⚠️ 考试提示：Rights 低于市价；Warrants 高于市价——必考对比\n\n════════════════════════════════════════\n九、发行人回购规则（SEC Rule 10b-18）\n════════════════════════════════════════\n\n📄 原文：\n"SEC Rule 10b-18 provides issuers with a \'safe harbor\' from manipulation charges when they repurchase their own common stock in the open market."\n\n【考点解析】\nRule 10b-18 回购安全港四项条件：\n1. 经纪商：每天只通过一家 BD 进行回购\n2. 时机：不在开盘前30分钟和收盘前30分钟（活跃股收盘前10分钟）\n3. 价格：不超过最高独立买价或最后独立成交价\n4. 成交量：不超过该股票 ADTV（日均成交量）的 25%\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n【本章核心考点速记】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n✦ 破产清算：有担保债权→行政费用→无担保债权→次级债→优先股→普通股\n✦ Outstanding = Issued - Treasury（库存股：无投票权、无股息）\n✦ 股息由董事会决定，股东不投票\n✦ 累积投票=少数股东保护；法定投票=多数股东占优\n✦ 优先股面值=$100；累积型积欠股息必须补发\n✦ Rights 认购价<市价（30-45天）；Warrants 认购价>市价（多年）\n✦ ADR=无优先认购权；有货币风险\n✦ Rule 144：报告公司6个月，非报告公司1年；成交量≤1%或4周均量（取大）'),
    4: ('【考试权重】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n所在考纲：Section 2 – Understanding Products and Their Risks\n本节总题量：33题（含第 3、4、5、7、8、9、10、20 章）\n本章预计题量：约 3–5 题\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n══════════════════════════════════════\n一、债券基本术语\n══════════════════════════════════════\n\n📄 原文：\n"A bond is a contract between an issuer and an investor... Debt service represents the total of all interest payments over the bond\'s life and the final repayment of the loan value (principal) at maturity. The issuer must stand ready to make these payments since it will be in default if any are missed."\n\n【考点解析】\n债务偿还（Debt Service）：债券存续期内所有利息支付总额 + 到期本金偿还\n杠杆融资（Leverage Financing）：发行方通过发债筹资（借助净资产）\n面值/本金（Par Value / Principal / Face Value）：到期时发行方支付的金额，通常 $1,000\n票面利率（Coupon Rate / Nominal Yield）：发行时确定的固定利率，基于 $1,000 面值计算\n到期日（Maturity Date）：债券到期，持有人收回本金的日期\n\n**利息计算示例：**\n6%企业债：年利息 = $1,000 × 6% = $60\n半年支付（标准）：每次 $30\n到期日6月1日 → 付息日为每年6月1日和12月1日\n\n⚠️ 考试提示：票面利率始终基于 $1,000 面值，与购买价格无关\n\n══════════════════════════════════════\n二、债券定价与折溢价\n══════════════════════════════════════\n\n📄 原文：\n"A bond that\'s sold for less than its par value is selling at a discount, while a bond that\'s sold for more than its par value is selling at a premium... A bond\'s price is usually stated as a percentage of its par value."\n\n【考点解析】\n价格表示法：以面值百分比表示（"100"= 100%面值 = $1,000）\n每个"点（point）"= 面值的1% = $10\n\n| 价格 | 百分比 | 美元   | 状态            |\n|------|--------|--------|-----------------|\n| 99   | 99%    | $990   | 折价（Discount） |\n| 100  | 100%   | $1,000 | 平价（Par）      |\n| 101  | 101%   | $1,010 | 溢价（Premium）  |\n\n**交易单位（必考）：**\n- 企业债/市政债：以 1/8 点为单位\n  87 1/8 = 87.125% = $871.25\n- 国债（T-notes/T-bonds）：以 1/32 点为单位\n  99.08 = 99又8/32 = 99.25% = $992.50\n\n⚠️ 考试提示：国债用32分之一，企业债用8分之一——必考计算\n\n══════════════════════════════════════\n三、利率与价格的反向关系（最核心考点）\n══════════════════════════════════════\n\n📄 原文：\n"As interest rates increase, the prices of existing bonds decrease and, as interest rates decrease, the prices of existing bonds increase."\n\n【考点解析】\n市场利率上升 → 旧债券吸引力下降 → 价格下跌（折价出售）\n市场利率下降 → 旧债券吸引力上升 → 价格上涨（溢价交易）\n\n利率风险（Interest-Rate Risk）：\n- 长期债券价格波动 > 短期债券（长期债利率风险更大）\n- 但短期利率的波动幅度 > 长期利率（短期利率更不稳定）\n- 不要混淆：长期债券更脆弱 vs 短期利率更多变\n\n信用风险（Credit Risk）：\n- 发行方可能违约，无法支付利息或本金\n- 高信用风险发行方必须提供更高收益率\n- 公司被评为更高风险 → 债券价格下跌\n\n⚠️ 考试提示："价格-利率反向关系"是SIE最核心考点，务必熟记\n\n══════════════════════════════════════\n四、信用评级体系\n══════════════════════════════════════\n\n📄 原文：\n"Credit rating companies include Moody\'s, Standard and Poor\'s (S&P), and Fitch Investors Service. Each company evaluates the possibility that an issuer may default and assigns the issue a credit rating."\n\n【考点解析】\n| 等级              | Moody\'s | S&P  | Fitch    |\n|------------------|---------|------|----------|\n| 最佳              | Aaa     | AAA  | AAA      |\n| 高质量            | Aa      | AA   | AA       |\n| 中上              | A       | A    | A        |\n| 中等（投资级下限） | Baa     | BBB  | BBB      |\n| 投机              | Ba      | BB   | BB       |\n|                  | B       | B    | B        |\n|                  | Caa     | CCC  | CCC      |\n| 违约              | C       | D    | DDD/DD/D |\n\n★ 投资级分界线：Moody\'s Baa / S&P BBB 及以上\n细分：Moody\'s加1/2/3（1最高）；S&P用+/-符号\n\n⚠️ 考试提示：Aaa/AAA是最高评级；投资级与投机级分界（Baa/BBB）是必考\n\n══════════════════════════════════════\n五、应计利息（Accrued Interest）\n══════════════════════════════════════\n\n📄 原文：\n"Accrued interest is the amount of interest that the seller is entitled to receive (from the buyer) and the amount that the buyer is required to pay (to the seller) for a bond being sold in the secondary market. For calculation purposes, corporate and municipal bonds use 30 days in every month and 360 days in the year, while U.S. government T-notes and T-bonds use actual days in every month and 365 days in the year."\n\n【考点解析】\n- 债券在两次付息日之间出售，卖方有权收取其持有期间的利息\n- 买方支付应计利息给卖方，下次付息日再收回全期利息\n\n计息惯例（必考）：\n- 企业债和市政债：每月30天，每年360天（30/360）\n- 美国国债（T-notes/T-bonds）：实际天数/365天（Actual/365）\n\n⚠️ 考试提示：30/360用于公司债和市政债；实际天数用于国债\n\n══════════════════════════════════════\n六、零息债券（Zero-Coupon Bonds）\n══════════════════════════════════════\n\n📄 原文：\n"Zero-coupon bonds don\'t pay periodic interest. Instead, an investor purchases a zero-coupon at a deep discount from its par value, but redeems the bond for its full face value at maturity. The difference between the purchase price and the amount that the investor receives at maturity is considered the bond\'s interest."\n\n【考点解析】\n- 不定期支付利息\n- 以大幅折价购买，到期按面值偿还\n- 折扣额 = 投资者的利息收入\n- 到期越长，折扣越大\n- 适合需要未来特定时间一笔钱的投资者（如子女教育基金）\n\n⚠️ 考试提示：零息债券税务上每年仍需按"应计利息"纳税（幻影收入 Phantom Income）\n\n══════════════════════════════════════\n七、债券期限结构\n══════════════════════════════════════\n\n📄 原文：\n"If all of the bonds in an offering are due to mature on the same date, it\'s referred to as a term bond issue. On the other hand, if parts of an offering will mature sequentially over several years, it\'s referred to as a serial bond issue."\n\n【考点解析】\n到期债（Term Bond）：整批债券同日到期\n分期债（Serial Bond）：债券分批按年度到期，可实现等额还款（Level Debt Service）\n气球到期（Balloon Maturity）：部分债券分期到期，大部分在最后到期\n\n⚠️ 考试提示：市政债通常采用分期债结构\n\n══════════════════════════════════════\n八、提前赎回条款（Call 与 Put）\n══════════════════════════════════════\n\n📄 原文：\n"A bond offering may include a call provision which allows the issuer to redeem its outstanding bonds before they reach maturity... Put provisions give the bondholder the right to redeem the bond on a specified date (or dates) prior to maturity."\n\n【考点解析】\n赎回条款（Call Provision）：\n- 赋予发行方在到期前赎回债券的权利\n- 主要目的：利率下降时以低成本重新融资\n- 可赎回债券通常提供更高票面利率作为补偿\n\n赎回保护期（Call Protection）：\n- 通常为发行后5–10年内禁止赎回\n- 赎回溢价（Call Premium）：赎回时支付高于面值的金额\n- 例：callable at 102 = 支付$1,020\n\n赎回类型：\n- 全额赎回（In-whole）：整批债券同时赎回\n- 部分赎回（Partial / Lottery Call）：部分债券随机赎回\n- 灾难赎回（Catastrophe Call）：抵押品被损毁时触发，豁免提前披露要求\n\n回售条款（Put Provision）：\n- 赋予债券持有人在指定日期以面值回售的权利\n- 保护投资者免受利率上升的损失\n- 通常导致收益率较低、价格较高\n\n⚠️ 考试提示：Call=发行方权利（低利率时行权）；Put=持有人权利（高利率时行权）\n\n══════════════════════════════════════\n九、可转换债券（Convertible Bonds）\n══════════════════════════════════════\n\n📄 原文：\n"A convertible bond gives an investor the ability to convert the par value of his bond into a predetermined number of shares of the company\'s common stock... The price at which the bond can be converted is referred to as the conversion price and is set at the time that the bond is issued."\n\n【考点解析】\n核心公式：\n转换比率（Conversion Ratio）= 债券面值（$1,000）÷ 转换价格\n\n例题：转换价格 = $40\n转换比率 = $1,000 ÷ $40 = 25股/债券\n\n转换价值（Conversion Value）= 转换比率 × 当前股价\n\n判断是否转换：比较"卖出债券"和"转换后卖出股票"哪个获益更多\n\n强制转换（Forced Conversion）：\n当赎回价格 < 转换价值，持有人被迫选择：\n立即转换（更划算）或接受较低赎回金额\n\n税务处理（重要）：\n- 转换行为本身不是应税事件（NOT a taxable event）\n- 转换后股票的成本基准 = 原债券的成本基准\n- 出售股票时才产生税务事件\n\n优缺点：\n- 发行方：以较低票面利率借款\n- 投资者：接受较低利率，可分享股价上涨；有债券保底价值\n- 风险：大批转换后流通股增加（稀释效应）\n\n⚠️ 考试提示：转换公式和强制转换计算是高频考点；转换不触发税务是陷阱题\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n【本章核心考点速记】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n✦ 价格与利率反向变动（利率↑→价格↓）\n✦ 长期债券利率风险>短期债券；短期利率波动幅度>长期利率\n✦ 企业债/市政债=30/360计息；国债=实际天数/365\n✦ 企业债/市政债以1/8点交易；国债以1/32点交易\n✦ Aaa/AAA=最高评级；投资级≥Baa/BBB；低于此为垃圾债\n✦ Call=发行方权利（低利率时行权）；Put=持有人权利（高利率时行权）\n✦ 转换比率=$1,000÷转换价格\n✦ 债券转换为股票：不触发税务；成本基准继承\n✦ 零息债券：折价购买，到期收面值；有幻影收入税（年度纳税）'),
    5: ('【考试权重】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n所在考纲：Section 2 – Understanding Products and Their Risks\n本节总题量：33题（含第 3、4、5、7、8、9、10、20 章）\n本章预计题量：约 5–8 题\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n══════════════════════════════════════\n一、美国国债（Treasury Securities）概览\n══════════════════════════════════════\n\n📄 原文：\n"Treasury securities are considered the safest type of fixed-income investment and are suitable for the most conservative investors. Since the securities are backed by the full faith and credit of the U.S. government, they have virtually no credit risk. This \'no default\' status is the benchmark against which the credit ratings of all other issuers are measured."\n\n【考点解析】\n- 信用风险最低（几乎为零），是所有其他发行方信用评级的基准\n- 免于1933年证券法注册要求（豁免证券）\n- 利息：联邦应税，免州/地方税\n\n| 类型                | 期限              | 特点                                    |\n|---------------------|-------------------|-----------------------------------------|\n| T-Bills（国库券）   | ≤1年（4/13/26/52周）| 零息折价；收益率报价；最小面值$100     |\n| T-Notes（中期国债） | 2–10年            | 半年付息；电子化；最小面值$100          |\n| T-Bonds（长期国债） | >10年             | 半年付息；电子化；最小面值$100          |\n| TIPS                | 5、10、30年       | 本金按CPI调整；利率固定                 |\n| STRIPS              | 零息              | 剥离国债利息/本金创建；收益率报价       |\n| CMBs（现金管理票据）| 极短期（可至1天） | 非定期发行；现金流管理                  |\n\n⚠️ 考试提示：T-Bills是唯一以收益率报价的国债；国债利息免州/地方税\n\n══════════════════════════════════════\n二、TIPS（通胀保护国债）\n══════════════════════════════════════\n\n📄 原文：\n"The rate of interest on TIPS is fixed; however, the principal amount on which that interest is paid may vary based on the change in the Consumer Price Index (CPI). During a period of inflation (a rise in CPI), the principal value will increase. However, if deflation occurs (from a decline in CPI), the principal value of the instrument will decrease (but not below $1,000)."\n\n【考点解析】\n- 利率固定，但计息基准（本金）随CPI变动\n- 通胀期（CPI上升）：本金增加 → 利息增加\n- 通缩期（CPI下降）：本金减少，但不低于原始面值$1,000\n- 利息：联邦应税，免州/地方税\n\n例题：\n4% TIPS，本金因通胀调整为$1,030\n年利息 = $1,030 × 4% = $41.20\n半年利息 = $41.20 ÷ 2 = $20.60\n\n⚠️ 考试提示：TIPS通缩保护下限为原始面值$1,000\n\n══════════════════════════════════════\n三、STRIPS 与 T-Bills 报价\n══════════════════════════════════════\n\n📄 原文：\n"The Treasury created its Separate Trading of Registered Interest and Principal Securities (STRIPS) program. Dealers are able to purchase T-notes and T-bonds and separately resell the coupon and principal payments as zero-coupons... STRIPS are backed by the full faith and credit of the U.S. Treasury and are quoted on a yield basis."\n\n【考点解析】\nSTRIPS：\n- 将国债的利息和本金"剥离"后分别作为零息债券出售\n- 以收益率报价（非面值百分比）\n- 有美国财政部的完全信用背书\n\n区分易混概念：\n- Treasury Receipts (TRs)：由经纪商发行，仅由国债作担保（非财政部直接背书）\n- Treasury STRIPS：财政部官方计划，有完全直接背书\n\nT-Bills报价特殊性：\n- 以折现收益率（Discount Yield）报价，非面值百分比\n- Bid收益率 > Asked收益率（因价格与收益率反向）\n- 债券等价收益率（Bond Equivalent Yield）始终 > 折现收益率\n\n⚠️ 考试提示：STRIPS有财政部背书；Treasury Receipts没有\n\n══════════════════════════════════════\n四、国债拍卖（Treasury Auctions）\n══════════════════════════════════════\n\n📄 原文：\n"When Treasury auctions are held, securities firms compete by submitting bids to buy Treasuries through an automated system... Non-competitive bids are filled first; however, the bidders must agree to accept the yield and price as determined by the auction. All winners of the auction will ultimately pay the lowest price of the accepted competitive tenders. This single price auction process is referred to as a Dutch auction."\n\n【考点解析】\n竞争性投标（Competitive Tender）：\n- 由证券公司参与，指定价格/收益率\n- 类似限价买入订单，可能不成交\n- 填单顺序靠后\n\n非竞争性投标（Non-Competitive Tender）：\n- 个人投资者参与，不指定价格\n- 类似市价买入订单，保证成交\n- 优先成交，但接受拍卖决定的价格\n\n荷兰式拍卖（Dutch Auction）：\n- 所有获胜者以最低接受价格（最低竞争中标价）统一成交\n- Single Price Auction（统一价格拍卖）\n\n拍卖时间表：\n| 品种              | 拍卖频率          | 发行时间              |\n|------------------|-------------------|-----------------------|\n| 4周国库券         | 每周              | 周二拍卖，周四发行    |\n| 13/26周国库券     | 每周              | 周一拍卖，周四发行    |\n| 52周国库券        | 每4周             | 周二拍卖，周四发行    |\n| 2/3/5年期国债     | 每月              | 月底发行              |\n| 10年期国债        | 每季度（2/5/8/11月）| 15日发行            |\n| 30年期国债        | 每季度（2/5/8/11月）| 15日发行            |\n\n⚠️ 考试提示：非竞争性投标先成交；荷兰式拍卖=统一价格\n\n══════════════════════════════════════\n五、机构证券（Agency Securities）\n══════════════════════════════════════\n\n📄 原文：\n"Agency securities include debt instruments that are issued and/or guaranteed by federal agencies and by government-sponsored enterprises (GSEs)... their yields are slightly higher than the yields of corresponding U.S. Treasury securities."\n\n【考点解析】\n联邦机构（Federal Agencies）——有政府完全信用背书：\n- GNMA（吉利美）：属于HUD；有美国政府完全信用背书；利息全部应税（联邦+州+地方）\n\n政府支持企业（GSEs）——私人拥有，国会授权，无直接政府背书：\n- FNMA（房利美）：购买FHA/VA/传统抵押贷款；利息全部应税\n- FHLMC（房地美）：为储蓄机构融资；利息全部应税\n- FFCB（联邦农业信贷银行）：农业贷款；利息联邦应税，免州/地方税\n- FHLB（联邦住房贷款银行）：为储蓄机构提供流动性；利息联邦应税，免州/地方税\n\n税务速查：\n| 机构   | 联邦税 | 州/地方税 |\n|--------|--------|-----------|\n| GNMA   | 应税   | 应税      |\n| FNMA   | 应税   | 应税      |\n| FHLMC  | 应税   | 应税      |\n| FFCB   | 应税   | 免税      |\n| FHLB   | 应税   | 免税      |\n\n⚠️ 考试提示：GNMA是唯一有政府完全背书的抵押机构；GNMA/FNMA/FHLMC利息全部应税\n\n══════════════════════════════════════\n六、抵押贷款支持证券（MBS）与预付款风险\n══════════════════════════════════════\n\n📄 原文：\n"The most common security issued by government agencies is a mortgage-backed pass-through certificate... In addition to the risks that are inherent in many fixed-income investments (e.g., interest-rate, credit, and liquidity risk), mortgage-backed securities are subject to a special type of risk which is referred to as prepayment risk. This is the risk that\'s tied to homeowners paying off their mortgages early."\n\n【考点解析】\n传递证书（Pass-Through Certificate）：\n- 发行方将一批抵押贷款打包成资产池\n- 向投资者出售对该资产池的不可分割权益\n- 月度付款（利息+本金混合）传递给投资者\n\nGNMA 修正传递证书特点：\n- 由FHA/VA抵押贷款支持\n- GNMA 保证每月按时支付（即使房主未还款）\n- 名义期限25–30年，实际平均寿命更短\n\n预付款风险（Prepayment Risk）——MBS特有：\n- 利率下降时，房主倾向于重新融资提前还款\n- 投资者面临本金提前返还，但再投资收益率更低\n- 这是MBS与普通债券的核心区别\n\n资产支持证券（ABS）：\n- 将信用卡应收款、汽车贷款、学生贷款等打包证券化\n- 优点：较高收益率、高信用质量、现金流可预测\n- 风险：利率风险、信用风险、预付款风险\n\n⚠️ 考试提示：预付款风险是MBS独特风险；利率降→提前还款→再投资收益降\n\n══════════════════════════════════════\n七、市政债券（Municipal Bonds）\n══════════════════════════════════════\n\n📄 原文：\n"Municipal bonds are issued by states, territories and possessions of the United States, as well as other political subdivisions... For most investors, the primary advantage of municipal bonds is that the interest received is typically exempt from federal tax."\n\n【考点解析】\n市政债基本特征：\n- 发行方：州、地方政府、公共机构（如市政局）\n- 有一定违约风险（非联邦政府背书）\n- 利息：通常免联邦税\n- 本州债券利息通常还免州/地方税（三重免税效果）\n\n两大类型对比：\n| 项目       | GO债（一般责任债）              | Revenue债（收益债）            |\n|-----------|-------------------------------|-------------------------------|\n| 还款来源   | 税收（不动产税/所得税等）       | 项目收入（过路费、使用费等）    |\n| 需要选民批准| 是                            | 否                             |\n| 可行性研究  | 否                            | 是                             |\n| 债务上限   | 受约束                        | 不受约束                       |\n| 风险       | 相对较低                      | 相对较高（依赖项目收入）        |\n\n各类收益债券：\n- 住房收益债（Housing Revenue）：租金/抵押贷款还款\n- 宿舍债（Dormitory）：学生学费\n- 医疗卫生债（Health Care）：非营利医院收入\n- 公用事业债（Utility Revenue）：用户费用\n- 交通债（Transportation）：通行费\n- 特殊税收债（Special Tax）：特定税收（非地产税）\n- 特别评估债（Special Assessment）：受益者专项收费\n- 道义责任债（Moral Obligation）：项目收入+州道义背书（非法律义务）\n- 工业发展债（IDB）：企业租赁付款；信用评级基于企业（非市政）\n- 双重担保债（Double-Barreled Bond）：同时有收入和税收来源\n\n⚠️ 考试提示：GO债=选民批准+税收；Revenue债=可行性研究+项目收入——高频对比考点\n\n══════════════════════════════════════\n八、市政票据（Municipal Notes）\n══════════════════════════════════════\n\n📄 原文：\n"Municipal notes are short-term issues that are normally issued to assist in financing a project or to assist a municipality in managing its cash flow."\n\n【考点解析】\n| 缩写  | 全称                              | 用途                     |\n|-------|-----------------------------------|--------------------------|\n| TAN   | Tax Anticipation Note             | 预期未来税收，用于当前运营 |\n| RAN   | Revenue Anticipation Note         | 预期未来收入（联邦/州补贴）|\n| TRAN  | Tax & Revenue Anticipation Note   | TAN+RAN合并              |\n| BAN   | Bond Anticipation Note            | 为最终发行长期债券过渡融资 |\n| GAN   | Grant Anticipation Note           | 预期联邦补助金            |\n| CLN   | Construction Loan Note            | 为建设项目提供临时资金    |\n\n市政票据评级：\n- Moody\'s：MIG 1（最高）→ MIG 2 → MIG 3 → SG（投机）\n- VRDOs 使用 VMIG 体系\n- S&P：SP-1+ → SP-1 → SP-2 → SP-3\n\n⚠️ 考试提示：BAN是为最终长期债券发行前的过渡融资，常考\n\n══════════════════════════════════════\n九、市政债发行流程\n══════════════════════════════════════\n\n📄 原文：\n"Like U.S. government and government agency securities, municipal securities are exempt from the registration and prospectus requirements of the Securities Act of 1933... The underwriter acts as a vital link between the issuer and the investing public by assisting the issuer in pricing the securities, structuring the financing, and preparing a disclosure document (referred to as the official statement)."\n\n【考点解析】\n市政债免于1933年证券法注册（豁免证券）\n披露文件：Official Statement（官方声明，非招募书）\n\nGO债发行要求：\n1. 选民批准\n2. 不超过债务上限\n\nRevenue债发行要求：\n1. 可行性研究（聘请咨询工程师评估项目可行性）\n2. 无需选民批准\n\n承销方式：\n| 证券类型                | 主要承销方式                    |\n|------------------------|--------------------------------|\n| 美国国债                | 拍卖（Auction）                |\n| 市政一般责任债（GO）    | 竞争性销售（Competitive Sale） |\n| 市政收益债              | 协商销售（Negotiated Sale）    |\n| 企业债                  | 协商销售（Negotiated Sale）    |\n\n竞争性销售：邀请多家承销商竞标，最低利率成本者获选\n协商销售：发行方直接指定承销商，协商条款\n\n⚠️ 考试提示：GO债=竞争性销售；Revenue债/企业债=协商销售\n\n══════════════════════════════════════\n十、企业债券（Corporate Bonds）\n══════════════════════════════════════\n\n📄 原文：\n"Corporate bonds are divided into two major categories—secured and unsecured. Although all debt that\'s issued by a corporation is backed by the issuer\'s full faith and credit, secured bonds are additionally backed by specific corporate assets."\n\n【考点解析】\n有担保债券（Secured Bonds）：\n- 抵押债（Mortgage Bond）：不动产（第一或第二抵押权）\n- 设备信托证书（Equipment Trust Certificate）：特定设备（铁路车厢、飞机等）\n- 担保信托债（Collateral Trust Bond）：第三方有价证券（股票/债券）放入托管\n\n无担保债券（Unsecured Bonds / Debentures）：\n- 仅凭公司完全信用担保\n- 违约时与普通债权人同等索偿权\n\n次级无担保债（Subordinated Debentures）：\n- 清算时索偿权低于普通无担保债权人\n- 但仍优先于股东\n\n完整清算顺序（6步，必背）：\n1. 有担保债权人（包括有担保债券）\n2. 行政费用（税款、工资、律师/会计师）\n3. 普通债权人（包括无担保债券/Debentures）\n4. 次级债权人（Subordinated Debentures）\n5. 优先股股东\n6. 普通股股东\n\n高收益债/垃圾债（High-Yield / Junk Bonds）：\n- S&P评级低于BBB / Moody\'s低于Baa\n- 更高违约风险 → 更高票面利率补偿\n\n其他类型：\n- 收益债（Income Bonds）：只有盈利才支付利息；平价交易（无应计利息）；高度投机\n- 担保债（Guaranteed Bond）：母公司为子公司债券提供担保\n\n⚠️ 考试提示：Debenture=无担保；Subordinated Debenture=次级无担保；清算顺序必须背熟\n\n══════════════════════════════════════\n十一、国际债券（Eurodollar / Yankee / Eurobonds）\n══════════════════════════════════════\n\n📄 原文：\n"Eurodollar bonds pay their principal and interest in U.S. dollars, but are issued outside of the United States (primarily in Europe)... Yankee bonds allow foreign entities to borrow money in the U.S. marketplace. These bonds are registered with the SEC and sold primarily in the United States."\n\n【考点解析】\n| 类型               | 发行地            | 计价货币   | 监管    |\n|--------------------|-------------------|------------|---------|\n| 欧洲美元债         | 美国境外（欧洲）  | 美元       | 非SEC   |\n| 扬基债（Yankee）   | 美国境内          | 美元       | SEC注册 |\n| 欧洲债（Eurobond） | 某国境内          | 另一国货币 | 多样化  |\n\n例：俄罗斯企业在伦敦发行瑞士法郎计价债券 = Eurobond（外付债）\n\n⚠️ 考试提示：Yankee Bond=外国实体在美国发行的美元债，需SEC注册\n\n══════════════════════════════════════\n十二、货币市场工具（Money Market Securities）\n══════════════════════════════════════\n\n📄 原文：\n"Short-term debt instruments with one year or less to maturity are referred to as money-market securities... Commercial paper is short-term, unsecured corporate debt which typically matures in 270 days or less. Due to its short maturity, commercial paper is exempt from the registration and prospectus requirements of the Securities Act of 1933."\n\n【考点解析】\n| 工具                        | 发行方 | 特点                                         |\n|----------------------------|--------|----------------------------------------------|\n| 商业票据（Commercial Paper）| 公司   | 期限≤270天；无担保；最小$100,000；折价；免注册 |\n| 银行承兑汇票（BA）          | 银行   | 促进国际贸易；货物+银行双重担保               |\n| 可转让存单（Negotiable CD） | 银行   | 最低$100,000；有二级市场；$250K以下FDIC保障   |\n| 联邦基金（Fed Funds）       | 银行间 | 隔夜拆借；每日波动；FRB间接影响               |\n| 回购协议（Repo）            | 经纪商 | 抵押证券借贷；通常隔夜                        |\n| 逆回购（Reverse Repo）      | 经纪商 | 买入证券同时约定回售                          |\n\n商业票据信用评级：\n- S&P：A1（最高）→ A2 → A3\n- Fitch：F1+（最高）→ F1 → F2 → F3\n- Moody\'s：P-1（最高）→ P-2 → P-3；投机级=NP（Not Prime）\n\n利率关系：\n- 联邦基金利率影响其他短期利率（FRB不直接设定）\n- 优惠利率（Prime Rate）=银行对最佳客户的贷款利率\n- SOFR（担保隔夜融资利率）=LIBOR的替代基准利率\n\n⚠️ 考试提示：商业票据≤270天免注册；最小面值$100,000；联邦基金利率非FRB直接设定；LIBOR已被SOFR替代\n\n══════════════════════════════════════\n十三、债券利息税务总结（必考速查表）\n══════════════════════════════════════\n\n📄 原文：\n"The interest received on T-notes and T-bonds is taxed at the federal level, but exempt from state and local taxation... Any interest earned on [GNMA securities] is subject to federal, state, and local taxes."\n\n【考点解析】\n| 证券类型                              | 联邦税 | 州/地方税  |\n|--------------------------------------|--------|-----------|\n| T-Bill / T-Note / T-Bond             | 应税   | 免税      |\n| TIPS / STRIPS                        | 应税   | 免税      |\n| GNMA（吉利美）                       | 应税   | 应税      |\n| FNMA（房利美）                       | 应税   | 应税      |\n| FHLMC（房地美）                      | 应税   | 应税      |\n| FFCB / FHLB                          | 应税   | 免税      |\n| 市政债（Municipal Bonds）            | 免税   | 视情况*   |\n| 领土/属地债券（Territory/Possession） | 免税   | 免税      |\n| 企业债（Corporate Bonds）            | 应税   | 应税      |\n\n*市政债：大多数州对本州居民购买本州债券免州/地方税\n"三免"规则：市政债 + 投资者为该州居民 = 联邦、州、地方税全免\n\n⚠️ 考试提示：税务表是必须熟背的速查表；GNMA全部应税；国债免州税；市政债免联邦税\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n【本章核心考点速记】\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n✦ 国债：联邦应税，免州/地方税；T-Bills折价发行+收益率报价\n✦ TIPS：本金随CPI调整，利率固定；通缩下限=$1,000\n✦ 非竞争性投标先成交；Dutch Auction=统一价格\n✦ GNMA=政府完全背书；FNMA/FHLMC=GSE（无直接背书）\n✦ GNMA/FNMA/FHLMC利息全部应税；FFCB/FHLB免州税\n✦ GO债=选民批准+税收担保；Revenue债=可行性研究+项目收入\n✦ MBS预付款风险：利率降→提前还款→再投资收益降\n✦ Mortgage Bond=不动产；Equipment Trust=设备；Collateral=有价证券\n✦ Debenture=无担保；Subordinated Debenture=次级无担保\n✦ 商业票据≤270天免注册；最小面值$100,000\n✦ 市政债利息联邦免税；本州居民购买本州债=三重免税\n✦ SOFR已替代LIBOR作为基准利率'),
    6: ("""【考试权重】★★★☆☆
所在考纲：Section 2 – Understanding Products and Their Risks
本章预计题量：约 3–5 题

══════════════════════════════════════
一、普通股（Common Stock）
══════════════════════════════════════

📄 原文：
"Outstanding shares = Issued shares − Treasury shares"

【考点解析】
▸ 股份四种状态（必背）：
  • Authorized（授权股）：公司章程允许的最大发行量
  • Issued（已发行）：已实际发行给投资者的股份
  • Treasury（库存股）：公司回购的自有股——无投票权，不获股息
  • Outstanding（流通股）= Issued − Treasury

▸ 普通股股东权利：
  • 查阅公司财务记录
  • 选举董事会、对重大事项投票（合并、股票分拆等）
  • 股息权（但是否派发由董事会决定，股东不投票）
  • 证券转让权；破产清算时剩余财产请求权（排最末）

⚠️ 考试提示：股东无权对股息发放投票——这是董事会权力（高频陷阱）

══════════════════════════════════════
二、投票机制（Voting Methods）
══════════════════════════════════════

| 投票方式 | 机制 | 受益方 |
|----------|------|--------|
| 法定投票（Statutory） | 每股每项议题1票 | 大股东（多数派） |
| 累积投票（Cumulative） | 总票数=持股×候选人数，可集中投给一人 | 小股东（少数派） |

例：持有1,000股，选举3名董事
  法定投票：每位候选人最多1,000票
  累积投票：共3,000票，可全投给同一人

⚠️ 考试提示：累积投票保护少数股东——高频考点

══════════════════════════════════════
三、优先股（Preferred Stock）
══════════════════════════════════════

📄 原文：
"Preferred stockholders have a senior claim on assets over common stockholders, but a junior claim compared to bondholders. Preferred stock typically pays a fixed dividend based on its par value ($100)."

【考点解析】
▸ 基本特征：面值$100；固定股息；无投票权；利率敏感（利率↑→价格↓）

▸ 五类优先股（必背）：
| 类型 | 关键特征 |
|------|---------|
| 累积型（Cumulative） | 积欠股息（Arrears）必须全额补发，才能对普通股派息 |
| 非累积型（Non-cumulative） | 未派股息直接作废，无补发义务 |
| 参与型（Participating） | 固定股息之外，还可分享额外超额利润 |
| 可赎回型（Callable） | 公司可按约定价格提前赎回 |
| 可转换型（Convertible） | 可按固定比率转换为普通股 |

▸ 可转换优先股计算：
  转换比率 = $100面值 ÷ 转换价格
  转换价值 = 转换比率 × 当前股价

⚠️ 考试提示：Dividends in Arrears只有累积型才有；优先股面值=$100（非$1,000）

══════════════════════════════════════
四、认购权（Rights）与认股权证（Warrants）
══════════════════════════════════════

| 特征 | Rights（认购权） | Warrants（认股权证） |
|------|----------------|-------------------|
| 认购价格 | 低于当前市场价 | 高于当前市场价 |
| 有效期限 | 短（约30–45天） | 长（通常数年） |
| 分发对象 | 现有普通股股东 | 新债券/优先股购买者 |
| 主要目的 | 维持股东持股比例 | 作为债券的"甜头"（sweetener） |

⚠️ 考试提示：Rights低于市价；Warrants高于市价——必考对比

══════════════════════════════════════
五、美国存托凭证（ADRs）
══════════════════════════════════════

📄 原文：
"ADRs allow investors to purchase securities of foreign companies in U.S. markets, priced and paying dividends in U.S. dollars."

【考点解析】
▸ 外国公司股票在美国市场交易；以美元计价和派息
▸ 仍具汇率风险（外币→美元转换风险）
▸ 无优先认购权（No Preemptive Rights）
▸ Sponsored ADR：交易所上市，发行公司赞助
▸ Unsponsored ADR：OTC市场，银行自行发行

⚠️ 考试提示：ADR无优先认购权（易错高频点）

══════════════════════════════════════
六、股息关键日期（Dividend Dates）
══════════════════════════════════════

▸ 顺序（必背）：
  1. 宣布日（Declaration Date）：董事会宣布股息
  2. 除息日（Ex-Dividend Date）：T+1结算下 = 登记日前1个交易日
     → 在除息日当天或之后买入的股东不获此次股息
  3. 登记日（Record Date）：确定有权获息的股东名单
  4. 支付日（Payment Date）：实际发放股息

⚠️ 考试提示：T+1结算→除息日=登记日前1个交易日

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【速记】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✦ Outstanding = Issued − Treasury（库存股：无投票权、无股息）
✦ 股息由董事会决定，股东不投票
✦ 累积投票保护小股东；法定投票有利大股东
✦ 优先股面值$100；累积型积欠股息必须补发
✦ Rights认购价低于市价（30–45天）；Warrants高于市价（多年）
✦ ADR：美元计价，有汇率风险，无优先认购权
✦ 除息日 = 登记日前1个交易日（T+1）"""),
    7: ("""【考试权重】★★★★☆
所在考纲：Section 2 – Understanding Products and Their Risks
本章预计题量：约 6–8 题

══════ 共同基金基础 ══════

NAV（净资产值）= (总资产 − 负债) ÷ 流通股数
POP（公开募集价）= NAV ÷ (1 − 销售佣金%)
正向定价（Forward Pricing）：当天收盘后 NAV 定价，不论何时下单
赎回必须在 7 个日历日内完成

══════ 费用结构 ══════

12b-1 费：最高 1% 年率，按季度从基金净资产扣除
费用率（Expense Ratio）= 总运营费用 ÷ 平均净资产（不含销售费用）
免佣基金（No-Load）：12b-1 ≤ 0.25%，且无销售费用

══════ 三大份额类别 ══════

A类：前端最高8.5%，12b-1最低，长期持有最便宜，有折扣点
B类：后端递减（CDSC），12b-1较高，约7年后自动转换为A类
C类：无前端/后端，12b-1最高（≈1%），不转换，短期用成本高

B/C类无折扣点；长期投资首选A类

══════ 折扣点与优惠政策 ══════

折扣点（Breakpoints）：同一基金家族同类别累计金额享受佣金折扣
意向书（LOI）：有效期13个月，可倒追90天；非约束性，不达标须补交差价
累计权利（ROA）：将历史持仓计入折扣门槛（累积有效）
最高8.5%销售费用：必须同时提供折扣点AND ROA

违禁行为：
- Breakpoint Sales：刻意分拆让客户无法享受折扣
- Selling Dividends：除息日前购入"赚取"股息
- Switching/Churning：频繁在基金间切换收取佣金
- 股息再投资必须按NAV，不得收销售费用

══════ UITs（单位投资信托）══════

设立依据：信托契约（Indenture），由受托人（Trustees）管理
属于"监管"非"主动管理"（Supervised, not Managed）
SBIs最低面值$1,000；固定投资组合，设立后不再交易，无管理费

══════ 封闭式基金（Closed-End Funds）══════

一次性IPO，固定股数；在交易所二级市场买卖
供需定价，可溢价/折价于NAV
收佣金（Commission），不收销售费用；可融资（Marginable）

━━ 速记 ━━
✦ NAV = (资产−负债)÷股数；POP = NAV÷(1−SC%)
✦ 7日历日内赎回；正向定价
✦ A类前端≤8.5%；B类后端→7年转A；C类最贵长期
✦ LOI = 13个月，可倒追90天，非约束性
✦ ROA = 历史持仓累积计入折扣
✦ 8.5%最高销售费 = 必须同时有折扣点+ROA
✦ UIT = 固定组合，无管理费，SBI最低$1,000
✦ 封闭式 = IPO一次，交易所买卖，可溢/折价"""),
    8: ("""【考试权重】★★★★☆
所在考纲：Section 2 – Understanding Products and Their Risks
本章预计题量：约 5–7 题

══════ 固定年金 vs 变额年金 ══════

固定年金：不是证券，仅需州保险执照，保险公司保证收益，置于一般账户
变额年金：是证券，需要 Series 6/7 + 州保险执照，收益取决于投资表现，置于独立账户

独立账户（Separate Account）与保险公司一般账户隔离
独立账户依照1940年投资公司法注册
积累期：买入→积累单位（Accumulation Units）
年金化：开始领取→转换为年金单位（Annuity Units）
年金单位价值每月浮动（取决于投资表现）

══════ 身故赔偿 ══════

在积累期，身故赔偿 = max（已缴纳总保费，账户当前价值）
保证投资者至少能拿回全部已缴保费

══════ 年金化选项 ══════

Straight Life（纯终身）：最高月付，持续至死亡，无受益人
Life with Period Certain：终身+保证最低支付期，提前死亡则付给受益人
Unit Refund：终身+退还未领金额，有受益人
Joint & Last Survivor：两人均在世按全额，一方死后降低支付

Straight Life月付最高，但死后无受益人

══════ 税务规则 ══════

59½岁前提取：10%罚款+普通所得税
年金化后领取：全部按普通所得税征税（非资本利得）
变额年金无法定最高销售费用上限

══════ 税收优惠年金（403b / TSA）══════

适用：非营利组织、公立学校教职工
供款：税前资金；领取：全额应税

══════ 1035 免税转换 ══════

允许：年金→年金，寿险→年金
不允许：年金→寿险
不触发应税事件

══════ 指数年金（EIC）══════

不是证券；有最低保证利率；有参与率上限；15年投降期

══════ 529 教育储蓄 ══════

$19,000/年；前置5年=$95,000；K-12每年$10,000；学生贷款终身$10,000

══════ 529A ABLE ══════

$19,000/年；一人一账户；SSI阈值$100,000；最高$500,000

주요합규：年金交换本金批准须在7个营业日内完成

━━ 速记 ━━
✦ 固定年金≠证券；变额年金=证券（需Series 6/7+保险执照）
✦ 独立账户按1940年法注册；与一般账户隔离
✦ 积累单位→年金单位（年金化时转换）
✦ 身故赔偿 = max(总保费, 账户价值)
✦ Straight Life月付最高，无受益人
✦ 59½前提取：10%罚款+普通所得税
✦ 1035 = 免税转换（年金→年金可；年金→寿险不可）
✦ EIC = 非证券，有最低保证+参与率上限，15年投降期
✦ 529：$19K/年；可前置5年=$95K
✦ 529A ABLE：$19K/年，$100K SSI阈值，一人一账户"""),
    9: ("""【考试权重】★★★★☆
所在考纲：Section 2 – Understanding Products and Their Risks
本章预计题量：约 5–7 题

══════ ETF（交易所交易基金）══════

被动管理为主（追踪指数）；在交易所盘中买卖，按市场价成交（非NAV）
费用：收佣金，不收销售费用；管理费率低于共同基金
可融资（Marginable）；可卖空（Shortable）

杠杆/反向ETF：每日重置机制，长期持有因波动衰减偏离预期倍数——仅适合短期

══════ ETN（交易所交易票据）══════

本质是发行机构的无担保债务（非基金）
无利息支付；到期按约定指数收益偿还；期限10-30年
主要风险：发行人信用风险（发行银行违约则损失全部本金）

══════ 对冲基金 ══════

不受1940年投资公司法约束；通过Reg D私募发行
仅面向合格投资者（净资产>$1M不含主宅，或年收入>$200K）
费用：2-and-20（2%管理费+20%业绩分成）；流动性极低

══════ REITs（房地产投资信托）══════

注册依据：1933年证券法（非1940年投资公司法）
三类：抵押型（Mortgage）、权益型（Equity）、混合型（Hybrid）

税务规则：
- 至少分配90%应税收入→免企业所得税
- 股息按普通所得税率征税（非合格股息）
- 不传递亏损（区别于DPPs！）
- 2018年起：投资者享20% QBI扣除额

══════ DPPs（直接参与项目）══════

LP结构：
- 普通合伙人（GP）：至少持有1%资本，无限连带责任，负责日常运营
- 有限合伙人（LP）：被动投资者，有限责任，不参与管理

清算顺序：有担保债权人→无担保债权人→LP→GP
GP排在LP之后（清算时最后分配）

税务：被动亏损可结转，只能与被动收入对冲
通过Reg D发行；最高承销费用10%

DPP类型：
- 房地产：折旧抵税
- 石油天然气勘探型：最高风险，最高税收优惠（无形钻井费用）
- 石油天然气开发型：较低风险，在已知储量区域
- 石油天然气平衡型：勘探+开发混合
- 石油天然气收入型：最低风险，购买已成熟油井

━━ 速记 ━━
✦ ETF = 被动管理，交易所交易，收佣金，可融资/卖空
✦ 杠杆/反向ETF = 每日重置，只适合短期
✦ ETN = 无担保债务，无利息，有信用风险，10-30年
✦ 对冲基金 = Reg D，合格投资者，2-and-20，不受1940年法约束
✦ REIT = 90%分配免企税；股息普通所得税；不传递亏损；2018起20% QBI
✦ DPP = LP结构；GP无限责任排清算末位；被动亏损结转
✦ 最高承销费用10%；石油勘探型=最高风险+最高税收优惠"""),
    10: ("""【考试权重】★★★★★
所在考纲：Section 2 – Understanding Products and Their Risks
本章预计题量：约 8–10 题

══════ 期权基本术语 ══════

买方（Buyer）= Long = Holder：支付权利金，获得权利
卖方（Seller）= Writer = Short：收取权利金，承担义务
Call（看涨期权）：买入权利；买方看涨
Put（看跌期权）：卖出权利；买方看跌
1份合约 = 100股

权利金 = 内在价值 + 时间价值

实值（ITM）：Call时市价>执行价；Put时市价<执行价
平值（ATM）：市价=执行价
虚值（OTM）：Call时市价<执行价；Put时市价>执行价
只有实值期权有内在价值

══════ 盈亏平衡价格 ══════

Call盈亏平衡 = 执行价 + 权利金（"Call UP"）
Put盈亏平衡 = 执行价 - 权利金（"Put DOWN"）

例：买入Call，执行价$50，权利金$3 → 盈亏平衡=$53
例：买入Put，执行价$50，权利金$3 → 盈亏平衡=$47

══════ 期权风险/收益矩阵 ══════

Long Call：最大收益无限，最大亏损=权利金
Naked Short Call：最大收益=权利金，最大亏损无限
Long Put：最大收益=执行价-权利金（股价跌至0），最大亏损=权利金
Short Put：最大收益=权利金，最大亏损=执行价-权利金

══════ 期权类型 ══════

美式（American）：到期前任何时间行权，适用于股权期权
欧式（European）：仅到期日行权，适用于指数期权、货币期权
指数期权：现金结算（不交割股票）

══════ 期权行权流程 ══════

买方通知BD → BD通知OCC → OCC随机指定 → 被指定BD → 分配给客户
OCC（期权清算公司）保证所有上市期权的履约
结算：T+1

期权到期规则：
- 交易停止：到期日东部时间下午4:00
- 买方行权通知截止：下午5:30
- 技术到期：下午11:59（第三个星期五）

ODD（期权披露文件）：开户前或开户时必须提供，由OCC创建

══════ 套期保值与期权策略 ══════

持有多头股票→买入Put（Protective Put）：保护下行风险
持有空头股票→买入Call（Protective Call）：保护上行风险

备兑看涨（Covered Call）：
- 持有股票+卖出Call
- 产生权利金收入；上行收益被封顶
- 无需保证金账户

裸空看涨（Naked Call）：
- 无股票+卖出Call
- 无限亏损风险（最危险策略）
- 必须保证金账户

━━ 速记 ━━
✦ 买方=Long=Holder（付权利金有权利）；卖方=Writer（收权利金有义务）
✦ Call=右买（ITM：市价>执行价）；Put=右卖（ITM：市价<执行价）
✦ Call盈亏平衡=执行价+权利金；Put盈亏平衡=执行价-权利金
✦ Long Call：无限收益，亏损限于权利金
✦ Naked Short Call：收益限于权利金，亏损无限（最危险）
✦ 美式期权任何时间行权；欧式仅到期日（指数用欧式）
✦ OCC保证所有上市期权；结算T+1
✦ ODD=期权披露文件，开户前必须提供，OCC制作
✦ 备兑Call=持股+卖Call，上行封顶，无需保证金
✦ 裸空Call=无股+卖Call，无限亏损，需保证金账户
✦ 保护性Put=持股+买Put，对冲下行风险"""),
    11: ("""【考试权重】★★★★☆
所在考纲：Section 1 – Knowledge of Capital Markets
本章预计题量：约 5–7 题

══════ 经济指标 ══════

领先指标（提前预测）：股价、新屋许可证、制造业新订单、消费者信心指数
滞后指标（经济变化后才跟）：失业率、CPI、企业库存
同步指标：GDP、个人收入、制造业产出

股市是最重要的领先指标；失业率是滞后指标

══════ 经济周期 ══════

扩张→顶峰→收缩/衰退→谷底
衰退 = GDP连续两个季度负增长
萧条 = 严重且持续的衰退

══════ 货币政策（联储Fed）══════

三大工具：
- 公开市场操作（最常用）：买入国债=宽松（注入资金）；卖出国债=紧缩（抽走资金）
- 贴现率：降低=宽松；提高=紧缩（联储直接设定）
- 法定准备金率：降低=宽松；提高=紧缩

联邦基金利率：银行间隔夜拆借利率；联储不直接设定（通过公开市场操作影响）

══════ 财政政策（政府）══════

扩张性：增加支出/减税→刺激经济
紧缩性：减少支出/增税→抑制通胀
执行较慢（需立法），不如货币政策灵活

══════ 通胀与利率 ══════

通胀上升→利率上升→债券价格下跌
通胀下降→利率下降→债券价格上涨

实际GDP = 剔除通胀后的真实增长；名义GDP = 未剔除通胀

失业类型：摩擦性（换工作）、结构性（技能不匹配）、周期性（衰退导致）、季节性

━━ 速记 ━━
✦ 领先：股价、新屋许可、消费者信心
✦ 滞后：失业率、CPI
✦ 衰退=GDP连续两季度负增长
✦ 最常用工具=公开市场操作；买国债=宽松；卖国债=紧缩
✦ 联储不直接设定联邦基金利率
✦ 财政政策=国会+总统；货币政策=联储"""),
    12: ("""【考试权重】★★★☆☆
所在考纲：Section 1 – Knowledge of Capital Markets
本章预计题量：约 3–5 题

══════ 市场结构 ══════

一级市场：新证券首次发行（IPO），发行方筹集资金
二级市场：已发行证券在投资者之间交易，发行方不获资金

交易所（NYSE）= 拍卖市场，指定做市商（DMM）
NASDAQ = 经销商市场，多个做市商竞争报价

第三市场：场外交易上市股票
第四市场：机构直接交易（ECN）

经纪商：代客户交易，收佣金（代理身份）
自营商：以自有资金买卖，赚价差（主体身份）
同一笔交易中BD只能为一种身份

══════ 证券分析 ══════

基本面分析：评估公司财务和内在价值；使用P/E、EPS、股息收益率等
技术分析：研究历史价格和成交量图表；假设历史走势会重复

有效市场假说：
- 弱式：技术分析无效
- 半强式：基本面分析无效
- 强式：无人能持续跑赢市场

常用比率：P/E=股价÷EPS；股息收益率=年股息÷股价；流动比率=流动资产÷流动负债

══════ 投资风险 ══════

系统性风险（Market Risk）：影响整个市场，无法通过分散消除
非系统性风险（Specific Risk）：只影响特定公司/行业，可分散消除

Beta(β)：β=1与市场同步；β>1波动大于市场；β<1波动小于市场
分散化可消除非系统性风险，不能消除系统性风险

━━ 速记 ━━
✦ 一级=新发行；二级=已发行交易
✦ NYSE=拍卖市场；NASDAQ=经销商市场
✦ 同一笔交易BD只能为一种身份
✦ 系统性风险无法分散；非系统性可分散
✦ β>1波动大；β<1波动小"""),
    13: ("""【考试权重】★★★★☆
所在考纲：Section 3 – Understanding Trading, Customer Accounts and Prohibited Activities
本章预计题量：约 5–7 题

══════ 客户账户类型 ══════

个人账户：单一持有人

联名账户：
- JTWROS（生存者取得权）：一方死亡→另一方自动继承全部
- TIC（按份额共有）：一方死亡→份额进入遗产（按遗嘱）

未成年人账户：
- UGMA：现金和证券；UTMA：更广泛资产（房产等）
- 监护人控制；不可撤销赠与；成年后移交未成年人
- 每个账户只有一个监护人和一个未成年人

信托账户：受托人管理，受益人享有
法人/合伙账户：需提供公司决议或合伙协议

══════ 新账户开设（KYC）══════

必须获取：姓名、地址、SSN/税号、出生日期
必须记录：投资目标、财务状况、风险承受能力

══════ 保证金账户 ══════

Reg T（联储制定）：初始保证金=50%
维持保证金：25%（FINRA制定）
触发追加保证金通知（Margin Call）：账户权益跌破25%

担保协议（Hypothecation）：客户授权BD以证券作抵押
再质押（Rehypothecation）：BD可将客户证券转质押给银行，最多140%

══════ SIPC 保护 ══════

每账户$500,000，其中现金最高$250,000
保护BD倒闭导致的资产丢失；不保护投资亏损；不是政府机构

══════ 全权委托账户 ══════

须书面授权（Power of Attorney）
每笔交易后主管必须审查；不得过度交易（Churning）

━━ 速记 ━━
✦ JTWROS：一方死亡→另一方自动继承全部
✦ TIC：一方死亡→份额进入遗产
✦ UGMA/UTMA：不可撤销；成年后移交；一账户一监护人
✦ KYC必须：姓名、地址、SSN、出生日期
✦ Reg T=50%（联储）；维持保证金25%（FINRA）
✦ 再质押最多140%
✦ SIPC：$500K总额，$250K现金；非政府机构"""),
    14: ("""【考试权重】★★★★★
所在考纲：Section 3 – Understanding Trading, Customer Accounts and Prohibited Activities
本章预计题量：约 6–8 题

══════ 传统IRA ══════

年供款$7,000（50岁+$1,000）；供款截止至报税截止日
税务递延增长；提取按普通所得税
59½前提取：10%罚款；73岁起强制RMD
无雇主计划→供款可扣税；有雇主计划→超过收入门槛不可扣税

══════ Roth IRA ══════

税后供款；合格提取完全免税（账户满5年+59½岁以上）
无RMD（持有人在世期间无强制取款）
有收入限制；高收入者不可供款

══════ SEP-IRA ══════

适用于自雇人士和小企业主；仅雇主供款
最高25%薪资或$69,000（取较低值）；税前供款

══════ SIMPLE IRA ══════

适用于100名以下雇员小企业
雇员供款最高$16,000（50岁+$3,500）；雇主须匹配
2年规则：前2年提取罚款25%（而非10%！）

══════ 401(k) ══════

雇员供款最高$23,000（50岁+$7,500）
雇主可匹配；59½前提取10%罚款

══════ Keogh / HR-10 ══════

适用于自雇人士；最高25%净自雇收入/$69,000
必须在12月31日前设立（不可等到报税截止日）

══════ 退休账户对比 ══════

传统IRA：税务递延，73岁RMD，提取应税
Roth IRA：免税提取，无RMD（最大优势）
SEP：仅雇主供款，上限高
SIMPLE：小企业，2年内提取25%罚款
401(k)：最常见雇主计划

━━ 速记 ━━
✦ IRA/Roth IRA：$7,000/年，50岁+$1,000
✦ Roth IRA：税后，合格提取免税，无RMD
✦ SIMPLE IRA 2年内提取=25%罚款（非10%！）
✦ SEP：仅雇主供款，最高$69K
✦ 401(k)：$23,000/年，50岁+$7,500
✦ 59½前提取：10%罚款（SIMPLE前2年25%）
✦ Keogh须12月31日前设立"""),
    15: ("""【考试权重】★★★★☆
所在考纲：Section 3 – Understanding Trading, Customer Accounts and Prohibited Activities
本章预计题量：约 5–7 题

══════ 订单类型 ══════

市价单（Market Order）：立即以最佳价格成交；价格不确定
限价单（Limit Order）：指定最低卖价/最高买价；价格确定，执行不确定
止损单（Stop Order）：触发后变为市价单；用于限制亏损
止损限价单（Stop-Limit）：触发后变为限价单；有价格保护但可能不成交

卖出止损价 < 市价（防多头亏损）；买入止损价 > 市价（防空头亏损）

订单有效期：
- Day Order：当天结束自动取消（默认）
- GTC：直到执行或手动取消
- FOK：立即全部成交否则全部取消
- IOC：立即部分/全部成交，未成交部分取消
- MOC：收盘时执行

══════ 交易结算 ══════

2024年起所有主要证券统一T+1结算：
股票、企业债、市政债、国债、共同基金、期权均为T+1

交收失败：卖方未按时交付→买方BD可强制回购（Buy-In）

══════ 做市商与报价 ══════

做市商同时报买价和卖价；价差(Ask-Bid)=做市商利润
SEC Rule 15c3-3：客户证券须单独保管，不得与公司资金混用

══════ 卖空 ══════

借入证券→卖出→价格下跌→买回→归还→获利
必须在保证金账户；最大亏损无限（股价可无限上涨）
逆向ETF可在现金账户使用（非直接卖空）

══════ 除息规则 ══════

除息日=登记日前1个交易日（T+1制度下）
除息日当天或之后买入→不享受股息
除息日前一天买入→享受股息

━━ 速记 ━━
✦ 市价单最快但价格不确定；限价单价格确定但可能不成交
✦ 止损单触发→市价单；止损限价单触发→限价单
✦ 所有主要证券T+1结算（2024年起）
✦ 卖空必须保证金账户；最大亏损无限
✦ 除息日=登记日前1个交易日"""),
    16: ("""【考试权重】★★★★☆
所在考纲：Section 3 – Understanding Trading, Customer Accounts and Prohibited Activities
本章预计题量：约 5–7 题

══════ 适配性原则（Suitability）══════

三层要求：
1. 合理基础：该策略对某类投资者适合
2. 客户特定：对具体这位客户适合
3. 定量：推荐频次合理（防过度交易）

客户档案8大因素：年龄、投资期限、流动性需求、财务状况、税务状况、投资目标、投资经验、风险承受能力

══════ Regulation Best Interest（Reg BI）══════

仅适用于零售客户；推荐时须履行最佳利益义务
四大义务：披露、关注（评估费用/风险/替代品）、利益冲突、合规
Form CRS：BD和顾问均须向零售客户提供，说明服务类型、费用、利益冲突

══════ 投资目标分类 ══════

资本保值：货币市场、国债（风险最低）
收入：债券、优先股、股息股
增长：成长股、ETF
投机：期权、杠杆产品、DPP（风险最高）
税务优化：市政债、税收优惠账户

══════ KYC 与身份验证 ══════

CIP要求：姓名、出生日期、地址、身份证明文件
信托账户需Trust Agreement；公司账户需Corporate Resolution

══════ 特殊规定 ══════

证券行业雇员在他处开户须通知本公司
老年客户疑似金融剥削：可冻结账户最多15个营业日；可通知可信赖联系人

━━ 速记 ━━
✦ 适配性三层：合理基础→客户特定→定量
✦ 8大因素：年龄、期限、流动性、财务、税务、目标、经验、风险
✦ Reg BI = 零售客户最佳利益
✦ Form CRS：BD和顾问均须提供给零售客户
✦ 老年客户疑似剥削：冻结账户最多15个营业日"""),
    17: ("""【考试权重】★★★★☆
所在考纲：Section 1 – Knowledge of Capital Markets / Section 4
本章预计题量：约 5–6 题

══════ 1933年证券法 ══════

目的：确保新证券发行时充分披露（一级市场）
核心：全面披露，不评判投资价值

新股发行流程：
1. 提交注册说明书（Registration Statement）
2. 冷静期（Cooling-Off Period）= 20天
3. 冷静期内：可分发红鲱鱼招募书（Red Herring）；不得接订单/收款/做广告
4. 生效后：可销售，须提供最终招募书

豁免证券（无需注册）：国债、市政债、≤270天商业票据、银行证券
豁免交易：Reg D（私募，合格投资者）；Reg A（简化注册，≤$75M）；Reg CF（众筹，≤$5M）

══════ 1934年证券交易法 ══════

目的：监管二级市场，创建SEC
Rule 10b-5：最重要的反欺诈规则

公众公司报告：
- 10-K：年度报告（审计）
- 10-Q：季度报告（未审计）
- 8-K：重大事项即时披露
- DEF 14A：代理声明（股东大会）

══════ 1940年投资公司法 ══════

规范共同基金、封闭式基金等；三类：管理公司、UIT、面额证书公司

══════ 1940年投资顾问法 ══════

>$110M：须在SEC注册；$25M-$110M：向州注册；<$25M：仅向州注册

══════ Rule 144 ══════

内部人士出售受限制证券：持有期≥6个月（已报告公司）
每3个月限额：流通股1%或4周平均周交易量（取较大值）
>5,000股或>$50,000须提交Form 144

━━ 速记 ━━
✦ 1933年法=一级市场，全面披露；冷静期20天
✦ 冷静期可发红鲱鱼，不能接订单/收款
✦ 豁免证券：国债、市政债、≤270天商业票据
✦ Reg D=私募+合格投资者
✦ 1934年法=二级市场，创建SEC
✦ Rule 10b-5=最重要反欺诈规则
✦ 10-K年报；10-Q季报；8-K重大事项即时
✦ Rule 144：受限证券再售持有期≥6个月"""),
    18: ("""【考试权重】★★★★☆
所在考纲：Section 4 – Overview of the Regulatory Framework
本章预计题量：约 4–6 题

══════ 监管机构体系 ══════

联邦：
- SEC：1934年法创立，最高监管机构
- FRB：制定Reg T（保证金），货币政策
- Treasury/FinCEN：金融犯罪执法

SRO（自律组织）：
- FINRA：最大SRO，监管BD和注册代表
- NYSE、CBOE：证券/期权交易所
- MSRB：市政证券规则制定（只制规则，不执法）

MSRB只制定规则，执法由FINRA和SEC执行
FINRA是针对BD最重要的SRO

══════ FINRA 核心规则 ══════

Rule 2010：诚信商业行为准则
Rule 2111：适配性
Rule 3110：主管审查义务
Rule 4512：客户账户信息记录

注册：SIE无门槛；Series 6=共同基金/变额年金；Series 7=一般证券
纪律：警告→罚款→停职→吊销执照

══════ 州级监管（蓝天法）══════

各州自行制定；联邦豁免不等于州豁免
统一证券法（Uniform Securities Act）：多数州采用范本

══════ 承销方式 ══════

包销（Firm Commitment）：承销商全包，发行方无风险
尽力销售（Best Efforts）：卖不完退回，风险在发行方
全买或全退（AON）：全部售出才生效

东方账户：所有成员共同承担未售出部分
西方账户（Divided）：各成员只对自己的份额负责（更常见）

══════ 持续披露 ══════

Reg FD：禁止选择性向特定人披露重大信息
内部人士：10天内报告>10%股权变动（Form 4）

━━ 速记 ━━
✦ SEC=最高监管；FINRA=最大SRO监管BD
✦ MSRB=只制规则，不执法
✦ FRB制定Reg T（保证金）
✦ 包销=发行方无风险；尽力销售=发行方承担风险
✦ 西方（Divided）账户=各成员只对自己份额负责
✦ Reg FD=禁止选择性披露"""),
    19: ("""【考试权重】★★★★★
所在考纲：Section 3 – Understanding Trading, Customer Accounts and Prohibited Activities
本章预计题量：约 7–9 题

══════ 内幕交易（Insider Trading）══════

📄 原文：Trading on material, non-public information is illegal under Section 10(b) and Rule 10b-5.

【考点解析】
• 重大信息（Material）：合理投资者会认为对投资决策有重要影响
• 非公开信息（Non-Public）：尚未通过合法渠道公开披露
• 内部人士（Insider）：董事、高管、10%以上股东及收到信息的人
• 信息接收者（Tippee）：收到内幕信息者，若知情使用同样违法
• 提供者（Tipper）也违法（即使自己不交易）

内幕交易处罚（ITSFEA 1988）：
• 个人：最高罚款 $5M；最高监禁 20年
• 公司：最高罚款 $25M
• 民事罚款：获利的3倍

══════ 市场操纵（Market Manipulation）══════

| 行为 | 说明 |
|------|------|
| 粉饰行情（Painting the Tape）| 一方或串通双方反复交易，制造活跃假象 |
| 洗售（Wash Sales）| 同一投资者买入卖出同一证券，无真实所有权转移 |
| 对倒（Matched Orders）| 事先约定以相同价格相互对冲，制造交易量 |
| 拉高出货（Pump and Dump）| 散布虚假利好抬价，高位出售套利 |
| 压低吸筹（Short and Distort）| 散布虚假利空做空套利 |

══════ 过度交易（Churning）══════

• 在全权委托账户中过度交易以赚取佣金
• 判断标准：交易频率与客户投资目标是否相符
• 违反适配性和最佳利益原则

══════ 欺诈与不当销售行为 ══════

| 行为 | 说明 |
|------|------|
| 未经授权交易（Unauthorized Trading）| 未获客户许可即进行交易 |
| 挪用客户资金（Misappropriation）| 将客户资金据为己用 |
| 虚假陈述（Misrepresentation）| 提供虚假或误导性信息 |
| 遗漏重要信息（Omission of Material Facts）| 故意隐瞒重要信息 |
| 保证收益（Guaranteeing Returns）| 承诺一定收益或无风险 |
| 混同（Commingling）| 将客户资金与公司资金混在一起 |
| 抢先交易（Front-Running）| 在执行客户大单前，先为自己或他人下单获利 |
| 保留热销新股（Free-Riding / Withholding）| BD成员保留热销新股自用，不对客户发售 |

══════ 反洗钱（AML）规定 ══════

📄 原文：The Bank Secrecy Act requires financial institutions to assist government agencies in detecting and preventing money laundering.

【考点解析】

洗钱三阶段：
1. 置入（Placement）：将现金放入金融系统
2. 分层（Layering）：通过复杂交易掩盖来源
3. 融合（Integration）：洗净资金重新进入合法经济

必须申报的报告：
| 报告类型 | 触发条件 |
|---------|---------|
| CTR（货币交易报告）| 单日现金交易超过 $10,000（必须申报，无论是否可疑）|
| SAR（可疑活动报告）| 可疑交易（无金额下限）；交易后30天内提交；60天内若需调查 |

⚠️ 考试提示：
• CTR = 超过$10,000现金；SAR = 可疑（无下限）
• 提交SAR后**不得通知**当事人（Tipping Off 违法）
• 结构化拆单（Structuring）= 故意将交易拆小以躲避CTR → 本身即违法

AML 计划要求（BD 必须建立）：
• 书面AML政策和程序
• 指定AML合规官（Compliance Officer）
• 员工培训
• 独立审计/测试

══════ 个人礼品与其他规定 ══════

• 礼品限额：每人每年 $100（非现金）
• 现金礼品：任何金额均禁止
• 合规监管：所有员工通讯须按规定保留（电子邮件保存3年）
• 电话录音：交易相关通话须保留

━━ 速记 ━━
✦ 内幕交易 = 重大非公开信息；提供者和接收者均违法
✦ 最高刑事处罚：个人$5M/20年；公司$25M
✦ 抢先交易（Front-Running）= 在客户大单前先下自己的单
✦ 洗钱三阶段：置入→分层→融合
✦ CTR = 现金超$10,000（无论是否可疑）
✦ SAR = 可疑活动（无金额下限）；提交后不得通知当事人
✦ 结构化拆单（Structuring）本身违法
✦ 礼品上限：$100/人/年；现金礼品任何金额均禁止
✦ 保证收益、未授权交易、混同资金均为重大违规"""),
    20: ("""【考试权重】★★★★☆
所在考纲：Section 2 – Understanding Products and Their Risks
本章预计题量：约 4–6 题

══════ 一、资本利得与资本损失（Capital Gains & Losses）══════

📄 原文：
"A capital gain occurs when an investor sells a security for more than its cost basis. A capital loss occurs when an investor sells a security for less than its cost basis."

【考点解析】
▸ 短期资本利得（Short-Term Capital Gain）：
  • 持有期 ≤ 12个月
  • 按普通所得税率（Ordinary Income Tax Rate）征税

▸ 长期资本利得（Long-Term Capital Gain）：
  • 持有期 > 12个月
  • 享受优惠税率：0% / 15% / 20%（按收入水平适用）

▸ 资本损失处理规则：
  • 可用于抵消资本利得
  • 超出利得部分：每年最多可抵消 $3,000 普通收入
  • 超额部分：结转至下一年使用（无限期结转）

⚠️ 考试提示：持有期刚满12个月算短期；超过12个月才算长期

══════ 二、成本基准（Cost Basis）══════

【考点解析】
▸ 常见计算方法：
  | 方法 | 说明 |
  |------|------|
  | FIFO（先进先出）| 假设最先买入的股票最先卖出；默认方法 |
  | 特定股份确认（Specific Identification）| 指定卖出哪批股票；最灵活 |
  | 平均成本法（Average Cost）| 所有股票成本取平均；仅适用于共同基金 |

▸ 特殊情形：
  • 继承获得的证券（Inherited Securities）：
    成本基准 = 继承人死亡当日的公平市场价值（Step-Up in Basis）
    持有期视为长期（无论实际持有多久）
  • 赠予获得的证券（Gifted Securities）：
    成本基准 = 赠予方的原始成本；持有期 = 赠予方的持有期

⚠️ 考试提示：继承证券自动获得"升基"（Step-Up in Basis），且一律视为长期

══════ 三、洗售规则（Wash Sale Rule）══════

【考点解析】
▸ 核心规则：
  • 在出售日前后各30天（共61天窗口期）内
  • 买入相同或实质相同的证券
  • 则不得申报该笔亏损（损失被"冻结"）

▸ 被冻结的损失：加入新买入证券的成本基准，持有期同样延续

⚠️ 考试提示：61天窗口（前30+卖出日+后30）；损失不消失而是加入成本基准

══════ 四、股息税务处理══════

【考点解析】
▸ 合格股息（Qualified Dividends）：
  • 来自美国公司或合格外国公司，满足持有期要求
  • 税率：适用长期资本利得率（0% / 15% / 20%）

▸ 普通股息（Ordinary Dividends）：按普通所得税率征税
  • 包括：货币市场基金利息、短期持有股票股息、REIT股息（大部分）

▸ 股息再投资计划（DRIP）：
  • 即使不收现金，股息仍需当年纳税

⚠️ 考试提示：REIT股息通常为普通股息（非合格股息）

══════ 五、利息收入税务══════

| 证券类型 | 联邦税 | 州/地方税 |
|---------|--------|-----------|
| 企业债利息 | 普通收入税 | 应税 |
| 美国国债利息 | 普通收入税 | 免税 |
| 市政债利息 | 免税 | 视情况（本州通常免）|
| 领土债券利息 | 免税 | 免税（三重免税）|
| 零息债券OID | 年度纳税（幻影收入）| 视类型 |

▸ OID（原始发行折价 / Original Issue Discount）：
  • 零息债券每年须就折价摊销部分纳税，即使未收到现金
  • 国债STRIPS：联邦应税，免州税

══════ 六、税收优惠账户（Tax-Advantaged Accounts）══════

| 账户类型 | 供款税务 | 增长 | 提款 | RMD |
|---------|--------|------|------|-----|
| 传统IRA | 可抵税 | 递延 | 应税 | 73岁起有 |
| Roth IRA | 税后 | 免税 | 免税 | 无 |
| 401(k) | 税前 | 递延 | 应税 | 73岁起有 |
| 529 | 税后 | 免税 | 教育用途免税 | 无 |

▸ 传统IRA：税前供款→税收递延→提款时纳税；73岁起须RMD
▸ Roth IRA：税后供款→免税增长→合格提款免税；无RMD
▸ 401(k)：雇主赞助；税前供款；供款上限更高
▸ 59½岁前提款：额外10%罚税（传统IRA/401(k)均适用）

⚠️ 考试提示：Roth IRA：供款税后、提款免税、无RMD——与传统IRA完全相反

══════ 七、税收损失收割（Tax-Loss Harvesting）══════

▸ 定义：年末卖出亏损证券，实现损失以抵消资本利得
▸ 须遵守洗售规则（不能在30天内买回相同证券）

━━ 速记 ━━
✦ 短期资本利得（≤12月）= 普通税率；长期（>12月）= 优惠率
✦ 洗售规则：前后30天内买回同类证券 → 不得申报亏损
✦ 继承证券：Step-Up in Basis（升基）+ 自动视为长期
✦ FIFO = 默认成本基准方法；平均成本法仅用于共同基金
✦ 合格股息：适用长期资本利得税率（比普通税率低）
✦ 零息债券：每年须就OID（幻影收入）纳税，即使没有收到现金
✦ 传统IRA：递延纳税；Roth IRA：免税增长+免税提款
✦ 401(k)/IRA提前（59½前）提款：10%罚税
✦ 73岁起：传统IRA和401(k)均须开始最低分配（RMD）
✦ 市政债：联邦免税；本州债券额外免州/地方税（三重免税）"""),
}
def get_todays_chapter():
    for arg in sys.argv:
        if arg.startswith('--chapter='):
            return int(arg.split('=')[1])
    # Count weekdays (Mon-Fri) from TRACKING_START up to and including TODAY
    weekdays = 0
    cursor = TRACKING_START
    while cursor <= TODAY:
        if cursor.weekday() < 5:
            weekdays += 1
        cursor += timedelta(days=1)
    return ((weekdays - 1) % TOTAL_CHAPTERS) + 1

def extract_quick_notes(text):
    """Return only the 速记 bullet lines from a chapter's OFFICIAL_NOTES entry."""
    marker = '【本章核心考点速记】'
    idx = text.find(marker)
    if idx == -1:
        return text
    # Skip the two ━━━ separator lines surrounding the header
    after = text[idx + len(marker):]
    lines = after.splitlines()
    bullets = [l for l in lines if l.strip().startswith('✦')]
    return '\n'.join(bullets) if bullets else after.strip()

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

    # ── Daily notes push (SR1 学习群) ──
    elif ntype == 'daily-notes':
        ch = get_todays_chapter()
        note = OFFICIAL_NOTES.get(ch)
        ch_titles = {
            1:'市场参与者',2:'监管框架',3:'股票',4:'债券基础',5:'债券种类',
            6:'投资公司',7:'包销',8:'客户账户',9:'交易与订单',10:'行情报价',
            11:'经济学',12:'技术分析',13:'期权基础',14:'期权策略',15:'直接参与计划',
            16:'退休账户',17:'年金与保险',18:'客户沟通',19:'禁止行为',20:'税务考量',
        }
        title_str = ch_titles.get(ch, f'第{ch}章')
        if note:
            bullets = extract_quick_notes(note)
        else:
            bullets = '（本章速记即将更新，敬请期待）'
        content = (
            f'<at user_id="all">所有人</at>\n\n'
            f'📚 **SIE 今日速记 · 第{ch}章：{title_str}**\n\n'
            f'{bullets}\n\n'
            f'📖 完整精读笔记 → {SITE_URL}'
        )
        payload = {'msg_type': 'text', 'content': {'text': content}}
        if DRY_RUN:
            print(f'[DRY RUN] daily-notes preview:\n{content}')
        else:
            r = requests.post(NOTES_WEBHOOK, json=payload)
            print(f'daily-notes response: {r.text}')

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
