import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import numpy as np
import google.generativeai as genai
import time


# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration for Pinecone and gemini
pinecone_api_key = os.getenv('PINECONE_API_KEY')
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)

index_name = "journal-entries"
# Check if the index exists, if not, create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name, 
        dimension=384,  # Dimension of embeddings
        metric='cosine',  # Using cosine similarity
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(name=index_name)

# Initialize the Sentence Transformer model only once to improve performance
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """Get the embedding of the text using Sentence Transformers."""
    return model.encode(text)

def add_journal_entry(entry):
    """Add a new journal entry to Pinecone."""
    embedding = get_embedding(entry)
    index.upsert(vectors=[(entry, np.array(embedding).tolist())])  # Ensure the embedding is converted to list
    return "Entry added to the journal!"

def query_journal(query, top_k=15):
    """Query the journal entries from pinecone for relevant entries based on the query."""
    query_embedding = get_embedding(query)
    if isinstance(query_embedding, np.ndarray):
        query_embedding = query_embedding.tolist()  # Convert to list only if it's an ndarray

    try:
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=False
        )
        print(results)
        documents = []
        for match in results['matches']:
            # If the similarity score is less than 0.1 then skip the document (this avoids hallucinations)
            if match['score'] < 0.1:
                continue
            print(match['id'])
            documents.append(match['id'])
        print(documents)
        return documents
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return []


def grader_llm(query, context):   
    '''
    This function uses gemini to summarize the most relevant context retrieved from the journal entries.
    '''
    try:
        introduction = """You are serving as an intelligent pre-processor for a sophisticated journaling chatbot. Your role is to evaluate the context extracted from a user's journal stored in a vector database. Here is what you need to do:

                            1. **Review the Context:** You are provided with snippets of journal entries as context. These entries may contain various details, some of which are more relevant to the user's query than others.

                            2. **Assess Relevance:** Determine which parts of the context are most relevant to the user's query. Focus on identifying key information that will help in answering the user's question effectively.

                            3. **Summarize the Context:** Condense the relevant information into a clear, concise summary. Your summary should streamline the context, making it easier for the final language model (LLM) to understand and use effectively. Avoid unnecessary details that do not contribute to answering the query.

                            4. **Rewrite for Clarity:** Ensure that your summary is written in clear, straightforward language. This step is crucial as the final LLM relies on the clarity of the context you provide to generate an accurate and helpful response.

                            **Instructions:**
                            - Do not answer the query directly.
                            - Provide a summarized context that includes only the relevant details.
                            - Write the summary in a way that any advanced language model can easily understand and use to formulate a response.

                            **Example:**
                            - **Query:** "What should I buy for the upcoming camping trip?"
                            - **Context:** "I need to remember to buy a tent and sleeping bags. Last time I went camping I forgot the tent and had to sleep under the stars. It rained all night. Also, check if the old camping stove is still working."
                            - **Your Task:** Summarize this context to focus only on the essentials for the final LLM: "For the camping trip, purchase a tent and sleeping bags. Verify the condition of the camping stove."

                            Please proceed with summarizing the given context based on the user's query provided.
                        """
        generator_prompt = f"{introduction}\n\nContext: {context}\n\nQuestion: {query}"
        print(generator_prompt)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(generator_prompt)
        return response.text
    
    except Exception as e:
        print("Error generating response:", e)
        return "I'm sorry, I couldn't generate a response at the moment."


def generate_response(query, context): 
    """Generate a response using the Gemini API."""

    try:
        introduction = """**Role:** You are a sophisticated personal assistant powered by advanced AI. Your responses are generated based on the context provided from a user's journal entries. 

                        **Objective:** You are tasked with answering questions by utilizing specific information pulled from the journal entries. Your answers should be informative, directly relevant, and articulated in a manner that is both clear and helpful to the user.

                        **Formatting Instructions:**
                        - **Clarity:** Ensure your responses are straightforward and easy to understand.
                        - **Detail:** Provide detailed answers that are directly supported by the context when available.
                        - **Tone:** Maintain a friendly and professional tone throughout your responses.
                        - **Formatting:** Format answers to make them look presentable and organized.

                        **Guidelines for Response:**
                        - **Relevant Context:** Use the context given from the journal entries to form your answers. If the context directly addresses the query, base your answer on that information.
                        - **No Context Available:** If no relevant context is provided or if the context is insufficient to form a complete answer, respond with: "I'm sorry, I am a Journaling bot and I don't know how to answer that question."

                        **Example Scenario:**
                        - **Question:** "What should I pack for my trip to Paris next week?"
                        - **Provided Context:** "Last trip to Paris, I forgot my charger and adapter, and it was difficult to keep my devices charged."
                        - **Expected Response:** "For your trip to Paris next week, make sure to pack a charger and adapter to keep your devices charged. It might also be wise to check the weather forecast to pack accordingly."

                        **Task:**
                        Given the query and the context from the journal, generate a response that adheres to these instructions. Ensure that your response is not only factually accurate but also practically useful, taking into account any specifics mentioned in the journal entries.
                    """
        generator_prompt = f"{introduction}\n\nContext: {context}\n\nQuestion: {query}\n\n"
        print(generator_prompt)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(generator_prompt)
        return response.text
    
    except Exception as e:
        print("Error generating response:", e)
        return "I'm sorry, I couldn't generate a response at the moment."

def handle_query(query):
    """Handle the query by fetching context and generating a response."""
    relevant_entries = query_journal(query)
    context = ". ".join(relevant_entries)
    grader_context = grader_llm(query, context)
    # Give a 2 sec delay to avoid rate limiting
    time.sleep(2)
    return generate_response(query, grader_context)
