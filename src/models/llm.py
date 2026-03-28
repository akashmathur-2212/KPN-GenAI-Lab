import os
from dotenv import load_dotenv
# from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from src.logging.logger import get_logger
logger = get_logger(__name__)

# Load env variables
load_dotenv()

def setup_models():

    # LLM
    logger.info("Initializing AzureOpenAI client.")

    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT")
    )
    logger.info("AzureOpenAI client initialized successfully.")

    # EMBEDDINGS
    logger.info("Initializing AzureOpenAI Embeddings...")

    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-large",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )
    logger.info("AzureOpenAI Embeddings initialized successfully.")

    return llm, embeddings