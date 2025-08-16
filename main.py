#!/usr/bin/env python3
"""
Recipe From Fridge (offline)
Usage:
  python main.py --input "eggs, spinach, cheese"
"""
import argparse, requests, os, sys

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = "llama3.2:4b"
TIMEOUT = 120

def run_llama(prompt):
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("response","").strip()

def build_prompt(items):
    return (
        "You are a recipe assistant. Given the available ingredients, suggest 3 recipes.\n"
        "For each recipe include: Title, Ingredients (list), Steps (numbered).\n"
        f"Available: {items}\n\nPrefer recipes that only use listed items plus common pantry basics (salt, oil, pepper)."
    )

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True)
    args = p.parse_args()
    print(run_llama(build_prompt(args.input)))

if __name__ == "__main__":
    main()
