# Think9 Brain

**Cross-Brand Intelligence Engine**

Think9 Brain is a Streamlit proof of concept for a shared intelligence layer where every experiment, meeting, decision and outcome across a portfolio becomes reusable knowledge for every brand.

## The Problem

Knowledge becomes fragmented as brand count grows: insights live in meetings, documents, reports and disconnected team memories.

## The Solution

Think9 Brain centralizes organizational memory, retrieves evidence across brands, identifies portfolio patterns, recommends a next action and preserves the resulting decision.

## Why Agentic

Specialized agents handle ingestion, retrieval, reasoning, decision memory and action. They share one knowledge layer while humans approve consequential actions.

## Core Features

- Premium Intelligence Hub with evidence-backed answers
- Local TF-IDF retrieval with no paid API key required
- TXT/PDF upload and session indexing
- Cross-brand synthesis, recommendations and heuristic confidence
- Decision Memory and Action Center
- Architecture view showing the human-in-the-loop flow

## System Architecture

`data_loader` parses sources, `retrieval` chunks and ranks evidence, `intelligence` applies deterministic portfolio reasoning, and `actions` manages the simulated task queue. The flow is:

**Knowledge → Evidence → Cross-Brand Reasoning → Decision → Action**

## Prototype Demo

The flagship demo connects Brand Gamma's price friction with Brand Alpha's 250 ml pilot and Brand Beta's 17% trial-pack conversion lift, then recommends a controlled 30-day Gamma pilot.

## Demo Questions

- Should Brand Gamma introduce trial-size products?
- What have we learned about price-sensitive consumers?
- Which supply chain risks have appeared across brands?
- What packaging strategies have worked previously?

## Tech Stack

Python, Streamlit, pandas, scikit-learn TF-IDF/cosine similarity, pypdf and python-dotenv.

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Prototype vs Production

Brand Alpha, Brand Beta and Brand Gamma are fictional demonstration brands and all included organizational knowledge is synthetic demo data. Jira, Slack and email execution are simulated. Production would add live connectors, tenant and brand access controls, RBAC, document permissions, audit logs, encryption, enterprise identity, observability and human approval workflows.

## 30-Day MVP Roadmap

- Week 1: Data ingestion and connectors
- Week 2: Knowledge layer and retrieval
- Week 3: Agentic reasoning and decision memory
- Week 4: Enterprise integrations and pilot
