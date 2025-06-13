import requests
from typing import Optional, List
from pydantic import Field
from langchain.llms.base import LLM  # 假設你有安裝 langchain

class OllamaLLM(LLM):
    api_url: str = Field(...)
    model: str = "llama3.2:1b"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "prompt": prompt,
        }
        response = requests.post(f"{self.api_url}/api/generate", json=payload, headers=headers, stream=True)
        output = ""

        for line in response.iter_lines():
            if line:
                data = line.decode('utf-8')
                import json
                try:
                    chunk = json.loads(data)
                    output += chunk.get("response", "")
                    if chunk.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue
        return output

    @property
    def _llm_type(self) -> str:
        return "ollama"
