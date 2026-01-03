# LLM Lead Scorer

A small Python project that uses an LLM (via the OpenRouter API) to score how good a fit each company is for a simple task-and-project management SaaS, reading from a CSV and writing scores back to a CSV.

---

## Features

- Reads company names from `leads.csv`.
- Sends a structured scoring prompt for each company to an LLM.
- Expects a JSON response with `score` (1–10) and `reason`.
- Writes `Company, Score, Reason` into `scored_leads.csv`.
- Loads the OpenRouter API key from a local `.env` file.

---

## Project Structure

- `score_leads.py` – Main script (reads CSV, calls API, parses JSON, writes output).
- `leads.csv` – Input list of companies (single `Company` column).
- `scored_leads.csv` – Generated output with scores and reasons.
- `.env` – Contains your `OPENROUTER_API_KEY` (not committed to git).
- `requirements.txt` – Python dependencies.

---

## Setup

1. **Clone the repository**

   ```
   git clone https://github.com/<your-username>/llm-lead-scorer.git
   cd llm-lead-scorer
   ```

2. **(Optional) Create and activate a virtual environment**

   ```
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**

   In the project root, create a file named `.env`:

   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

   The script uses `python-dotenv` to load this environment variable at runtime.

---

## Usage

1. Make sure `leads.csv` exists, for example:

   ```csv
   Company
   Stripe
   Swiggy
   Byju's
   ```

2. Run the script:

   ```
   python score_leads.py
   ```

3. Check `scored_leads.csv` for output similar to:

   ```csv
   Company,Score,Reason
   Stripe,9,"Stripe operates in a fast-paced tech environment with multiple projects and teams, making task management essential for their operations."
   ```

---

## Customization

- Edit the prompt inside `score_leads.py` to change:
  - The type of SaaS (e.g., CRM, invoicing).
  - The scoring criteria or scale.
- Change the model name to use a different LLM available via OpenRouter.
- Add or remove companies in `leads.csv` to score different leads.

---

