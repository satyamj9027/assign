
# 1) Server binary मौजूद?
uvx jobspy-mcp --help

# 2) Claude Desktop
# \~/.config/claude/claude_desktop_config.json
{
  "mcpServers": {
    "jobspy": {
      "command": "uvx",
      "args": ["jobspy-mcp"]
    }
  }
}
python -jobspy
`jobspy-mcp` अकेला नहीं है। Hiring loop के लिए MCP को **4 layers** में सोचो — JobSpy सिर्फ **Board scrape** वाली परत है।

---

## Hierarchy (Talent Foreman + MCP)

```
Talent Foreman
 ├── Demand (jobs कहाँ खुली हैं)
 │    ├── jobspy-mcp              boards scrape (Naukri/Indeed/LinkedIn)
 │    ├── JobsPipe MCP            30+ ATS+boards, normalized
 │    ├── job-scout-mcp           Greenhouse/Lever/Ashby + HN + RemoteOK
 │    ├── openhire-mcp            ~120 career sites, US/EU/China
 │    └── USAJOBS / Adzuna        official keys
 ├── People (candidates कहाँ हैं)
 │    ├── github-talent-mcp       GitHub score + JD rank
 │    ├── github/github-mcp-server official repos/PRs/code
 │    ├── HeroHunt / SeekOut MCP  1B+ profiles (paid)
 │    └── LinkedIn MCP            session scrape — ToS risk
 ├── Pipeline (ATS अंदर)
 │    ├── Workable official MCP   38 tools
 │    ├── Greenhouse official     36 tools (Jun 2026 rollout)
 │    ├── Ashby community         ~66 tools
 │    └── Recruitee / Manatal / Zoho Recruit
 └── Outreach / Calendar
      ├── Gmail + Calendar MCP    (Resume-Filtering-Agent जैसा)
      └── Unipile / Fintalio      LinkedIn+email sequences
```

---

## 1) Demand — jobs खोजो (JobSpy के अलावा)

| MCP | Source | Key / ToS | India? | कब लो |
|---|---|---|---|---|
| **JobsPipe** | 30+ ATS + boards, dedup | Bearer; live `mcp.jobspipe.dev/mcp` | global | daily pipeline |
| **job-scout-mcp** | Greenhouse, Lever, Ashby, HN, RemoteOK | zero key | ATS-heavy firms | Staff roles, clean JSON |
| **openhire-mcp** | ~120 career sites + Beisen | no résumé upload | China+US+EU | AI/Infra radar |
| **jobs-mcp** (Ashishkosana) | US SWE ATS + new-grad | local | US only | US backend |
| **recruiting-jobs-mcp** | ATS + HN + hiring-signal | Apify token | company slugs | “कौन hire कर रहा है” |
| **@servation/job-search-mcp** | LinkedIn + 8 ATS, 0–100 fit score | `npx` | mixed | job-seeker triage |

JobsPipe connect:

```bash
claude mcp add --transport http jobspipe https://mcp.jobspipe.dev/mcp \
  --header "Authorization: Bearer jp_live_YOUR_KEY"
```

---

## 2) People — Staff GenAI + Java shortlist

**github-talent-mcp** — यही “repo stars + speaker-list” वाला tool है: `search_developers`, `get_developer_profile`, `get_repo_contributors`, `rank_candidates` vs JD। Claude/Cursor stdio।  
Repo: `carolinacherry/github-talent-mcp`

**Official GitHub MCP** (`github/github-mcp-server`, hosted + OAuth) — code/PR/issues; talent score नहीं, पर candidate के org repos पढ़ने के लिए चाहिए।

Paid people-search: **HeroHunt MCP**, **SeekOut MCP** — LinkedIn+GitHub index, Boolean नहीं, natural-language `people_search`।

**LinkedIn MCP** (`stickerdaniel/linkedin-mcp-server`, ~2k+ stars) — profiles/jobs/inbox, **browser session**। Powerful, **ToS + ban risk** — main account पर मत चलाओ।

---

## 3) Pipeline — company ATS (official)

| Vendor | Status | Tools | Note |
|---|---|---|---|
| **Workable** | live | 38 | हर plan पर free MCP |
| **Greenhouse** | Jun 2026 rollout | 36 | pipeline + governed writes |
| **Manatal / Zoho Recruit / Pinpoint** | live | 15+ | mid-market ATS |
| **Ashby / Lever** | mostly community | 50–66 | unofficial wrappers |
| **Indeed** | official beta | — | vendor list Jul 2026 |

ये JobSpy की जगह नहीं — ये **तुम्हारे requisition के अंदर** candidates move करते हैं।

---

## Practical pack — Bengaluru Staff GenAI + Java

एक Claude/Cursor config में सिर्फ ये चार:

```json
{
  "mcpServers": {
    "jobspy": { "command": "uvx", "args": ["jobspy-mcp"] },
    "github-talent": { "command": "uv", "args": ["run", "github-talent-mcp"] },
    "github": { "url": "https://api.githubcopilot.com/mcp/", "headers": { "Authorization": "Bearer ghp_..." } },
    "jobspipe": { "url": "https://mcp.jobspipe.dev/mcp", "headers": { "Authorization": "Bearer jp_live_..." } }
  }
}
```

Flow:
1. **JobsPipe / job-scout** → Stripe/OpenAI-style ATS पर “Staff + Java + LLM” JD  
2. **jobspy-mcp** → `naukri` + `indeed`, location `Bengaluru` (LinkedIn मत जोड़ो पहले)  
3. **github-talent-mcp** → `language:Java`, location India, `rank_candidates` उसी JD पर  
4. HITL shortlist → personalized mail  

Naukri volume JobSpy से; company truth ATS MCP से; people signal GitHub MCP से।

---

## मत मिलाओ

- Auto-apply bots (AIHawk) MCP नहीं, account ban।  
- Unofficial LinkedIn scrape production agent में नहीं।  
- 10 MCP एक साथ = context bloat; Foreman 3–4 tools रखे।

**एक लाइन:** Demand = JobsPipe / job-scout / JobSpy। People = github-talent-mcp। Pipeline = Workable/Greenhouse official। Outreach अलग Gmail MCP।
Code से live URL तक ये **एक chain** है। हर tool अलग layer है — Git code रखता है, Docker pack करता है, Kubernetes चलाता है।

### Big picture (एक नज़र)

```
Developer laptop
 └── Git repo (commits, branches)
      └── GitHub (remote + PR + Actions)
           └── CI: test → docker build → push image
                └── Registry (GHCR / Docker Hub / ECR)
                     └── CD / GitOps (Actions or Argo CD)
                          └── Kubernetes cluster
                               └── Deployment → ReplicaSet → Pod → Container
                                    └── Service → Ingress → Internet URL
```

---

### 1) Git hierarchy

Git = version control. Remote नहीं, सिर्फ history।

```
Repository
 ├── .git/                 (सारी history)
 ├── working tree          (तुम्हारी files)
 ├── staging (index)
 ├── commit
 │    └── parent commit(s)
 ├── branch                (pointer to a commit)
 │    ├── main / master
 │    ├── develop
 │    └── feature/*
 ├── tag                   (v1.2.0)
 └── remote                (origin → GitHub)
```

आम flow: `edit → git add → git commit → git push`

---

### 2) GitHub hierarchy

GitHub = Git + collaboration + CI।

```
GitHub Account / Org
 └── Repository
      ├── Default branch (main)
      ├── Other branches
      ├── Commit / SHA
      ├── Pull Request
      ├── Actions Workflow  (.github/workflows/*.yml)
      │    └── Job → Step (test, build, deploy)
      ├── Packages / GHCR   (container images)
      ├── Environments      (dev, staging, prod + secrets)
      ├── Secrets / Variables
      └── GitHub Deployments (optional record)
```

Git = history  
GitHub = वो history + PR review + automation

---

### 3) Docker hierarchy

Docker = app + runtime को **image** में pack करना।

```
Dockerfile
 └── Image  (layers: OS → deps → app)
      └── Tag   (myapp:1.4.2  या  myapp:sha-a1b2c3)
           └── Registry
                ├── Docker Hub
                ├── GHCR (ghcr.io)
                └── AWS ECR / GCR / ACR
                     └── Container (image का running instance)
                          ├── Process (PID 1)
                          ├── Filesystem (image layers + writable layer)
                          └── Ports / env / mounts
```

एक image से unlimited containers।  
Kubernetes **image को चलाता है**, Dockerfile को नहीं।

---

### 4) Kubernetes hierarchy

K8s = बहुत सारे containers को cluster पर manage करना।

```
Kubernetes Cluster
 ├── Control Plane     (API server, etcd, scheduler, controllers)
 └── Worker Node(s)    (kubelet + container runtime + kube-proxy)
      │
      ├── Namespace     (dev / staging / prod / team-a)
      │
      ├── Workloads
      │    ├── Deployment          (stateless app, rolling update)
      │    │    └── ReplicaSet     (N copies maintain करो)
      │    │         └── Pod       (smallest schedulable unit)
      │    │              └── Container(s)   ← Docker/OCI image
      │    ├── StatefulSet         (DB, Redis — stable name + disk)
      │    ├── DaemonSet           (हर node पर 1 pod — logs, agents)
      │    └── Job / CronJob
      │
      ├── Traffic
      │    ├── Service             (stable ClusterIP / DNS to pods)
      │    ├── Ingress / Gateway   (HTTP host/path → Service)
      │    └── NetworkPolicy
      │
      └── Config & storage
           ├── ConfigMap / Secret
           ├── PersistentVolume (cluster)
           └── PersistentVolumeClaim (namespace)
```

Controller chain:

**Deployment → ReplicaSet → Pod → Container on a Node**

Pod मर गया तो ReplicaSet नया बनाता है। Image change हुआ तो Deployment नया ReplicaSet बनाता है (rolling update)।


Official MCP Registry
 └── Directories: Glama · Smithery · PulseMCP · mcp.so
      └── Categories
           ├── Local IO          Filesystem, Git, Memory
           ├── Dev tools         GitHub, Playwright, Chrome DevTools, Context7, Sentry
           ├── Data              Postgres, Supabase, ClickHouse, Redis, BigQuery
           ├── Cloud             AWS / Azure / GCP, Cloudflare, K8s, Docker, Terraform
           ├── Search / Web      Brave, Exa, Tavily, Firecrawl, Fetch, Apify
           ├── Productivity      Notion, Linear, Jira/Rovo, Obsidian, Calendar
           ├── Comms             Slack, Gmail, Discord, Teams
           ├── Money / CRM       Stripe, HubSpot, Salesforce
           ├── Design            Figma
           ├── Automation        n8n MCP
           └── Verticals         Hiring (JobSpy, JobsPipe), Ads, Home Assistant…

बाजार में MCP अब “10 servers” नहीं — **Glama ~80k**, Official Registry + Smithery + PulseMCP मिलाकर **1 लाख+** listings। ज्यादातर weekend repos हैं। काम का नक्शा **category** से बनता है, नाम रटने से नहीं।

आज (30 Aug 2026) download king: **Chrome DevTools MCP** (~15L/week)। Stars वाले giants: **n8n**, **Browser Use**, **Context7**, official **Filesystem/GitHub**।

---

## Hierarchy (MCP market)

```
Official MCP Registry
 └── Directories: Glama · Smithery · PulseMCP · mcp.so
      └── Categories
           ├── Local IO          Filesystem, Git, Memory
           ├── Dev tools         GitHub, Playwright, Chrome DevTools, Context7, Sentry
           ├── Data              Postgres, Supabase, ClickHouse, Redis, BigQuery
           ├── Cloud             AWS / Azure / GCP, Cloudflare, K8s, Docker, Terraform
           ├── Search / Web      Brave, Exa, Tavily, Firecrawl, Fetch, Apify
           ├── Productivity      Notion, Linear, Jira/Rovo, Obsidian, Calendar
           ├── Comms             Slack, Gmail, Discord, Teams
           ├── Money / CRM       Stripe, HubSpot, Salesforce
           ├── Design            Figma
           ├── Automation        n8n MCP
           └── Verticals         Hiring (JobSpy, JobsPipe), Ads, Home Assistant…
```

खोजने के लिए खुद एक MCP है: **MCPfinder** — agent directories में server ढूँढकर install JSON देता है।

---

## Category-wise जो वास्तव में use होते हैं

### 1) Local / reference
| MCP | काम |
|---|---|
| **Filesystem** | allowed folders read/write |
| **Git** | local repo history |
| **Memory** | persistent entity graph |
| **Fetch / Sequential Thinking** | URL→text, step reasoning |

Starter kit यहीं से शुरू होता है।

### 2) Dev tools
| MCP | Maintainer | काम |
|---|---|---|
| **GitHub** | GitHub official, hosted OAuth | PRs, issues, Actions, code search |
| **Playwright** | Microsoft | browser बिना screenshot-vision |
| **Chrome DevTools** | Google | inspect, perf, DOM |
| **Context7** | Upstash | live library docs (hallucinated API कम) |
| **Sentry** | Sentry | errors, stack traces |
| **Linear / Atlassian Rovo** | vendors | issues + Jira/Confluence |

### 3) Databases
**Postgres MCP Pro** (read-only mode), **Supabase**, **ClickHouse**, **MongoDB**, **Redis**, **Neon**, **BigQuery**, **Qdrant** (vectors)। Production में हमेशा **read-only** पहले।

### 4) Cloud / infra
**AWS** (ECS सबसे downloaded cloud MCP), **Azure**, **GCP**, **Cloudflare**, **Kubernetes**, **Docker**, **Terraform**, **Vercel**।

### 5) Search + scrape
**Brave Search**, **Exa**, **Tavily**, **Firecrawl**, **Apify**, **Browser Use**, **Browserbase** (hosted browser)। JobSpy जैसा scrape इसी परिवार का cousin है।

### 6) Docs / PM / comms
**Notion** (`https://mcp.notion.com/mcp`), **Obsidian**, **Google Drive/Workspace**, **Slack**, **Gmail**, **Google Calendar**, **Asana**, **Airtable**।

### 7) Business
**Stripe** (payments), **HubSpot / Salesforce / Apollo** (CRM), **PostHog** (product analytics), **Ahrefs + Search Console + Google Ads MCP** (SEO/ads)।

### 8) Design + automation
**Figma Context MCP**, **n8n** (workflow को agent से चलाओ)।

### 9) Vertical (तुम्हारा hiring वाला कोना)
पहले वाली list: **jobspy-mcp**, **JobsPipe**, **job-scout-mcp**, **github-talent-mcp**, **Workable/Greenhouse official**, **HeroHunt/SeekOut**। ये general market का छोटा slice है।

---

## Practical — 2 packs, 6–7 MCP से ज़्यादा मत लगाओ

**Coder pack**  
Filesystem + GitHub + Context7 + Playwright + Postgres (RO) + Sentry  

**Talent Foreman pack**  
JobsPipe या job-scout + github-talent-mcp + GitHub official + Gmail + Calendar + Notion (JD/scorecards)

```json
{
  "mcpServers": {
    "filesystem": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/you/proj"] },
    "github": { "url": "https://api.githubcopilot.com/mcp/" },
    "context7": { "command": "npx", "args": ["-y", "@upstash/context7-mcp"] },
    "playwright": { "command": "npx", "args": ["-y", "@playwright/mcp"] }
  }
}
```

---

## चेतावनी (market की सच्चाई)

- 80k listings ≠ 80k production-ready। बहुत में **no auth / SSRF**।  
- Download volume **first-party** (Google, AWS, Azure, Chrome) के पास है।  
- हर MCP context window खाता है — 20 servers लगाना agent को मंद करता है।

Directories: [glama.ai](https://glama.ai) · [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) · PulseMCP · Smithery।

बताओ अगला कट किस vertical का चाहिए — **DB**, **cloud**, **browser**, या **comms** — उसी की install-ready shortlist दूँ।


2 मिनट की search के बाद: Glama पर **~80k servers / 85 categories** हैं। नीचे **hiring/dev के अलावा** वो areas हैं जहाँ MCP सच में अलग use-case खोलता है।

---

## Hierarchy (area → use-case → MCP)

```
Physical world
 ├── Home / IoT     Home Assistant, Hue, MQTT, 3D printer, ROS
 ├── Maps / weather OpenStreetMap, Google Maps, Open-Meteo, flood risk
Money
 ├── Markets        Alpha Vantage, Financial Datasets, FRED, FMP
 ├── Trade          Alpaca, MT5, Binance, Coinbase
 ├── Crypto/DeFi    CCXT, DexPaprika, Ensotrade
Law + science
 ├── Legal          RegIntel (41 jurisdictions), CourtListener
 ├── Papers         arXiv, PubMed, Semantic Scholar
Health / travel / shop
 ├── FHIR / forms   easydocforms (PHI बाहर)
 ├── Flights/hotels Booking, Airbnb aggregators, eSIM
 └── Shopify        products, orders, inventory
Create
 ├── 3D / games     Blender MCP, Unity, Unreal, Godot, Roblox
 ├── Music / video  Ableton, Spotify, YouTube transcript, Plex
 └── Reverse eng    Ghidra MCP
```

---

## 1) Finance & trading
| MCP | Use-case |
|---|---|
| **Alpha Vantage** `mcp.alphavantage.co` | stocks + forex + crypto + macros + news sentiment |
| **Financial Datasets** | income/balance/cashflow + price + news |
| **Alpaca / Public** | paper + live orders (options भी) |
| **FRED** | Fed rates, inflation, yield curve |
| **Ko Financial** | SEC, 13F, insider, Congress trades |
| **CCXT / Binance / Coinbase** | exchange data + crypto execution |
| **FundedNext** | prop-firm account rules / drawdown chat |

**Use-case:** “NVDA last 4Q margins vs Fed funds, then paper-buy Alpaca पर।” Agent data MCP से पढ़े, execution MCP अलग + HITL।

---

## 2) Home, IoT, factory
- **Home Assistant official** (HA 2025.2+) + community **ha-mcp** (~4.4k stars, 95+ tools) — lights, climate, locks, automations  
- Device-specific: **Philips Hue, Tuya, SmartThings, HomeKit**  
- Industrial: **MQTT, OPC UA, Siemens PLC, ThingsBoard**  
- Hobby: **ESP32/RPi GPIO, OctoPrint / 3D printer, ROS robots**  
- Sensor: **air-Q** indoor air quality

**Use-case:** “Good night” = lock + AC 24°C + lights off — एक prompt, कई tool calls। Destructive writes से पहले backup (ha-mcp policy)।

---

## 3) Maps, travel, local
- **OpenStreetMap MCP**, **Google Maps MCP** (geocode, directions, elevation)  
- **Open-Meteo / WeatherAPI**  
- **England flood-risk** (Environment Agency open data)  
- Travel connectors: hotels across Booking/Airbnb/Vrbo, walking tours, eSIM buy-in-chat  
- **discava** — local business search, no key

**Use-case:** Bengaluru interview trip — flights/hotel MCP + Calendar MCP + Maps directions।

---

## 4) Legal, research, health
- **RegIntel** — GDPR, DORA, SEC, FCA… 41 jurisdictions  
- **CourtListener / Federal Register** (US case law)  
- Academic: **arXiv + PubMed + Crossref** connectors  
- **2s-io/sdk** — एक MCP में patents, census, earthquakes, Wikipedia, papers (pay-per-call)  
- Health: **FHIR / Epic-Cerner** guides; **easydocforms** — PDF intake, PHI agent context में नहीं जाता  

**Use-case (तुम्हारा hiring loop):** Staff GenAI JD के लिए `search_arxiv("tool calling agents Java")` + GitHub-talent MCP।

---

## 5) E-commerce
**Shopify MCP Pro** — list/create products, orders, inventory, discounts, fulfillments, refunds।  
और: catalog search, Daraz-style regional scrapers, exception-handling (lost package) agents।

**Use-case:** “Low stock SKUs निकालो, 10% discount code बनाओ, Slack पर alert।”

---

## 6) Creative / games / media (सबसे “अलग”)
| MCP | Use-case |
|---|---|
| **Blender MCP** | prompt → 3D scene, physics, render |
| **Unity / Unreal / Godot MCP** | scene, NPC, scripts Editor के अंदर |
| **Roblox Studio official MCP** | built into Studio |
| **Ableton MCP** | music from prompts |
| **Spotify / Plex / Twitch / TMDB** | play, library, scores |
| **YouTube transcript MCP** | video को chat में लाओ |
| **Ghidra MCP** | reverse engineer binaries |
| **F1 FastF1 MCP** | race telemetry |

---

## Practical mini-packs (3 MCP, ज़्यादा नहीं)

**Quant research:** Alpha Vantage + FRED + Memory  
**Smart home:** ha-mcp + Calendar  
**Staff hiring + papers:** job-scout/JobsPipe + github-talent + arXiv/PubMed  
**Shop ops:** Shopify + Slack + Postgres RO  
**Creative:** Blender + Filesystem + YouTube transcript  

Directories: [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) (Legal / Gaming / IoT sections), [glama.ai](https://glama.ai) 85 categories, [Alpha Vantage MCP](https://mcp.alphavantage.co/)。

Trading/home पर **write tools = real money / real locks** — हमेशा confirm gate। अगला area बोलो (crypto execution, FHIR, या Blender) तो उसी की install config लिख दूँ।
---

### 5) End-to-end FLOW (code → URL)

```
1. Code
   laptop: feature branch
        ↓ git commit + push
2. GitHub
   PR opened → reviewers
        ↓ merge to main
3. GitHub Actions (CI)
   checkout
   unit tests
   docker build -t ghcr.io/org/app:sha-abc123
   docker push
        ↓
4. Registry
   image stored
        ↓
5. CD  (दो styles)

   A) Direct deploy
      Actions: kubectl set image deployment/app app=...:sha-abc123

   B) GitOps (better)
      Actions image tag को k8s-manifests repo में commit करे
      Argo CD Git देखे → cluster sync करे
        ↓
6. Kubernetes
   Deployment new ReplicaSet
   new Pods pull image
   readiness probe OK
   old Pods terminate
        ↓
7. Service
   selector से नए pods को traffic
        ↓
8. Ingress
   app.example.com → Service:80
        ↓
9. User browser
```





---

### 6) Objects का mapping (क्या किससे जुड़ा)

| Layer | Object | Example |
|--------|--------|---------|
| Source | Git commit | `a1b2c3d` |
| Remote | GitHub repo + PR | `org/api` |
| Package recipe | Dockerfile | `FROM node:22` |
| Artifact | Image tag | `ghcr.io/org/api:a1b2c3d` |
| Desired replicas | Deployment | `replicas: 3` |
| Actual copies | ReplicaSet | `api-7f8d9` |
| Running unit | Pod | `api-7f8d9-xk2m` |
| Process | Container | `api` |
| Machine | Node | `ip-10-0-11-25` |
| Stable network | Service | `api.prod.svc.cluster.local` |
| Public URL | Ingress | `https://api.example.com` |

---

### 7) Cloud से जोड़ो (पिछली hierarchy)

K8s cluster आमतौर AWS पर बैठता है:

```
AWS Account → Region → VPC → Subnet (private)
 └── EKS Node Group = EC2 instances
      └── kubelet
           └── Pod
                └── Container
```

Node की **private IP** EC2 की होती है।  
Pod की अपनी **cluster IP** अलग होती है।  
Internet Ingress → NLB/ALB → Node → Pod।

---

### 8) Mini example

Repo में:

- `src/` — application
- `Dockerfile`
- `k8s/deployment.yaml` — Deployment + Service
- `.github/workflows/ci.yml` — test, build, push

`deployment.yaml` का दिल:

```yaml
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: api
          image: ghcr.io/org/api:sha-abc123
```

Actions merge पर नया SHA tag push करता है → K8s उस image के 3 pods चलाता है।

---

**एक लाइन याद रखो:**  
Git इतिहास है, Docker डिब्बा है, Kubernetes डिब्बों का मैनेजर है, Deployment वो object है जो कहता है “हमेशा N healthy copies चलाओ”।


======================

नीचे **AWS default quotas** के साथ पूरी hierarchy है। संख्याएँ **एक Account × एक Region** की default limits हैं। ज्यादातर **Service Quotas** से बढ़ाई जा सकती हैं।

### Hierarchy + numbers

```
AWS Organization
 ├── Roots: 1
 ├── OUs: 2,000 max
 ├── OU nesting: 5 levels
 └── Accounts: default 10  (increase up to ~50,000)
      │
      └── AWS Account
           ├── Regions you can use: ~39 commercial
           │    └── AZs per Region: usually 3+  (example: ap-south-1a/b/c)
           │
           └── Per Region quotas
                ├── VPCs: 5 default  (increase → hundreds possible)
                ├── Internet Gateways: 5  (= VPCs quota; 1 IGW attach per VPC)
                ├── Egress-only IGW: 5
                ├── Elastic IPs: 5
                ├── Security Groups: 2,500
                ├── Network Interfaces (ENI): 5,000
                └── EC2 On-Demand: vCPU quota (new accounts often start ~5 vCPU)
                     │
                     └── Each VPC
                          ├── Subnets: 200
                          ├── IPv4 CIDRs: 5  (up to 50)
                          ├── IPv6 CIDRs: 5  (up to 50)
                          ├── Route tables: 200
                          ├── Routes per table: 50 default (up to 500)
                          ├── NACLs: 200
                          ├── NACL rules: 20 inbound + 20 outbound
                          ├── NAT Gateways per AZ: 5
                          ├── Regional NAT per VPC: 5
                          ├── Interface VPC endpoints: 50
                          ├── Gateway endpoints / Region: 20
                          ├── VPC peering (active): 50
                          └── 1 IGW attached
                               │
                               └── Each Subnet (lives in 1 AZ only)
                                    ├── IPs from CIDR
                                    │    /16 VPC  → 65,536 IPs theoretical
                                    │    /20 default subnet → ~4,096
                                    │    AWS reserves 5 IPs per subnet
                                    ├── 1 Route table association
                                    ├── 1 NACL association
                                    └── Resources
                                         ├── EC2 + ENI
                                         ├── SGs per ENI: 5
                                         ├── SG rules: 60 in + 60 out
                                         │    (SG count × rules ≤ 1,000)
                                         ├── Public / Elastic IP (optional)
                                         └── NAT GW only in public subnet
```

### Quick quota table

| Resource | Default | Scope | Increase? |
|----------|---------|--------|-----------|
| Accounts in Organization | 10 | Org | Yes (~50k) |
| OUs | 2,000 | Org | No |
| VPCs | **5** | Region | Yes |
| Subnets | **200** | VPC | Yes |
| Internet Gateway | 5 | Region | With VPC quota |
| IGW attached to one VPC | **1** | VPC | No |
| NAT Gateway | **5** | AZ | Yes |
| Elastic IP | **5** | Region | Yes |
| Security Groups | 2,500 | Region | Yes |
| SGs on one ENI/EC2 | **5** | ENI | Yes (max 16) |
| ENIs | 5,000 | Region | Yes |
| Route tables | 200 | VPC | Yes |
| NACLs | 200 | VPC | Yes |
| EC2 count | **vCPU quota**, not “N instances” | Region | Yes |

EC2 का limit “100 machines” जैसा नहीं है। New account पर Standard On-Demand अक्सर **5 vCPU** से शुरू होता है (तकरीबन 1–2 छोटे instances)। Quota बढ़ाकर सैकड़ों/हजारों instances चल सकते हैं — RAM/CPU type पर depend।

### Visual (same architecture, now with limits)

Public subnet → IGW  
Private subnet → NAT (public subnet में) → IGW  
NAT per AZ default max **5**





### Practical example (Mumbai `ap-south-1`, defaults)

एक नए account में बिना quota increase:

- **5 VPCs**
- हर VPC में **200 subnets** → theoretically 1,000 subnets / Region  
- 3 AZs × (1 public + 1 private) = **6 subnets** काफी हैं ज्यादातर apps के लिए  
- **5 Elastic IPs** पूरे Region के लिए  
- **5 NAT Gateways per AZ**  
- EC2: पहले छोटे T-class ही, जब तक vCPU quota न बढ़े  

Default VPC खुद बनाता है: `172.31.0.0/16` + हर AZ में `/20` subnet + 1 IGW।

### क्या hard limit है, क्या soft?

- **Hard-ish:** 1 IGW per VPC, subnet एक AZ में ही, 5 reserved IPs per subnet  
- **Soft (request से बढ़े):** VPCs, subnets, EIPs, NAT, SGs, ENI, EC2 vCPU, Org accounts  

Console: **Service Quotas** → VPC / EC2। Account और Region अलग-अलग quota रखते हैं।

चाहो तो अगला: “1 VPC में 3 AZ production layout कितने subnets/NAT/EIP लगेंगे” का exact recommended design लिख दूँ।


==============================

**हाँ, Redis में Vector DB capability है।**  
Plain Redis सिर्फ cache नहीं रहा — **Redis Query Engine** (पुराना नाम **RediSearch**) से ये **Vector Search** भी करता है। साथ में hierarchy भी साफ है।

### Redis Hierarchy (Proper Tree)

```
Redis Deployment
 ├── Instance / Node  (single Redis process)
 │    └── Logical Databases  (db0 … db15, SELECT command)
 │         └── Keys  (user:1001:profile  जैसी colon naming)
 │              └── Value = Data Structure
 │                   ├── String
 │                   ├── Hash
 │                   ├── List
 │                   ├── Set
 │                   ├── Sorted Set (ZSet)
 │                   ├── Stream
 │                   ├── JSON
 │                   └── Vector Set  (Redis 8)
 │
 └── Redis Cluster  (scale-out)
      └── 16,384 Hash Slots
           └── Shards  (Primary + Replicas)
```

**Note:** Mongo/Postgres जैसा Database → Schema → Table नहीं होता। Redis में **Key** ही namespace है।







---

### Redis में Vector कैसे काम करता है?

दो रास्ते हैं:

| Method | कब use करें | Commands |
|--------|-------------|----------|
| **Redis Query Engine** (`FT.SEARCH`) | Production RAG, hybrid search, filters | `FT.CREATE` + `KNN` |
| **Vector Sets** (Redis 8) | Simple similarity, lightweight | `VADD` + `VSIM` |

**Index types:** FLAT, **HNSW**, SVS-VAMANA  
**Metrics:** Cosine, L2 (Euclidean), Inner Product  
**Storage:** Hash या JSON documents के अंदर embedding field  
**Hybrid:** Vector + Full-text + metadata filter एक query में (`FT.HYBRID` Redis 8.4+)

### Example (Query Engine)

```bash
FT.CREATE docs-idx ON HASH PREFIX 1 doc: SCHEMA
  content TEXT
  embedding VECTOR HNSW 6 TYPE FLOAT32 DIM 1536 DISTANCE_METRIC COSINE

FT.SEARCH docs-idx "*=>[KNN 5 @embedding $vec AS score]"
  PARAMS 2 vec <binary_embedding>
  SORTBY score
```

### Free में कैसे चलाओ?

- **Self-host:** Redis Open Source / Redis Stack (Docker) — vector included  
- **Cloud Free:** Redis Cloud Essentials (~30 MB) — prototyping के लिए  
- Memory-heavy है: embeddings RAM में रहते हैं, बड़ा corpus हो तो Qdrant/pgvector सस्ता पड़ सकता है





### कब Redis Vector चुनें?

- Cache + Session + Vector **एक ही जगह** चाहिए  
- Ultra-low latency RAG / semantic cache  
- Already Redis use कर रहे हो  

**कब अलग Vector DB बेहतर:**  
बहुत बड़े billions-of-vectors scale, या cheap disk-based storage चाहिए → **Qdrant / Milvus / pgvector (Neon)**।

चाहो तो अगला: Redis vs Qdrant vs Neon का सीधा comparison बता दूँ।


==========================





1. File / blob से अपने आप (Azure indexer)
ये blob/SharePoint indexer अक्सर निकालता है:
Field
उदाहरण
metadata_storage_name
Resume_Amit_Java.pdf
metadata_storage_path
container + blob path
metadata_storage_size
bytes
metadata_storage_content_type
application/pdf
metadata_storage_last_modified
timestamp
metadata_storage_file_extension
.pdf
metadata_storage_content_md5
checksum
metadata_content_type
document MIME
metadata_author
PDF/DOC author
metadata_title
document title
metadata_creation_date / last_modified
file props
metadata_page_count / word_count
Office/PDF
metadata_language
अगर detect हो
ये file के अंदर के paragraphs नहीं — OS/Office header की properties।
2. तुम ख़ुद लगाते हो (सबसे ज़रूरी — RAG / Career)
Tenant + उत्पाद logic यहीं बैठती है:
Field
उदाहरण
काम
user_id / tenant_id
u1, acme-corp
ACL — preFilter हमेशा
session_id
sess_abc
इस chat का doc
doc_type
resume, jd, offer, policy
सिर्फ़ resumes खोजो
source
upload, gmail, drive
कहाँ से आया
status
indexing, ready, failed
agent तभी चले जब ready
year / as_of
2026
पुराना JD मत लाओ
country / city
IN, Bengaluru
labor market slice
role_family
backend, data
facet
seniority
mid, senior
filter
skills_tags
["java","spring"]
tags — exact collection filter
language
en, hi

pii_level
high
अलग index/policy
visibility
private, shared

chunk_index / parent_id
3, doc_99
parent-child RAG
page_number
2
citation
content_hash
sha256
dedupe
embedding_model
text-embedding-3
version pin
schema_version
v3
old chunks ignore
Career Orchestrator के लिए न्यूनतम:
user_id, doc_type, resume_doc_id, status, year, content_hash
3. “Description” / title — हाँ, लेकिन छोटा card
Field
क्या लिखो
क्या मत लिखो
title
Amit — Java Backend Resume
पूरा CV
description
एक लाइन: 4 yrs Spring, Kafka
सारे bullets
filename
original name
—
ये metadata fields हैं अगर अलग columns हो। अंदर का 3-page text content में रखो।
Description को:
filterable = exact पूरे string से काटना (कम useful)
searchable = नाम/short blurb पर keyword (अक्सर useful)
4. Business / compliance
classification: public, confidential
retention_until / ttl
legal_hold: bool
consent_version
created_by, uploaded_at
indexer_run_id

Algorithm
1. PARTITION BY से समूह काटो (optional) — हर dept अलग ranking
2. ORDER BY से समूह के अंदर sort करो
3. पहली पंक्ति rank = 1
4. अगली पंक्ति:
      same ORDER key as previous?
        हाँ → RANK/DENSE_RANK = वही नंबर
              ROW_NUMBER = +1 हमेशा
        नहीं →
              RANK       = (पिछली तक कितनी पंक्तियाँ) + 1   ← gap
              DENSE_RANK = पिछला rank + 1                  ← no gap
5. अगला partition पर rank फिर 1 से
सूत्र (एक partition में, 1-based):
\[
\begin{aligned}
\text{ROW\_NUMBER}(i) &= i \\
\text{RANK}(i) &= 1 + \#\{j : key_j \succ key_i\} \\
\text{DENSE\_RANK}(i) &= 1 + \#\{\text{distinct keys strictly before } i\}
\end{aligned}
\]

यहाँ \(key_j \succ key_i\) मतलब “\(j\) sorting में \(i\) से पहले / बेहतर”।
Visual (salary DESC)
name   salary
Ada    200
Bob    200
Cia    150
Dan    100
Eve    100
name
salary
ROW_NUMBER
RANK
DENSE_RANK
Ada
200
1
1
1
Bob
200
2
1
1
Cia
150
3
3 ← gap
2
Dan
100
4
4
3
Eve
100
5
4
3
दो first place → RANK तीसरे को 3 देता है (silver नहीं, कांस्य जैसा gap)
DENSE_RANK तीसरे को 2 देता है (कोई पद खाली नहीं)



Extracted Text — सभी Images

मैंने uploaded images से visible text extract किया है। कुछ screenshots में text blurry/angled है, इसलिए जहाँ exact wording स्पष्ट नहीं है वहाँ मैंने [unclear] रखा है।


---

1. gVisor Architecture

gVisor Architecture

Kubernetes
     ↓
containerd
     OCI
     ↓
runsc
     ↓
 ┌───────────────────────┐
 │       Sandbox         │
 │                       │
 │       Sentry          │ ←── 9P ──→ Gof er
 │                       │
 └───────────────────────┘
        ↓
   KVM/ptrace
        ↓
Host Linux Kernel

Visible labels:

gVisor Architecture

Kubernetes

containerd

OCI

runsc

Sandbox

Sentry

Gofer

9P

KVM/ptrace

User Kernel

Host Linux Kernel

gVisor



---

2. Agent Architecture / Workflow

Image में diagram का text:

User
  │
  │ Query
  ↓
Agent
  │
  │ 1. Invoke LLM
  ↓
Large Language
Model (LLM)
  │
  │ 2. Tool Selection
  │    Create Session
  ↓
┌───────────────────────────────┐
│ Code Interpreter              │
│ Shell                         │
│ File System                   │
│                               │
│ Code Interpreter Session      │
└───────────────────────────────┘
  │
  │ 3. Telemetry
  ↓
Observability

Tool Result
  ↓
Agent
  │
  │ Result
  ↓
User

Main labels:

User

Query

Agent

1. Invoke LLM

Large Language Model (LLM)

2. Tool Selection

Create Session

Code Interpreter

Shell

File System

Code Interpreter Session

3. Telemetry

Observability

4. Tool Result

Result



---

3. LangGraph — Graph Building

Visible code:

# ---------------------------- Graph Building ----------------------------

sql_agent_graph = StateGraph(AgentSchema)

# Nodes
sql_agent_graph.add_node(curate_ques, name="curate_ques")
sql_agent_graph.add_node(
    prompt_query_context,
    name="prompt_query_context"
)
sql_agent_graph.add_node(generate_sql, name="generate_sql")
sql_agent_graph.add_node(is_safe_sql, name="is_safe_sql")
sql_agent_graph.add_node(canceled_sql, name="canceled_sql")
sql_agent_graph.add_node(execute_sql, name="execute_sql")
sql_agent_graph.add_node(
    represent_final_answer,
    name="represent_final_answer"
)

# Edges
sql_agent_graph.add_edge(START, "curate_ques")
sql_agent_graph.add_edge("curate_ques", "prompt_query_context")
sql_agent_graph.add_edge("prompt_query_context", "generate_sql")
sql_agent_graph.add_edge("generate_sql", "is_safe_sql")

Terminal Error shown

File "c:\Data_Agent\agents\sql_analyst.py", line 188,
in is_safe_sql_edge

is_safe = state.is_safe_sql_response

File "C:\Data_Agent\.venv\Lib\site-packages\pydantic\main.py",
line 1042, in __getattr__

raise AttributeError(...)

AttributeError: 'AgentSchema' object has no attribute
'is_safe_sql_response'

Important error

AttributeError: 'AgentSchema' object has no attribute 'is_safe_sql_response'


---

4. Conditional Edge

Visible code:

# Conditional Edge Function
def is_safe_sql_edge(state: AgentSchema) -> str:
    is_safe = state.is_safe_sql_response

    if is_safe.lower() == "yes":
        return "execute_sql"

    else:
        return "canceled_sql"

sql_agent_graph.add_conditional_edges(
    "is_safe_sql",
    is_safe_sql_edge
)

# sql_agent_graph.add_edge("is_safe_sql", "execute_sql")
# sql_agent_graph.add_edge("is_safe_sql", "canceled_sql")

sql_agent_graph.add_edge("canceled_sql", END)
sql_agent_graph.add_edge("execute_sql", "represent_final_answer")
sql_agent_graph.add_edge("represent_final_answer", END)

Flow

START
  ↓
curate_ques
  ↓
prompt_query_context
  ↓
generate_sql
  ↓
is_safe_sql
  ↓
 ┌───────────────┴───────────────┐
 │                               │
Yes                             No
 │                               │
 ↓                               ↓
execute_sql                 canceled_sql
 │                               │
 ↓                               ↓
represent_final_answer          END
 │
 ↓
END


---

5. represent_final_answer() Node

Visible code:

# Represent the final answer Node
def represent_final_answer(state: AgentSchema) -> AgentSchema:

    execution_result = state.sql_query_execution_result
    curated_question = state.curated_ques

    llm = pick_llm("low")

    prompt = f"""
You are an SQL analyst agent. Your task is to provide a final answer to the user based on the
execution result of the SQL query and the user's original question. The final answer should be
concise, clear, and directly address the user's query. Avoid including any SQL code or technical
details in the final answer. The final answer should be in a user-friendly format that is easy to
understand. If the execution result is empty or does not provide a clear answer to the user's question, explain.

Here is the execution result: {execution_result} \n

Here is the user's original question: {curated_question}
"""

llm_response = llm.invoke(prompt).content  # Get the final answer from the LLM

state.final_answer = llm_response
state.messages = state.messages + [
    AIMessage(content=f"{llm_response}")
]  # Append the final answer to the messages

return state


---

6. AgentSchema — Pydantic Schema

Visible imports:

from pydantic import BaseModel, Field
from typing import Annotated, Literal
from operator import add

AgentSchema

class AgentSchema(BaseModel):

    messages: Annotated[list, add] = Field(
        ...,
        description="List of messages to be processed by the agent"
    )

    user_question: str = Field(
        ...,
        description="The original question asked by the user"
    )

    curated_ques: str = Field(
        ...,
        description="Curated user question"
    )

    prompt_query_context: str = Field(
        ...,
        description="A detailed prompt with SQL DB context that will help agent..."
    )

    generated_sql_query: str = Field(
        ...,
        description="The SQL query generated by the agent based on the curated..."
    )

    is_safe: Literal["Yes", "No"] = Field(
        ...,
        description="Indicates whether the generated SQL query is safe to..."
    )

    comments: str = Field(
        ...,
        description="Comments regarding the safety of the generated SQL query"
    )

    sql_query_execution_result: str = Field(
        ...,
        description="The result of executing the generated SQL query on..."
    )

    final_answer: str = Field(
        ...,
        description="The final answer generated by the agent based on the SQL query..."
    )

JudgeSchema

class JudgeSchema(BaseModel):

    answer: Literal["Yes", "No"] = Field(
        ...,
        description="Indicates whether the generated SQL query is safe to execute"
    )

    comments: str = Field(
        ...,
        description="Additional comments or feedback from the judge regarding the SQL query"
    )


---

7. execute_sql() Node

Visible code:

# Execute SQL Query Node
def execute_sql(state: AgentSchema) -> AgentSchema:

    sql_query = state.generated_sql_query

    conn_details = {
        "host": os.environ["host"],
        "port": os.environ["port"],
        "user": os.environ["user"],
        "password": os.environ["password"],
        "dbname": os.environ["dbname"]
    }

    obj = DatabaseUtil(conn_details)

    execution_result = obj.execute_sql(sql_query)
    # Execute the SQL query on the database

    state.sql_query_execution_result = execution_result

    return state


---

8. is_safe_sql() — SQL Security Judge

Visible code:

def is_safe_sql(state: AgentSchema) -> AgentSchema:

    sql_query = state.generated_sql_query

    llm = pick_llm("medium")

    llm_judge = llm.with_structured_output(JudgeSchema)

    prompt = f"""
You are an SQL Judge for data security. Your task is to determine whether the SQL query is
safe or not. The SQL query should only be used for data retrieval and should not modify the
database in any way. Neither the SQL query nor the prompt should contain any SQL commands that can modify the
database, such as INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, or any other commands that can change
the structure or content of the database. If the SQL query is safe, respond with "Yes" otherwise respond with
"No". Additionally, provide comments explaining your decision.

Here's the SQL query to evaluate:

{sql_query}
"""

response = llm_judge.invoke(prompt).model_dump()
# Get the structured output as a dictionary

state.is_safe_sql_response = response["answer"]

return state

SQL commands explicitly mentioned

INSERT

UPDATE

DELETE

DROP

ALTER

TRUNCATE

CREATE


Purpose:

> SQL query should be used only for data retrieval and should not modify the database.




---

9. generate_sql() Node

Visible code:

# Generate SQL Query Node
def generate_sql(state: AgentSchema) -> AgentSchema:

    prompt = state.prompt_query_context

    llm = pick_llm("medium")
    # Pick the appropriate LLM based on the level of the question

    generated_sql_query = llm.invoke(prompt)
    # Generate the SQL query using the LLM

    state.generated_sql_query = generated_sql_query

    return state


---

⚠️ Main Issue Visible in the Screenshots

आपके screenshots में schema और graph के बीच naming mismatch दिख रहा है।

AgentSchema में field है:

is_safe: Literal["Yes", "No"]

लेकिन conditional edge में लिखा है:

state.is_safe_sql_response

और is_safe_sql() में भी:

state.is_safe_sql_response = response["answer"]

इसलिए error आ रहा है:

AttributeError:
'AgentSchema' object has no attribute 'is_safe_sql_response'

Consistent solution

अगर schema में यही field रखना है:

is_safe: Literal["Yes", "No"]

तो code को consistently:

state.is_safe = response["answer"]

और:

def is_safe_sql_edge(state: AgentSchema) -> str:
    if state.is_safe.lower() == "yes":
        return "execute_sql"
    else:
        return "canceled_sql"

करना होगा।

REDDIS : LRU, LFU, CLUSTRING,IRIS and so on

Generative AI mein Search/Retrieval ke main types
Broadly, 7 important techniques ya families samajh sakte ho:
#
Technique
Basic idea
Best use
1
Keyword / Lexical Search
Exact words match karna
IDs, names, codes
2
TF-IDF
Important words ko higher weight
Traditional document search
3
BM25
Improved keyword relevance scoring
Search engines, RAG
4
Vector / Semantic Search
Meaning ke basis par similarity
Natural-language questions
5
Hybrid Search
Keyword + Vector combine
General-purpose RAG
6
Semantic Reranking
Retrieved results ko LLM/model se re-rank karna
Better relevance
7
Knowledge Graph / Graph Search
Entities aur relationships ke through retrieval
Multi-hop questions
Sparse retrieval mein TF-IDF/BM25 jaise methods aur dense retrieval mein embed

Memory types
Memory in Foundry Agent Service extracts and stores three types of long-term memory:
Memory type
Description
Retrieval guidance
Configuration
User profile memory
Durable user preferences and personal context, such as language preference, product defaults, or accessibility needs.
Retrieve near the beginning of each conversation to establish stable personalization context.
Enabled by default. To configure and disable, see Create a memory store.
Chat summary memory
Distilled summaries of prior conversation topics and threads.
Retrieve per turn using current conversation messages to surface relevant continuity context.
Enabled by default. To configure and disable, see Create a memory store.
Procedural memory
Reusable how-to routines and operating patterns inferred from prior interactions.
Retrieve when the user asks for a recurring workflow or task the agent has handled before.
Enabled by default. To configure and disable, see Create a memory store.
Memory management and retention
Memory in Foundry Agent Service supports fine-grained management and retention controls for production scenarios:
Item-level memory CRUD: Create, read, update, list, and delete individual memory items.
Store-level default retention: Set a default TTL (seconds) for memory entries created in a store.
Direct memory commands: Apply immediate remember-or-forget behavior when users explicitly request memory changes.
With these controls, you can balance personalization quality with privacy, compliance, and data lifecycle requirements.






Agent Governance = Policy + Identity + Access Control + Guardrails + Monitoring + Audit + Human Oversight + Accountability
उदाहरण के लिए अगर एक AI agent को company के Gmail, Salesforce और payment system का access है, तो governance पूछती है:
Agent की identity क्या है?
उसे कौन-कौन से systems access करने चाहिए?
क्या वह email भेज सकता है?
क्या वह पैसे transfer कर सकता है?
maximum transaction limit क्या है?
sensitive customer data पढ़ सकता है या नहीं?
हर action का audit log बनेगा?
risky action पर human approval चाहिए?
agent गलत काम करने लगे तो kill switch कहाँ है?




USA AI Agent Governance – Frameworks, Rules & Policies (in Points)
Federal / National Level
NIST AI Risk Management Framework (AI RMF) – Main voluntary framework used across USA for AI risk management
NIST AI Agent Standards Initiative (launched February 2026) – Specific standards for AI agents (identity, security, interoperability)
Agentic AI Risk-Management Standards Profile (UC Berkeley CLTC) – Special guidance for autonomous AI agents (complements NIST AI RMF)
Framework to Advance AI Governance and Risk Management in National Security – For AI use in national security systems
FedRAMP – Authorization program for cloud-based AI services used by government
Key Executive Orders
Executive Order 14179 (January 2025) – Removing Barriers to American Leadership in Artificial Intelligence
Executive Order 14365 (December 2025) – Ensuring a National Policy Framework for Artificial Intelligence
Executive Order 14409 (June 2026) – Promoting Advanced Artificial Intelligence Innovation and Security
Executive Order 14319 (2025) – Preventing Woke AI in the Federal Government
OMB Memoranda
OMB Memorandum M-25-21 – Accelerating Federal Use of AI through Innovation, Governance, and Public Trust
OMB Memorandum M-26-04 – Increasing Public Trust in Artificial Intelligence Through Unbiased AI Principles
Agency Guidance
CISA + NSA Joint Guidance – “Careful Adoption of Agentic AI Services” (May 2026)
NIST Cybersecurity Framework (CSF) AI Profile – Cybersecurity guidance applied to AI agents
Major State-Level Rules
Colorado – Automated Decision-Making Technology Act (ADMTA / SB 26-189)
Texas – Responsible Artificial Intelligence Governance Act (TRAIGA / HB 149)
California – SB 53 (Transparency in Frontier Artificial Intelligence Act) + AB 2013 + CPPA ADMT Regulations
New York City – Local Law 144 (Automated Employment Decision Tools)
Illinois – AI-related employment rules under Human Rights Act
Utah – AI Policy Act (disclosure requirements)
Other Commonly Used Standards
ISO/IEC 42001:2023 – International AI Management System Standard (widely followed in USA)
OWASP Top 10 for Agentic Applications – Security risks specific to AI agents
Most Important Ones for AI Agents:
NIST AI Risk Management Framework (AI RMF)
NIST AI Agent Standards Initiative
Agentic AI Risk-Management Standards Profile
CISA/NSA Joint Guidance on Agentic AI

---
Extracted Text

Types of Agents

1. Simple Agents


2. ReAct Agent


3. Plan & Execute Agent


4. Reflection Agent


5. Multi Agent System


6. Hierarchical Agent


7. Swarm / Collaborative Agents (A2A)



Sub Agents

Supervisor + Workers

Router + Specialists

Generator + Critic

Researcher + Writer + Editor


MCP Components

1. MCP Host — Agent / LLM application (Claude, Cursor, etc.)


2. MCP Client — Host के अंदर MCP Server से बात करने वाला component


3. MCP Server — Tools / Resources provider


4. Tools — Functions जिन्हें Agent call कर सकता है


5. Resources — Data sources (files, DB, APIs)


6. Prompts — Reusable prompt templates



Popular MCP Servers

1. Filesystem (Local files)


2. GitHub


3. Postgres / SQLite


4. Brave Search / Google Search


5. Slack (messages, channels)


6. Google Drive


7. Puppeteer / Browser


8. Memory


9. Playwright


10. BigQuery


11. Zapier


12. Figma


13. Salesforce


14. Azure MCP


15. Docker / Kubernetes MCP



Other MCP / Integrations

1. Obsidian (Personal Knowledge Base)


2. Telegram (Messaging)


3. Discord


4. Stripe


5. Shopify (E-commerce)


6. JIRA - Project


7. Confluence


8. Sentry

AgentSchema agent
Algorithm:
User question receive करें।
Question को curate करें।
DB schema/context जोड़ें।
SQL generate करें।
SQL safety check करें।
Safe होने पर execute करें।
Execution result को state में store करें।
Result को RAG/Evaluation layer में भेजें।

Final Result =
LLM(Code)
→ Validate
→ Execute
→ Test
→ Repair(if needed)
→ Execute
→ Explain

**✅ Definition**

**Chunking Strategies** are different methods of splitting documents into smaller pieces (chunks) before creating embeddings and storing them in a Vector Database.

Good chunking improves retrieval quality. Bad chunking causes important information to be split or lost.

---

### **Main Chunking Strategies**

Here are the most widely used chunking strategies:

| #  | Strategy                        | Description                                      | Best For                          |
|----|----------------------------------|--------------------------------------------------|-----------------------------------|
| 1  | **Fixed-Size Chunking**          | Split by fixed number of characters/tokens       | Simple documents                  |
| 2  | **Recursive Character Chunking** | Tries to split on logical separators (paragraphs, sentences) | Most general use case            |
| 3  | **Sentence-based Chunking**      | Splits by sentences                              | When sentence context is important|
| 4  | **Paragraph-based Chunking**     | Splits by paragraphs                             | Well-structured documents         |
| 5  | **Semantic Chunking**            | Splits based on meaning / topic change           | High-quality RAG                  |
| 6  | **Document Structure Chunking**  | Uses headings, sections, markdown structure      | PDFs, technical docs, reports     |
| 7  | **Sliding Window Chunking**      | Overlapping chunks                               | When context continuity is needed |
| 8  | **Agentic / LLM-based Chunking** | LLM decides the best split points                | Complex or highly unstructured data |
| 9  | **Parent-Child Chunking**        | Small chunks for retrieval + large parent for context | Advanced RAG systems             |
| 10 | **Token-based Chunking**         | Splits by exact token count                      | When model context is limited     |

---

### **Most Recommended Strategies (2026)**

1. **Recursive Character Text Splitter** → Best default choice
2. **Semantic Chunking** → Best quality
3. **Parent-Child (Hierarchical) Chunking** → Best for advanced RAG
4. **Structure-aware Chunking** → Best for PDFs and reports

---

### **Important Keywords**
**Chunking Strategy**, **Fixed-Size Chunking**, **Recursive Character Splitting**, **Semantic Chunking**, **Sliding Window**, **Parent-Child Chunking**, **Overlap**, **Chunk Size**, **Chunk Overlap**

---

### **Quick Code Examples**

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter
)

text = "Your long document text here..."

# 1. Fixed Size
fixed_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# 2. Recursive (Most Popular)
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# 3. Token-based
token_splitter = TokenTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = recursive_splitter.split_text(text)
```

---

### **How to Choose Chunk Size**

| Use Case                     | Recommended Chunk Size | Overlap     |
|-----------------------------|------------------------|-------------|
| General documents           | 500 – 1000 characters  | 10–20%      |
| Technical / Code heavy      | 300 – 600 tokens       | 50–100      |
| Semantic / High accuracy    | 400 – 800 characters   | 100–200     |
| Parent-Child                | Small: 200, Parent: 1500| -           |

---

### **Summary**

There are **around 8–10 main chunking strategies**.  

In practice, most production systems use one of these three:
- **Recursive Character Chunking** (default & reliable)
- **Semantic Chunking** (higher quality)
- **Parent-Child Chunking** (best advanced technique)

---

**Would you like me to show:**
1. Full comparison with code for the top 4 strategies?
2. Semantic Chunking implementation?
3. Parent-Child Chunking example?


---
---

Main Whitespace-Based Chunking Techniques
Technique
How it works
When to use
Simple Whitespace Split
Splits only on spaces
Very basic / token-like splitting
Newline-based Chunking
Prefers splitting on \n and \n\n
Documents with clear paragraphs
Recursive Whitespace Chunking
Tries multiple whitespace separators in order
Most recommended default
Whitespace + Overlap
Adds overlapping characters/tokens
Preserves context across chunks
Custom Separator List
You define priority of whitespace separators
Fine-tuned control
Recommended Configuration (Most Common)
separators = [
    "\n\n",   # Double newline (paragraphs) - highest priority
    "\n",     # Single newline
    ". ",     # Sentence end + space
    " ",      # Single space
    ""        # Character level (last resort)
]



Typical good settings:
chunk_size: 500 – 1000 characters (or 300–800 tokens)
chunk_overlap: 10–20% of chunk_size (usually 50–200)
length_function: len (characters) or token counter

मार्केट में open-source और enterprise स्तर के कई बेहतरीन LLM Gateways उपलब्ध हैं:
 * LiteLLM: ओपन-सोर्स (MIT लाइसेंस), सबसे लोकप्रिय और स्व-होस्ट (Self-host) करने के लिए बेहतरीन। यह 100+ से ज्यादा प्रोवाइडर्स को सपोर्ट करता है।
 * OpenRouter: ज़ीरो-ऑप्स (Managed) सर्विस। बिना किसी इंफ्रास्ट्रक्चर सेटअप के एक ही API कुंजी से सैकड़ों मॉडल्स एक्सेस करने के लिए बेस्ट।
 * Portkey: एंटरप्राइज गवर्नेंस, गार्डरेल्स, प्रॉम्प्ट मैनेजमेंट और ऑब्जर्वेबिलिटी (Observability) के लिए।
 * Kong AI Gateway: अगर आप पहले से Kong API Gateway का इस्तेमाल कर रहे हैं, तो यह एंटरप्राइज AI ट्रैफिक मैनेज करने के लिए सबसे उपयुक्त है।
 * Cloudflare AI Gateway: क्लाउडफ्लेयर इकोसिस्टम का उपयोग करने वाले ऐप्स के लिएCaching और एनालिटिक्स मैनेज करने का सबसे आसान विकल्प।
 * Helicone / Bifrost: हाई-परफॉरमेंस, कम लेटेंसी (Low-latency) और ऑब्जर्वेबिलिटी-फर्स्ट गेटवे के लिए जाने जाते हैं।





Components:

Q

A

Brain

Orchestrator

Tools.

Memory

Supervisor

Goal Interpretation

Planning

Reasoning

Tool Selection

Task Sequencing

Conditional Routing

Retry Logic

Looping & Iteration

Delegation

External Actions

Knowledge Base Access

Short-Term Memory

Long-Term Memory

State Tracking

Approval Requests (HITL)

Guardrails Enforcement

Edge Case Escalation

पन्ने पर लिखा सब टेक्स्ट, जितना पढ़ा जा सका — इलाकेवार। कुछ जगह स्याही ओवरलैप है, वे `?` से मार्क हैं।

---

## ऊपर बाएँ — RAG लिस्ट (1–18)

**RAG** (शीर्ष पर आधा कटा)

1. Standard RAG — FAQ Bot  
2. Agentic RAG — Personal Assistant  
3. Graph RAG — medical diagnosis  
4. Modular RAG — Enterprise  
5. Memory Augmented RAG — Chatbot  
6. Multi-modal RAG — stock updates  
7. Federated RAG (Privacy maintain) — multi Org. data  
8. Streaming RAG — Live data (stock updates)  
9. OD & RA RAG (Open Domain RA) — General knowledge (Search Engine)  
10. Contextual Retrieval RAG — Conversations (Customer support)  
11. Enhanced RAG — Domain Specific (Legal / medical)  
12. Domain-Specific RAG  
13. Hybrid RAG (Hypothetical Document Embeddings) — E-commerce  
14. *(नंबर 14 लाइनों में मेट्रिक्स से मिल गया)*  
15. Hybrid? (Complex Queries)  
16. Recursive / MultiStep RAG (ReAct?) — Education  
17. CRAG (Corrective RAG) — Critical / healthcare  
18. Speculative RAG  

17–18 के पास ब्रैकेट:  
`(Education tutorials)`  
`(complex research)`

बाएँ किनारे आधा कटा: `context?` / `token embedding?`

---

## बीच में — मेट्रिक्स (लिस्ट के ऊपर लिखा)

**Accuracy = (TP + TN) / (TP + TN + FP + FN)**

**Confusion Matrix**

**F1 Score = 2 × Precision × Recall / (Precision + Recall)**

कैंसर उदाहरण:

- Total Patient? = 100?  
- Actual Cancer / Predicted  
- Pred Cancer | No Cancer  
- Actual Cancer: **8 TP**, **2 FN**  
- Actual No Cancer: **2 FP**, **90? TN**  
- Accuracy = 98/100? = **99.6%?** *(अंक धुंधले: 8+90+?)*

---

## दाएँ ऊपर — Transformer

**Transformer**  
2017 — Attention Is All You Need  
with parallel processing (RNN)  
Long-range dependencies (LSTM) short?

पाइपलाइन:

- Input Text  
- ↓ Tokenization — Tokens  
- ↓ Embedding Layer → Vector Represent.  
- ↓ Positional Encoding (Position Info Add)  
- ↓ Encoder Block (N times)  
- ↓ Decoder Block (N times)  
- ↓ Linear Layer (Logits)  
- ↓ Softmax → Probabilities  
- Output Text  

---

## दाएँ मध्य — छोटे मॉडल / “install transformers”

1. DistilBERT → 66 M Params  
2. T5-small (Google T5) — 60 M Params  
   Encoder–Decoder both  
   Translation, summarization  
3. All-MiniLM-L6-v2 — 22 M  
   (Sentence-transformers)  
4. Gemma-2B (Google Gemma-2B)  
   → Chat, text generation  
5. Phi-3.5-mini (Microsoft Phi-3.5-mini-instruct)  
6. Qwen 2.5-VL-1.7?B  
   Vision-language  
7. SmolLM-1.7B  
   Hugging Face  
8. Stable Diffusion 1.5 B?  
   (Text + image)  
9. BERT, GPT  
   Encoder / Decoder  
10. Qwen 2.5-Coder-1.5B  
    Code completion  
11. Whisper — S… *(कटा: Speech?)*

---

## नीचे बाएँ — MCP

**MCP (Model Context Protocol)**

transport 3 types exist:

1. **stdio** (Standard Input/Output) → local server  
2. **SSE** (Server-Sent Events, useful for streaming)  
3. **Streamable HTTP** (HTTP based, good for multipurpose remote server)

**Atlassian Rovo MCP →**

**Read operations →**  
- Jira-search  
- jira-get-issue  
- jira-get-all-projects  
- jira-get-project-issues?  
- jira-get-board-issues?  

**Write operations →**  
- jira-create-issue  
- jira-update-issue *(कटा)*

पास में: `jira-sprint`, `jira-epic?`

**PII (Personal Information)**  
Session, Guardrails

---

## नीचे मध्य — NLP बॉक्स

from transformers import  
Autotokenizer, pipeline  
CausalLM? torch  

- NLP — Natural  
- RNN — Recurrent Neural Network  
- CNN — Convolutional  
- LSTM — Long-term memory? / Long Short-Term Memory  
- GRU —  
- ReLU  
- (Image)  
- Attention improved version  

---
```
AGENTS  (paper list)

(1)  Simple Reflex Agent        — Alerts / filters
(2)  Model-based Agent          — Stateful chat / inventory
(3)  Goal-based Agent           — Trip / career plan
(4)  Utility-based Agent        — Salary vs COL vs WLB
(5)  Learning Agent             — Recommendations
(6)  Hybrid Agent               — Reflex + planner (support bot)

(7)  Conversational Agent       — FAQ Bot
(8)  Tool-use Agent             — Personal Assistant
(9)  ReAct Agent                — Multi-step helpdesk
(10) Plan-and-Execute Agent     — Education / research
(11) Reflexion Agent            — Self-correct tutor
(12) Speculative / ToT Agent    — Score A, B, C → best
(13) RAG Agent                  — Knowledge base Q&A
(14) Agentic RAG Agent          — Docs + tools assistant
(15) Graph Agent                — Medical diagnosis
(16) Memory Agent               — Long-run chatbot
(17) Multimodal Agent           — Stock charts + news
(18) Streaming Agent            — Live market data
(19) Federated Agent            — Multi-org, privacy
(20) Router Agent               — Customer support triage
(21) Domain Specialist Agent    — Legal / medical / tax
(22) Coding Agent               — Repo + tests
(23) Research Agent             — Open-domain search
(24) Computer-use Agent         — Browser / forms
(25) Voice Agent                — Mock interview
(26) Workflow / Graph Agent     — Enterprise SOP
(27) Guardrail / QA Agent       — Fact-check (healthcare)
(28) HITL Agent                 — High-stakes approval
(29) Orchestrator Agent         — Route to specialist teams
(30) Multi-agent (swarm)        — Parallel research team
```

```
RAG  →  AGENT   (same use-case)

Standard RAG              →  Conversational / RAG Agent     — FAQ Bot
Agentic RAG               →  Agentic RAG / Tool-use         — Personal Assistant
Graph RAG                 →  Graph Agent                    — Medical diagnosis
Modular RAG               →  Workflow + workers             — Enterprise
Memory Augmented RAG      →  Memory Agent                   — Chatbot
Multi-modal RAG           →  Multimodal Agent               — Stock updates
Federated RAG             →  Federated Agent                — Multi-org data
Streaming RAG             →  Streaming Agent                — Live data
Open-Domain RAG           →  Research Agent                 — Search engine
Contextual Retrieval RAG  →  Session / Contextual Agent     — Customer support
Enhanced / Domain RAG     →  Domain Specialist              — Legal / medical
Hybrid RAG (HyDE)         →  Hybrid / Utility Agent         — E-commerce
Recursive / MultiStep RAG →  ReAct + Plan-and-Execute       — Education
CRAG                      →  Reflexion / QA Agent           — Critical healthcare
Speculative RAG           →  Speculative / ToT Agent        — Select best plan
```

```
MULTI-AGENT SHAPES

(1) Supervisor–Worker     — boss routes, specialists do
(2) Hierarchical          — high / mid / low layers
(3) Sequential pipeline   — A → B → C
(4) Parallel scatter      — many at once, then merge
(5) Peer / debate         — agents argue, then vote
(6) Maker–Checker         — writer + critic
```


DAG ( Directed Acyclic Graph) :

START
  ↓
curate_ques
  ↓
prompt_query_context
  ↓
generate_sql
  ↓
is_safe_sql
  ↓
 ┌───────────────┐
 │               │
Yes             No
 │               │
 ↓               ↓
execute_sql   canceled_sql
 │               │
 ↓               ↓
represent_final  END
 │
 ↓
END
• Loop Engineering

• Harness Engineering

• MCP A2A

• A2P

• Context Engineering

• Prompt Model

•  model Armor

• Prompt Techniques

• Searching Strategy

• MCP Server and MCP Client
Context Engineering Details:

• Background information required for AI

• Helps AI understand the scenario
• Loop Engineering

• Harness Engineering

• MCP A2A

• AP2

• Context Engineering

• Prompt Model

• Model Armor

• Prompt Techniques

• Searching Strategy

• MCP Server and MCP Client

Context Engineering & Prompt Engineering Details:


Content Filters, Prompt Shields, Protected Material Detection aur Groundedness Detection


• Prompt Tech: Systematic design of prompts for LLMs.

• Prompt Template: Reusable structure with placeholders (Role, Task, Context, Output Format, Constraints).

• Prompt Techniques:

  • Zero-shot (Direct task)

  • Few-shot (Examples based)

  • Chain-of-Thought / CoT (Step-by-step reasoning)

  • Role Prompting (Persona based)

  • ReAct (Reasoning + Action/Tools)

  • Self-Consistency (Majority voting)

  • Tree of Thoughts (Branching reasoning)

• Core Components: Role + Task + Context + Format + Constraints
Context Window Includes:

• System Instructions / Persona

• User Input / Prompt

• Conversation History / Chat Memory

• External Context / RAG Documents

• Available Tools / Function Schemas

• Model Output / Tool Responses
Agent Skill
(skill.md)
• Role prompting (Writing, analysis, code review): Assign the model an expert persona before the task • Chain-of-thought (Math, reasoning, multi-step problems): Ask it to show its reasoning process before answering • Few-shot prompting (Formatting, tone matching, repetitive tasks): Provide 2-3 examples before the task • System prompts (Consistent output across sessions): Set permanent rules, context, and format instructions • Sandwich method (Long, detailed tasks): Restate the core request at top and bottom of prompt • Decomposition (Complex multi-part projects): Break one big task into a sequence of smaller prompts • Negative constraints (Output quality control): Tell it explicitly what to exclude or avoid • Self-critique loop (High-stakes final drafts): Ask the model to review and improve its own output
---

Guardrails, Model Armor & Agent Model Armor Overview

1. Guardrails Kaise Likhte Hain?

• Methods:

  • Custom: Regex + Rules + Classifiers (Full control, low cost, high maintenance).

  • Third-party Libraries: Guardrails AI, NeMo Guardrails, Llama Guard (Ready-made, powerful).

  • Managed Services: Google Model Armor, AWS Bedrock Guardrails, Azure Content Safety (Scalable, easy, vendor lock-in).

• Defense-in-depth Approach: Regex/Keywords (fast layer) + ML Classifiers (Llama Guard/Prompt Guard) + LLM-as-a-Judge (advanced detection).

2. Input vs Output Guardrails

• Input Guardrails (Pre-LLM): Prompt Injection, Jailbreak, PII, Toxic content, Off-topic inputs ko rokta hai.

• Output Guardrails (Post-LLM): Hallucination, Toxic responses, Sensitive Data leakage, Wrong formats ko filter/mask karta hai.

3. Model Armor (Google Cloud)

• Google ka enterprise-grade managed security service.

• Screen karta hai prompts aur responses dono ko (Injection, PII, Harmful content, Malicious URLs).

• Model-agnostic security + compliance platform.

4. Agent Model Armor / Agent Guardrails

Agents multi-step tools execution karte hain, isliye inme extra security layers hoti hain:

• Tool Permission Control: Kis tool ko access dena hai.

• Action / Scope Guard: Agent ko boundary ke andar rakhna.

• Budget / Rate Limiting: API execution costs aur limits control karna.

• Runtime Policy Enforcement & Audit Logging: Har action step par policy check aur tracing.

• Tools/Services: AgentArmor, LlamaFirewall, Google Model Armor integration.
---

NeMo Guardrails & Custom Guardrails Overview

1. NeMo Guardrails Availability

• Free & Open Source: Apache 2.0 license, NVIDIA dwara maintain kiya gaya.

• Commercial aur personal projects dono me bina kisi fee ke usable.

2. Key Guardrails Frameworks Comparison

• NeMo Guardrails: Open Source (Apache 2.0) - Dialog flow, Topic control, Agent execution.

• Guardrails AI: Open Source (Apache 2.0) - Output validation, Structured data validation.

• Llama Guard (Meta): Open Source (Llama License) - Input/Output Safety classification.

• LLM Guard: Open Source (MIT) - PII, Toxicity, Prompt Injection scanner.

• Managed Services (Paid): Google Model Armor, AWS Bedrock Guardrails, Azure Content Safety.

3. Custom Guardrails Building Options

• NeMo Custom Rails: Colang (DSL) me Input, Output, Dialog, Retrieval, aur Execution rails.

• Guardrails AI: Custom Python validators.

• From Scratch: Custom Regex + ML Classifiers + LLM-as-a-Judge API pipeline.

4. Guardrails Deployment & Reusability (MCP-like)

• Microservices, FastAPI/HTTP servers (`nemoguardrails server`), Docker, aur Kubernetes Helm charts ke through deploy karke kisi bhi application (Python, Node, Go) se consumption possible.

5. Supported Guardrails Strategies & NeMo Rail Types

• Supported Policies: Security (Jailbreak, Injection), Compliance (PII Masking), Content Safety (Toxicity), Topic Control, Business Rules, Output Formats, Agent Tool Control.

• NeMo 5 Rail Types:

  1. Input Rails (User prompt check)

  2. Dialog Rails (Conversation flow control)

  3. Retrieval Rails (RAG content check)

  4. Execution Rails (Tool/Action permissions for Agents)

  5. Output Rails (LLM response check)


, Prompt Injection, Data Leakage, Malicious URLs
Prompt Casing

• XML / HTML Tags Casing: `<user_input>...</user_input>`

• Markdown Block Casing: `Triple Backticks`

• JSON Wrapper Casing: Pass input in structured JSON format

Prompt Caching

• Caching System Prompts: Store frequently used system instructions or context in the cache to reduce latency and API costs.

• Cache Time-to-Live (TTL): Define appropriate expiration times for the cached context to balance freshness and performance.

• Incremental Caching: Cache only the static parts of your prompt and append dynamic user inputs to maximize cache hits.
Agent Caching

• Definition: Techniques to reduce latency and save API costs by caching LLM calls, tool results, and context.

• Types of Caching:

  • Prompt / Context Caching: Caches static instructions/system prompts to avoid resending large context.

  • Semantic Caching: Uses vector embeddings to return cached responses for semantically similar queries.

  • Tool Result Caching: Caches output from external APIs or tool calls.

  • Plan / Intermediate Result Caching: Caches intermediate DAG results in multi-agent workflows.

• Benefits: Cuts API cost by 40–80% and improves latency by 13–65%.

• Google ADK Integration: Built-in support using `ContextCacheConfig` (min_tokens, ttl_seconds, cache_intervals) and Redis integration for semantic caching.

• Advanced Techniques: Workload-Aware Caching, Agentic Plan Caching, and Keepalive strategies.


Tool Poisoning

• Definition: Security attack in AI Agents where a tool sends malicious/manipulated data back to the agent, contaminating the context and altering decisions.

• Key Concepts: Tool Output Poisoning, Indirect Prompt Injection, Context Contamination, Agent Hijacking.

• Root Causes: Compromised tools/APIs, malicious third-party developers, lack of output validation, supply chain attacks, and data source poisoning.

• Impact: Incorrect reasoning/decisions, sensitive data leakage, execution of unauthorized actions, and propagation of poison across multi-agent systems.

• Mitigation / Prevention:

  • Validate & sanitize tool outputs.

  • Strict schema validation.

  • Principle of least privilege for tool permissions.

  • Human-in-the-loop (HITL) for sensitive operations.

  • Robust logging and monitoring.
Cost & Latency Management in AI Agents

• Core Problems: High token usage increases costs, while excessive LLM calls and context sizes increase latency.

• Key Concepts: Token Optimization, Model Routing, Prompt/Semantic Caching, Context Window Management, Parallel Tool Calling, Streaming.

• Optimization Techniques:

  • Context Minimization: Summarize history, send only relevant data, and keep prompts clear/concise.

  • Model Routing: Use lightweight/cheaper models (e.g., Flash, Mini, Haiku) for simple tasks/intent classification, and large models only for complex reasoning.

  • Caching Strategies: Apply Exact Caching, Semantic Caching (for similar queries), and Prompt Caching (for static system prompts).

  • Agent Design Controls: Set max steps/recursion limits, implement early stopping, optimize tool calls, and use sub-agents with restricted context.

  • Latency Improvements: Enable streaming for fast TTFT (Time-To-First-Token) and leverage parallel tool execution.

• Monitoring & Metrics: Track token usage, cost per successful task, and set cost alerts using observability tools (LangSmith, Phoenix, Helicone).
AI Evaluation Methods (AI Agents / LLM Systems)

• Definition: Process to evaluate AI Agent/LLM System correctness, assessing final answer and full Trajectory (decisions, tool calls, reasoning).

• Major Evaluation Methods:

  • Task Success Rate (TSR): End-to-end completion rate (Pass/Fail or score-based).

  • Trajectory Evaluation: Verifying steps, tool calls, loop prevention, and comparing with reference trajectory.

  • Tool Call Accuracy: Tool selection, argument accuracy, and output interpretation.

  • LLM-as-a-Judge: Evaluates outputs/trajectories using strong LLMs & Rubrics (Correctness, Faithfulness, Helpfulness).

  • Human Evaluation: Manual review for edge cases and high-reliability production feedback.

  • Automated / Code Metrics: Deterministic checks via Unit tests, Regex, Exact match.

  • RAG-Specific Metrics: Faithfulness, Context Precision/Recall, Answer Relevancy.

  • Cost & Performance Metrics: Latency, Token Usage/Cost, Tool Call count, Error Rate.

• Evaluation Types:

  • Offline Evaluation: Done during development on datasets to catch regressions.

  • Online Evaluation: Real-time production monitoring and user feedback.

• Popular Frameworks: LangSmith, AgentEvals, DeepEval, Ragas, Braintrust, Phoenix (Arize).

• Best Practices: Evaluate trajectory along with final output, use a combination of multiple evaluators, and run continuous production monitoring.
MCP Server Connection Mechanisms

• Definition: Connection between MCP Client (App) and MCP Server established over a Transport Layer using JSON-RPC protocol.

• Key Transports:

  • stdio Transport (Local): Client launches server as a subprocess; communicates via `stdin`/`stdout`. Preferred for local tools (Claude Desktop, Cursor).

  • Streamable HTTP / SSE Transport (Remote): Client connects to remote/cloud servers using HTTP POST / SSE streams.

• Connection Handshake & Lifecycle:

  1. Transport Selection (`stdio` or `HTTP`).

  2. Connection Establishment.

  3. Initialize Handshake: Protocol version negotiation & capabilities exchange.

  4. Tool Discovery: Client calls `tools/list` to fetch available tools.

  5. Execution: Client invokes required tools via session.

• Transport Recommendations:

  • Local / Personal Tools → stdio

  • Remote / Cloud / Multi-user → Streamable HTTP
Contract Mechanism in Agent Architecture

• Definition: Interface, input-output rules, and expectations defined between Agent, Tools, State, and other Agents to ensure strict data formatting, reliability, and error reduction.

• Key Contract Mechanisms:

  • Tool Schema / Function Calling Contract: Defines tool names, descriptions, and parameter requirements via JSON Schema.

  • State Contract: Uses Pydantic or TypedDict to enforce type safety and structured data flow across Agent nodes.

  • Structured Output Contract: Enforces LLM final answers to adhere strictly to specified JSON/Pydantic schemas.

  • Inter-Agent Message Contract: Defines explicit message formats and protocols for Agent-to-Agent (A2A) communication in multi-agent systems.

  • Design-by-Contract: Implements pre-conditions, post-conditions, and state invariants.

• Preferred Modern Stack: `Tool Schema (JSON Schema) + State Contract (Pydantic) + Structured Output`.

• Key Benefits: Minimizes hallucinated tool calls, prevents runtime crashes/type errors, improves production reliability, and simplifies debugging.
ADK Telemetry Overview

• Definition: Built-in Observability system for Google's Agent Development Kit (ADK) based on OpenTelemetry (OTel). Records, visualizes, and debugs full AI Agent lifecycles via Traces, Metrics, and Logs.

• Key Components: Traces (Distributed Tracing), Metrics (Tokens, Latency, Error Rate), Logs (GenAI Events), OTLP Protocol, Context Propagation, and Span Hierarchy.

• Span Hierarchy Flow: Root Span (Agent Run) $\rightarrow$ Child Spans (`call_llm`) $\rightarrow$ Nested Tool Spans (`execute_tool`).

• Data Captured: Prompts/Completions (optional), Token Usage (Input/Output), Model/Provider, Tool Names/Arguments/Results, Latency, Exceptions, and Session/User IDs.

• Key Functions & Flags:

  • Python: `maybe_set_otel_providers()`, `google_cloud.get_gcp_exporters()`

  • CLI: `adk web --otel_to_cloud`, `adk deploy agent_engine --trace_to_cloud`

• Integrations: Google Cloud Trace/Logging, Jaeger, Grafana Tempo, Datadog, Monocle, Galileo, MLflow, Weights & Biases (Weave).

• Best Practices:

  • Keep full message content disabled in production (`captureMessageContent = false`) for PII safety.

  • Set explicit `OTEL_SERVICE_NAME` and apply sampling for high traffic.
Detailed Overview: Prompt Caching & System Prompts

• Definition & Mechanics: Prompt Caching (Prefix Caching) reuses the KV-Cache (Key-Value Attention States) created during the LLM's prefill stage. If consecutive requests share an exact starting prefix, the model skips processing those tokens.

• Role of System Prompt:

  • System Prompts, Tool Definitions, Few-shot Examples, and Static Documents form the primary Cacheable Prefix because they remain static.

  • Dynamic data (e.g., timestamps, session IDs, user inputs) inside the System Prompt will trigger a Cache Break.

• Google ADK Implementation:

  • `static_instruction`: Assigned to system instructions; cacheable.

  • `instruction`: Dynamic turn instructions passed in the user payload.

  • Configured at app level using `ContextCacheConfig` (with parameters like `min_tokens`, `ttl_seconds`, `cache_intervals`).

• Cacheability Breakdown:

  • Cacheable: System Prompts, Tool Schemas, Static Documents / RAG context.

  • Non-Cacheable: User Queries, Conversation History, Dynamic Tool Results.
Cache Terms:

• Cache Hit: Required data is successfully found and retrieved from the cache.

• Cache Miss: Required data is not found in the cache and must be fetched from the original source.
Additional Caching Terms:

• Exact Match Caching: Reusing the exact cached response when the entire query matches a previously processed request.

• Semantic Caching: Reusing a cached response for new queries that are semantically similar to previously cached requests, even if the exact wording is different.

Caching Strategies
1. Exact Match Cache

Matches only identical strings
Fastest, but lowest recall
Use case: High precision requirements
2. Fuzzy Match Cache

Handles typos via edit distance
Medium speed and recall
Use case: User input with spelling errors
3. Semantic Cache

Understands meaning via embeddings
Slower, but highest recall
Use case: Natural language variations

===========================

MongoDB Atlas में Hierarchy :

Organization
 └── Project(s)
      └── Cluster(s)
           └── Database(s)
                └── Collection(s)
                     └── Document(s)

Qdrant DB :

Cluster (Qdrant Instance)
 └── Collection(s)
      └── Shard(s) + Replicas
           └── Segment(s)
                └── Point(s)
                     ├── ID
                     ├── Vector(s)
                     └── Payload (Metadata)

PostgreSQL :

Database Cluster (Instance)
 └── Database(s)
      └── Schema(s)          ← (public by default)
           └── Table(s) / View(s) / Sequence(s) / Function(s)
                └── Column(s) + Row(s)


Redis :

Redis Cluster
 └── Master Nodes (+ Replicas)
      └── Hash Slots (कुल 16,384 slots)
           └── Keys (slot में map होते हैं)
                └── Data Structures

Redis Instance / Cluster
 └── Logical Database (db0 – db15)
      └── Keys (user:1001, product:123 ...)
           └── Value
                ├── String
                ├── Hash
                ├── List
                ├── Set
                ├── Sorted Set
                └── Stream ...



Best Free / Open-Source Vector DBs (2026):
Vector DB
Free Option
Best For
Self-Hosted
Notes
Weaviate
Sandbox (14 days) + Full Open Source
Hybrid Search (BM25 + Vector)
Yes
Modules बहुत powerful
Milvus / Zilliz
Zilliz Free Tier (5 GB ≈ 1M vectors) + Open Source
Billion-scale data
Yes
Enterprise level
Chroma
100% Free (Open Source)
Prototyping & LangChain
Yes
सबसे आसान local setup
pgvector
Free (Postgres Extension)
Existing Postgres users
Yes
Supabase / Neon free tier पर चलता है
Pinecone
Free Starter Tier (limited vectors)
Zero-ops Managed
No
Fully managed
LanceDB
100% Free (Open Source)
Multimodal & Embedded
Yes
Serverless style
FAISS (Meta)
100% Free Library
High-performance search
Yes
Full DB नहीं, library है
• Microsoft Governance
• Azure Prompt Shield

• Guardrails
• Azure Prompt Shield: Detects and blocks direct prompt injection (jailbreak) and indirect prompt injection attempts.

• Guardrails: Multi-point controls that scan user inputs and model outputs for safety, preventing harmful or policy-violating content generation.
• GCP Identity GIS: Used for authentication and OAuth flows.
Security Defenses:

• Prompt Injection Prevention: Use Prompt Casing (XML/JSON wrappers), sanitize inputs, and employ pre-LLM guardrails.

• Tool Poisoning Prevention: Validate and sanitize tool outputs, enforce strict schema validation, use the Principle of Least Privilege, and implement Human-in-the-loop (HITL) for sensitive operations.





Tool Poisoning Prevention Techniques (Azure & Agents)
 * Tool Allowlisting & Discovery Restriction: केवल स्वीकृत (approved) टूल्स को ही एजेंट द्वारा इस्तेमाल करने दें।
 * Trusted MCP Server Architecture & Review: थर्ड-पार्टी MCP सर्वर्स को कनेक्ट करने से पहले उनका सिक्योरिटी रिव्यू करें।
 * Deterministic Tool Descriptions: टूल डिस्क्रिप्शन को छोटा, एक्शन-ओरिएंटेड और अनावश्यक निर्देशों से मुक्त रखें।
 * Untrusted Data Boundary for Tool Outputs: टूल के आउटपुट को हमेशा डेटा मानें, उसे कभी भी सिस्टम इंस्ट्रक्शन न समझें।
 * Azure Prompt Shields: टूल आउटपुट, फाइलों या वेब पेजों में छिपे अप्रत्यक्ष (indirect) प्रॉम्प्ट इंजेक्शन को ब्लॉक करें।
 * Tool-Call Intervention Point: टूल रन होने से पहले उसके आर्गुमेंट्स और रिक्वेस्ट को पॉलिसी से वैलिडेट करें।
 * Deterministic Authorization Outside LLM: ऑथराइजेशन का फैसला LLM के बाहर एप्लीकेशन लॉजिक से लें।
 * Least Privilege via Microsoft Entra ID: एजेंट्स को केवल आवश्यक RBAC अनुमतियाँ (Permissions) दें।
 * Secret Isolation: प्रॉम्प्ट या टूल आउटपुट में API कीज, टोकन्स या क्रेडेंशियल्स कभी न भेजें।
 * Human-in-the-Loop Approval: डिलीट, सेंड, या ट्रांसफर जैसे संवेदनशील कामों के लिए मैन्युअल अप्रूवल लें।
 * Azure AI Gateway Governance: MCP ट्रैफिक के लिए सेंट्रल ऑथेंटिकेशन, रेट लिमिटिंग और ऑडिटिंग लागू करें।
 * Defense-in-Depth Pipeline: मल्टी-लेयर सिक्योरिटी गेट्स का इस्तेमाल करें ताकि एक लेयर फेल होने पर दूसरी सुरक्षा दे सके।
 * 








Risk, जैसे jailbreak / indirect attack / harmful content, detect होता है।



Context Poisoning, Memory Poisoning, Tool Poisoning, Prompt Poisoning and Injection 


Memory types
Memory in Foundry Agent Service extracts and stores three types of long-term memory:
Memory type
Description
Retrieval guidance
Configuration
User profile memory
Durable user preferences and personal context, such as language preference, product



ROLLBACK TYPES AND TECHNIQUES 


Mathematical Foundations (1800s–1940s)
Early Neural Models (McCulloch-Pitts 1943, Perceptron 1958)
Symbolic AI + Expert Systems (1950s–1980s)
Backpropagation + Multi-layer Nets (1986)
Classical Machine Learning (1990s–2010)
RNN (1980s–1990s)
LSTM / GRU (1997 से मुख्य)
Deep Learning Boom (2012)
Attention Mechanism (2014–15)
Transformer (2017)
Large Language Models (2018–2020)
RAG (2020)
Generative AI Mainstream (2022–अब)



Here is the complete list of all AWS services and deployment options mentioned above:
 * EC2 (Elastic Compute Cloud)
 * AWS Elastic Beanstalk
 * AWS ECS (Elastic Container Service)
 * AWS EKS (Elastic Kubernetes Service)
 * AWS Fargate
 * AWS ECR (Elastic Container Registry)
 * AWS Lambda
 * AWS App Runner
 * Amazon API Gateway
 * AWS Amplify
 * Amazon S3 (Simple Storage Service)
 * Amazon CloudFront
 * AWS Management Console
 * AWS CLI (Command Line Interface)
 * AWS CloudFormation
 * AWS CDK (Cloud Development Kit)
 * AWS CodePipeline
Microsoft Azure
 * Azure Virtual Machines (VMs)
 * Azure App Service
 * Azure Container Instances (ACI)
 * Azure Kubernetes Service (AKS)
 * Azure Red Hat OpenShift
 * Azure Container Apps
 * Azure Container Registry (ACR)
 * Azure Functions
 * Azure Static Web Apps
 * Azure Blob Storage
 * Azure Content Delivery Network (CDN)
 * Azure Portal
 * Azure CLI
 * Azure PowerShell
 * Azure Resource Manager (ARM) Templates
 * Azure Bicep
 * Azure Pipelines (Azure DevOps)
Google Cloud Platform (GCP)
 * Compute Engine
 * App Engine
 * Cloud Run
 * Google Kubernetes Engine (GKE)
 * Artifact Registry / Container Registry
 * Cloud Functions
 * Firebase Hosting
 * Cloud Storage (GCS)
 * Cloud CDN
 * Cloud Endpoints / Apigee
 * Google Cloud Console
 * gcloud CLI
 * Google Cloud Deployment Manager
 * Cloud Build



1. Production issue with the rate limiting in AWS
and so on


