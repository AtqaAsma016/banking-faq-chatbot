# 🏦 Asma — Banking FAQ Chatbot

AI-powered banking assistant for Pakistani bank customers, built with LLaMA 3, LangChain, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.2-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red?logo=streamlit&logoColor=white)

## Setup

```bash
git clone https://github.com/AtqaAsma016/banking-faq-chatbot.git
cd banking-faq-chatbot
pip install -r requirements.txt
cp .env.example .env  # Add your Groq API key
streamlit run app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

## Features
- 20+ curated Pakistani banking FAQs
- Conversation memory for follow-up questions
- Quick question buttons, chat export, session stats
- Islamic banking, NRP accounts, loans, cards & more

## Example Questions
- "How do I open a savings account?"
- "What is the ATM withdrawal limit?"
- "Do you offer Islamic banking?"
- "How do I apply for a home loan?"

## Tech Stack
Python · LangChain · Groq LLaMA 3.3 · Streamlit · python-dotenv
