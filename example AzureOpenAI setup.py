from openai import AsyncAzureOpenAI
import asyncio

AZURE_OPENAI_RESOURCE=""
AZURE_OPENAI_KEY=""
AZURE_OPENAI_MODEL="gpt-4o"
USER_AGENT = ""
AZURE_OPENAI_PREVIEW_API_VERSION=""
# TODO Change System prompt
AZURE_OPENAI_SYSTEM_MESSAGE = (f"You are a QA bot designed to compare answers provided by a bot and other by an expert. "
                              f"Your task is to analyze both answers and determine if they convey the same context. "
                              f"##'Your response must be either pass or fail'## nothing else just one word."
                              f" exceptions : if answer 1 conatins the documents provided do not contain any specific information and asnswer 2 contains no then pass")

AZURE_OPENAI_TEMPERATURE=0
AZURE_OPENAI_TOP_P=1.0
AZURE_OPENAI_MAX_TOKENS=4000
AZURE_OPENAI_STREAM=False





# Initialize Azure OpenAI Client
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
    model_args = prepare_model_args("user",message)
    response = await azure_openai_client.chat.completions.create(**model_args)
    print(response.choices[0].message.content)


async def main():
    await call_model(f"answer 1 : My car is old and it costs 100 rupee"
                     f"answer 2 : Car is new and it cost 100 dollars" )

asyncio.run(main())
