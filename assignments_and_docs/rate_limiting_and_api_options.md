# Pollinations.ai Open-Source Model (openai-fast) Explanation

We integrated the **Pollinations.ai** text generation API in the project to resolve the rate limits and quota blocks encountered on the Google Gemini API. Here is a detailed guide on the model, its capabilities, endpoints, and mitigations.

---

## 1. Model Overview

* **Model Identifier**: `openai-fast` (aliased as `openai`, `gpt-oss`, `gpt-oss-20b`, `ovh-reasoning`)
* **Description**: **GPT-OSS 20B Reasoning LLM**
* **Provider**: Hosted via [Pollinations.ai](https://pollinations.ai/) using OVH Cloud resources.
* **Architecture**: A 20 Billion Parameter Open-Source Transformer Reasoning model.
* **Modalities**: Input: Text, Output: Text.
* **Features**: Supports tool calling/arguments extraction and reasoning tasks.

---

## 2. Key Benefits of the Model

1. **Keyless and Anonymous**:
   Unlike major commercial API providers (Google, OpenAI, Anthropic), you can query this model without registering an account, generating an API key, or managing tokens.
2. **Cost-Free**:
   It is entirely free to query for general developers, hobbyists, and automation agents.
3. **Open-Source Compliance**:
   Uses an open-source model architecture, making it compliant with workspaces prioritizing open-source foundations.

---

## 3. How to Connect (Python API)

You can connect directly via the standard Python `requests` library. No special SDK is required.

### Simple Request Example:
```python
import requests

url = "https://text.pollinations.ai"
payload = {
    "messages": [
        {"role": "system", "content": "You are a professional banking assistant."},
        {"role": "user", "content": "Tell me a short bank joke."}
    ],
    "model": "openai-fast"
}

response = requests.post(url, json=payload, timeout=60)
print(response.text)
```

---

## 4. Rate-Limiting & Crucial Mitigations

Because it is a free, public endpoint, it is heavily monitored and subject to rate limits to prevent script abuse. To ensure stable execution within complex workflows (like LangGraph state transitions), the following mitigations are implemented in our notebook:

### 1. Request Pacing (`time.sleep(10)`)
* **Issue**: Sending consecutive requests within a split second (such as transitioning from `Classifier Node` $\rightarrow$ `Agent Node` $\rightarrow$ `Responder Node`) triggers a `429 Too Many Requests` API block.
* **Fix**: A mandatory `time.sleep(10)` cooldown is inserted at the beginning of each API call. This spaces the requests out and ensures the endpoint handles them smoothly.

### 2. High Connection Timeout (`timeout=60`)
* **Issue**: Under heavy public demand, requests may experience brief server-side network lag, leading to `Read timed out` connection errors.
* **Fix**: The request timeout is set to 60 seconds to allow the backend model sufficient time to complete generation.

### 3. Request Retry Loop
* **Issue**: Temporary network drops.
* **Fix**: The connection logic includes a `try-except` block that retries failed requests up to 3 times before raising a final exception.

---

## 5. Alternative Options (If limits are still hit)

If your project grows and requires faster speed or more parallel requests, you can transition to:
1. **Gemini 1.5 Flash (Paid or Higher Free Quota)**: Register a billing account in Google AI Studio to unlock 1,000+ Requests Per Day (RPD).
2. **Groq API**: Offers high-speed open-source Llama-3 inference for free with an API key registration.
3. **Local Ollama**: Install [Ollama](https://ollama.com/) locally and download a small model (e.g. `llama3` or `qwen2.5:1.5b-instruct`). You can query it offline via `http://localhost:11434/api/generate` with zero cost, zero keys, and infinite quotas.
