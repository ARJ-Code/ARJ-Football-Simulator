import json
from llamaapi import LlamaAPI
from dotenv import load_dotenv
import os

load_dotenv()

llama_api_key = os.getenv('LLAMA_API_KEY')

llama = LlamaAPI(llama_api_key)


def query(prompt: str):
    api_request_json = {
        "messages": [
            {"role": "user", "content": prompt},
        ],
    }

    response = llama.run(api_request_json)

    return response.json()['choices'][0]['message']['content']
