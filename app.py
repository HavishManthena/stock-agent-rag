import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import FunctionCallingAgentWorker

# Secure API Token Initialization
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-key-here")

# Mock External Live Stock Market API Tool
def get_live_stock_price(ticker: str) -> str:
    """Fetches real-time market data valuation parameters for a given stock ticker asset."""
    # In a full production build, you would hook this up to Alpha Vantage, Yahoo Finance, etc.
    market_matrix = {
        "AAPL": {"price": "$185.40", "volume": "52M", "trend": "+1.2%"},
        "TSLA": {"price": "$178.20", "volume": "84M", "trend": "-2.4%"},
        "NVDA": {"price": "$915.00", "volume": "41M", "trend": "+5.8%"}
    }
    ticker_upper = ticker.upper()
    if ticker_upper in market_matrix:
        data = market_matrix[ticker_upper]
        return f"Live data for {ticker_upper}: Price={data['price']}, Vol={data['volume']}, Daily Trend={data['trend']}"
    return f"Ticker {ticker_upper} not found in live liquidity pools."

def setup_agentic_rag():
    # 1. Create directory and dummy structural data for internal files
    os.makedirs("./company_profiles", exist_ok=True)
    with open("./company_profiles/nvidia_profile.txt", "w") as f:
        f.write("NVIDIA Corporation Internal Strategy Document:\n"
                "- Core Focus: Next-gen Blackwell GPU architecture pipelines.\n"
                "- Risk Assessment: Supply chain bottlenecks in advanced packaging arrays.\n"
                "- Investment Runway: Allocated $4.2B into AI data center infrastructure nodes.")

    # 2. Build the standard RAG Knowledge Base over files
    documents = SimpleDirectoryReader("./company_profiles").load_data()
    vector_index = VectorStoreIndex.from_documents(documents)
    rag_query_engine = vector_index.as_query_engine()

    # 3. Wrap the RAG engine and Live API into Agent Tools
    tools = [
        QueryEngineTool(
            query_engine=rag_query_engine,
            metadata=ToolMetadata(
                name="company_knowledge_base",
                description="Accesses internal strategy, risks, and institutional data files."
            )
        ),
        # Wrap our Python function as an agent tool
        QueryEngineTool.from_defaults(
            fn=get_live_stock_price,
            name="live_market_ticker_api",
            description="Fetches live market spot pricing and trading volume indexes."
        )
    ]

    # 4. Instantiate the intelligent routing Agent Worker
    agent = FunctionCallingAgentWorker.from_tools(tools, verbose=True).as_agent()
    return agent

if __name__ == "__main__":
    stock_agent = setup_agentic_rag()
    
    # Test Question 1: Forces the agent to route to the Live API tool
    print("\n🚀 Executing Live Market Query...")
    stock_agent.chat("What is the current live price and volume trend for NVDA?")
    
    # Test Question 2: Forces the agent to route to the RAG Knowledge Base tool
    print("\n🚀 Executing Internal Document Query...")
    stock_agent.chat("What are the internal risks mentioned regarding NVIDIA's GPU supply chain?")
