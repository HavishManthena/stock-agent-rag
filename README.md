# 🛰️ Multi-Agent Stock Market RAG Router

An advanced Agentic Retrieval-Augmented Generation pipeline using `LlamaIndex` function calling hooks. The system dynamically routes queries between a semantic vector database of company documents and live external market pricing tools.

## ⚡ Architecture Flow
1. **User Query Intake:** Determines processing intent via an LLM function routing layer.
2. **Tool Selection Core:** Auto-evaluates if the data requires semantic file retrieval or raw deterministic data endpoints.
3. **Context Compilation:** Merges discrete tool outputs back into a clean analytical response.

## 🛠️ Installation & Boot Options

```bash
git clone [https://github.com/YOUR_USERNAME/stock-agent-rag.git](https://github.com/YOUR_USERNAME/stock-agent-rag.git)
cd stock-agent-rag
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python app.py
