import chromadb
import openai
from dotenv import load_dotenv
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Disable tokenizer parallelism

# Load environment variables from the .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please check your .env file.")

# ChromaDB paths
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="growing_vegetables")

# Get user query
user_query = input("What do you want to know about growing vegetables? \n\n")

# Query ChromaDB
results = collection.query(
    query_texts=[user_query],
    n_results=1,
)

# Ensure results are valid
if not results or not results.get('documents') or not results['documents'][0]:
    print("No relevant information found in the database.")
    exit()


# Create system prompt
system_prompt = f"""
You are a helpful assistant. You answer questions about growing vegetables in 
Florida. But you only answer based on the knowledge I'm providing you.
You don't use your internal knowledge, and you don't make things up.

And give the answer in point format .

If you don't know the answer, you can say "I don't know".

-----------------------------

The data:
"""+str(results['documents'])+"""
"""

# Generate response using GPT-4
response = response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query},
    ],
)
print(system_prompt)
# Print response
print("\n\n-----------------------------------\n\n")
print(response.choices[0].message.content)