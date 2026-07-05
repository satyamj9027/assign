# Career Orchestrator - Agent Memory & Compression - Complete Step-by-Step Dry Run

---

## 🎬 SHURUAT: Scenario Setup

**User:** Rahul Sharma
**Problem:** Career guidance chahiye — Data Analyst se Data Scientist mein transition karna hai
**Background:** 2.5 saal ka experience, B.Tech CS, Python + SQL skills
**Location Preference:** Remote / Bangalore / Hyderabad

---

## ✅ TURN 1 - Pehli Baat (10:00 AM)

### User Ne Kya Bola?
```
"Main ek Data Analyst hoon, 2.5 saal ka experience hai. 
Mujhe Data Scientist banna hai. Kahan se shuru karun?"
```

### Ab Kya Hota Hai - Step-by-Step:

**Step 1: System Pehle Long-term Memory Check Karta Hai**
- System sochega: "Kya Rahul Sharma naam ka koi user pehle se saved hai?"
- User Profile Store mein jaake dekhta hai "user_789" key ke liye
- Kuch nahi milta (first time user)
- System sochta hai: "Yeh naya user hai, iska koi data nahi hai"

**Step 2: Supervisor Agent Query Parse Karta Hai (LLM Call #1)**
- **Model**: GPT-4o / LLaMA 3 (Groq)
- **Input Tokens**: 200 (user message + system instructions)
- **Supervisor Sochta Hai**:
  - "User career transition poochh raha hai"
  - "Pehle unka profile samajhna padega"
  - "RIASEC Interest Profiler Agent call karna chahiye"
  - "Skills Matcher Agent bhi call karna chahiye"
- **Output**: Multi-agent routing plan
- **Yeh LLM Call #1 hai**

**Step 3: Interest Profiler RIASEC Agent Activate Hota Hai (Tool Call)**
- Agent function `interest_profiler_career_fit()` chalta hai
- O*NET Interest data use karta hai
- Input: User ke stated interests ("problem solving, data, helping organizations")
- Output:
  ```json
  {
    "dominant_interests": ["Investigative", "Conventional"],
    "career_fit_score": { "Data Scientists": 94, "BI Analysts": 89 }
  }
  ```

**Step 4: Skills Knowledge Abilities Matcher Agent Activate Hota Hai (Tool Call)**
- Agent function `skills_knowledge_abilities_matcher()` chalta hai
- O*NET Database se match karta hai
- Input: ["Python", "SQL", "Data Analysis", "Pandas", "Power BI"]
- Output:
  ```json
  {
    "top_matches": [
      { "occupation": "Data Scientists", "match_score": 92, 
        "missing_skills": ["Machine Learning", "Deep Learning", "Big Data"] },
      { "occupation": "BI Analysts", "match_score": 95, 
        "missing_skills": ["Advanced Data Visualization"] }
    ]
  }
  ```

**Step 5: Compression Check Hota Hai**
- System dekhta hai: Abhi sirf 2 messages hain
- Total tokens: 500
- Threshold: 3000 tokens (abhi bahut door)
- Decision: **Compression nahi chahiye**

**Step 6: Short-term Memory Save Hoti Hai**
- Checkpointer mein "user_789" thread create hota hai
- Save karta hai: User message + Agent responses + Tool outputs
- Thread ID: "user_789"
- Version: 1

**Step 7: Long-term Memory Save Hoti Hai (User Profile Store)**
- Store mein "user_789" key banti hai
- Save hota hai:
  ```json
  {
    "first_interaction": "2026-07-05",
    "current_role": "Data Analyst",
    "experience_years": 2.5,
    "target_role": "Data Scientist",
    "skills": ["Python", "SQL", "Data Analysis", "Pandas", "Power BI"],
    "riasec_dominant": ["Investigative", "Conventional"]
  }
  ```
- Yeh permanent save ho gaya

### Is Turn Mein Kya Use Hua?
- **LLM Call**: 1 baar (Supervisor — routing decision)
- **Tool Call**: 2 baar (RIASEC Agent + Skills Matcher Agent)
- **Embedding**: 0 baar (semantic search nahi ki)
- **Storage**: Short-term + Long-term dono create

---

## ✅ TURN 2 - Skills Gap & Career Path (10:08 AM)

### Agent Ne Kya Bola?
```
"Rahul ji, aapka profile dekha. Data Scientist ke liye 
aapke paas Python, SQL, Pandas already hain — bahut achha!
Main 3 key gaps dekh raha hoon: Machine Learning, Deep Learning, Big Data.
Kya aap apna resume share karenge taaki main zyada personalized advice de sakun?"
```

### User Ne Kya Bola?
```
"Haan, main resume share karta hoon. Aur batao — financially 
kitna cost aayega transition mein? Main Texas mein hoon."
```

### Ab Kya Hota Hai - Step-by-Step:

**Step 1: Long-term Memory Load Hota Hai**
- System User Profile Store se "user_789" ka data load karta hai
- Milta hai: `{current_role: "Data Analyst", skills: [...], target_role: "Data Scientist"}`
- Ye data system message mein add ho jaata hai
- LLM ko pata hai: "User Data Analyst hai, career switch chahiye"

**Step 2: Supervisor Multi-Task Identify Karta Hai (LLM Call #2)**
- **Model**: GPT-4o
- **Input Tokens**: 800
- **Supervisor Sochta Hai**:
  - "User ne resume share karne ka kaha — Resume Parser Agent call karo"
  - "User ne financial feasibility poochha — Financial Agent call karo"
  - "Location: Texas mention kiya — COL Agent bhi chahiye"
  - "Parallel mein run karo sabko"
- **Output**: Parallel execution plan
- **Yeh LLM Call #2 hai**

**Step 3: PARALLEL AGENT EXECUTION (Sab Tool Calls, No LLM):**

*Agent A: Resume Parser #16*
- Input: Resume file (PDF)
- Tool function: `resume_parser_profile_extractor(file=resume.pdf)`
- Output:
  ```json
  {
    "extracted_skills": ["Python", "SQL", "Data Analysis", "Power BI", "Excel"],
    "education": "B.Tech Computer Science (2021)",
    "experience": [{"company": "TCS", "role": "Data Analyst", "years": 2.5}],
    "certifications": ["Google Data Analytics Certificate"]
  }
  ```

*Agent B: Financial Career Switch Feasibility #22*
- Input: current_salary = $65K, target = $108K, bootcamp_cost = $12K
- Tool function: `financial_career_switch_feasibility(current_salary=65000, target=108000)`
- Output:
  ```json
  {
    "is_feasible": true,
    "payback_period_months": 9,
    "roi_2_year_usd": 66000,
    "risk_level": "Medium",
    "shortfall_usd": 20000,
    "shortfall_strategy": "Part-time freelance during transition"
  }
  ```

*Agent C: Location COL Agent #8*
- Input: current_location = "Texas", target_location = "Remote/Bangalore"
- Tool function: `location_col_state_market(from="Texas", role="Data Scientist")`
- Output:
  ```json
  {
    "texas_median_salary": 108000,
    "texas_col_index": 92,
    "remote_advantage": "Save $8K/year on commute",
    "top_alternatives": ["Austin TX", "Raleigh NC", "Nashville TN"]
  }
  ```

**Step 4: Compression Check Hota Hai**
- Ab messages: 6 (3 user + 2 agent + 1 tool output bundle)
- Total tokens: 1500
- Threshold: 3000 (abhi safe)
- Decision: **Compression nahi chahiye**

**Step 5: Short-term Memory Update**
- Checkpointer mein naya version save hota hai
- Messages ab: 6
- Version: 2

**Step 6: Long-term Memory Update**
- User profile update hota hai:
  ```json
  {
    "resume_parsed": true,
    "financial_feasibility": "feasible",
    "location_preference": "Remote/Texas",
    "risk_tolerance": "Medium"
  }
  ```

### Is Turn Mein Kya Use Hua?
- **LLM Call**: 1 baar (Call #2 — Supervisor routing)
- **Tool Call**: 3 baar (Resume Parser + Financial Agent + COL Agent — parallel)
- **Embedding**: 0 baar
- **Storage**: Short-term + Long-term update

---

## ✅ TURN 3 - Education & Learning Path (10:18 AM)

### Agent Ne Kya Bola?
```
"Bahut achha Rahul ji! Financial analysis ke mutabik:
- Transition feasible hai (payback: 9 months)
- 2-year ROI: $66,000 gain
- Risk: Medium (shortfall of $20K, solve with freelancing)

Ab main aapke liye personalized learning path banata hoon.
Kya Machine Learning mein aapka koi prior exposure hai?"
```

### User Ne Kya Bola?
```
"Thoda basic ML pata hai — linear regression, decision trees.
But deep learning bilkul nahi. Aur main prefer karunga free ya low-cost courses.
Timeline: 6 months mein transition complete karna hai."
```

### Ab Kya Hota Hai - Step-by-Step:

**Step 1: Long-term Memory Load**
- "user_789" ka poora profile load hota hai
- Isme: skills, resume data, financial feasibility sab hai
- LLM ko context milta hai

**Step 2: Teesri LLM Call - Supervisor (Call #3)**
- **Model**: GPT-4o
- **Input Tokens**: 2000 (ab context badh gaya hai)
- **Supervisor Sochta Hai**:
  - "User ka ML level: basic"
  - "Deep Learning: zero"
  - "Budget: free/low-cost"
  - "Timeline: 6 months"
  - "Course Aggregator Agent call karo"
  - "Skills Gap Agent bhi call karo precise plan ke liye"
- **Output**: Tool call plan
- **Yeh LLM Call #3 hai**

**Step 3: Course & Learning Path Aggregator Agent (Tool Call)**
- Tool function: `course_learning_path_aggregator(skill_gaps=["ML", "Deep Learning", "Big Data"], budget="free_low_cost", timeline_months=6)`
- Output:
  ```json
  {
    "learning_path": [
      {"month": "1-2", "skill": "Machine Learning", 
       "course": "Andrew Ng ML Specialization (Coursera - Free Audit)",
       "platform": "Coursera", "cost": 0},
      {"month": "2-3", "skill": "Advanced ML + Feature Engineering",
       "course": "Kaggle ML Courses", "platform": "Kaggle", "cost": 0},
      {"month": "3-4", "skill": "Deep Learning Basics",
       "course": "fast.ai Practical Deep Learning", "platform": "fast.ai", "cost": 0},
      {"month": "4-5", "skill": "TensorFlow / PyTorch",
       "course": "TensorFlow Developer Certificate Prep (Coursera)", "cost": 49},
      {"month": "5-6", "skill": "Big Data + End-to-End Projects",
       "course": "Build 2-3 Kaggle competition notebooks + GitHub portfolio",
       "cost": 0}
    ],
    "total_estimated_cost": 49,
    "certifications_recommended": ["TensorFlow Developer Certificate", "IBM Data Science Professional"]
  }
  ```

**Step 4: Skills Gap Agent (Tool Call)**
- Tool function: `skills_gap_upskilling_recommender(current=["Python", "SQL", "Pandas"], target_role="Data Scientist")`
- Output:
  ```json
  {
    "critical_gaps": [
      {"skill": "Machine Learning", "importance": 95, "current_level": "Basic", "target": "Advanced"},
      {"skill": "Deep Learning", "importance": 80, "current_level": "None", "target": "Intermediate"},
      {"skill": "Statistics & Probability", "importance": 88, "current_level": "Medium", "target": "Advanced"}
    ],
    "ready_skills": ["Python", "SQL", "Data Wrangling", "Visualization"],
    "estimated_months_to_ready": 6
  }
  ```

**Step 5: Compression Check**
- Messages: 8
- Tokens: 2600
- Threshold: 3000 (approaching!)
- Decision: **Compression nahi abhi — lekin next turn mein trigger ho sakta hai**

**Step 6: Memory Updates**
- Short-term: Version 3 (8 messages)
- Long-term: Learning path + skill gaps user profile mein save ho gaye

### Is Turn Mein Kya Use Hua?
- **LLM Call**: 1 baar (Call #3 — Supervisor)
- **Tool Call**: 2 baar (Course Aggregator + Skills Gap Agent)
- **Embedding**: 0 baar
- **Storage**: Short-term + Long-term update

---

## ✅ TURN 4, 5, 6 - Conversation Continues (10:25 - 10:50 AM)

### Turn 4:
```
Agent: "Yeh raha aapka 6-month personalized plan! Total cost sirf $49.
        Aapke strong areas: Python, SQL — yeh aapka competitive advantage hai.
        Kya aap resume bhi optimize karna chahenge Data Scientist JD ke liye?"

User: "Haan! Resume optimize karo. Aur — kya Bangalore mein 
       Data Scientist ke liye market kaisi hai abhi?"

Agent: "Zaroor! Resume optimization aur Bangalore market analysis kar raha hoon..."
       [ATS Resume Optimizer + Job Search Agent call hota hai]
       
       "Bangalore mein currently 2,400+ Data Scientist openings hain.
        Median salary: ₹18-28 LPA. Remote openings bhi strong hain."
```

### Turn 5:
```
User: "Bahut achha! Interview ke liye bhi prepare karna hai.
       Data Scientist ke mock interview questions do."

Agent: "Bilkul! Mock interview session shuru karte hain."
       [AI Mock Interview Agent #18 call hota hai]
       
       "Q1: Supervised vs Unsupervised Learning explain karo real examples se."
       "Q2: Class imbalance problem handle kaise karoge?"
       "Q3: Feature engineering mein kaunsi techniques use karte ho?"
       
User: "Feature engineering mein main SMOTE, PCA use karta hoon..."
```

### Turn 6:
```
Agent: "Bahut achha jawab! Interview Feedback Agent analysis kar raha hai..."
       [Interview Feedback Agent #19 call hota hai]
       
       "Feedback: 
       - Q1: 8/10 (examples aur explain dono achhe)
       - Q2: 9/10 (SMOTE mention — advanced knowledge)
       - Q3: 7/10 (PCA achha, but mention Random Forest feature importance bhi)
       Improvement: Business impact ko zyada emphasize karo answers mein."

User: "Salary negotiation ke liye bhi guide karo. 
       Mujhe ek offer mila hai Austin TX se — $95,000 Data Scientist role."
```

### Ab Kya Hota Hai - Step-by-Step (Har Turn Mein):

**Har Turn Mein 1 LLM Call (Supervisor) + Tool Calls:**

**Turn 4 - LLM Call #4:**
- Input tokens: 3200 (context badh gaya)
- Parallel tool calls:
  - ATS Resume Optimizer (#17): JD keywords add kiye resume mein
  - Job Search Agent (#6): Bangalore Data Scientist openings fetched
- Long-term memory: `resume_optimized: true, target_city: "Bangalore"` save

**Turn 5 - LLM Call #5:**
- Input tokens: 4500
- Tool call:
  - AI Mock Interview Agent (#18): 3 technical questions generated
- Short-term memory: Interview questions + user answers save

**Turn 6 - LLM Call #6:**
- Input tokens: 6000
- Tool calls:
  - Interview Feedback Agent (#19): User ke answers score kiye
  - Salary Negotiation Coach (#26): BLS OEWS Austin data fetch + script banaya

**Compression Check Har Turn Mein:**
- Turn 4: 3200 tokens (warning zone approach)
- Turn 5: 4500 tokens (approaching threshold)
- Turn 6: 6000 tokens → **Threshold 3000 cross ho gaya!**

**Short-term Memory Har Turn Update Hoti Hai:**
- Version 4, 5, 6 save hote hain
- Messages grow: 10, 14, 20

**Long-term Memory Har Important Decision Pe Update:**
- Resume optimization saved
- Mock interview scores saved
- Salary negotiation context saved

---

## ⚠️ COMPRESSION TRIGGER - 10:55 AM

### Kya Hua?
System ne dekha:
- Messages: 20 ho gaye
- Total tokens: 8,500 ho gaye
- Threshold: 3,000 tokens (humne set kiya tha)
- **Ab compression zaroori hai!**

---

## 🗜️ COMPRESSION PROCESS - Step-by-Step

### Step 1: System Check Karta Hai
System sochta hai:
- "Context window mein bahut saari messages aa gayi hain"
- "Agar compress nahi kiya toh kuch messages drop ho jayenge"
- "Mujhe summarization karna chahiye — important career data save karna hai"

### Step 2: Compression Method Decide Hota Hai
System analyze karta hai teen options:

**Option 1: Trimming**
- Sirf latest 6 messages rakho
- Baki sab hata do
- Fast hai but career data loss hoga (resume, scores, financial plan)

**Option 2: Summarization**
- Purani 20 messages ka structured summary banao
- Sirf summary + latest 2 messages rakho
- Thoda slow hai but sab career info preserve hoti hai

**Option 3: Hybrid**
- Summary + latest 5 messages rakho
- Balance achha rahega

**System chooses:** Summarization (career data critical hai — kuch bhi lose nahi karna)

### Step 3: Summarization LLM Call Hoti Hai (Call #7)
- **Model**: GPT-4o
- **Input**: 20 messages (8,500 tokens)
- **Prompt**: "Is career counseling conversation ka structured summary banao. Sab key decisions, data points, aur user ka current status cover karo."
- **LLM Reads Sab Messages**:
  - User: Data Analyst, 2.5 yrs exp, Python+SQL, target = Data Scientist
  - RIASEC: Investigative + Conventional (dominant)
  - Skill gaps: ML (basic→advanced), Deep Learning (none→intermediate)
  - 6-month plan: Coursera + fast.ai + Kaggle ($49 total)
  - Financial: Feasible, ROI $66K/2yr, risk = Medium
  - Resume: Optimized for Data Scientist JD
  - Mock interview: Q1=8/10, Q2=9/10, Q3=7/10
  - Job market: Bangalore - 2400+ openings, ₹18-28 LPA
  - Salary offer: $95K Austin TX (below median $108K)
- **LLM Generates Summary** (300 words, 400 tokens)
- **Output**: Comprehensive career summary ready
- **Yeh LLM Call #7 hai**

### Step 4: Summary Save Hoti Hai
- Summary object state mein add hota hai
- Short-term memory mein (checkpointer)
- Long-term memory mein bhi (User Profile Store)

### Step 5: Old Messages Remove Ho Jaate Hain
- M1 se M18 (18 messages) delete ho jaate hain
- Sirf M19 (Salary Negotiation feedback) aur M20 (User's response) rehte hain
- Trimming operation (no LLM, just list slice)

### Step 6: Final State Ready
Ab state mein:
- Summary: 300 words (400 tokens)
- Messages: 2 latest messages (500 tokens)
- Total: 900 tokens (89% reduction!)

### Is Compression Phase Mein Kya Use Hua?
- **LLM Call**: 1 baar (Call #7 — summarization)
- **Tool Call**: 0 baar
- **Embedding**: 0 baar
- **Storage**: Short-term update + Long-term update

---

## ✅ TURN 7 - After Compression (11:05 AM)

### User Ne Kya Bola?
```
"Salary negotiation script ready hai kya? 
Main kal call karne wala hoon Austin offer ke liye."
```

### Ab Kya Hota Hai - Step-by-Step:

**Step 1: Long-term Memory Load**
- User Profile Store se "user_789" ka poora profile milta hai
- Isme sab hai: skills, plan, resume status, interview scores, financial data

**Step 2: Short-term Memory Load**
- Checkpointer se latest state milti hai
- Isme summary + last 2 messages hain
- Summary mein likha hai: "Salary offer $95K, market median $108K, counter = $115K"
- LLM ko purani 20 messages nahi padhni padti

**Step 3: Salary Negotiation Agent Call (Tool Call)**
- Tool function: `salary_negotiation_coach(offered=95000, role="Data Scientist", location="Austin TX", skills=[...])`
- Output:
  ```json
  {
    "market_data": { "median_austin": 108000, "p25": 88000, "p75": 140000 },
    "suggested_counter": 115000,
    "negotiation_script": "Thank you for the offer! Based on BLS OEWS data for Austin 
     and my ML experience with Python and SQL, I was expecting $110K-$120K range. 
     Can we reach $115,000?",
    "alternative_asks": [
      "Remote flexibility (saves $8K/year)",
      "$5K annual learning budget",
      "$5K sign-on bonus"
    ]
  }
  ```

**Step 4: Final Synthesis Agent (LLM Call #8)**
- **Model**: GPT-4o
- **Input**:
  - Career summary (400 tokens)
  - Latest 2 messages (500 tokens)
  - Salary negotiation tool output (300 tokens)
  - Total: ~1200 tokens (bahut kam!)
- **LLM Sochta Hai**:
  - "Summary mein salary offer $95K hai, market $108K hai"
  - "Counter offer $115K suggested hai"
  - "Script ready karna hai user ke liye"
  - "QA Agent se verify karwana hai pehle"
- **Output**: Full negotiation guide ready

**Step 5: QA & Fact Checker Agent (Tool Call)**
- Tool function: `quality_assurance_fact_checker(response=final_output, sources=["BLS OEWS", "Glassdoor"])`
- Hallucination check: ✅ All salary figures verified against BLS OEWS
- Citation check: ✅ Sources attached
- Confidence: 0.93

**Step 6: Compression Check**
- Ab messages: 4 (summary + 2 old + 1 new)
- Tokens: ~1200
- Threshold: 3000 se bahut door
- Decision: **No compression needed**

**Step 7: Memory Update**
- Short-term: Naya message add
- Long-term: `salary_negotiation_ready: true, counter_offer_amount: 115000` save

---

## 📊 POORA JOURNEY - CONVERSATION SUMMARY

### Total Kya Kya Use Hua?

**LLM Calls (Total 8 Calls):**
| Call # | Turn | Purpose | Input Tokens |
|--------|------|---------|--------------|
| **Call #1** | Turn 1 | Supervisor — initial routing + query parse | 200 |
| **Call #2** | Turn 2 | Supervisor — parallel agent orchestration | 800 |
| **Call #3** | Turn 3 | Supervisor — learning path planning | 2000 |
| **Call #4** | Turn 4 | Supervisor — resume + job market routing | 3200 |
| **Call #5** | Turn 5 | Supervisor — mock interview orchestration | 4500 |
| **Call #6** | Turn 6 | Supervisor — interview feedback + salary | 6000 |
| **Call #7** | Compression | Summarizer — compress 20 messages | 8500 |
| **Call #8** | Turn 7 | Synthesis — final salary negotiation guide | 1200 |

**Total Input Tokens: 26,400**
**Total Output Tokens: ~1,200**

**Tool Calls (Total 12 Calls):**
| # | Agent | Turn |
|---|-------|------|
| 1 | `interest_profiler_career_fit` | Turn 1 |
| 2 | `skills_knowledge_abilities_matcher` | Turn 1 |
| 3 | `resume_parser_profile_extractor` | Turn 2 |
| 4 | `financial_career_switch_feasibility` | Turn 2 |
| 5 | `location_col_state_market` | Turn 2 |
| 6 | `course_learning_path_aggregator` | Turn 3 |
| 7 | `skills_gap_upskilling_recommender` | Turn 3 |
| 8 | `ats_resume_optimizer` | Turn 4 |
| 9 | `real_time_job_search` (Bangalore) | Turn 4 |
| 10 | `ai_mock_interview` | Turn 5 |
| 11 | `interview_feedback_scoring` | Turn 6 |
| 12 | `salary_negotiation_coach` | Turn 7 |
| 13 | `quality_assurance_fact_checker` | Turn 7 |

**Embedding Calls: 0** (is flow mein direct key-value aur tool calls use hue, semantic search nahi)

---

## 🧠 HAR MEMORY KA DESIGN - STEP-BY-STEP

### Short-term Memory Kaise Design Ki?

**Design Process:**

**Pehle:** Socho ki kya store karna hai?
- Current conversation ki saari messages
- Tool call outputs (resume parse, skills gap, interview Q&A)
- Supervisor routing decisions
- Metadata: timestamp, token count

**Phir:** Socho ki kaise store karein?
- Thread ID se identify karo (user_789)
- Har nayi message + tool output ko append karo
- Har Supervisor execution ke baad save karo
- Version history maintain karo

**Phir:** Socho ki kab delete karein?
- Jab compression trigger ho (3000 tokens ke baad)
- Purani messages hatao
- Summary rakho + latest 2-5 messages ke saath

**Final Design:**
```
Thread: user_789
├── Version 1: [M1(query), M2(RIASEC_output), M3(skills_output)] (500 tokens)
├── Version 2: [M1...M6] (1500 tokens)
├── Version 3: [M1...M8] (2600 tokens)
├── Version 4: [M1...M10] (3200 tokens)
├── Version 5: [M1...M14] (4500 tokens)
├── Version 6: [M1...M20] (8500 tokens) ← Compression trigger
└── Version 7: [Summary + M19, M20] (900 tokens) ← After compression
```

---

### Long-term Memory Kaise Design Ki?

**Design Process:**

**Pehle:** Socho ki kya store karna hai?
- User identity (name, id, education)
- Career goals aur current role
- Skills (present + gaps)
- Financial profile
- Learning plan progress
- Interview scores
- Job preferences + salary expectations

**Phir:** Socho ki kaise store karein?
- Namespace: user_profiles
- Key: user_789
- Value: JSON object
- Har important decision pe update karo

**Phir:** Socho ki kab update karein?
- Turn 1: User profile create (role, skills, RIASEC)
- Turn 2: Financial feasibility + resume parse results
- Turn 3: Learning path + skill gaps
- Turn 4: Resume optimized + target city
- Turn 5: Mock interview sessions saved
- Turn 6: Interview scores + salary context
- Compression: last_conversation_summary added
- Turn 7: Negotiation strategy saved

**Final Design:**
```json
Namespace: user_profiles
Key: user_789
Value: {
  "personal": {
    "name": "Rahul Sharma",
    "first_interaction": "2026-07-05",
    "education": "B.Tech CS (2021)"
  },
  "career": {
    "current_role": "Data Analyst",
    "experience_years": 2.5,
    "target_role": "Data Scientist",
    "employer": "TCS"
  },
  "skills": {
    "current": ["Python", "SQL", "Pandas", "Power BI", "Excel"],
    "gaps": ["Machine Learning (Advanced)", "Deep Learning", "Big Data"],
    "riasec_dominant": ["Investigative", "Conventional"]
  },
  "learning_plan": {
    "timeline_months": 6,
    "total_cost_usd": 49,
    "status": "plan_created",
    "key_courses": ["Andrew Ng ML Specialization", "fast.ai", "Kaggle"]
  },
  "financial": {
    "current_salary_usd": 65000,
    "target_salary_usd": 108000,
    "transition_feasible": true,
    "payback_months": 9,
    "risk_level": "Medium"
  },
  "job_market": {
    "preferred_locations": ["Remote", "Bangalore", "Texas"],
    "bangalore_openings": 2400,
    "salary_range_inr_lpa": "18-28"
  },
  "interview_prep": {
    "mock_sessions": 1,
    "avg_score": 8,
    "improvement_areas": ["Business impact emphasis"]
  },
  "salary_negotiation": {
    "offer_received_usd": 95000,
    "counter_offer_usd": 115000,
    "market_median_austin": 108000,
    "negotiation_ready": true
  },
  "last_conversation_summary": "User is Data Analyst transitioning to Data Scientist. 
   6-month plan created ($49 cost). Resume optimized. Mock interview done (avg 8/10). 
   Salary offer $95K Austin TX, counter = $115K recommended."
}
```

---

### Summary Memory Kaise Design Ki?

**Design Process:**

**Pehle:** Socho ki kya store karna hai?
- Career status summary
- All key data points (skills, plan, financial, market)
- Session metadata
- Key entities: SOC codes, course names, salary figures

**Phir:** Socho ki kab generate karein?
- Jab tokens > 3000
- Jab messages > 15-18
- Session ke end mein (for future sessions)

**Phir:** Socho ki kaise generate karein?
- LLM ko saari messages do
- Career-specific structured summary likhne ko kaho
- Domain-specific entities preserve karne ko kaho

**Final Design:**
```json
Summary: {
  "text": "Rahul Sharma (user_789) is a Data Analyst with 2.5 yrs exp at TCS 
   targeting Data Scientist role. Skills: Python, SQL, Pandas (strong). Gaps: 
   ML (advanced), Deep Learning, Big Data. 6-month plan created (cost $49). 
   Financial transition feasible (ROI $66K/2yr). Resume optimized for DS JDs. 
   Mock interview avg score 8/10. Salary offer: $95K Austin TX, counter: $115K. 
   Bangalore market: 2400+ openings, ₹18-28 LPA.",
  "metadata": {
    "generated_at": "2026-07-05T10:55:00Z",
    "compressed_from": { "messages": 20, "tokens": 8500 },
    "compressed_to": { "tokens": 400 }
  },
  "key_entities": {
    "soc_code": "15-2051.00",
    "courses": ["Andrew Ng ML", "fast.ai", "Kaggle"],
    "salary_offer": 95000,
    "counter_offer": 115000,
    "interview_score_avg": 8
  },
  "current_status": "Salary negotiation ready — call scheduled tomorrow"
}
```

---

### Vector Memory Kaise Use Hota? (Semantic Search Phase)

**Design Process (Jab Use Hota Hai):**

Career orchestrator mein semantic search **zyada important** hai kyunki:
- User kabhi bhi puchh sakta hai: "Mujhe us course ka naam yaad nahi jo tune suggest kiya tha"
- Ya: "Bangalore wali baat phir batao"
- Ya: "Finance wala plan explain karo"

**Pehle:** Kya store karna hai?
- Har important conversation chunk (career plan, financial data, job market info)
- O*NET occupation profiles
- BLS salary data by metro

**Phir:** Kaise store karein?
- Har chunk ko embedding mein convert karo (text-embedding-3-small)
- Qdrant vector store mein save karo
- Metadata: user_id, topic, timestamp, source

**Phir:** Kab use karein?
- Jab user ka query vague ho ("woh finance wali baat")
- Query ko embedding mein convert karo
- Top-K similar chunks retrieve karo
- LLM ko de do as context

**Design Example:**
```
Document 1:
  Text: "Rahul ka financial plan: bootcamp $12K, transition 8 months, 
         ROI $66K/2yr, risk Medium"
  Embedding: [0.231, 0.567, ...] (1536 dims)
  Metadata: {user_id: "user_789", topic: "financial_plan", timestamp: "2026-07-05"}

Document 2:
  Text: "6-month learning plan: Andrew Ng ML (Month 1-2), 
         fast.ai DL (Month 3-4), Kaggle projects (Month 5-6)"
  Embedding: [0.112, 0.890, ...]
  Metadata: {user_id: "user_789", topic: "learning_plan"}

Document 3:
  Text: "Data Scientist SOC 15-2051.00 — Skills: Python, ML, Statistics. 
         Median salary Austin $108K."
  Embedding: [0.445, 0.223, ...]
  Metadata: {source: "O*NET + BLS", topic: "job_profile"}
```

---

## 📈 PERFORMANCE - KYA EFFECT PADA?

### Compression Ke Pehle (Turn 1-6):
- **Messages**: 20
- **Tokens**: 8,500
- **Context usage**: 6.6% of 128K context window
- **LLM response time**: ~600ms per Supervisor call (context bada tha)
- **Parallel agent overhead**: 3 agents simultaneously, ~1200ms total
- **Cost per turn**: ~$0.22 average

### Compression Ke Baad (Turn 7):
- **Messages**: 2 + Summary
- **Tokens**: 900
- **Context usage**: 0.7% of 128K context window
- **LLM response time**: ~320ms (89% faster!)
- **Cost per turn**: $0.028 (87% cheaper!)

### Parallel Execution Ka Benefit (Turn 2):
```
Serial execution:
  Resume Parser     → 800ms
  Financial Agent   → 600ms
  COL Agent         → 500ms
  TOTAL: 1,900ms

Parallel execution:
  All 3 simultaneously → 800ms (only max agent time)
  TOTAL: 800ms (58% faster!)
```

---

## 🎯 FINAL SUMMARY - KAB KAUNSA MODEL/AGENT USE HUA

### LLM (GPT-4o) - 8 Calls Total:
1. Initial routing & query understanding (Call #1, Turn 1)
2. Parallel orchestration plan (Call #2, Turn 2)
3. Learning path planning (Call #3, Turn 3)
4. Resume + job market routing (Call #4, Turn 4)
5. Mock interview orchestration (Call #5, Turn 5)
6. Interview feedback + salary routing (Call #6, Turn 6)
7. Summarization — 20 messages → 300 word summary (Call #7, Compression)
8. Final salary negotiation synthesis (Call #8, Turn 7)

### Specialist Tool Agents (No LLM) - 13 Calls Total:
| # | Agent | Purpose |
|---|-------|---------|
| 1-2 | RIASEC + Skills Matcher | Career fit analysis |
| 3-5 | Resume Parser + Financial + COL | Feasibility & profile |
| 6-7 | Course Aggregator + Skills Gap | Learning path |
| 8-9 | ATS Optimizer + Job Search | Resume + market |
| 10 | Mock Interview | Interview prep |
| 11 | Interview Feedback | Scoring |
| 12-13 | Salary Negotiation + QA Checker | Final output |

### Embedding Model (text-embedding-3-small) - 0 Calls (This Session):
- Is conversation mein direct key-value + structured tool calls use hue
- Embedding tab use hogi jab user vague ya semantic query kare
- Production mein: O*NET profiles + BLS salary data pre-embedded hote hain

### Storage (No LLM) - Har Turn Mein:
- **Short-term** (Redis Checkpointer): Har turn ke baad save (7 versions)
- **Long-term** (User Profile Store - PostgreSQL): 7 updates across all turns
- **Summary**: Compression phase mein 1 baar save (Short-term + Long-term dono)
- **Vector Store** (Qdrant): Career plan chunks stored for semantic retrieval

---

## 🏗️ COMPLETE ARCHITECTURE MAP (Is Session Ka)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   CAREER ORCHESTRATOR ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────┐    ┌──────────────────────┐   ┌────────────────┐ │
│  │   USER INPUT     │───▶│  SUPERVISOR AGENT    │──▶│ SPECIALIST     │ │
│  │   (Rahul)        │    │  (LLM — GPT-4o)      │   │ AGENTS (Tools) │ │
│  └──────────────────┘    └──────────────────────┘   └────────────────┘ │
│         │                         │                         │           │
│         ▼                         ▼                         ▼           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    MEMORY LAYER (4 Types)                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────┐  ┌───────────┐  │   │
│  │  │Short-term  │  │Long-term   │  │ Summary  │  │ Vector DB │  │   │
│  │  │(Redis/     │  │(PostgreSQL │  │(Checkpt) │  │(Qdrant)   │  │   │
│  │  │Checkpointer│  │User Store) │  │          │  │           │  │   │
│  │  └────────────┘  └────────────┘  └──────────┘  └───────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                   COMPRESSION LAYER                             │   │
│  │  ┌─────────────┐   ┌──────────────────┐   ┌─────────────────┐  │   │
│  │  │ Trimming    │   │ Summarization    │   │ Hybrid          │  │   │
│  │  │ (No LLM)    │   │ (LLM Call #7)    │   │ (LLM + Trim)    │  │   │
│  │  └─────────────┘   └──────────────────┘   └─────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│            ┌─────────────────────────────────────┐                     │
│            │ QA & FACT CHECKER + SYNTHESIZER      │                     │
│            └─────────────────────────────────────┘                     │
│                              │                                          │
│                              ▼                                          │
│                    [FINAL OUTPUT TO USER]                               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 COMPLETE TOKEN COUNT TABLE (Per Turn)

| Turn | Agent(s) Active | LLM Input Tokens | Tool Calls | Compression? |
|------|----------------|-----------------|------------|--------------|
| Turn 1 | Supervisor + RIASEC + Skills Matcher | 200 | 2 | ❌ |
| Turn 2 | Supervisor + Resume Parser + Financial + COL (parallel) | 800 | 3 | ❌ |
| Turn 3 | Supervisor + Course Aggregator + Skills Gap | 2000 | 2 | ❌ |
| Turn 4 | Supervisor + ATS Optimizer + Job Search | 3200 | 2 | ❌ |
| Turn 5 | Supervisor + Mock Interview | 4500 | 1 | ❌ |
| Turn 6 | Supervisor + Interview Feedback + Salary Coach | 6000 | 2 | ⚠️ Trigger! |
| Compression | Summarizer LLM | 8500 | 0 | ✅ Executed |
| Turn 7 | Supervisor + Salary Coach + QA Checker | 1200 | 2 | ❌ |

**Grand Total LLM Input Tokens: 26,400**
**Grand Total Tool Calls: 13**

---

## 💡 KEY LEARNINGS - Is Dry Run Se

1. **Parallel Execution** — Career orchestrator mein multiple agents ek saath chalte hain (Turn 2 mein 3 agents parallel). Yeh response time 58% reduce karta hai.

2. **Supervisor Pattern** — Har turn mein ek LLM call (Supervisor) hoti hai jo decide karta hai ki kaun sa specialist agent call karna hai. Specialist agents sirf tools hain — unhe apna LLM nahi chahiye.

3. **Memory Layering** — Career data bahut important hai (financial plan, scores, skill gaps). Isliye hum 4 types of memory use karte hain (short, long, summary, vector) — ek bhi miss nahi hona chahiye.

4. **Compression Timing** — 3000 token threshold set ki gayi thi. Turn 6 ke baad 8500 tokens ho gaye — compression ne 89% reduction diya aur Turn 7 super fast ho gaya.

5. **QA Agent** — Har final output pe Quality Assurance Agent check karta hai. Career advice mein accuracy critical hai — koi bhi hallucination user ke career ko affect kar sakti hai.

6. **Tool vs LLM** — 13 specialist tool calls mein se kisi ne bhi LLM use nahi ki. Sirf 8 Supervisor/Synthesis calls LLM use karti hain. Yeh system ko fast aur cost-efficient banata hai.
