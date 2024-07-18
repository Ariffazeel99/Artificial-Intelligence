from openai import AsyncAzureOpenAI
import asyncio
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Access the environment variables
AZURE_OPENAI_RESOURCE = os.getenv("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")
USER_AGENT = os.getenv("USER_AGENT")
AZURE_OPENAI_PREVIEW_API_VERSION = os.getenv("AZURE_OPENAI_PREVIEW_API_VERSION")
AZURE_OPENAI_SYSTEM_MESSAGE = ("Assume you are an Expert writer")

AZURE_OPENAI_TEMPERATURE = 0
AZURE_OPENAI_TOP_P = 1.0
AZURE_OPENAI_MAX_TOKENS = 4000
AZURE_OPENAI_STREAM = False

def init_openai_client():
    azure_openai_client = None
    try:
        endpoint = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
        
        # Authentication
        aoai_api_key = AZURE_OPENAI_KEY

        # Deployment
        deployment = AZURE_OPENAI_MODEL
        if not deployment:
            raise Exception("AZURE_OPENAI_MODEL is required")

        # Default Headers
        default_headers = {"x-ms-useragent": USER_AGENT}

        azure_openai_client = AsyncAzureOpenAI(
            api_version=AZURE_OPENAI_PREVIEW_API_VERSION,
            api_key=aoai_api_key,
            default_headers=default_headers,
            azure_endpoint=endpoint,
        )

        return azure_openai_client
    except Exception as e:
        print("Exception in Azure OpenAI initialization", e)
        azure_openai_client = None
        raise e

def prepare_model_args(role, message):
    messages = [{"role": "system", "content": AZURE_OPENAI_SYSTEM_MESSAGE}]
    messages.append({"role": role, "content": message})

    model_args = {
        "messages": messages,
        "temperature": float(AZURE_OPENAI_TEMPERATURE),
        "max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
        "top_p": float(AZURE_OPENAI_TOP_P),
        "stop": None,
        "stream": AZURE_OPENAI_STREAM,
        "model": AZURE_OPENAI_MODEL, 
    }

    return model_args

async def call_model(message):
    azure_openai_client = init_openai_client()
    model_args = prepare_model_args("user", message)
    response = await azure_openai_client.chat.completions.create(**model_args)
    completion = response.choices[0].message.content
    print(completion)
    return completion

if __name__ == "__main__":
    asyncio.run(call_model("tell me a joke"))