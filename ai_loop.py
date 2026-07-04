#!/usr/bin/env python3
"""
Simple AI loop.

Usage:
  - Install dependencies: pip install -r requirements.txt
  - To run with local fallback AI (no API key): python ai_loop.py
  - To run using OpenAI (if you have an API key): export OPENAI_API_KEY="sk..." && python ai_loop.py --openai
Type "exit" or "quit" to leave the loop.
"""
import os
import sys

try:
    import openai
except Exception:
    openai = None


def openai_response(prompt):
    if openai is None:
        raise RuntimeError("openai package not installed")
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = key
    # Use the chat completion API if available, otherwise fall back to completion
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            max_tokens=150,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        # Fallback to older Completion API
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
        )
        return resp.choices[0].text.strip()


def local_fallback(prompt):
    # A tiny deterministic "AI" fallback: echo and reverse a bit
    return f"Fallback AI — you said: {prompt} — reversed: {prompt[::-1]}"


def get_ai_response(prompt, use_openai):
    if use_openai:
        try:
            return openai_response(prompt)
        except Exception as e:
            return f"[OpenAI error: {e}] Falling back to local AI.\n{local_fallback(prompt)}"
    else:
        return local_fallback(prompt)


def main():
    use_openai = "--openai" in sys.argv
    print("Starting AI loop. Type 'exit' or 'quit' to stop.")
    if use_openai:
        print("OpenAI mode requested. Ensure OPENAI_API_KEY is set.")
    while True:
        try:
            prompt = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if prompt.lower() in ("exit", "quit"):
            print("Goodbye.")
            break
        if not prompt:
            continue
        response = get_ai_response(prompt, use_openai)
        print(response)


if __name__ == "__main__":
    main()
