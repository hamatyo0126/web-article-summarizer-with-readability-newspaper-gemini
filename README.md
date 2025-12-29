# web-article-summarizer-with-readability-newspaper-gemini
A web article summarizer using Readability.js, Newspaper3k, and Gemini.  
Extracts content and generates English/Japanese summaries.

Author: hamatyo0126

## Overview
This program provides an execution environment that combines two types of web page
content extraction algorithms and a summarization algorithm.

## Content Extraction Algorithms
① **Readability.js** (JavaScript-based content extraction algorithm)  
   Requires Node.js (JavaScript runtime) – free  
   Node.js installer: https://nodejs.org/ja/download

② **Newspaper** (Python library for news article extraction)

## Summarization Algorithm
**Google Gemini** (Google's AI assistant)  
API key can be obtained here (free, Google account required):  
https://aistudio.google.com/api-keys

Edit the `.env` file in the same folder.  
**Never share your `.env` file containing your API key.**

## Required Python Libraries
```
pip install requests
pip install newspaper3k
pip install google-genai
pip install python-dotenv
```

## Environment File (.env)
Create a file named `.env` in the same directory as the script and add your Gemini API key:

```
GEMINI_API_KEY=xxxxxxx   # Replace xxxxxxx with your actual API key
```

**Important:**  
Never share your `.env` file with anyone.  
It contains your personal API key and must remain private.
```



```
# web-article-summarizer-with-readability-newspaper-gemini（日本語版 README）

Web記事を Readability.js、Newspaper3k、Gemini を使って抽出・要約するツールです。  
英語と日本語の要約を自動生成します。

Author: hamatyo0126

## 概要
このプログラムは、2種類の Web ページ抽出アルゴリズムと Gemini による要約機能を組み合わせた実行環境を提供します。

## コンテンツ抽出アルゴリズム
① **Readability.js**（JavaScript ベースの抽出アルゴリズム）  
　Node.js（無料）が必要  
　Node.js インストーラ: https://nodejs.org/ja/download

② **Newspaper**（Python のニュース記事抽出ライブラリ）

## 要約アルゴリズム
**Google Gemini**（Google の AI アシスタント）  
API キーは以下から取得できます（無料、Google アカウントが必要）：  
https://aistudio.google.com/api-keys

同じフォルダにある `.env` ファイルを編集して API キーを設定してください。  
**API キーを含む `.env` ファイルは絶対に他人と共有しないでください。**

## 必要な Python ライブラリ
```
pip install requests
pip install newspaper3k
pip install google-genai
pip install python-dotenv
```

## .env ファイルの作成方法
スクリプトと同じディレクトリに `.env` という名前のファイルを作成し、以下のように Gemini API キーを記述します。

```
GEMINI_API_KEY=xxxxxxx   # xxxxxxx をあなたの API キーに置き換えてください
```

**重要:**  
`.env` ファイルはあなたの個人 API キーを含むため、絶対に他人と共有しないでください。

---
