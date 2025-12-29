"""
Author: hamatyo0126

This program provides an execution environment that combines two types of web page
content extraction algorithms and a summarization algorithm.

[Content Extraction Algorithms]
① Readability.js (JavaScript-based content extraction algorithm)
   Requires Node.js (JavaScript runtime) – free
   Node.js installer: https://nodejs.org/ja/download

② Newspaper (Python library for news article extraction)

[Summarization Algorithm]
   Google Gemini (Google's AI assistant)
   API key can be obtained here (free, Google account required):
   https://aistudio.google.com/api-keys

   Edit the ".env" file in the same folder.
   Never share your .env file containing your API key.

[Required Python Libraries]
pip install requests        : Apache License 2.0
pip install newspaper3k     : MIT License
pip install google-genai    : Apache License 2.0
pip install python-dotenv   : BSD 3‑Clause
"""

# System libraries
import sys
from dotenv import load_dotenv
import os

# Readability.js libraries
import subprocess
import json
import requests

# Newspaper library
from newspaper import Article
import re

# Gemini library
from google import genai


# --- Load Gemini API Key ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


# --- URL input ---
print("Starting extraction with Readability.js\n")
url = input("Enter the URL of the article you want to summarize:\n").strip()

dummy_url = "https://en.wikipedia.org/wiki/GitHub"
used_dummy_readability = False


# ============================================================
#  Clean text function (Japanese + English noise removal)
# ============================================================
def clean_text(text):
    """
    Remove common noise phrases from Japanese and English news sites.
    """

    noise_keywords = [
        # Japanese
        "おすすめ",
        "関連記事",
        "人気記事",

        # English - Recommendations
        "Recommended",
        "Recommended for you",
        "You may also like",
        "Suggested",
        "Suggested for you",
        "Editor’s picks",
        "Top picks",

        # English - Related articles
        "Related articles",
        "Related stories",
        "Related content",
        "More on this topic",
        "More like this",
        "In case you missed it",
        "ICYMI",

        # English - Popular articles
        "Popular articles",
        "Most popular",
        "Trending",
        "Trending now",
        "Most read",
        "Top stories",
        "Hot right now",
    ]

    # Remove lines containing noise keywords
    filtered_lines = []
    for line in text.split("\n"):
        if not any(keyword.lower() in line.lower() for keyword in noise_keywords):
            filtered_lines.append(line)

    # Remove very short lines (ads, noise)
    filtered_lines = [line for line in filtered_lines if len(line.strip()) > 20]

    # Remove Wikipedia-style section headers
    filtered_text = "\n".join(filtered_lines)
    filtered_text = re.sub(r"==.*?==", "", filtered_text)

    return filtered_text.strip()


# ============================================================
#  Readability.js extraction
# ============================================================
def extract_with_readability(target_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        html = requests.get(target_url, headers=headers).text

        result = subprocess.run(
            ["node", "extract.js"],
            input=html.encode("utf-8"),
            stdout=subprocess.PIPE
        )

        article = json.loads(result.stdout.decode("utf-8"))
        title = article.get("title") or "Unknown Title"
        text = article.get("textContent") or ""

        if len(text.strip()) < 100:
            return None, None

        return title, text

    except Exception as e:
        print("Readability failed:", e)
        return None, None


# Try extraction with user URL
continue_flag_Readability = 1
title, text = extract_with_readability(url)

# Retry with dummy URL if failed
if not text:
    print("Readability extraction failed. Retrying with dummy URL...")
    title, text = extract_with_readability(dummy_url)
    used_dummy_readability = True

# Dummy also failed
if not text:
    print("Extraction failed even with dummy URL.\n")
    print("Check if Node.js is installed.\n")
    print("Ensure extract.js is in the same folder.\n")
    print("Or contact the script author.\n")
    continue_flag_Readability = 0
else:
    if used_dummy_readability:
        print("Dummy URL extraction succeeded:\n", dummy_url, "\n")
        print("Do you want to summarize the dummy URL using Readability?\n")
        continue_flag_Readability = int(input("Yes:1, No:Other\n").strip())


# Summarize Readability result
if continue_flag_Readability == 1:
    text = "\n".join([line.strip() for line in text.split("\n") if line.strip()])

    print("\nStarting summarization with Gemini (Readability result)...\n")
    prompt = f"""
Summarize the following article in English, in 500 characters or less.
Then summarize the same article in Japanese, in 500 characters or less.

Title: {title}

Content:
{text}
"""
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    print("=== Summary by Readability & Gemini ===")
    print(response.text)
    print("\n")


# ============================================================
#  Newspaper extraction
# ============================================================
print("Do you want to run extraction with Newspaper?")
continue_flag_Newspaper = int(input("Yes:1, No:Other\n").strip())
if continue_flag_Newspaper != 1:
    print("Exiting.")
    sys.exit(0)


def extract_with_newspaper(target_url):
    try:
        article = Article(target_url)
        article.download()
        article.parse()
    except Exception as e:
        print("Newspaper extraction failed. Retrying with dummy URL.", e)
        return None, None

    title = article.title
    text = clean_text(article.text)

    if len(text.strip()) < 100:
        return None, None

    return title, text


# Newspaper extraction
title, text = extract_with_newspaper(url)

# Retry with dummy if failed
if not text:
    print("Newspaper extraction failed. Retrying with dummy URL...")
    title, text = extract_with_newspaper(dummy_url)

    if not text:
        print("Extraction failed even with dummy URL.\n")
        print("Please contact the script author.\n")
        sys.exit(0)
    else:
        print("Dummy URL extraction succeeded:\n", dummy_url, "\n")
        print("Do you want to summarize the dummy URL using Newspaper?\n")
        continue_flag_Newspaper = int(input("Yes:1, No:Other\n").strip())

if continue_flag_Newspaper != 1:
    print("Exiting.")
    sys.exit(0)


# Summarize Newspaper result
print("\nStarting summarization with Gemini (Newspaper result)...\n")
prompt = f"""
Summarize the following article in English, in 500 characters or less.
Then summarize the same article in Japanese, in 500 characters or less.

Title: {title}

Content:
{text}
"""
response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=prompt
)
print("=== Summary by Newspaper & Gemini ===")
print(response.text)
