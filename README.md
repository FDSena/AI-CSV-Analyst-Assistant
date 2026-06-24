# AI Process Mining Assistant

Analyzing business process logs to find bottlenecks, predict which cases are likely to be late, and surface recurring issues from text comments, with an LLM layer on top that turns the technical output into something a business person can actually read.

## Why this project

I wanted something closer to what a Data Scientist / Data Ops role actually looks like day to day, rather than another "load CSV, train model, plot accuracy" notebook. Most internship postings I'm targeting (process mining, MLOps, RPA-adjacent roles) describe end-to-end ownership: understand the business need, clean and structure the data, build something predictive, and make it usable by people who don't write Python. This project is my attempt to cover that whole loop on a single, realistic use case.

I'm using insurance claims processing as the running example (request → document check → validation → decision → closed), but the pipeline isn't tied to that domain, it works on any case/activity/timestamp event log.

## What it does

- **Process mining**: reconstructs how cases actually flow through the process, finds the slowest steps, the most common paths, and where cases loop back or get stuck.
- **Delay prediction**: a classifier flags cases at risk of running late, before they actually do.
- **Text analysis**: clusters free-text comments to find recurring root causes (missing document, customer error, manual bottleneck, etc.) instead of relying on someone reading every comment.
- **Reporting + recommendations**: an LLM agent reads the analytical output and writes a short business summary plus automation suggestions, with a priority and a reason attached , not just "AI says automate this."
- **Dashboard**: a Streamlit app to browse all of the above without touching the notebooks.

The LLM part is intentionally a thin layer on top, not the core. If the API is unavailable or the output is mediocre, the rest of the project (SQL, ML, NLP, dashboard) still stands on its own.

## Pipeline

```
raw event log → cleaning & feature engineering → SQL storage
              → process mining (paths, bottlenecks)
              → delay prediction model
              → text clustering on comments
              → LLM report + automation suggestions
              → Streamlit dashboard
```

## Data

Working with a simulated event log first (case_id, activity, timestamp, department, status, duration, priority, comment, cost), since it's easy to control and shape toward specific failure patterns I want to detect. I'd like to validate the pipeline against a real public event log too , the BPI Challenge datasets are the standard reference in process mining and would make the results more credible than a hand-generated log.

| Column | Description |
|---|---|
| case_id | Unique case identifier |
| activity | Step name |
| timestamp | When the step happened |
| user_id | Agent/user who performed it |
| department | Department involved |
| status | Current case status |
| duration | Duration of the activity |
| priority | Case priority |
| comment | Free-text note |
| cost | Estimated cost of the step |

## Stack

Python, pandas, SQLite, scikit-learn (+ XGBoost/LightGBM if the baseline isn't good enough), basic NLP (TF-IDF + clustering, embeddings if time allows), Streamlit, pytest, GitHub Actions.
LLM calls go through the Claude or OpenAI API for the reporting/recommendation layer , kept separate from the core pipeline so it can be swapped or disabled.

## Project structure

```
ai-process-mining-assistant/
├── data/               raw and processed event logs
├── notebooks/          exploration, process mining, modeling, text analysis
├── src/
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── database.py
│   ├── process_mining.py
│   ├── train_model.py
│   ├── predict.py
│   ├── text_analysis.py
│   ├── report_generator.py
│   └── automation.py
├── app/
│   └── streamlit_app.py
├── models/
├── reports/
├── tests/
├── requirements.txt
└── README.md
```

## Status

Work in progress, built over summer 2026 alongside a part-time job. Core pipeline (process mining + delay prediction) is the priority; the LLM reporting layer comes once that's solid.

- [ ] Data cleaning & feature engineering
- [ ] SQL storage + KPI queries
- [ ] Process mining module
- [ ] Delay prediction model
- [ ] Text clustering on comments
- [ ] LLM reporting agent
- [ ] LLM automation recommendation agent
- [ ] Streamlit dashboard
- [ ] Tests + CI

## What I'd still like to add

Validating against a real public dataset (BPI Challenge), comparing the LLM-suggested automation priorities against a simple rule-based score (frequency × cost × duration) to check whether the LLM's judgment is actually reasonable, and possibly Dockerizing the whole thing if there's time left.
