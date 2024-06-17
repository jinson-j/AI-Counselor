# Import HuggingFaceEmbedding class for embedding purposes
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Initialize the embedding model with a specific model version
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Import core functionalities from llama_index
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
# Import Ollama class for language model operations
from llama_index.llms.ollama import Ollama

# Standard library import for JSON operations
import json
# Import JSONalyzeQueryEngine for querying operations
from llama_index.core.query_engine import JSONalyzeQueryEngine

# Define file paths for course and policy data

# Load course data from JSON file
with open('backend/data/cdata.json') as f:
    d = json.load(f)

# Initialize the query engine with loaded data and specific configurations
query_engine = JSONalyzeQueryEngine(
    list_of_dict=d,
    llm= Ollama(model="llama3", request_timeout=900.0),
    verbose=True,
    streaming=True,
)

# Import display utilities from IPython for output formatting
from IPython.display import Markdown, display


# Define a function to call the AI model with a given query
def call_ai(query):
    
    # Prepend a standard instruction to the query
    query = "ONLY TYPE THE SQL QUERY WHEN SEARCHING THE DATABASE.  Here is the question: " + query

    # Execute the query using the initialized query engine
    response = query_engine.query(query)
    # Return the response as a string
    return str(response)
