import tiktoken
import os
from aleph_alpha_client import Client, TokenizationRequest, DetokenizationRequest
from dotenv import load_dotenv

load_dotenv()

def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def num_tokens_from_string_aleph_alpha(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    client = Client(token=os.getenv("AA_TOKEN"))
    params = {
        "prompt": string,
        "tokens": True,
        "token_ids": False
    }
    tokenization_request = TokenizationRequest(**params)
    tokenization_response = client.tokenize(request=tokenization_request, model=f"luminous-{model_name}")
    tokens = tokenization_response.tokens
    return len(tokens)