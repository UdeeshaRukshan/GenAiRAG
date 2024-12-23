from langchain_community.document_loaders import WebBaseLoader
import bs4
import os 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['USER_AGENT'] = 'myagent'
# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Test with a known working URL (e.g., Python docs)
url = ["https://docs.python.org/3/"]
print(f"Loading from URL: {url}")  # Debug: Ensure the URL is correct

loader = WebBaseLoader(
    web_paths=["https://bbc.com"],
    bs_kwargs=dict(
        # Remove SoupStrainer or use a broader filter
        parse_only=None  # Allow parsing all HTML content
    )
)

# Load the documents
try:
    text_documents = loader.load()
    print(text_documents[0].page_content )
except Exception as e:
    print(f"Error loading documents: {e}")
