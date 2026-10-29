
import httpx

# Ollama typically runs locally on port 11434 without needing internet
OLLAMA_URL = "http://localhost:11434/api/generate"

async def query_local_ai(prompt: str, model: str = "llama3") -> str:
    """
    Sends a prompt to a locally running LLM (via Ollama) completely offline.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "No response generated.")
    except httpx.ConnectError:
        return "[GhostGrid Error] Could not connect to local AI engine. Is Ollama running offline?"
    except Exception as e:
        return f"[GhostGrid Error] {str(e)}"

if __name__ == "__main__":
    import asyncio
    # Quick test runner
    async def test():
        print("Testing local AI connection...")
        answer = await query_local_ai("Hello GhostGrid, give a 1-sentence status report.")
        print(answer)
        
    asyncio.run(test())