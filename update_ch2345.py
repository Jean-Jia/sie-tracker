import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

ch2 = """【考试权重】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
所在考纲：Section 1 – Knowledge of Capital Markets
本节总题量：12题（含第 1、2、11、19 章）
本章预计题量：约 2–3 题
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

══════════════════════════════════════
一、监管体系四层级
══════════════════════════════════════

📄 原文：
"The securities industry operates under a layered regulatory framework: federal regulation, state regulation, self-regulatory organizations (SROs), and firm-specific rules."

【考点解析】
美国证券监管分四层：
1. 联邦监管（Federal）：SEC 主导，整体市场监督
2. 州级监管（State）：各州 Blue-Sky Laws（蓝天法）
3. 自律组织（SROs）：FINRA、MSRB、CBOE
4. 公司内部规定：Written Supervisory Procedures（WSP）

⚠️ 考试提示：SEC 负责民事执法；DOJ（司法部）处理刑事案件

══════════════════════════════════════
二、主要联邦监管机构
══════════════════════════════════════

📄 原文：
"The SEC is an independent federal agency... The Federal Reserve Board (FRB) acts as the nation's central bank and is responsible for monetary policy... The FDIC insures bank deposits up to $250,000 per depositor per FDIC-insured bank."

【考点解析】
**SEC（证券交易委员会）**
- 独立联邦机构，负责证券市场整体监管
- Division of Enforcement 负责民事执法
- 刑事案件由 DOJ 处理

**FRB（联邦储备委员会）**
- 美国中央银行，制定货币政策
- 工具：贴现率（Discount Rate）、法定准备金率（Reserve Requirements）、Reg T（保证金）
- 通过公开市场操作（Open Market Operations）影响联邦基金利率（Fed Funds Rate）
- 注意：FRB 不直接"设定"联邦基金利率，而是"影响"

**FDIC（联邦存款保险公司）**
- 保险金额：每位储户每家银行最高 $250,000

⚠️ 考试提示：Reg T 由 FRB 制定，管理保证金账户

══════════════════════════════════════
三、自律组织（SROs）
══════════════════════════════════════

📄 原文：
"Self-regulatory organizations (SROs) are non-governmental organizations that have the power to create and enforce industry regulations and standards. The primary SRO for broker-dealers is FINRA."

【考点解析】
**FINRA（金融业监管局）**
- 主要 SRO，监管经纪商和证券代表
- 四项规则体系：
  · Conduct Rules（行为规则）
  · Uniform Practice Code（UPC，统一操作规范）
  · Code of Procedure（纪律程序，FINRA 对会员）
  · Code of Arbitration（仲裁规范，解决金钱纠纷，裁决不可上诉）

**MSRB（市政证券规则制定委员会）**
- 负责制定市政债券规则
- 无执法权：BD 由 SEC/FINRA 执法，银行经销商由货币监理署/FRB/FDIC 执法

**CBOE（芝加哥期权交易所）**
- 最大的期权交易所，期权市场的 SRO

**NASAA（北美证券管理协会）**
- 协调各州 Blue-Sky Laws（统一证券法 USA）

⚠️ 考试提示：MSRB 只制定规则不执法——是高频考点

══════════════════════════════════════
四、重要联邦证券立法（必考）
══════════════════════════════════════

📄 原文：
"The Securities Act of 1933 requires full disclosure of all material information relating to a new securities offering... The Securities Exchange Act of 1934 created the SEC and governs secondary market transactions."

【考点解析】

**1933年证券法（Securities Act of 1933）**
- 规范一级市场（Primary Market，新发行）
- 核心要求：完整披露（Full and Fair Disclosure）
- 要求发行招募说明书（Prospectus）

**1934年证券交易法（Securities Exchange Act of 1934）**
- 规范二级市场（Secondary Market）
- 创建了 SEC
- 制定了 Regulation T（保证金规定）
- 反欺诈条款

**1938年马洛尼法案（Maloney Act）**
- 创建了 NASD（全国证券商协会）→ 2007年合并为 FINRA

**1940年投资顾问法（Investment Advisers Act of 1940）**
- ABC 测试：Advice（建议）、Business（业务）、Compensation（报酬）三者兼具则需注册
- 豁免：律师、会计师、教师、工程师提供的附带性建议

**1940年投资公司法（Investment Company Act of 1940）**
- 规范 FACs、UITs、开放式/封闭式管理公司
- 超过100名股东触发注册要求
- 发行股份最低资产要求：$100,000
- 要求提交半年报和年报

**1970年SIPA / SIPC（证券投资者保护法/公司）**
- 每个独立客户最高保障 $500,000，其中现金最高 $250,000
- 由行业自筹资金，非政府保障
- 覆盖：街名证券（Street-name securities）
- 不覆盖：市场亏损、不当行为造成的损失
- 现金账户+保证金账户合并计算；联名账户=独立客户
- 不覆盖：大宗商品、其他BD账户、高管个人账户

**1974年ERISA**
- 规范私人合格退休计划（如401k）
- 涵盖：归属条款、资金要求、资格要求、受托责任

**1975年证券法修正案**
- 正式创建了 MSRB

**1988年内幕交易法（Insider Trading Act）**
- 禁止使用重大非公开信息（Material Non-Public Information）
- 知情者（Tippers）和受知者（Tippees）均承担责任
- 刑事处罚：最高罚款 $5,000,000 / 最高监禁 20年
- 民事处罚：SEC 可追诉三倍损害赔偿（Treble Damages = 3×）

**1990年廉价股改革法案（Penny Stock Reform Act）**
- 适用于场外股票 < $5/股
- 要求买方签署风险披露声明

**1991年TCPA**
- 禁止打扰名单（Do Not Call）
- 仅允许早8点至晚9点（当地时间）联系

**2001年USA爱国者法案（USA PATRIOT Act）**
- 反洗钱（AML）法规
- CTR：现金交易 > $10,000 必须申报
- SAR：可疑交易 ≥ $5,000 必须申报
- CIP（客户身份识别程序）

⚠️ 考试提示：1933法=一级市场+招募书；1934法=二级市场+创建SEC；SIPC保额必记

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【本章核心考点速记】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✦ SEC=民事执法；DOJ=刑事执法
✦ FRB 通过公开市场操作影响（非直接设定）联邦基金利率
✦ FDIC 保额=$250,000/储户/银行
✦ MSRB=制定规则但无执法权
✦ SIPC=$500K保障（$250K现金上限）；非政府资金；不保市场亏损
✦ 1933法=一级市场+招募说明书；1934法=二级市场+创建SEC
✦ 内幕交易：刑事 $5M罚款/20年监禁；民事=3倍赔偿
✦ CTR>$10,000；SAR≥$5,000
✦ ABC测试=判断是否需注册为投资顾问
✦ ERISA=私人退休计划（401k等）的监管法律"""

ch3 = """【考试权重】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
所在考纲：Section 2 – Understanding Products and Their Risks
本节总题量：33题（含第 3、4、5、7、8、9、10、20 章）
本章预计题量：约 4–6 题
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

══════════════════════════════════════
一、公司与股权基础
══════════════════════════════════════

📄 原文：
"A corporation is a separate legal entity... Shareholders of a corporation have limited liability, meaning that they can lose no more than the amount of their investment."

【考点解析】
- 公司是独立法人实体
- 股东有有限责任（Limited Liability）：最多损失投资本金
- 债券持有人 = 债权人：有权收取利息和本金，无投票权
- 股东 = 所有者：有权获得股息、有投票权

**破产清算顺序（Chapter 7，必背）：**
1. 有担保债权人（Secured Creditors）
2. 行政费用（Administrative Claims）：税款、工资、律师/会计师费
3. 无担保债权人（Unsecured Creditors / Debenture holders）
4. 次级债权人（Subordinated Creditors）
5. 优先股股东（Preferred Stockholders）
6. 普通股股东（Common Stockholders）

⚠️ 考试提示：清算顺序是必考题，普通股股东排最后

══════════════════════════════════════
二、普通股（Common Stock）
══════════════════════════════════════

📄 原文：
"Common stock represents the basic ownership unit of a corporation... The par value of common stock is an arbitrary amount that's used only for bookkeeping purposes."

【考点解析】
**股份状态术语（必考）：**
- Authorized（授权股份）：公司章程允许发行的最大股份数
- Issued（已发行）：已实际发行给投资者的股份
- Treasury（库存股）：公司回购的自有股份；无投票权；不获股息
- Outstanding（流通股）= Issued - Treasury：拥有投票权，获得股息

**普通股股东权利：**
1. 查阅财务记录权
2. 投票权（选举董事会、股票分拆、合并/收购）
3. 股息权（但董事会决定是否派息，股东不投票）
4. 所有权证明
5. 转让权

⚠️ 考试提示：股东不对股息进行投票——这是董事会的权力（高频陷阱）

══════════════════════════════════════
三、投票方式
══════════════════════════════════════

📄 原文：
"Statutory voting allows a shareholder to cast one vote per share for each issue to be decided... Cumulative voting allows shareholders to cast all of their votes for a single candidate."

【考点解析】
**法定投票（Statutory Voting）：**
- 每股 × 每项议题 = 1票
- 有利于大股东（多数派）

**累积投票（Cumulative Voting）：**
- 总票数 = 持股数 × 议题数
- 可将所有票集中投给同一候选人
- 有利于小股东（少数派）

例题：持有1,000股，选举3名董事
- 法定投票：每位候选人最多1,000票
- 累积投票：共3,000票，可全部投给1人

⚠️ 考试提示：累积投票保护少数股东是核心考点

══════════════════════════════════════
四、限制性证券与控制性证券（Rule 144）
══════════════════════════════════════

📄 原文：
"Restricted securities are unregistered securities that are typically received from an issuer through a private placement... Control securities are registered securities that are held by affiliates of an issuing company."

【考点解析】
**限制性证券（Restricted Securities）：**
- 未注册证券，通常来自私募发行
- 报告公司：6个月持有期
- 非报告公司：1年持有期

**控制性证券（Control Securities）：**
- 已注册，持有人为内部人士（高管、董事、>10%股东）
- 无强制持有期，但受 Rule 144 成交量限制

**Rule 144 规则（必考）：**
- 出售时需提交 Form 144
- 90天销售期内有效
- 成交量限制 = 流通股的1% 或 过去4周平均周成交量，取较大值
- 非附属人士（Non-affiliates）无成交量限制

⚠️ 考试提示：Rule 144 同时适用限制性证券和控制性证券，但持有期起算点不同

══════════════════════════════════════
五、股票分类
══════════════════════════════════════

📄 原文：
"Blue-chip stocks are shares of large, well-known companies with a long history of dividend payments... Cyclical stocks are stocks of companies whose earnings tend to fluctuate with the business cycle."

【考点解析】
蓝筹股（Blue-chip）：大型稳定公司，有股息历史（如道指成分股）
成长股（Growth）：收益快速增长，低/无股息（如科技公司）
防御股（Defensive）：抗经济衰退，需求稳定（公用事业、食品、制药）
收益股（Income）：高股息支付（公用事业股）
周期股（Cyclical）：收益随经济周期波动（汽车、钢铁、建筑）

⚠️ 考试提示：公用事业股同时是防御股和收益股

══════════════════════════════════════
六、优先股（Preferred Stock）
══════════════════════════════════════

📄 原文：
"Preferred stockholders have a senior claim on assets over common stockholders, but a junior claim compared to bondholders... Preferred stock typically pays a fixed dividend that's based on its par value ($100)."

【考点解析】
**优先股基本特征：**
- 优先于普通股，次于债券持有人
- 通常无投票权
- 面值 $100（与普通股不同）
- 固定股息率（基于面值计算）
- 适合追求收入的投资者

**优先股类型（必考）：**
累积型（Cumulative）：欠发的股息（Dividends in Arrears）必须在支付普通股股息前全部补发
非累积型（Non-cumulative）：未支付股息直接作废，无法追回
参与型（Participating）：除固定股息外，可能获得额外股息
可赎回型（Callable）：公司有权按指定价格赎回
可转换型（Convertible）：可按固定比率转换为普通股

**可转换优先股：**
- 转换比率 = $100面值 ÷ 转换价格
- 交易价格取赎回价值和转换价值中的较高者

⚠️ 考试提示：累积型"积欠股息"是最常考知识点；优先股面值=$100（非$1,000）

══════════════════════════════════════
七、美国存托凭证（ADRs）
══════════════════════════════════════

📄 原文：
"American Depositary Receipts (ADRs) allow investors to purchase the securities of foreign companies in U.S. markets... ADRs are priced and pay dividends in U.S. dollars."

【考点解析】
- 外国股票在美国市场交易的方式
- 以美元计价和支付股息
- Sponsored（有担保型）：在交易所上市，由发行公司支付费用
- Unsponsored（无担保型）：在场外市场（OTC）交易，由银行发行
- 享有股息权，无优先认购权（No Preemptive Rights）
- 风险：市场风险 + 货币风险（汇率风险）

⚠️ 考试提示：ADR 无优先认购权是易错点

══════════════════════════════════════
八、认购权（Rights）与认股权证（Warrants）
══════════════════════════════════════

📄 原文：
"Rights are issued to existing common shareholders and allow them to purchase additional shares at a price that's below the current market price... Warrants are issued to purchasers of stocks or bonds and allow the holder to purchase shares at a price that's above the current market price."

【考点解析】
认购权（Rights）：
- 发给现有普通股股东
- 认购价格低于当前市场价
- 有效期短：30–45天
- 每股获得一份认购权，目的是维持持股比例

认股权证（Warrants）：
- 随股票/债券发行作为"甜头"（sweetener）
- 认购价格高于当前市场价
- 有效期长：数年
- 可单独分离交易
- 内在价值 = 市场价 - 认购价（正值时）

对比总结：
| 项目     | Rights       | Warrants     |
|----------|--------------|--------------|
| 认购价格  | 低于市价      | 高于市价      |
| 有效期    | 短（30-45天） | 长（数年）    |
| 发给谁    | 现有股东      | 新证券购买者  |

⚠️ 考试提示：Rights 低于市价；Warrants 高于市价——必考对比

════════════════════════════════════════
九、发行人回购规则（SEC Rule 10b-18）
════════════════════════════════════════

📄 原文：
"SEC Rule 10b-18 provides issuers with a 'safe harbor' from manipulation charges when they repurchase their own common stock in the open market."

【考点解析】
Rule 10b-18 回购安全港四项条件：
1. 经纪商：每天只通过一家 BD 进行回购
2. 时机：不在开盘前30分钟和收盘前30分钟（活跃股收盘前10分钟）
3. 价格：不超过最高独立买价或最后独立成交价
4. 成交量：不超过该股票 ADTV（日均成交量）的 25%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【本章核心考点速记】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✦ 破产清算：有担保债权→行政费用→无担保债权→次级债→优先股→普通股
✦ Outstanding = Issued - Treasury（库存股：无投票权、无股息）
✦ 股息由董事会决定，股东不投票
✦ 累积投票=少数股东保护；法定投票=多数股东占优
✦ 优先股面值=$100；累积型积欠股息必须补发
✦ Rights 认购价<市价（30-45天）；Warrants 认购价>市价（多年）
✦ ADR=无优先认购权；有货币风险
✦ Rule 144：报告公司6个月，非报告公司1年；成交量≤1%或4周均量（取大）"""

ch4 = """【考试权重】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
所在考纲：Section 2 – Understanding Products and Their Risks
本节总题量：33题（含第 3、4、5、7、8、9、10、20 章）
本章预计题量：约 3–5 题
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

══════════════════════════════════════
一、债券基本术语
══════════════════════════════════════

📄 原文：
"A bond is a contract between an issuer and an investor... Debt service represents the total of all interest payments over the bond's life and the final repayment of the loan value (principal) at maturity. The issuer must stand ready to make these payments since it will be in default if any are missed."

【考点解析】
债务偿还（Debt Service）：债券存续期内所有利息支付总额 + 到期本金偿还
杠杆融资（Leverage Financing）：发行方通过发债筹资（借助净资产）
面值/本金（Par Value / Principal / Face Value）：到期时发行方支付的金额，通常 $1,000
票面利率（Coupon Rate / Nominal Yield）：发行时确定的固定利率，基于 $1,000 面值计算
到期日（Maturity Date）：债券到期，持有人收回本金的日期

**利息计算示例：**
6%企业债：年利息 = $1,000 × 6% = $60
半年支付（标准）：每次 $30
到期日6月1日 → 付息日为每年6月1日和12月1日

⚠️ 考试提示：票面利率始终基于 $1,000 面值，与购买价格无关

══════════════════════════════════════
二、债券定价与折溢价
══════════════════════════════════════

📄 原文：
"A bond that's sold for less than its par value is selling at a discount, while a bond that's sold for more than its par value is selling at a premium... A bond's price is usually stated as a percentage of its par value."

【考点解析】
价格表示法：以面值百分比表示（"100"= 100%面值 = $1,000）
每个"点（point）"= 面值的1% = $10

| 价格 | 百分比 | 美元   | 状态            |
|------|--------|--------|-----------------|
| 99   | 99%    | $990   | 折价（Discount） |
| 100  | 100%   | $1,000 | 平价（Par）      |
| 101  | 101%   | $1,010 | 溢价（Premium）  |

**交易单位（必考）：**
- 企业债/市政债：以 1/8 点为单位
  87 1/8 = 87.125% = $871.25
- 国债（T-notes/T-bonds）：以 1/32 点为单位
  99.08 = 99又8/32 = 99.25% = $992.50

⚠️ 考试提示：国债用32分之一，企业债用8分之一——必考计算

══════════════════════════════════════
三、利率与价格的反向关系（最核心考点）
══════════════════════════════════════

📄 原文：
"As interest rates increase, the prices of existing bonds decrease and, as interest rates decrease, the prices of existing bonds increase."

【考点解析】
市场利率上升 → 旧债券吸引力下降 → 价格下跌（折价出售）
市场利率下降 → 旧债券吸引力上升 → 价格上涨（溢价交易）

利率风险（Interest-Rate Risk）：
- 长期债券价格波动 > 短期债券（长期债利率风险更大）
- 但短期利率的波动幅度 > 长期利率（短期利率更不稳定）
- 不要混淆：长期债券更脆弱 vs 短期利率更多变

信用风险（Credit Risk）：
- 发行方可能违约，无法支付利息或本金
- 高信用风险发行方必须提供更高收益率
- 公司被评为更高风险 → 债券价格下跌

⚠️ 考试提示："价格-利率反向关系"是SIE最核心考点，务必熟记

══════════════════════════════════════
四、信用评级体系
══════════════════════════════════════

📄 原文：
"Credit rating companies include Moody's, Standard and Poor's (S&P), and Fitch Investors Service. Each company evaluates the possibility that an issuer may default and assigns the issue a credit rating."

【考点解析】
| 等级              | Moody's | S&P  | Fitch    |
|------------------|---------|------|----------|
| 最佳              | Aaa     | AAA  | AAA      |
| 高质量            | Aa      | AA   | AA       |
| 中上              | A       | A    | A        |
| 中等（投资级下限） | Baa     | BBB  | BBB      |
| 投机              | Ba      | BB   | BB       |
|                  | B       | B    | B        |
|                  | Caa     | CCC  | CCC      |
| 违约              | C       | D    | DDD/DD/D |

★ 投资级分界线：Moody's Baa / S&P BBB 及以上
细分：Moody's加1/2/3（1最高）；S&P用+/-符号

⚠️ 考试提示：Aaa/AAA是最高评级；投资级与投机级分界（Baa/BBB）是必考

══════════════════════════════════════
五、应计利息（Accrued Interest）
══════════════════════════════════════

📄 原文：
"Accrued interest is the amount of interest that the seller is entitled to receive (from the buyer) and the amount that the buyer is required to pay (to the seller) for a bond being sold in the secondary market. For calculation purposes, corporate and municipal bonds use 30 days in every month and 360 days in the year, while U.S. government T-notes and T-bonds use actual days in every month and 365 days in the year."

【考点解析】
- 债券在两次付息日之间出售，卖方有权收取其持有期间的利息
- 买方支付应计利息给卖方，下次付息日再收回全期利息

计息惯例（必考）：
- 企业债和市政债：每月30天，每年360天（30/360）
- 美国国债（T-notes/T-bonds）：实际天数/365天（Actual/365）

⚠️ 考试提示：30/360用于公司债和市政债；实际天数用于国债

══════════════════════════════════════
六、零息债券（Zero-Coupon Bonds）
══════════════════════════════════════

📄 原文：
"Zero-coupon bonds don't pay periodic interest. Instead, an investor purchases a zero-coupon at a deep discount from its par value, but redeems the bond for its full face value at maturity. The difference between the purchase price and the amount that the investor receives at maturity is considered the bond's interest."

【考点解析】
- 不定期支付利息
- 以大幅折价购买，到期按面值偿还
- 折扣额 = 投资者的利息收入
- 到期越长，折扣越大
- 适合需要未来特定时间一笔钱的投资者（如子女教育基金）

⚠️ 考试提示：零息债券税务上每年仍需按"应计利息"纳税（幻影收入 Phantom Income）

══════════════════════════════════════
七、债券期限结构
══════════════════════════════════════

📄 原文：
"If all of the bonds in an offering are due to mature on the same date, it's referred to as a term bond issue. On the other hand, if parts of an offering will mature sequentially over several years, it's referred to as a serial bond issue."

【考点解析】
到期债（Term Bond）：整批债券同日到期
分期债（Serial Bond）：债券分批按年度到期，可实现等额还款（Level Debt Service）
气球到期（Balloon Maturity）：部分债券分期到期，大部分在最后到期

⚠️ 考试提示：市政债通常采用分期债结构

══════════════════════════════════════
八、提前赎回条款（Call 与 Put）
══════════════════════════════════════

📄 原文：
"A bond offering may include a call provision which allows the issuer to redeem its outstanding bonds before they reach maturity... Put provisions give the bondholder the right to redeem the bond on a specified date (or dates) prior to maturity."

【考点解析】
赎回条款（Call Provision）：
- 赋予发行方在到期前赎回债券的权利
- 主要目的：利率下降时以低成本重新融资
- 可赎回债券通常提供更高票面利率作为补偿

赎回保护期（Call Protection）：
- 通常为发行后5–10年内禁止赎回
- 赎回溢价（Call Premium）：赎回时支付高于面值的金额
- 例：callable at 102 = 支付$1,020

赎回类型：
- 全额赎回（In-whole）：整批债券同时赎回
- 部分赎回（Partial / Lottery Call）：部分债券随机赎回
- 灾难赎回（Catastrophe Call）：抵押品被损毁时触发，豁免提前披露要求

回售条款（Put Provision）：
- 赋予债券持有人在指定日期以面值回售的权利
- 保护投资者免受利率上升的损失
- 通常导致收益率较低、价格较高

⚠️ 考试提示：Call=发行方权利（低利率时行权）；Put=持有人权利（高利率时行权）

══════════════════════════════════════
九、可转换债券（Convertible Bonds）
══════════════════════════════════════

📄 原文：
"A convertible bond gives an investor the ability to convert the par value of his bond into a predetermined number of shares of the company's common stock... The price at which the bond can be converted is referred to as the conversion price and is set at the time that the bond is issued."

【考点解析】
核心公式：
转换比率（Conversion Ratio）= 债券面值（$1,000）÷ 转换价格

例题：转换价格 = $40
转换比率 = $1,000 ÷ $40 = 25股/债券

转换价值（Conversion Value）= 转换比率 × 当前股价

判断是否转换：比较"卖出债券"和"转换后卖出股票"哪个获益更多

强制转换（Forced Conversion）：
当赎回价格 < 转换价值，持有人被迫选择：
立即转换（更划算）或接受较低赎回金额

税务处理（重要）：
- 转换行为本身不是应税事件（NOT a taxable event）
- 转换后股票的成本基准 = 原债券的成本基准
- 出售股票时才产生税务事件

优缺点：
- 发行方：以较低票面利率借款
- 投资者：接受较低利率，可分享股价上涨；有债券保底价值
- 风险：大批转换后流通股增加（稀释效应）

⚠️ 考试提示：转换公式和强制转换计算是高频考点；转换不触发税务是陷阱题

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【本章核心考点速记】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✦ 价格与利率反向变动（利率↑→价格↓）
✦ 长期债券利率风险>短期债券；短期利率波动幅度>长期利率
✦ 企业债/市政债=30/360计息；国债=实际天数/365
✦ 企业债/市政债以1/8点交易；国债以1/32点交易
✦ Aaa/AAA=最高评级；投资级≥Baa/BBB；低于此为垃圾债
✦ Call=发行方权利（低利率时行权）；Put=持有人权利（高利率时行权）
✦ 转换比率=$1,000÷转换价格
✦ 债券转换为股票：不触发税务；成本基准继承
✦ 零息债券：折价购买，到期收面值；有幻影收入税（年度纳税）"""

ch5 = """【考试权重】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
所在考纲：Section 2 – Understanding Products and Their Risks
本节总题量：33题（含第 3、4、5、7、8、9、10、20 章）
本章预计题量：约 5–8 题
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

══════════════════════════════════════
一、美国国债（Treasury Securities）概览
══════════════════════════════════════

📄 原文：
"Treasury securities are considered the safest type of fixed-income investment and are suitable for the most conservative investors. Since the securities are backed by the full faith and credit of the U.S. government, they have virtually no credit risk. This 'no default' status is the benchmark against which the credit ratings of all other issuers are measured."

【考点解析】
- 信用风险最低（几乎为零），是所有其他发行方信用评级的基准
- 免于1933年证券法注册要求（豁免证券）
- 利息：联邦应税，免州/地方税

| 类型                | 期限              | 特点                                    |
|---------------------|-------------------|-----------------------------------------|
| T-Bills（国库券）   | ≤1年（4/13/26/52周）| 零息折价；收益率报价；最小面值$100     |
| T-Notes（中期国债） | 2–10年            | 半年付息；电子化；最小面值$100          |
| T-Bonds（长期国债） | >10年             | 半年付息；电子化；最小面值$100          |
| TIPS                | 5、10、30年       | 本金按CPI调整；利率固定                 |
| STRIPS              | 零息              | 剥离国债利息/本金创建；收益率报价       |
| CMBs（现金管理票据）| 极短期（可至1天） | 非定期发行；现金流管理                  |

⚠️ 考试提示：T-Bills是唯一以收益率报价的国债；国债利息免州/地方税

══════════════════════════════════════
二、TIPS（通胀保护国债）
══════════════════════════════════════

📄 原文：
"The rate of interest on TIPS is fixed; however, the principal amount on which that interest is paid may vary based on the change in the Consumer Price Index (CPI). During a period of inflation (a rise in CPI), the principal value will increase. However, if deflation occurs (from a decline in CPI), the principal value of the instrument will decrease (but not below $1,000)."

【考点解析】
- 利率固定，但计息基准（本金）随CPI变动
- 通胀期（CPI上升）：本金增加 → 利息增加
- 通缩期（CPI下降）：本金减少，但不低于原始面值$1,000
- 利息：联邦应税，免州/地方税

例题：
4% TIPS，本金因通胀调整为$1,030
年利息 = $1,030 × 4% = $41.20
半年利息 = $41.20 ÷ 2 = $20.60

⚠️ 考试提示：TIPS通缩保护下限为原始面值$1,000

══════════════════════════════════════
三、STRIPS 与 T-Bills 报价
══════════════════════════════════════

📄 原文：
"The Treasury created its Separate Trading of Registered Interest and Principal Securities (STRIPS) program. Dealers are able to purchase T-notes and T-bonds and separately resell the coupon and principal payments as zero-coupons... STRIPS are backed by the full faith and credit of the U.S. Treasury and are quoted on a yield basis."

【考点解析】
STRIPS：
- 将国债的利息和本金"剥离"后分别作为零息债券出售
- 以收益率报价（非面值百分比）
- 有美国财政部的完全信用背书

区分易混概念：
- Treasury Receipts (TRs)：由经纪商发行，仅由国债作担保（非财政部直接背书）
- Treasury STRIPS：财政部官方计划，有完全直接背书

T-Bills报价特殊性：
- 以折现收益率（Discount Yield）报价，非面值百分比
- Bid收益率 > Asked收益率（因价格与收益率反向）
- 债券等价收益率（Bond Equivalent Yield）始终 > 折现收益率

⚠️ 考试提示：STRIPS有财政部背书；Treasury Receipts没有

══════════════════════════════════════
四、国债拍卖（Treasury Auctions）
══════════════════════════════════════

📄 原文：
"When Treasury auctions are held, securities firms compete by submitting bids to buy Treasuries through an automated system... Non-competitive bids are filled first; however, the bidders must agree to accept the yield and price as determined by the auction. All winners of the auction will ultimately pay the lowest price of the accepted competitive tenders. This single price auction process is referred to as a Dutch auction."

【考点解析】
竞争性投标（Competitive Tender）：
- 由证券公司参与，指定价格/收益率
- 类似限价买入订单，可能不成交
- 填单顺序靠后

非竞争性投标（Non-Competitive Tender）：
- 个人投资者参与，不指定价格
- 类似市价买入订单，保证成交
- 优先成交，但接受拍卖决定的价格

荷兰式拍卖（Dutch Auction）：
- 所有获胜者以最低接受价格（最低竞争中标价）统一成交
- Single Price Auction（统一价格拍卖）

拍卖时间表：
| 品种              | 拍卖频率          | 发行时间              |
|------------------|-------------------|-----------------------|
| 4周国库券         | 每周              | 周二拍卖，周四发行    |
| 13/26周国库券     | 每周              | 周一拍卖，周四发行    |
| 52周国库券        | 每4周             | 周二拍卖，周四发行    |
| 2/3/5年期国债     | 每月              | 月底发行              |
| 10年期国债        | 每季度（2/5/8/11月）| 15日发行            |
| 30年期国债        | 每季度（2/5/8/11月）| 15日发行            |

⚠️ 考试提示：非竞争性投标先成交；荷兰式拍卖=统一价格

══════════════════════════════════════
五、机构证券（Agency Securities）
══════════════════════════════════════

📄 原文：
"Agency securities include debt instruments that are issued and/or guaranteed by federal agencies and by government-sponsored enterprises (GSEs)... their yields are slightly higher than the yields of corresponding U.S. Treasury securities."

【考点解析】
联邦机构（Federal Agencies）——有政府完全信用背书：
- GNMA（吉利美）：属于HUD；有美国政府完全信用背书；利息全部应税（联邦+州+地方）

政府支持企业（GSEs）——私人拥有，国会授权，无直接政府背书：
- FNMA（房利美）：购买FHA/VA/传统抵押贷款；利息全部应税
- FHLMC（房地美）：为储蓄机构融资；利息全部应税
- FFCB（联邦农业信贷银行）：农业贷款；利息联邦应税，免州/地方税
- FHLB（联邦住房贷款银行）：为储蓄机构提供流动性；利息联邦应税，免州/地方税

税务速查：
| 机构   | 联邦税 | 州/地方税 |
|--------|--------|-----------|
| GNMA   | 应税   | 应税      |
| FNMA   | 应税   | 应税      |
| FHLMC  | 应税   | 应税      |
| FFCB   | 应税   | 免税      |
| FHLB   | 应税   | 免税      |

⚠️ 考试提示：GNMA是唯一有政府完全背书的抵押机构；GNMA/FNMA/FHLMC利息全部应税

══════════════════════════════════════
六、抵押贷款支持证券（MBS）与预付款风险
══════════════════════════════════════

📄 原文：
"The most common security issued by government agencies is a mortgage-backed pass-through certificate... In addition to the risks that are inherent in many fixed-income investments (e.g., interest-rate, credit, and liquidity risk), mortgage-backed securities are subject to a special type of risk which is referred to as prepayment risk. This is the risk that's tied to homeowners paying off their mortgages early."

【考点解析】
传递证书（Pass-Through Certificate）：
- 发行方将一批抵押贷款打包成资产池
- 向投资者出售对该资产池的不可分割权益
- 月度付款（利息+本金混合）传递给投资者

GNMA 修正传递证书特点：
- 由FHA/VA抵押贷款支持
- GNMA 保证每月按时支付（即使房主未还款）
- 名义期限25–30年，实际平均寿命更短

预付款风险（Prepayment Risk）——MBS特有：
- 利率下降时，房主倾向于重新融资提前还款
- 投资者面临本金提前返还，但再投资收益率更低
- 这是MBS与普通债券的核心区别

资产支持证券（ABS）：
- 将信用卡应收款、汽车贷款、学生贷款等打包证券化
- 优点：较高收益率、高信用质量、现金流可预测
- 风险：利率风险、信用风险、预付款风险

⚠️ 考试提示：预付款风险是MBS独特风险；利率降→提前还款→再投资收益降

══════════════════════════════════════
七、市政债券（Municipal Bonds）
══════════════════════════════════════

📄 原文：
"Municipal bonds are issued by states, territories and possessions of the United States, as well as other political subdivisions... For most investors, the primary advantage of municipal bonds is that the interest received is typically exempt from federal tax."

【考点解析】
市政债基本特征：
- 发行方：州、地方政府、公共机构（如市政局）
- 有一定违约风险（非联邦政府背书）
- 利息：通常免联邦税
- 本州债券利息通常还免州/地方税（三重免税效果）

两大类型对比：
| 项目       | GO债（一般责任债）              | Revenue债（收益债）            |
|-----------|-------------------------------|-------------------------------|
| 还款来源   | 税收（不动产税/所得税等）       | 项目收入（过路费、使用费等）    |
| 需要选民批准| 是                            | 否                             |
| 可行性研究  | 否                            | 是                             |
| 债务上限   | 受约束                        | 不受约束                       |
| 风险       | 相对较低                      | 相对较高（依赖项目收入）        |

各类收益债券：
- 住房收益债（Housing Revenue）：租金/抵押贷款还款
- 宿舍债（Dormitory）：学生学费
- 医疗卫生债（Health Care）：非营利医院收入
- 公用事业债（Utility Revenue）：用户费用
- 交通债（Transportation）：通行费
- 特殊税收债（Special Tax）：特定税收（非地产税）
- 特别评估债（Special Assessment）：受益者专项收费
- 道义责任债（Moral Obligation）：项目收入+州道义背书（非法律义务）
- 工业发展债（IDB）：企业租赁付款；信用评级基于企业（非市政）
- 双重担保债（Double-Barreled Bond）：同时有收入和税收来源

⚠️ 考试提示：GO债=选民批准+税收；Revenue债=可行性研究+项目收入——高频对比考点

══════════════════════════════════════
八、市政票据（Municipal Notes）
══════════════════════════════════════

📄 原文：
"Municipal notes are short-term issues that are normally issued to assist in financing a project or to assist a municipality in managing its cash flow."

【考点解析】
| 缩写  | 全称                              | 用途                     |
|-------|-----------------------------------|--------------------------|
| TAN   | Tax Anticipation Note             | 预期未来税收，用于当前运营 |
| RAN   | Revenue Anticipation Note         | 预期未来收入（联邦/州补贴）|
| TRAN  | Tax & Revenue Anticipation Note   | TAN+RAN合并              |
| BAN   | Bond Anticipation Note            | 为最终发行长期债券过渡融资 |
| GAN   | Grant Anticipation Note           | 预期联邦补助金            |
| CLN   | Construction Loan Note            | 为建设项目提供临时资金    |

市政票据评级：
- Moody's：MIG 1（最高）→ MIG 2 → MIG 3 → SG（投机）
- VRDOs 使用 VMIG 体系
- S&P：SP-1+ → SP-1 → SP-2 → SP-3

⚠️ 考试提示：BAN是为最终长期债券发行前的过渡融资，常考

══════════════════════════════════════
九、市政债发行流程
══════════════════════════════════════

📄 原文：
"Like U.S. government and government agency securities, municipal securities are exempt from the registration and prospectus requirements of the Securities Act of 1933... The underwriter acts as a vital link between the issuer and the investing public by assisting the issuer in pricing the securities, structuring the financing, and preparing a disclosure document (referred to as the official statement)."

【考点解析】
市政债免于1933年证券法注册（豁免证券）
披露文件：Official Statement（官方声明，非招募书）

GO债发行要求：
1. 选民批准
2. 不超过债务上限

Revenue债发行要求：
1. 可行性研究（聘请咨询工程师评估项目可行性）
2. 无需选民批准

承销方式：
| 证券类型                | 主要承销方式                    |
|------------------------|--------------------------------|
| 美国国债                | 拍卖（Auction）                |
| 市政一般责任债（GO）    | 竞争性销售（Competitive Sale） |
| 市政收益债              | 协商销售（Negotiated Sale）    |
| 企业债                  | 协商销售（Negotiated Sale）    |

竞争性销售：邀请多家承销商竞标，最低利率成本者获选
协商销售：发行方直接指定承销商，协商条款

⚠️ 考试提示：GO债=竞争性销售；Revenue债/企业债=协商销售

══════════════════════════════════════
十、企业债券（Corporate Bonds）
══════════════════════════════════════

📄 原文：
"Corporate bonds are divided into two major categories—secured and unsecured. Although all debt that's issued by a corporation is backed by the issuer's full faith and credit, secured bonds are additionally backed by specific corporate assets."

【考点解析】
有担保债券（Secured Bonds）：
- 抵押债（Mortgage Bond）：不动产（第一或第二抵押权）
- 设备信托证书（Equipment Trust Certificate）：特定设备（铁路车厢、飞机等）
- 担保信托债（Collateral Trust Bond）：第三方有价证券（股票/债券）放入托管

无担保债券（Unsecured Bonds / Debentures）：
- 仅凭公司完全信用担保
- 违约时与普通债权人同等索偿权

次级无担保债（Subordinated Debentures）：
- 清算时索偿权低于普通无担保债权人
- 但仍优先于股东

完整清算顺序（6步，必背）：
1. 有担保债权人（包括有担保债券）
2. 行政费用（税款、工资、律师/会计师）
3. 普通债权人（包括无担保债券/Debentures）
4. 次级债权人（Subordinated Debentures）
5. 优先股股东
6. 普通股股东

高收益债/垃圾债（High-Yield / Junk Bonds）：
- S&P评级低于BBB / Moody's低于Baa
- 更高违约风险 → 更高票面利率补偿

其他类型：
- 收益债（Income Bonds）：只有盈利才支付利息；平价交易（无应计利息）；高度投机
- 担保债（Guaranteed Bond）：母公司为子公司债券提供担保

⚠️ 考试提示：Debenture=无担保；Subordinated Debenture=次级无担保；清算顺序必须背熟

══════════════════════════════════════
十一、国际债券（Eurodollar / Yankee / Eurobonds）
══════════════════════════════════════

📄 原文：
"Eurodollar bonds pay their principal and interest in U.S. dollars, but are issued outside of the United States (primarily in Europe)... Yankee bonds allow foreign entities to borrow money in the U.S. marketplace. These bonds are registered with the SEC and sold primarily in the United States."

【考点解析】
| 类型               | 发行地            | 计价货币   | 监管    |
|--------------------|-------------------|------------|---------|
| 欧洲美元债         | 美国境外（欧洲）  | 美元       | 非SEC   |
| 扬基债（Yankee）   | 美国境内          | 美元       | SEC注册 |
| 欧洲债（Eurobond） | 某国境内          | 另一国货币 | 多样化  |

例：俄罗斯企业在伦敦发行瑞士法郎计价债券 = Eurobond（外付债）

⚠️ 考试提示：Yankee Bond=外国实体在美国发行的美元债，需SEC注册

══════════════════════════════════════
十二、货币市场工具（Money Market Securities）
══════════════════════════════════════

📄 原文：
"Short-term debt instruments with one year or less to maturity are referred to as money-market securities... Commercial paper is short-term, unsecured corporate debt which typically matures in 270 days or less. Due to its short maturity, commercial paper is exempt from the registration and prospectus requirements of the Securities Act of 1933."

【考点解析】
| 工具                        | 发行方 | 特点                                         |
|----------------------------|--------|----------------------------------------------|
| 商业票据（Commercial Paper）| 公司   | 期限≤270天；无担保；最小$100,000；折价；免注册 |
| 银行承兑汇票（BA）          | 银行   | 促进国际贸易；货物+银行双重担保               |
| 可转让存单（Negotiable CD） | 银行   | 最低$100,000；有二级市场；$250K以下FDIC保障   |
| 联邦基金（Fed Funds）       | 银行间 | 隔夜拆借；每日波动；FRB间接影响               |
| 回购协议（Repo）            | 经纪商 | 抵押证券借贷；通常隔夜                        |
| 逆回购（Reverse Repo）      | 经纪商 | 买入证券同时约定回售                          |

商业票据信用评级：
- S&P：A1（最高）→ A2 → A3
- Fitch：F1+（最高）→ F1 → F2 → F3
- Moody's：P-1（最高）→ P-2 → P-3；投机级=NP（Not Prime）

利率关系：
- 联邦基金利率影响其他短期利率（FRB不直接设定）
- 优惠利率（Prime Rate）=银行对最佳客户的贷款利率
- SOFR（担保隔夜融资利率）=LIBOR的替代基准利率

⚠️ 考试提示：商业票据≤270天免注册；最小面值$100,000；联邦基金利率非FRB直接设定；LIBOR已被SOFR替代

══════════════════════════════════════
十三、债券利息税务总结（必考速查表）
══════════════════════════════════════

📄 原文：
"The interest received on T-notes and T-bonds is taxed at the federal level, but exempt from state and local taxation... Any interest earned on [GNMA securities] is subject to federal, state, and local taxes."

【考点解析】
| 证券类型                              | 联邦税 | 州/地方税  |
|--------------------------------------|--------|-----------|
| T-Bill / T-Note / T-Bond             | 应税   | 免税      |
| TIPS / STRIPS                        | 应税   | 免税      |
| GNMA（吉利美）                       | 应税   | 应税      |
| FNMA（房利美）                       | 应税   | 应税      |
| FHLMC（房地美）                      | 应税   | 应税      |
| FFCB / FHLB                          | 应税   | 免税      |
| 市政债（Municipal Bonds）            | 免税   | 视情况*   |
| 领土/属地债券（Territory/Possession） | 免税   | 免税      |
| 企业债（Corporate Bonds）            | 应税   | 应税      |

*市政债：大多数州对本州居民购买本州债券免州/地方税
"三免"规则：市政债 + 投资者为该州居民 = 联邦、州、地方税全免

⚠️ 考试提示：税务表是必须熟背的速查表；GNMA全部应税；国债免州税；市政债免联邦税

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【本章核心考点速记】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✦ 国债：联邦应税，免州/地方税；T-Bills折价发行+收益率报价
✦ TIPS：本金随CPI调整，利率固定；通缩下限=$1,000
✦ 非竞争性投标先成交；Dutch Auction=统一价格
✦ GNMA=政府完全背书；FNMA/FHLMC=GSE（无直接背书）
✦ GNMA/FNMA/FHLMC利息全部应税；FFCB/FHLB免州税
✦ GO债=选民批准+税收担保；Revenue债=可行性研究+项目收入
✦ MBS预付款风险：利率降→提前还款→再投资收益降
✦ Mortgage Bond=不动产；Equipment Trust=设备；Collateral=有价证券
✦ Debenture=无担保；Subordinated Debenture=次级无担保
✦ 商业票据≤270天免注册；最小面值$100,000
✦ 市政债利息联邦免税；本州居民购买本州债=三重免税
✦ SOFR已替代LIBOR作为基准利率"""

# Update index.html using regex (nulls already replaced in previous run)
with open(r'C:\Users\45410\Work\SIE考试工具\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'  2: `[^`]*`', lambda m: '  2: `' + ch2 + '`', html, flags=re.DOTALL)
html = re.sub(r'  3: `[^`]*`', lambda m: '  3: `' + ch3 + '`', html, flags=re.DOTALL)
html = re.sub(r'  4: `[^`]*`', lambda m: '  4: `' + ch4 + '`', html, flags=re.DOTALL)
html = re.sub(r'  5: `[^`]*`', lambda m: '  5: `' + ch5 + '`', html, flags=re.DOTALL)

with open(r'C:\Users\45410\Work\SIE考试工具\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated")

# Update notify.py using regex
with open(r'C:\Users\45410\Work\SIE考试工具\.github\scripts\notify.py', 'r', encoding='utf-8') as f:
    py = f.read()

py = re.sub(r'    2: \(.*\),', lambda m: '    2: (' + repr(ch2) + '),', py)
py = re.sub(r'    3: \(.*\),', lambda m: '    3: (' + repr(ch3) + '),', py)
py = re.sub(r'    4: \(.*\),', lambda m: '    4: (' + repr(ch4) + '),', py)
py = re.sub(r'    5: \(.*\),', lambda m: '    5: (' + repr(ch5) + '),', py)

with open(r'C:\Users\45410\Work\SIE考试工具\.github\scripts\notify.py', 'w', encoding='utf-8') as f:
    f.write(py)

print("notify.py updated")
