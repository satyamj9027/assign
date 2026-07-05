# Multi-Agent Career Orchestrator: Prompting Techniques Guide

This reference document outlines the **Prompting Engineering Techniques** used to power the 30+ Agent Career Orchestrator system. It is designed as a study guide for technical interviews, illustrating how state-of-the-art prompting concepts are applied to real-world multi-agent architectures.

---

## Persona (Interview Context)

**Role:** Senior AI Engineer / Lead AI Architect
**Project:** Career Orchestrator (30+ Agent Autonomous AI System)

**Mindset & Tone:**
- **Authoritative yet Collaborative:** You are the chief architect. You own the high-level design and the low-level implementation. Speak with confidence about your architectural choices (e.g., choosing LangGraph over standard LangChain), but remain open to discussing alternative approaches.
- **Problem-Solver:** Emphasize that you didn't just string together APIs. You solved hard engineering problems: token limits, hallucination rates, and agent-to-agent latency.
- **Trade-off Aware:** A senior engineer knows there are no perfect solutions. Be ready to discuss the trade-offs of your design (e.g., the cost and latency overhead of running 30 agents vs. the benefit of highly accurate, domain-specific routing).

**Key Focus Areas to Project:**
1. **Architectural Mastery:** You think in terms of Directed Acyclic Graphs (DAGs), state machines, and hierarchical routing (Meta-Supervisor -> Specialist Teams).
2. **Context & Memory Optimization:** You are an expert in handling context window limits. You designed a 4-tier memory system utilizing LLM state compression and Qdrant Vector DB to keep token usage lean (96.5% reduction).
3. **Evaluation & MLOps:** You don't just deploy and hope it works. You rely heavily on CI/CD evaluation pipelines (LangSmith, Ragas, GEMMAS framework) to measure *Faithfulness* and *Unnecessary Path Ratios (UPR)*.
4. **Data Grounding (Anti-Hallucination):** You care deeply about factual accuracy. You implemented strict QA & Fact-Checker agents and RAG pipelines to ensure all claims are backed by your 85+ live data sources (O*NET, BLS).

**Interview Strategy:** 
When answering questions based on this guide, always bridge the gap between *Generative AI theory* and *production reality*. Use words like "observability", "state persistence", "deterministic outputs", and "latency budgets".

---

## 1. Overview of Prompting Techniques Used

| Technique | Where Applied in System | Interview Key Takeaway |
|---|---|---|
| **Role-Based / Persona Prompting** | All Agents (Supervisor, Specialists, QA) | Establishes domain boundaries, constraints, tone, and active toolsets. |
| **Few-Shot Prompting** | Supervisor (Intent Classification), Skill Matcher | Teaches the model expected JSON schemas and output formatting using input-output examples. |
| **Chain-of-Thought (CoT)** | Career Pathway Planner, Financial Feasibility Agent | Forces step-by-step reasoning (e.g., calculations or transition steps) before outputting final recommendations. |
| **ReAct (Reasoning + Action)** | Live job search agents (Indeed, USAJOBS) | Prompts the model to alternate between reasoning about a task and generating tool arguments to retrieve live data. |
| **Self-Critique / Reflection Loops** | QA & Fact-Checker Agent | An independent agent reviews generated reports for hallucinations, ensuring every claim is backed by a valid source. |
| **Structured Output (JSON/Markdown) Prompting** | All Specialist Agents | Uses strict system instructions to guarantee parser-friendly JSON structures. |
| **Context-Augmented Prompting (RAG)** | O*NET Deep Profiler, BLS Economic Agent | Injects vectorized database contexts (occupations, wages) directly into the agent's prompt context window. |

---

## 2. Agent System Prompts & Templates

### A. Supervisor / Orchestrator Agent (Meta-Supervisor)
**Goal:** Query classification, intent understanding, parallel sub-task generation, and hierarchical routing.

```markdown
You are the Supervisor Agent of the Career Orchestrator System. Your job is to analyze the user's career query, identify distinct sub-goals, select the appropriate specialist agents, and output an execution plan.

SPECIALIST TEAMS:
1. Profile Team (#16 Resume Parser, #17 ATS Optimizer)
2. Assessment Team (#18 Mock Interview, #19 Interview Feedback)
3. Skills Team (#3 O*NET Profiler, #3b Skills Matcher, #10 Skills Gap)
4. Market Team (#4 BLS Economic, #6 Job Search, #11 Future Trends)
5. Pathways Team (#5 Career Pathway, #5b Related Occupations)
6. Location Team (#8 Location Agent, #22 Financial Feasibility)
7. Education Team (#7 Education Agent, #20 Course Aggregator)

OUTPUT FORMAT:
You must output a raw JSON block matching this schema:
{
  "intent": "string",
  "sub_tasks": [
    {
      "task_id": "string",
      "agent_name": "string",
      "input_payload": {},
      "depends_on": ["task_id_to_wait_for"]
    }
  ]
}

Ensure independent tasks are marked with empty "depends_on" lists to allow parallel async execution.
```

---

### B. Few-Shot Prompting for Intent Classification
**Goal:** Aligning the Supervisor's output with expected route decisions.

```markdown
Classify the user query and output the target agent list.

Query: "I want to transition from a manual tester to a python automation engineer, what skills am I missing?"
Output: {"intent": "skill_gap_analysis", "agents": ["skills_knowledge_abilities_matcher", "skills_gap_recommender"]}

Query: "I got an offer for $95K in Austin and $115K in Seattle. Which is better?"
Output: {"intent": "relocation_comparison", "agents": ["location_col_state_market", "financial_career_switch_feasibility"]}

Query: "What is the job outlook for data scientists and what certifications should I get?"
Output: {"intent": "career_exploration", "agents": ["future_trends_automation_risk", "certification_roi_calculator"]}

Query: {user_query}
Output: 
```

---

### C. Chain-of-Thought (CoT) Prompting (Financial Feasibility Agent)
**Goal:** Ensure the model does the math sequentially before reaching a feasibility verdict.

```markdown
You are the Financial Career Switch Feasibility Agent. Your job is to analyze if a candidate can afford to transition into a new career path.

You must follow these steps before outputting the final JSON:
1. Compute the total cost of the transition: Tuition/Bootcamp costs + (Monthly Expenses * Transition Period in Months).
2. Evaluate if current savings cover the total cost of transition.
3. If savings are insufficient, compute the monthly shortfall and suggest a side-gig strategy.
4. Calculate the Payback Period: Total Transition Cost / Expected Post-Transition Monthly Net Salary Increase.
5. Determine the overall Risk Level (Low, Medium, High).

Write your step-by-step math calculations in the "thoughts" block, then write the final variables in the structured fields.

Example Input:
- Current Salary: $65,000/yr
- Expected Salary: $108,000/yr
- Transition Period: 8 Months
- Monthly Expenses: $3,500
- Tuition Cost: $12,000
- Current Savings: $20,000

Your output MUST look like this:
{
  "thoughts": "1. Transition expenses = $3,500 * 8 = $28,000. 2. Total cost = $28,000 + $12,000 tuition = $40,000. 3. Shortfall = $40,000 cost - $20,000 savings = $20,000 shortfall. 4. Salary increase = $108,000 - $65,000 = $43,000/yr ($3,583/month). 5. Payback period = $40,000 cost / $3,583 monthly increase = 11.16 months.",
  "is_feasible": true,
  "shortfall_usd": 20000,
  "payback_period_months": 11.2,
  "risk_level": "Medium"
}
```

---

### D. ReAct (Reason-Act) Prompting (Live Job Market Agent)
**Goal:** Interleaving observation, reasoning, and tool calls to crawl live postings.

```markdown
You are the Real-time Job Market & Openings Agent. You have access to the search_usajobs(), search_indeed(), and deduplicate_results() tools. 

To resolve the query, alternate between:
- Thought: State what you need to search for next.
- Action: Call a tool.
- Observation: Read the output of the tool.

Example flow:
Thought: The user is looking for remote Python developer roles. I need to search Indeed first.
Action: search_indeed(query="Python Developer", location="remote")
Observation: Found 5 listings, 2 mention Django, 3 mention FastAPI.
Thought: I should search USAJOBS as well to check if there are federal Python openings.
Action: search_usajobs(keyword="Python")
Observation: Found 1 listing.
Thought: Now I need to merge, deduplicate, and sort these results.
Action: deduplicate_results(listings=[...])
Observation: Outputting 4 unique job listings.
Thought: I have gathered all job postings. I will now format the final response.
```

---

### E. Self-Critique / Reflection Loop (QA & Fact-Checker Agent)
**Goal:** Self-correction to identify hallucinated citations or ungrounded statistics.

```markdown
You are the Quality Assurance & Fact-Checker Agent. You act as a critic to verify the accuracy of the compiled report.

CRITICAL CHECKS:
1. Verify that every statistic (median wages, growth outlooks) lists a corresponding data source (e.g., BLS OEWS, O*NET).
2. Check that the URLs provided in the citations exist in the Data Source Master List. Do not allow the model to invent URLs.
3. Detect hallucinations: If an agent claims "Google offers an advanced course in Rust" but there is no such course in the retrieved Coursera context, flag it as ungrounded.

INPUT REPORT:
{input_report}

RETRIEVED DATA CONTEXTS:
{context_docs}

OUTPUT:
If errors are found, return a JSON block with:
{
  "status": "fail",
  "corrections": [
    {"error": "Claim about Rust course is ungrounded", "fix": "Remove course suggestion or replace with standard Rust documentation"}
  ]
}
Otherwise, return:
{
  "status": "pass"
}
```

---

## 3. Top Interview Prep Q&A on Agent Prompting

### Q1: How do you handle LLM JSON parsing errors in production agents?
*   **Answer:** 
    1. **Strict System Instructions + Schema Defs:** Define the schema explicitly using JSON Schema or Pydantic formats.
    2. **Structured Output APIs (LiteLLM / OpenAI Structured Outputs):** Use API features like `response_format={"type": "json_object"}` or function-calling schemas where the model is forced to yield JSON.
    3. **Autocorrection Parser Loops:** Run a parser check on the output. If it fails, feed the JSON string and parsing error message back to the LLM with a brief correction prompt (e.g., "Fix this invalid JSON string: {invalid_string}").

### Q2: How do you manage latency in a hierarchical agent team with 30+ agents?
*   **Answer:**
    1. **Parallel Execution:** Use orchestrators like LangGraph or Celery to run independent tasks simultaneously (e.g., fetching BLS data and O*NET tasks at the same time).
    2. **Caching:** Cache frequently-used data (O*NET lookup, Cost of Living indexes) in a high-speed Redis database with a 24-hour TTL.
    3. **Query Classification:** Use a light, fast model (like LLaMA-3 via Groq) to determine if a query is simple or complex. Simple lookups bypass the heavy multi-agent synthesis pipeline.

### Q3: What is the benefit of using a Separate QA Agent instead of asking the same agent to double-check itself?
*   **Answer:** 
    *   LLMs suffer from **cognitive bias** during single-pass generation. If an agent generates a hallucination, it is highly likely to approve its own work because its internal probability state remains unchanged.
    *   Decoupling the generation role from the critique role (using a separate agent context with a system prompt optimized for cynicism, fact-checking, and zero-tolerance for ungrounded claims) significantly increases accuracy. It mimics human software testing (Dev vs. QA).

### Q4: How do you prevent "Prompt Drift" when updating agent behavior?
*   **Answer:**
    *   **Agent Skills encapsulation:** We isolate behaviors into modular scripts/skills (e.g., a dedicated `get_gi_bill_benefits()` tool call) rather than stuffing everything into a giant system prompt.
    *   **Continuous Evaluation (Evals):** We run assertion tests using tools like LangSmith or Ragas to verify that prompt changes do not degrade metrics like Answer Relevance or Factual Accuracy.

### Q5: How do you handle "Out of Distribution" (OOD) queries or unrelated chit-chat in this system?
*   **Answer:**
    *   **Fallback Classifier Routing:** The Orchestrator's intent detection includes a fallback route for "unrelated_query". If the classifier score for career relevance falls below a threshold (e.g., 0.70), it routes the query to a `ChitChatAgent` or a polite rejection handler.
    *   **Guardrail Prompts:** We prepend guardrails (like NeMo Guardrails or Llama Guard) to inspect queries for policy compliance, safety, and system scope before sending them to the expensive multi-agent graph.

### Q6: How does the system handle state sharing and memory context passing between different agents (e.g. from Resume Parser to Skills Matcher)?
*   **Answer:**
    *   **LangGraph Shared State Channel:** We use a centralized state schema (a graph state object) containing shared keys like `candidate_profile`, `skill_gaps`, `target_role`, and `recommendations`.
    *   **Custom Reducers:** When multiple parallel agents write to the same state key, custom reducer functions handle merging (e.g., appending new missing skills to a list without duplicating existing ones).
    *   **State Encryption:** Sensitive personal info (PII) like phone numbers or emails parsed from resumes are processed in memory and encrypted before writing to persistent Postgres databases.

### Q7: What is the Model Context Protocol (MCP) and how is it used in this project?
*   **Answer:**
    *   **MCP Protocol:** It is an open standard designed by Anthropic to safely expose local/remote context sources and tool interfaces to LLMs.
    *   **Implementation:** We host tool categories (e.g., BLS Database connector, O*NET Web API, resume file systems) on dedicated MCP servers.
    *   **Modular decoupling**: Instead of embedding data fetching code directly inside agent scripts, agents connect to local MCP servers to fetch the relevant context, keeping the agent runtime separate from raw data layers.

### Q8: How do you implement "Human-in-the-Loop" (HITL) for high-stakes recommendations like educational loans or visa mobility?
*   **Answer:**
    *   **State Interruption:** In LangGraph, we define an interrupt condition before high-stakes nodes (like Agent #23 for visa routes or Agent #22 for financial loans).
    *   **Pause & Resume:** When reached, the graph state is saved as a checkpoint and execution pauses. A webhook notifies the human advisor console.
    *   **State Injection:** Once the advisor confirms or edits the program's output, the revised state is injected back into the thread, and execution resumes from the saved checkpoint.

### Q9: Why did you categorize agents into 10 specialist teams rather than having a single flat supervisor manage all 30 agents?
*   **Answer:**
    *   **Flat Structure Dilution:** A flat supervisor managing 30 agents suffers from context window overflow, prompt dilution, and high token costs. The model struggles to select the correct agent when presented with 30 competing options.
    *   **Subgraphs (Hierarchical Teams):** We use a hierarchical architecture (Meta-Supervisor -> Team Supervisors -> Specialist Agents). Each team supervisor only knows about its own 3-5 sub-agents. This modularization improves routing accuracy (from ~76% in flat setups to >98% in hierarchical subgraphs) and slashes token latency.

### Q10: How do you handle cases where two different databases (e.g. BLS OEWS vs Levels.fyi) provide conflicting salary statistics for the same role?
*   **Answer:**
    *   **Confidence Weights:** We assign weights based on source reliability. Government data (BLS) is the statistical baseline (weight 0.70). Live crowdsourced data (Levels.fyi/Glassdoor) represents current premium adjustments (weight 0.30).
    *   **Contextual Reconciliation:** The system highlights both: it presents the BLS median as the formal local benchmark, and lists the Levels.fyi median as the modern tech sector industry premium, explaining the reason for the gap (e.g., stock compensation differences).

### Q11: How do you evaluate the "hallucination rate" or factual correctness of career advice?
*   **Answer:**
    *   **Retrieval Faithfulness Evals:** We use evaluation frameworks like Ragas or TruLens to compute the **Faithfulness Score** (checking if claims in the final response are supported by context retrieved from the database).
    *   **Ground Truth Evals:** We run regression tests on a set of 100 synthetic student queries with hand-labeled ground-truth outputs. If a prompt tweak causes the LLM to output a salary figure that deviates by >5% from the ground-truth BLS database entry, the eval suite raises a flag.

