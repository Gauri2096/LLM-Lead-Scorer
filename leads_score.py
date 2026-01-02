import csv
import os
import requests
from dotenv import load_dotenv
import re
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"

def build_prompt(company_name: str) -> str:
    return (
         "I'm building a simple SaaS product for small teams that lets them create tasks, "
        "assign them, and track progress on projects.\n"
	"Use ONLY these factors: \n"
        "- Does the company have multiple teams working on internal projects?\n"
        "- Is it likely they already use or need project management tools?\n"
        "- Is the company large enough to pay for team SaaS?\n"
        "Ignore whether task management is part of their own product."
        f'How relevant is "{company_name}" as a potential customer from 1–10? '
        "Give a 1-line reason.\n"
        "Reply in this exact JSON format: "
        '{"score": <number>, "reason": "<short reason>"}'
    )

def call_openrouter(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",  
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-app-or-localhost", 
        "X-Title": "LLM Lead Scorer",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

def extract_json(text: str) -> dict:
    # Grab the first {...} block from the response
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find JSON in: {text}")
    json_str = match.group(0)
    return json.loads(json_str)

def main():
    input_path = "leads.csv"
    output_path = "scored_leads.csv"

    with open(input_path, newline="", encoding="utf-8") as f_in, \
         open(output_path, "w", newline="", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)
        fieldnames = ["Company", "Score", "Reason"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            company = row["Company"]
            prompt = build_prompt(company)
            raw_answer = call_openrouter(prompt)
            print(company, "->", raw_answer)  # still log for debugging

            try:
                parsed = extract_json(raw_answer)
                score = parsed.get("score")
                reason = parsed.get("reason")
            except Exception as e:
                score = ""
                reason = f"Failed to parse: {e}"

            writer.writerow({
                "Company": company,
                "Score": score,
                "Reason": reason,
            })
if __name__ == "__main__":
    main()
