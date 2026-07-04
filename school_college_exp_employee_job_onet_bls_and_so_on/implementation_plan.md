# Implementation Plan - Career Orchestration Agent System

This project implements a multi-agent **Career Orchestrator** in `school_college_exp_employee_job_onet_bls_and_so_on/school_college_exp_employee_job_onet_bls_and_so_on.ipynb`. It utilizes **LangGraph** and the **Groq API** (`llama-3.1-8b-instant`) to match candidates' personal profiles (education, school, college, experience, skills, and RIASEC interests) with the **O*NET Database** and **BLS (Bureau of Labor Statistics) Occupational Outlook** data.

---

## User Review Required

> [!IMPORTANT]
> The system requires a valid `GROQ_API_KEY` (already present in the parent folder's `.env` file). We will load it dynamically from `../.env` using `python-dotenv`.
>
> To make this notebook self-contained and run successfully without external database credentials, we will bundle static lookup databases for core **O*NET SOC Codes** and **BLS Wage Outlook Data** inside the notebook code. This ensures calculations (salary percentiles, skill gap percentages) run immediately and deterministically.

---

## Open Questions

* No open questions. The document `assignments_and_docs/career_orchestrator_agents_1.md` provides detailed input/output JSON schemas and a comprehensive list of 20 query-response examples which we will implement and validate.

---

## Proposed Changes

### [Career Orchestrator Project]

#### [NEW] [school_college_exp_employee_job_onet_bls_and_so_on.ipynb](file:///c:/Users/Dell%205400/OneDrive/Desktop/assignment-sat/assign/school_college_exp_employee_job_onet_bls_and_so_on/school_college_exp_employee_job_onet_bls_and_so_on.ipynb)

We will write a fully structured Jupyter Notebook containing:

1. **Setup & Dependencies**:
   - Installing `langgraph`, `groq`, `python-dotenv`, `pandas`, `tabulate`.
   - Loading the `.env` file from the parent directory.
   - Initializing the Groq client.

2. **Core Data Repositories (O*NET & BLS)**:
   - **O*NET Mock DB**: Detailed mappings for occupations (SOC codes, descriptions, required skills, RIASEC interest profile, required education level, daily tasks).
   - **BLS economic DB**: Median salaries, 25th/75th percentile salaries, job outlook growth rate (e.g., 2024-2034 projection), and state-level wage examples.

3. **LangGraph State Definition**:
   - Define a shared `AgentState` using Python's `TypedDict`. It will contain:
     - `query`: The user input query.
     - `candidate_profile`: User's profile (name, experience, education, skills, RIASEC scores, preferences).
     - `route_to`: Next node to run (managed by Supervisor).
     - `matched_occupations`: Match scores and details.
     - `skills_gap`: Missing skills and required upskilling levels.
     - `economic_outlook`: BLS wages and growth data.
     - `career_ladder`: Chronological progression ladder steps.
     - `final_report`: Complete synthesized response.

4. **Agent Nodes (Specialists)**:
   - **Supervisor Node**: Parses the query, inspects the state, and determines the routing path.
   - **Personal Profile Matcher Node**: Compares the user profile with the O*NET occupational requirements to calculate matching coefficients.
   - **O*NET deep-dive & Skills Matcher Node**: Performs skill gap analysis and compiles daily tasks.
   - **BLS Economic Agent Node**: Looks up salaries and growth rates, generating cost-of-living comparison tables.
   - **Career Pathway & Transition Planner Node**: Constructs the career ladders and lists immediate upskilling steps.
   - **Output Synthesizer Node**: Combines all specialists' data into a final clean report containing tables and bullet points.

5. **Graph Compilation**:
   - Assemble nodes into a `StateGraph`, configure edges (static and conditional), and compile using an in-memory checkpointer.

6. **Interactive Test Runner**:
   - Execute the graph on several user queries (e.g. transitioning careers, wage checks, skill gap analysis) and print the results with formatting.

---

## Verification Plan

### Automated Tests
* We will run the notebook's cells locally using the CLI or Jupyter execution commands to verify:
  1. The `.env` file loads successfully.
  2. The Groq API works without rate limits.
  3. The LangGraph compiler creates the graph successfully.
  4. The workflow successfully runs end-to-end, producing valid JSON states and markdown reports.

### Manual Verification
* Inspect the outputs in the Jupyer Notebook to ensure tables, salary information, and skill matching analysis are printed correctly.
