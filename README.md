# AI CSV Analyst Assistant

AI CSV Analyst Assistant is an AI-powered data analysis tool that helps users explore and understand CSV datasets without needing to write code.

The application automatically preprocesses a CSV file, profiles the dataset, detects data quality issues, generates useful insights, and uses an LLM layer to explain the results in natural language. The goal is to make data exploration more accessible for business users, students, and non-technical teams.

The project is designed to work with general CSV files, instead of being limited to one specific dataset structure.

## Why this project

I wanted to build something closer to what a Data Scientist, Data Analyst or Data Ops role actually looks like day to day: receiving a dataset, understanding its structure, cleaning it, identifying problems, extracting insights, and making the results understandable for people who do not write Python.

Many real-world data tasks start with a simple CSV file: sales data, customer data, marketing reports, HR data, insurance claims, support tickets, or operational logs. Before building a model or dashboard, the first challenge is usually understanding the dataset itself.

This project focuses on that first important step: turning an unknown CSV file into a clear, structured, and business-readable analysis.

## What it does

- **CSV preprocessing**: cleans column names, removes duplicated rows, and saves a processed version of the dataset.
- **Dataset profiling**: detects the dataset shape, column types, missing values, duplicated rows, numerical statistics, categorical distributions, and date columns.
- **Data quality checks**: highlights missing values, duplicate records, inconsistent column types, and potential outliers.
- **Insight generation**: extracts simple observations from the dataset, such as dominant categories, unusual values, correlations, or possible business trends.
- **LLM explanations**: uses an LLM to turn technical outputs into a clear natural-language summary.
- **Business recommendations**: suggests possible next steps depending on the dataset.
- **Optional visualizations**: generates basic charts for numerical and categorical columns.
- **Streamlit dashboard**: provides an interactive interface to upload a CSV, view the analysis, and ask questions.

The LLM part is intentionally kept as a layer on top of the analytical pipeline. The core analysis is done with Python, pandas, and SQL, while the LLM is used to explain the results in a more readable way.

## Example questions

The assistant should be able to answer questions such as:

- What is this dataset about?
- How many rows and columns does it contain?
- Which columns are numerical, categorical, or dates?
- Are there missing values?
- Are there duplicated rows?
- Which columns seem important?
- What are the main trends?
- Are there any outliers?
- What charts would be useful?
- What business insights can we extract?
- What should I analyze next?

## Pipeline

```text
CSV file
→ preprocessing
→ dataset profiling
→ data quality checks
→ insight generation
→ LLM explanation
→ dashboard / report
```

## Data

The project can be used with different types of CSV datasets, such as:

- insurance claims
- sales data
- customer data
- marketing data
- HR data
- support tickets
- e-commerce orders
- operational logs

The first test dataset is an insurance claims event log, but the project is no longer limited to process mining.

Example columns from the current dataset:

| Column | Description |
|---|---|
| case_id | Unique claim or case identifier |
| activity_name | Activity or step name |
| timestamp | Date and time of the event |
| claimant_name | Name of the claimant |
| agent_name | Name of the agent |
| adjuster_name | Name of the adjuster |
| claim_amount | Amount of the insurance claim |
| claimant_age | Age of the claimant |
| type_of_policy | Type of insurance policy |
| car_make | Car brand |
| car_model | Car model |
| car_year | Car year |
| type_of_accident | Type of accident |
| user_type | Human or RPA |

## Stack

- Python
- pandas
- SQLite
- scikit-learn
- Streamlit
- matplotlib
- Ollama or LLM API
- pytest
- GitHub Actions

## Project structure

```text
ai-csv-analyst-assistant/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── data_preprocessing.py
│   ├── data_profiler.py
│   ├── data_quality.py
│   ├── insight_generator.py
│   ├── chart_generator.py
│   ├── database.py
│   ├── ollama_client.py
│   └── report_generator.py
├── app/
│   └── streamlit_app.py
├── reports/
├── tests/
├── requirements.txt
└── README.md
```

## Status

Work in progress, built over summer 2026 alongside a part-time job.

- [x] Basic CSV preprocessing
- [ ] Generic dataset profiler
- [ ] Data quality checks
- [ ] Automatic insight generation
- [ ] SQLite storage
- [ ] LLM-powered explanations
- [ ] Streamlit dashboard
- [ ] Optional chart generation
- [ ] Tests
- [ ] CI with GitHub Actions

## Next steps

The next priority is to build the generic dataset profiler.

The profiler should automatically detect:

- dataset shape
- column names
- column types
- missing values
- duplicated rows
- numerical columns
- categorical columns
- date columns
- basic statistics
- top values per categorical column
- simple outliers
- possible target columns

After that, the LLM layer will use the profiling output to generate a clear summary and recommendations.

## Future improvements

- Add support for local LLMs through Ollama
- Add a chat interface in Streamlit
- Generate automatic visualizations
- Export analysis reports as Markdown or PDF
- Add optional specialized analysis modes, such as process mining when the dataset contains case, activity, and timestamp columns
- Add Docker support