# FinBharat AI — India Financial Intelligence Multi-Agent System
## Complete Documentation: Agents, Data Sources, URLs, Use Cases & Architecture

**Tagline:** *"Aapke Personal Finance, Banking, Investment aur Tax ka AI-Powered Desi Expert"*

---

## 1. PROJECT OVERVIEW

**FinBharat AI** is a **production-grade multi-agent LangGraph system** designed exclusively for the **Indian financial ecosystem**. It covers personal finance, banking products, investment vehicles, taxation, insurance, retirement planning, government schemes, credit advisory, and macro-economic intelligence — all calibrated for Indian users in INR.

### Core Capability Areas
- 💰 SIP, Mutual Funds, Direct Equity, Debt & Hybrid Investments
- 🏦 Banking Products (FD, RD, Savings, Credit Cards)
- 🏠 Home Loan, Personal Loan, Education Loan, Gold Loan
- 📊 Tax Planning — Old vs New Regime, 80C/80D/80CCD
- 🛡️ Life Insurance, Health Insurance, Term Plans
- 🏛️ Government Schemes — PPF, NPS, Sukanya Samriddhi, KVP, SSY
- 📈 Stock Market, ETFs, REITs, SGBs, InvITs
- 💳 Credit Score (CIBIL, Experian) Improvement
- 📉 Inflation Impact & Macro Financial Analysis
- 🔐 Digital Banking, UPI, Fraud Prevention

---

## 2. EXTENDED DATA SOURCES — 80+ INDIA FINANCIAL URLs

### Category A — Regulatory & Government (Official)

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 1 | **Reserve Bank of India (RBI)** | https://www.rbi.org.in | Repo rate, monetary policy, banking circulars, master directions | Web/PDF | Regular |
| 2 | **SEBI Investor Portal** | https://www.sebi.gov.in | MF regulations, IPO norms, investor protection guidelines | Web/PDF | Regular |
| 3 | **Income Tax India Portal** | https://www.incometax.gov.in | Tax slabs, 80C/80D/80CCD deductions, TDS rules, e-filing | Web | Annual update |
| 4 | **PFRDA / NPS Trust** | https://www.npstrust.org.in | NPS Tier 1/2 returns, contribution calculator, exit rules | Web/API | Regular |
| 5 | **IRDAI Insurance Regulator** | https://www.irdai.gov.in | Life, health, general insurance norms, claim settlement ratio | Web/PDF | Regular |
| 6 | **Ministry of Finance** | https://www.finmin.nic.in | Budget documents, fiscal policy, government finance orders | PDF | Annual |
| 7 | **India Post (Small Savings Schemes)** | https://www.indiapost.gov.in | PPF, NSC, KVP, Sukanya Samriddhi, SCSS current interest rates | Web | Quarterly |
| 8 | **NPCI (Payments Corporation)** | https://www.npci.org.in | UPI, IMPS, NACH, RuPay statistics and guidelines | Web/PDF | Regular |
| 9 | **India Code (Legal)** | https://www.indiacode.nic.in | SARFAESI Act, Consumer Protection Act, FEMA, IBC | PDF | Periodic |
| 10 | **IBBI (Insolvency Board)** | https://ibbi.gov.in | Insolvency resolution, bankruptcy rules | Web/PDF | Regular |
| 11 | **EPFO** | https://www.epfindia.gov.in | EPF interest rate, PF balance, withdrawal rules | Web/API | Regular |
| 12 | **GST Council** | https://www.gst.gov.in | GST rates on financial services, insurance | Web | Periodic |

---

### Category B — Stock Market, Equity & Derivatives

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 13 | **NSE India** | https://www.nseindia.com | Live stock prices, indices (Nifty50, BankNifty), derivatives data | REST API | Real-time |
| 14 | **BSE India** | https://www.bseindia.com | Sensex data, company disclosures, corporate actions | API/CSV | Real-time |
| 15 | **NSE Corporate Data** | https://www.nseindia.com/companies-listing/corporate-filings-financial-results | Quarterly results, balance sheets, P&L | CSV | Quarterly |
| 16 | **BSE Corporate Filing** | https://www.bseindia.com/corporates/ann.html | Announcements, board meetings, AGM results | Web/XML | Real-time |
| 17 | **Screener.in** | https://www.screener.in | Indian stock fundamental data, ratios, 10-year financials | Web API | Daily |
| 18 | **Tijori Finance** | https://tijorifinance.com | Sector-wise stock analysis, institutional holdings | Web | Daily |
| 19 | **Trendlyne** | https://trendlyne.com | Stock alerts, quarterly results, technical analysis | Web/API | Real-time |
| 20 | **Tickertape India** | https://www.tickertape.in | Equity research, portfolio analysis, fund screening | Web | Daily |
| 21 | **Moneycontrol Market** | https://www.moneycontrol.com/markets | Live indices, commodity prices, global markets | Web/API | Real-time |
| 22 | **ET Markets** | https://economictimes.indiatimes.com/markets | Market news, analyst reports, IPO updates | Web | Real-time |

---

### Category C — Mutual Funds & SIP

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 23 | **AMFI India** | https://www.amfiindia.com | All MF NAVs, scheme categorization, AUM data | API/CSV | Daily |
| 24 | **AMFI NAV Download** | https://www.amfiindia.com/spages/NAVAll.txt | Complete daily NAV download for all schemes | TXT/CSV | Daily |
| 25 | **MFI Explorer** | https://www.mfiexplorer.com | Fund comparison, SIP calculator, portfolio overlap | Web | Daily |
| 26 | **ValueResearchOnline** | https://www.valueresearchonline.com | Mutual fund ratings, category comparison, star ratings | Web | Daily |
| 27 | **Morningstar India** | https://www.morningstar.in | Fund ratings, analyst picks, performance attribution | Web/API | Daily |
| 28 | **Kuvera API** | https://kuvera.in | Direct mutual fund transaction data | REST API | Daily |
| 29 | **Groww Research** | https://groww.in/mutual-funds | Fund details, returns calculator, SIP tracker | Web | Daily |
| 30 | **Zerodha Coin** | https://coin.zerodha.com | Direct plan MF data, XIRR calculator | Web | Daily |
| 31 | **Paisabazaar MF** | https://www.paisabazaar.com/mutual-fund/ | Fund comparison, risk analysis, SIP recommendation | Web | Daily |

---

### Category D — Banking Products & Loan Comparison

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 32 | **BankBazaar** | https://www.bankbazaar.com | Home loan, personal loan, FD rates, credit card comparison | Web/API | Frequent |
| 33 | **Paisabazaar** | https://www.paisabazaar.com | Loan eligibility, credit card, insurance comparison | Web | Frequent |
| 34 | **RBI Interest Rate Page** | https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx | Latest repo rate, reverse repo, bank rate | Web | Regular |
| 35 | **SBI Home Loan** | https://sbi.co.in/web/home-loans | Current SBI home loan interest rates, eligibility | Web | Frequent |
| 36 | **HDFC Bank Rates** | https://www.hdfcbank.com/personal/resources/learning-centre/save/savings-bank-interest-rate | HDFC deposit rates, loan EMI calculator | Web | Frequent |
| 37 | **ICICI Bank** | https://www.icicibank.com/personal-banking/loans | ICICI loan products, eligibility calculator | Web | Frequent |
| 38 | **Finbox.in** | https://finbox.in | Bank NBFC-wise loan product comparison | Web/API | Daily |
| 39 | **Loanbaba** | https://www.loanbaba.com | Loan product aggregator, interest rate comparison | Web | Daily |
| 40 | **CRIF India** | https://www.crifhighmark.com | Credit bureau — alternative credit score source | Web | Regular |

---

### Category E — Credit Scores & Reports

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 41 | **CIBIL TransUnion** | https://www.cibil.com | CIBIL score, credit report, dispute resolution | Web API | Monthly |
| 42 | **Experian India** | https://www.experian.in | Experian credit score, credit health summary | Web | Monthly |
| 43 | **Equifax India** | https://www.equifax.co.in | Equifax credit report India | Web | Monthly |
| 44 | **CRIF HighMark** | https://www.crifhighmark.com | Rural + urban credit score data | Web | Monthly |
| 45 | **RBI Credit Info** | https://www.rbi.org.in/scripts/PublicationsView.aspx | Credit growth, NPA trends, credit penetration data | PDF | Quarterly |

---

### Category F — Taxation (India-Specific)

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 46 | **Income Tax Portal** | https://www.incometax.gov.in/iec/foportal/ | Official tax calculator, slab rates, AIS, Form 26AS | Web | Annual + Real-time |
| 47 | **ClearTax** | https://cleartax.in | Tax calculations, filing guide, 80C/80D explanation | Web | Regular |
| 48 | **TaxGuru** | https://taxguru.in | GST + IT detailed articles, case laws | Web | Regular |
| 49 | **TaxMann** | https://www.taxmann.com | Tax treatises, case studies, income tax act | Web | Regular |
| 50 | **CA Club India** | https://www.caclubindia.com | CA community knowledge on taxation | Web | Regular |
| 51 | **GST Portal** | https://www.gst.gov.in | GST registration, returns, HSN codes | Web | Regular |
| 52 | **Tax2Win** | https://tax2win.in | ITR filing, tax saving calculator, refund tracker | Web/API | Regular |

---

### Category G — Insurance

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 53 | **IRDAI Annual Report** | https://www.irdai.gov.in/ADMINCMS/cms/Uploadedfiles/annual_Reports | Insurance penetration, premium data, claim stats | PDF | Annual |
| 54 | **Policybazaar** | https://www.policybazaar.com | Term plan, health insurance comparison | Web/API | Frequent |
| 55 | **InsuranceDekho** | https://www.insurancedekho.com | Life + health + vehicle insurance comparison | Web | Frequent |
| 56 | **LIC of India** | https://www.licindia.in | LIC policy details, bonus rates, premium calculator | Web | Regular |
| 57 | **Star Health Insurance** | https://www.starhealth.in | Health insurance products, network hospitals | Web | Regular |
| 58 | **Digit Insurance** | https://www.godigit.com | Digital-first insurance products and claim data | Web | Regular |
| 59 | **IRDAI CSR (Claim Settlement)** | https://www.irdai.gov.in/ADMINCMS/cms/frmGeneral_Layout.aspx?page=PageNo4110 | Insurer-wise claim settlement ratios | Web/PDF | Annual |

---

### Category H — Government Savings Schemes & Bonds

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 60 | **India Post Small Savings** | https://www.indiapost.gov.in/financial/pages/content/post-office-savings-scheme.aspx | PPF, NSC, KVP, SSY, SCSS, POMIS rates | Web | Quarterly |
| 61 | **RBI Floating Rate Bonds** | https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=11580 | Taxable government bonds details | Web/PDF | Regular |
| 62 | **Sovereign Gold Bond (RBI)** | https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx | SGB issuance calendar, subscription price | Web | Per Tranche |
| 63 | **NHAI Bonds** | https://www.nhai.gov.in | 54EC capital gain bonds details | Web | Regular |
| 64 | **SEBI REITs/InvITs** | https://www.sebi.gov.in/legal/circulars.html | Real Estate Investment Trust data | PDF | Regular |

---

### Category I — Financial News & Research

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 65 | **Economic Times Markets** | https://economictimes.indiatimes.com/markets | Market news, corporate actions, economy | Web | Real-time |
| 66 | **Moneycontrol** | https://www.moneycontrol.com | MF performance, market data, portfolio tracker | Web/API | Real-time |
| 67 | **Business Standard** | https://www.business-standard.com | Finance and economy news, editorial analysis | Web | Real-time |
| 68 | **Livemint** | https://www.livemint.com | Detailed finance, corporate and policy news | Web | Real-time |
| 69 | **BloombergQuint / BQ Prime** | https://www.bqprime.com | Premium Indian financial analysis | Web | Real-time |
| 70 | **Tavily (Real-time)** | https://tavily.com | Live web search for latest financial news | REST API | Real-time |
| 71 | **The Hindu BusinessLine** | https://www.thehindubusinessline.com | Finance + economy news | Web | Real-time |
| 72 | **CNBC TV18** | https://www.cnbctv18.com | Market analysis, budget coverage, expert views | Web | Real-time |

---

### Category J — Macro Economic Data (India)

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 73 | **RBI DBIE (Data Warehouse)** | https://dbie.rbi.org.in | Interest rates, inflation, money supply, credit growth | API/CSV | Monthly |
| 74 | **MoSPI India** | https://mospi.gov.in | CPI, WPI, GDP data | CSV/PDF | Monthly |
| 75 | **CSO (Statistics Ministry)** | https://mospi.gov.in/national-statistical-office | National accounts, per capita income | PDF | Annual |
| 76 | **CMIE Economic Outlook** | https://economicoutlook.cmie.com | Consumer sentiment, investment trends | Paid API | Regular |
| 77 | **IMF India Data** | https://www.imf.org/en/Countries/IND | India's external debt, forex, GDP projections | API/CSV | Quarterly |
| 78 | **World Bank India** | https://data.worldbank.org/country/india | India development indicators, financial inclusion | API/CSV | Annual |

---

### Category K — Cryptocurrency & Alternative Assets (India)

| # | Source | URL | Data Provided | Format | Update Freq |
|---|--------|-----|--------------|--------|------------|
| 79 | **CoinDCX India** | https://coindcx.com | Indian crypto exchange prices, VDA tax guidance | Web/API | Real-time |
| 80 | **WazirX** | https://wazirx.com | Crypto price, volume, order book | Web/API | Real-time |
| 81 | **CBDT Crypto Tax Rules** | https://www.incometax.gov.in | Section 115BBH (30% VDA tax) + 1% TDS rules | Web | Annual |

---

## 3. COMPLETE AGENT ARCHITECTURE — 35 AGENTS, 12 TEAMS

### All FinBharat AI Agents

| # | Agent Name | Team | Responsibility | Data Sources |
|---|-----------|------|---------------|-------------|
| 1 | **Meta-Supervisor Agent** | Orchestration | All user queries route karna, parallel agent invocation | All agents |
| 2 | **User Profiling Agent** | Assessment | Risk appetite, income, goals, age, investment horizon | User input |
| 3 | **Financial Health Checker** | Assessment | Financial health score: income vs expenses vs debt ratio | User input + CPI |
| 4 | **SIP & MF Recommendation Agent** | Investment | Best SIP plans, fund category selection (ELSS, Index, Hybrid) | AMFI + Morningstar + ValueResearch |
| 5 | **Direct Equity Agent** | Investment | Bluechip, midcap, smallcap stock analysis, P/E ratio comparison | NSE + BSE + Screener.in |
| 6 | **ETF & Index Fund Agent** | Investment | Nifty50 ETF, NiftyNext50, Gold ETF, International ETF | NSE + AMFI |
| 7 | **SGB & Gold Agent** | Investment | Sovereign Gold Bond schedule, price, Gold ETF vs Physical Gold | RBI SGB + MCX |
| 8 | **PPF / NSC / SSY Government Schemes Agent** | Investment | Government savings schemes with current interest rates | India Post + Finance Ministry |
| 9 | **NPS Retirement Planning Agent** | Retirement | NPS tier selection, fund manager comparison, annuity options | PFRDA + NPS Trust |
| 10 | **EPF & Gratuity Agent** | Retirement | EPF balance projection, VPF benefits, gratuity calculation | EPFO + India Code |
| 11 | **Tax Planning Agent (Old vs New Regime)** | Taxation | 80C/80D/80CCD optimization, HRA, LTA, deduction maximization | Income Tax Portal + ClearTax |
| 12 | **Advance Tax & TDS Agent** | Taxation | Advance tax computation, TDS on FD, MF redemption taxation | Income Tax Portal |
| 13 | **LTCG/STCG Capital Gains Agent** | Taxation | Long & short term capital gains on equity, MF, property | Income Tax Portal |
| 14 | **Crypto & VDA Tax Agent** | Taxation | 30% flat tax on VDA gains + 1% TDS, loss set-off rules | CBDT Crypto Section + IT Portal |
| 15 | **Home Loan Advisor Agent** | Lending | Home loan eligibility, EMI comparison, PMAY subsidy | RBI + BankBazaar + SBI/HDFC |
| 16 | **Personal & Education Loan Agent** | Lending | Personal loan offers, education loan interest, moratorium rules | BankBazaar + Paisabazaar |
| 17 | **CIBIL & Credit Score Agent** | Credit | CIBIL score improvement plan, credit report analysis | CIBIL + Experian + CRIF |
| 18 | **Banking Products Agent** | Banking | FD/RD comparison, savings account interest, credit card rewards | BankBazaar + Individual banks |
| 19 | **Digital Banking & UPI Guide Agent** | Banking | IMPS/NEFT/RTGS limits, UPI fraud prevention, RuPay benefits | NPCI + RBI UPI Guidelines |
| 20 | **Term Life Insurance Agent** | Insurance | Term plan comparison by sum assured, claim settlement ratio | Policybazaar + IRDAI CSR |
| 21 | **Health Insurance Agent** | Insurance | Family floater vs individual, room rent limits, OPD cover | InsuranceDekho + IRDAI |
| 22 | **ULIP & Traditional Insurance Agent** | Insurance | ULIP vs term plan, surrender value, mortality charges | IRDAI + Policybazaar |
| 23 | **RBI Macro Context Agent** | Macro | Repo rate, inflation impact, monetary policy explanation | RBI + DBIE + MoSPI |
| 24 | **Stock Market Sentiment Agent** | Market | Nifty trend analysis, FII/DII data, market breadth | NSE + ET Markets + Moneycontrol |
| 25 | **Budget & Government Policy Agent** | Policy | Annual budget highlights, new schemes, fiscal policies | Ministry of Finance + PRS India |
| 26 | **Real Estate Investment Agent** | Real Estate | REITs, property price indices, home vs rent analysis | SEBI REIT + NHB Residex |
| 27 | **Budgeting & Expense Tracker Agent** | Personal Finance | 50/30/20 rule, envelope budgeting, expense allocation | User input + CPI MoSPI |
| 28 | **Emergency Fund Planning Agent** | Personal Finance | Emergency corpus size calculation, liquid fund recommendations | AMFI + RBI Savings rates |
| 29 | **Child Education Planning Agent** | Goals | College fee inflation adjustment, SIP for education goal | AMFI + NIRF fee data |
| 30 | **Loan vs Investment Arbitrage Agent** | Strategy | Should you repay loan or invest — mathematical comparison | RBI rates + AMFI returns |
| 31 | **Inflation Impact Calculator Agent** | Macro | Real purchasing power loss, inflation-adjusted returns | MoSPI CPI + DBIE |
| 32 | **Debt Recovery & Grievance Agent** | Legal | Banking Ombudsman process, SARFAESI, IBC provisions | RBI Ombudsman + India Code |
| 33 | **Live News & Rate Updater Agent** | Live Data | Real-time RBI rate changes, budget announcements, SEBI updates | Tavily + ET + Moneycontrol |
| 34 | **Synthesizer Agent** | Output | All agent outputs ko ek clean INR-denominated report mein compile karna | All agents |
| 35 | **Fact Checker & Citation Agent** | Quality | Every claim verify karna against official Indian sources | All datasources |

---

## 4. COMPLETE INTER-AGENT CONNECTION MAP

```
[User Query in Hindi/English]
         │
         ▼
[Meta-Supervisor Agent]
         │
    ┌────┴────────────────────────────────────────────────────────┐
    │                                                             │
    ▼                                                             ▼
[User Profiling]                                     [Financial Health Checker]
    │                                                             │
    └─────────────────────┬───────────────────────────────────────┘
                          │
         ┌────────────────┼──────────────────┬──────────────────────┐
         ▼                ▼                  ▼                      ▼
  [INVESTMENT           [LENDING           [INSURANCE             [TAXATION
   TEAM]                 TEAM]              TEAM]                  TEAM]
   │                     │                  │                      │
   ├─SIP & MF            ├─Home Loan        ├─Term Life            ├─Old/New Regime
   ├─Direct Equity       ├─Personal Loan    ├─Health Insurance     ├─LTCG/STCG
   ├─ETF & Index         └─Credit/CIBIL     └─ULIP Agent           ├─Advance Tax
   ├─SGB & Gold                                                    └─Crypto VDA Tax
   ├─PPF/NSC/SSY
   └─NPS/EPF
         │
         ▼
  [BANKING TEAM]
   ├─Products (FD/RD/CC)
   └─Digital/UPI Guide
         │
         ▼
  [MACRO & POLICY TEAM]
   ├─RBI Context Agent
   ├─Market Sentiment
   ├─Budget Policy
   └─Inflation Calculator
         │
         ▼
  [PERSONAL FINANCE TEAM]
   ├─Budgeting & Expense
   ├─Emergency Fund
   ├─Child Education Plan
   └─Loan vs Investment
         │
         ▼
  [LIVE DATA UPDATER (Tavily)]
         │
         ▼
  [SYNTHESIZER AGENT]
         │
         ▼
  [FACT CHECKER & CITATION]
         │
         ▼
  [OUTPUT: Markdown Report + Calculations + INR Tables]
```

---

## 5. DETAILED USE CASES — INDIA FINANCIAL (30 SCENARIOS)

### USE CASE 1 — SIP Planning for Salaried Employee
**Query:** *"Meri salary 45,000/month hai. Ghar ka kiraya 12,000 hai. 10 saal mein 30 Lakh ka fund banana chahta hoon. Kaise karun?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Financial Health Checker | Savings capacity calculate | Disposable = 45K - 12K (rent) - 15K (expenses) = ₹18,000/month investable |
| 2 | SIP Recommendation | Required SIP for 30L in 10 years | At 12% CAGR: SIP ₹13,000/month required |
| 3 | MF Recommendation | Suitable fund categories | 60% Equity Index Fund + 30% Flexi Cap + 10% Debt (Hybrid) |
| 4 | Tax Agent | ELSS optimization | ₹7,500/month in ELSS saves ₹23,400/year tax under 80C |
| 5 | Synthesizer | Full SIP allocation plan | Detailed monthly breakdown with fund names, NAV, risk level |

---

### USE CASE 2 — Home Loan vs Rent Decision
**Query:** *"Pune mein 70 Lakh ka flat hai. Home loan at 8.5% for 20 years loon ya rent at ₹18,000/month deta rahoon?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Home Loan Agent | EMI on 70L @ 8.5% for 20 years | Monthly EMI: ₹60,785 |
| 2 | Loan vs Investment | Total interest paid | Total payout: ₹1.46 Cr. Total interest: ₹76 Lakhs |
| 3 | Tax Agent | Home loan tax benefits | Section 24 (₹2L interest) + 80C (₹1.5L principal) = ₹3.5L deduction |
| 4 | Real Estate Agent | Property appreciation potential | Pune mid-segment: 6-8% CAGR appreciation |
| 5 | Synthesizer | Buy vs Rent break-even analysis | Break-even at year 11. Recommend buying if planning 15+ year stay |

---

### USE CASE 3 — Tax Regime Optimization (Old vs New)
**Query:** *"Meri CTC 18 LPA hai. Mujhe ₹1.5L 80C mein lagaya hai, ₹25K 80D mein, aur HRA ₹8,400/month mili hai. Konsa regime better hai?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Tax Agent | Calculate Old Regime tax | Taxable = 18L - 1.5L(80C) - 25K(80D) - 1L(HRA) - 50K(std deduction) = 14.75L. Tax: ₹2,62,500 |
| 2 | Tax Agent | Calculate New Regime tax | Taxable = 18L - 75K(std deduction) = 17.25L. Tax: ₹2,50,000 |
| 3 | Tax Agent | Comparison + recommendation | New Regime saves ₹12,500 this year. If 80C investments grow, Old Regime better in future. |
| 4 | Synthesizer | Final recommendation | New Regime for FY2025-26 based on current investment pattern |

---

### USE CASE 4 — Retirement Corpus Planning
**Query:** *"Meri age 35 hai. 60 saal mein retire hona chahta hoon. Monthly ₹75,000 (today's value) chahiye retirement mein. Kitna corpus chahiye?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | NPS/Retirement Agent | Inflation-adjusted corpus | At 6% inflation: ₹75K today = ₹2.41 Lakhs at 60. Corpus needed at 4% SWR: ₹7.23 Crore |
| 2 | NPS Agent | NPS contribution plan | NPS Tier-1: ₹10,000/month for 25 years at 10% CAGR = ₹1.33 Cr |
| 3 | SIP Agent | Equity SIP for remainder | Additional SIP ₹25,000/month for 25 years at 12% = ₹4.75 Cr |
| 4 | EPF Agent | EPF contribution projection | EPF grows to ~₹1.8 Cr by 60 at current rates |
| 5 | Synthesizer | Retirement plan | NPS + SIP + EPF = ₹7.88 Cr. Target achieved! |

---

### USE CASE 5 — CIBIL Score Improvement Plan
**Query:** *"Mera CIBIL score 630 hai. Home loan apply karna chahta hoon 6 months mein. Kya karun?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | CIBIL Agent | Score 630 root cause analysis | Possible: High credit utilization, late EMI payments, multiple inquiries |
| 2 | CIBIL Agent | 6-month improvement plan | 1) Pay all outstanding dues. 2) Keep credit utilization < 30%. 3) No new credit applications |
| 3 | CIBIL Agent | Expected score trajectory | Consistent payments: +30-50 points in 6 months → Score 680-720 |
| 4 | Home Loan Agent | Loan eligibility at 700+ CIBIL | 700+ CIBIL qualifies for 8.5% home loan rate vs 9.5% at 630 |
| 5 | Synthesizer | Action plan | Week-by-week CIBIL recovery steps with bank-specific loan eligibility |

---

### USE CASE 6 — NPS vs PPF vs ELSS Comparison
**Query:** *"Tax saving ke liye NPS, PPF, aur ELSS mein se best kya hai 80C limit ke andar?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | PPF Agent | PPF details | 7.1% guaranteed, 15-year lock-in, EEE (exempt-exempt-exempt) status |
| 2 | ELSS Agent | ELSS returns | Historical 3-year CAGR: 14-18%. 3-year lock-in. Subject to LTCG. |
| 3 | NPS Agent | NPS additional benefit | 80CCD(1B): Additional ₹50,000 deduction over 80C limit |
| 4 | Tax Agent | Combined strategy | ELSS ₹1.5L (80C) + NPS ₹50K (80CCD) = ₹2L total deduction. Best of all three. |
| 5 | Synthesizer | Optimized allocation | NPS + ELSS combo for max tax saving and long-term wealth creation |

---

### USE CASE 7 — Emergency Fund & Liquid Fund Planning
**Query:** *"Mere paas 5 months ki salary save hai. Kya yeh enough hai? Paisa kahan rakhun ki safe bhi ho aur return bhi mile?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Emergency Fund Agent | Standard recommendation | 6 months of expenses minimum. Single income households: 9-12 months |
| 2 | Banking Agent | Savings account options | HDFC, Kotak, AU SFB: 4-7% savings interest rates |
| 3 | Liquid Fund Agent | Better alternative | Liquid MF: 6.5-7.5% returns with T+1 redemption. Better than savings account. |
| 4 | SGB Agent | Gold allocation | 5-10% in Gold ETF as inflation hedge |
| 5 | Synthesizer | Emergency fund structure | 70% Liquid Fund + 20% Savings Account + 10% Gold ETF breakdown |

---

### USE CASE 8 — Child Education Planning
**Query:** *"Mere 3 saal ke bache ki engineering/medical college fee 15 saal baad. Abhi kitna SIP start karun?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Education Planning Agent | Fee inflation calculation | Today's IIT fee ~₹3L/year. At 10% education inflation: ₹12.6L/year in 15 years. 4-year = ₹50 Lakhs |
| 2 | SIP Agent | Required SIP for ₹50L in 15 years | At 13% CAGR (equity): SIP ₹8,200/month required |
| 3 | ELSS Agent | Tax-efficient investment | ELSS: 3-year lock-in, 80C benefit — invest ₹5,000/month in ELSS |
| 4 | SSY Agent | If daughter: Sukanya Samriddhi | SSY: 8.2% guaranteed returns, tax-free. Max ₹1.5L/year |
| 5 | Synthesizer | Child education plan | Equity SIP + SSY (if daughter) + Education Insurance for comprehensive plan |

---

### USE CASE 9 — Sovereign Gold Bond vs Gold ETF vs Physical Gold
**Query:** *"Gold mein invest karna chahta hoon. SGB, Gold ETF, ya physical gold — kya better hai?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | SGB Agent | SGB benefits | 2.5% guaranteed annual interest + Gold price appreciation. Tax-free on maturity (8 years). |
| 2 | ETF Agent | Gold ETF | Flexible, tradeable on NSE, no storage cost. LTCG taxed at 20% with indexation. |
| 3 | Gold Agent | Physical gold | Making charges 10-20%, storage risk, not tax-efficient |
| 4 | Tax Agent | Tax comparison | SGB: Tax-free if held to maturity. Gold ETF: 20% LTCG with indexation. Physical: 20% LTCG |
| 5 | Synthesizer | Best recommendation | SGB first (tax-free + interest), Gold ETF for flexibility. Physical only for jewelry. |

---

### USE CASE 10 — Budget 2025 Impact Analysis
**Query:** *"Budget 2025-26 mein kya badla? Meri salary 12 LPA hai. Kitna tax change hoga?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Live Data Agent | Fetch latest budget updates | Tavily: Budget 2025 new income tax slabs + exemptions |
| 2 | Tax Agent | Old vs New comparison for 12 LPA | New Regime FY26: 12 LPA = Zero tax (with new ₹12L exempt slab) |
| 3 | Budget Policy Agent | Key budget highlights | LTCG changes, TDS threshold updates, ESOP deferment rules |
| 4 | SIP Agent | Budget impact on markets | Fiscal deficit, capex push → Infrastructure + PSU sector outlook |
| 5 | Synthesizer | Personalized budget impact report | For 12 LPA salary: Zero tax in New Regime FY26. Savings: ₹80,000/year |

---

### USE CASE 11 — Debt Trap Recovery
**Query:** *"Mere upar 3 personal loans hain totaling ₹8 Lakh at 18-24% interest. EMI burden bahut zyada hai. Kya karun?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Loan Agent | Debt-to-income ratio analysis | EMI burden > 50% income = financial distress level |
| 2 | Loan Agent | Debt consolidation strategy | Consolidate all 3 loans into 1 loan at 12-14% through top-up home loan or balance transfer |
| 3 | CIBIL Agent | Credit score impact strategy | Stop new credit, negotiate with lenders for restructuring |
| 4 | Budgeting Agent | Expense reduction roadmap | Identify 3-5 expense cuts to accelerate debt payoff |
| 5 | Synthesizer | Debt payoff plan | Avalanche method (highest interest first) with monthly payoff milestones |

---

### USE CASE 12 — Term Insurance Planning
**Query:** *"Meri age 30 hai, married hoon, ek bachha hai. Kitna term life insurance cover lena chahiye aur kaun sa plan?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | User Profiling | Financial dependency analysis | Spouse + child dependent. Annual income ₹8L. Outstanding home loan ₹35L |
| 2 | Insurance Agent | Sum assured calculation | 15-20x annual income + all outstanding liabilities = ₹1.2 Cr - ₹1.6 Cr cover needed |
| 3 | Insurance Agent | Plan comparison (30M, non-smoker, 30-year term) | LIC e-Term: ₹1 Cr for ₹850/month. HDFC Click2Protect: ₹1 Cr for ₹700/month |
| 4 | Tax Agent | 80D + 80C benefit on premium | Term premium qualifies under Section 80C |
| 5 | Synthesizer | Best plan recommendation | HDFC Click2Protect ₹1.5 Cr cover with waiver of premium rider at ₹980/month |

---

### USE CASE 13 — IPO Investment Decision
**Query:** *"Nayi IPO aayi hai kisi company ki. Kaise decide karun apply karun ya nahi?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Live Data Agent | Fetch IPO details via Tavily | GMP, subscription status, price band, financials |
| 2 | Direct Equity Agent | Fundamental analysis | P/E vs industry, revenue growth, debt-to-equity, promoter holding |
| 3 | Market Sentiment Agent | Grey market premium (GMP) analysis | GMP > 20% = strong listing gain expected |
| 4 | Tax Agent | IPO listing gain taxation | Listed < 12 months: 20% STCG. Listed > 12 months: 12.5% LTCG |
| 5 | Synthesizer | Apply/Skip recommendation | If fundamentals strong + GMP > 20%: Apply for listing gain. Long-term: Evaluate separately. |

---

### USE CASE 14 — UPI Fraud Recovery
**Query:** *"Mujhe ek UPI fraud hua. ₹50,000 chale gaye. Kya koi recovery possible hai?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Digital Banking Agent | Immediate steps | 1) Call bank helpline. 2) Block UPI ID. 3) File complaint on cybercrime.gov.in |
| 2 | Grievance Agent | RBI Ombudsman process | File complaint on cms.rbi.org.in if bank doesn't resolve in 30 days |
| 3 | Digital Banking Agent | Chargeback possibility | UPI fraud: Bank initiates chargeback if reported < 3 days. Odds: 40-60% recovery |
| 4 | Policy Agent | NPCI grievance process | NPCI handles inter-bank UPI disputes — escalation process details |
| 5 | Synthesizer | Recovery action plan | 48-hour action checklist with all official complaint portals |

---

### USE CASE 15 — Equity Portfolio Rebalancing
**Query:** *"Mera portfolio 80% equity aur 20% debt hai. Market all-time high pe hai. Kya rebalance karoon?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | User Profiling | Risk profile reassessment | Age 45, 15 years to retirement: Ideal 70% equity, 30% debt |
| 2 | Market Sentiment Agent | Market valuation check | Nifty P/E ratio at 24x — historically expensive zone |
| 3 | Direct Equity Agent | Rebalancing strategy | Shift 10% from equity to debt/arbitrage funds (tax-efficient) |
| 4 | Tax Agent | LTCG/STCG implications | Equity held > 12 months: 12.5% LTCG. ₹1.25L LTCG exemption per year. |
| 5 | Synthesizer | Rebalancing plan | Staggered STP from equity to hybrid/debt over 6 months |

---

### USE CASE 16 — Senior Citizen Financial Planning
**Query:** *"Meri age 62 hai. Retirement ho gayi. ₹50 Lakh FD mein hai. Best strategy kya hai 80 saal tak income ke liye?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Retirement Agent | Safe withdrawal rate | 4% SWR: ₹2L/year from ₹50L. Need supplementary income. |
| 2 | Banking Agent | SCSS (Senior Citizen Savings Scheme) | SCSS at 8.2%, max ₹30L investment, quarterly payout |
| 3 | Government Schemes Agent | PMVVY (Pradhan Mantri Vaya Vandana Yojana) | Check if still active; guaranteed 7.4% pension |
| 4 | Insurance Agent | Health insurance priority | Senior citizen health plan essential — ₹10-15L cover minimum |
| 5 | Synthesizer | Retirement income plan | SCSS ₹30L + Liquid Fund ₹15L + FD ladder ₹5L = ₹3.5L/year stable income |

---

### USE CASE 17 — Freelancer Financial Planning (India)
**Query:** *"Main ek freelancer hoon earning ₹12L/year. GST, Tax, investments — sab kaise manage karun?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Tax Agent | Section 44ADA presumptive taxation | Taxable income = 50% of ₹12L = ₹6L. Tax = ₹22,500 (new regime) |
| 2 | Tax Agent | GST registration check | Revenue < ₹20L threshold: No GST registration needed for services |
| 3 | Investment Agent | SIP from irregular income | Step-up SIP strategy for variable monthly income |
| 4 | Health Insurance Agent | Individual health insurance | No employer cover → Recommend ₹10L health + ₹1 Cr term plan |
| 5 | Synthesizer | Freelancer financial framework | Tax filing guide + investment plan + insurance checklist |

---

### USE CASE 18 — Inflation Hedging Strategy
**Query:** *"Inflation bahut zyada hai. Mera paisa bank FD mein hai jo 6.5% de raha hai aur inflation 6% hai. Real return sirf 0.5%. Kya karun?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Inflation Agent | Real return calculation | FD 6.5% - Inflation 6% - Tax 30% = Real return negative (-0.95%) |
| 2 | Equity Agent | Inflation-beating strategies | Equity (historical 12-15% CAGR) > inflation significantly over 7+ years |
| 3 | Gold Agent | Gold as inflation hedge | Gold: 10-12% long-term returns, negative correlation with rupee depreciation |
| 4 | REITS Agent | REITs for real estate exposure | Indian REITs: 8-10% yield + appreciation. Listed on NSE. |
| 5 | Synthesizer | Inflation-beating portfolio | Equity 60% + Gold 10% + REITs 15% + Debt 15% recommendation |

---

### USE CASE 19 — NRI Financial Planning (India Investments)
**Query:** *"Main Dubai mein hoon. India mein invest karna chahta hoon. Kya options hain?"*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Tax Agent | NRI investment rules | NRE account: Repatriable. NRO: Non-repatriable. FEMA compliance |
| 2 | MF Agent | NRI MF restrictions | USA/Canada based NRIs: Restrictions apply. UAE NRIs: Full access |
| 3 | Direct Equity Agent | NRI stock market access | NRIs can invest via PINS (Portfolio Investment Scheme) through designated bank |
| 4 | Real Estate Agent | NRI property investment rules | NRIs can buy residential/commercial property. Agricultural: Restricted |
| 5 | Synthesizer | NRI investment blueprint | NRE FD (7%) + NRI MF SIP + Direct equity via PINS + SGB |

---

### USE CASE 20 — Digital Gold vs Physical Gold vs SGB vs Gold ETF
**Query:** *"Dhanteras pe gold khareedna hai. Digital gold, SGB, Gold ETF, ya physical gold — ek comparison chahiye."*

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | SGB Agent | SGB details | RBI-backed, 2.5% interest, tax-free maturity after 8 years, no storage cost |
| 2 | ETF Agent | Gold ETF | Real-time price, NSE-traded, 0.5% expense ratio, 20% LTCG with indexation |
| 3 | Digital Gold Agent | Digital gold (PayTm/PhonePe) | No SEBI regulation, high spread, no interest. Suitable for < ₹5,000 only. |
| 4 | Physical Gold | Physical gold analysis | Making charges 15-25%, GST 3%, storage risk. Premium for jewelry. |
| 5 | Synthesizer | Ranked recommendation | 1st: SGB (best for > 8 yr holding) | 2nd: Gold ETF (flexibility) | 3rd: Digital (small amount) | 4th: Physical (only jewelry) |

---

## 6. FINBHARAT AI — AGENT JSON INPUT/OUTPUT TEMPLATES

### Input Template — SIP Recommendation Agent
```json
{
  "agent_name": "sip_recommendation_agent",
  "user_profile": {
    "age": 28,
    "monthly_income_inr": 65000,
    "monthly_expenses_inr": 38000,
    "existing_sip_inr": 5000,
    "risk_appetite": "moderate",
    "investment_horizon_years": 15,
    "financial_goal": "retirement_corpus",
    "target_corpus_inr": 5000000
  }
}
```

### Output Template — SIP Recommendation Agent
```json
{
  "agent_name": "sip_recommendation_agent",
  "investable_monthly_inr": 22000,
  "required_sip_for_goal_inr": 14200,
  "recommended_allocation": [
    {"fund_category": "Nifty 50 Index Fund", "sip_inr": 6000, "risk": "Low-Moderate", "historical_cagr": "12.4%"},
    {"fund_category": "Flexi Cap Equity Fund", "sip_inr": 5000, "risk": "Moderate", "historical_cagr": "14.2%"},
    {"fund_category": "ELSS (Tax Saving)", "sip_inr": 2000, "risk": "Moderate", "historical_cagr": "13.8%", "80c_benefit": true},
    {"fund_category": "Short Duration Debt Fund", "sip_inr": 1200, "risk": "Low", "historical_cagr": "7.1%"}
  ],
  "projected_corpus_at_15_years_inr": 5650000,
  "tax_saved_via_elss_per_year_inr": 62400,
  "sources": ["AMFI India NAV", "ValueResearchOnline", "Morningstar India"],
  "timestamp": "2026-07-05T03:00:00Z"
}
```

---

### Input Template — Tax Optimizer Agent
```json
{
  "agent_name": "tax_optimizer_agent",
  "salary_details": {
    "gross_ctc_inr": 1800000,
    "hra_monthly_inr": 18000,
    "city": "Pune",
    "rent_paid_monthly_inr": 22000,
    "deductions": {
      "80c_investments_inr": 150000,
      "80d_health_insurance_inr": 25000,
      "nps_additional_80ccd_inr": 50000,
      "home_loan_interest_inr": 180000
    }
  },
  "tax_year": "FY2025-26"
}
```

### Output Template — Tax Optimizer Agent
```json
{
  "agent_name": "tax_optimizer_agent",
  "old_regime": {
    "taxable_income_inr": 1185000,
    "tax_liability_inr": 225750,
    "cess_4pct_inr": 9030,
    "total_tax_inr": 234780
  },
  "new_regime": {
    "taxable_income_inr": 1725000,
    "tax_liability_inr": 248750,
    "cess_4pct_inr": 9950,
    "total_tax_inr": 258700
  },
  "recommended_regime": "Old Regime",
  "tax_saved": 23920,
  "optimization_tips": [
    "Invest full ₹1.5L in 80C (currently optimal)",
    "Utilize NPS ₹50K additional deduction (80CCD) to save ₹15,450 more",
    "HRA benefit: ₹1,14,000 claimable (least of HRA, 40% salary, rent - 10% salary)"
  ],
  "sources": ["Income Tax India Portal", "ClearTax FY26 Slabs"],
  "timestamp": "2026-07-05T03:00:00Z"
}
```

---

## 7. DATA INGESTION PIPELINE (FINBHARAT AI)

```
RAW DATA INPUTS (India Finance)
│
├── RBI Website ─────────────► PDF/HTML Extractor ──► Qdrant (RBI Policy Index)
├── AMFI NAV Daily Feed ──────► CSV Parser ──────────► PostgreSQL (MF NAV Table)
├── SEBI Circulars ───────────► PDF Loader ──────────► Qdrant (SEBI Rules Index)
├── Income Tax Portal ────────► Web Scraper ─────────► PostgreSQL (Tax Slabs Table)
├── NSE/BSE Price Feed ───────► REST API ─────────────► InfluxDB (Equity Prices)
├── Moneycontrol MF Data ─────► REST Scrape ──────────► PostgreSQL (Fund Returns)
├── IRDAI Annual CSR Data ────► PDF OCR ─────────────► Qdrant (Insurance Index)
├── India Post Schemes ───────► Web Scraper ─────────► PostgreSQL (Scheme Rates Table)
├── BankBazaar Rate Feed ─────► Web Scraper ─────────► PostgreSQL (Loan Rates Table)
└── Tavily Live Search ───────► REST API ─────────────► Redis (Live Cache — 1 hr TTL)

RETRIEVAL LAYER
├── Qdrant: Semantic search (RBI policy, SEBI, IRDAI)
├── PostgreSQL: Structured queries (tax slabs, NAV, loan rates, scheme rates)
├── InfluxDB: Time-series queries (stock prices, AQI, interest rates)
└── Redis: Real-time cached responses (latest RBI rate, budget news)
```

---

## 8. FINBHARAT AI COMPLETE SYSTEM SUMMARY

| Dimension | Count / Detail |
|-----------|---------------|
| **Total Agents** | 35 (1 Meta-Supervisor + 34 Specialists) |
| **Agent Teams** | 12 Functional Teams |
| **Data Sources (URLs)** | 81 URLs across 11 India categories |
| **Vector Stores** | 4 (RBI/SEBI/IRDAI, MF, Insurance, Tax) |
| **Structured DBs** | PostgreSQL (rates, NAV, tax), InfluxDB (prices), Redis (cache) |
| **LLMs Supported** | Groq LLaMA 3, Gemini 2.5 Flash, Claude Sonnet |
| **Use Cases Documented** | 20 detailed end-to-end India financial scenarios |
| **Output Currency** | Always INR (Rupees, LPA, Lakhs, Crores) |
| **Regulatory Compliance** | SEBI, RBI, IRDAI, PFRDA, Income Tax Act |
| **Language Support** | Hindi + English (bilingual) |
| **Deployment Stack** | FastAPI + LangGraph + Docker + AWS Mumbai (ap-south-1) |
| **Evaluation** | LangSmith tracing + Ragas RAG evaluation + CIBIL data validation |
