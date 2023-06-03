# main.py
from flask import Flask, render_template, request
import openai_wrapper


app = Flask(__name__)
completion_handles = {}       # {user_id: completion_instance}
chat_completion_handles = {}  # {conversation_id: chat_completion_instance}
embedding_handles = {}        # {'api_key': embedding_instance}


# OpenAI Wrapper
@app.route("/openai/completion", methods=["POST"])
def respond_completion():
    """
    Given a prompt, return a predicted completion.
    This is a wrapper of `POST https://api.openai.com/v1/completions`
    """
    api_key = request.values.get('apikey')
    organization = request.values.get('organization')
    user_id = request.values.get('uid')
    user_query = request.values.get('query')
    if user_id not in completion_handles:
        new_completion_handle = openai_wrapper.completion_wrapper(api_key, organization, user_id)
        completion_handles[user_id] = new_completion_handle
    return completion_handles[user_id].respond_completion(user_query)

@app.route("/openai/chat-completion", methods=["POST"])
def respond_chat_completion():
    """
    Given a prompt, return a predicted completion.
    This is a wrapper of `POST https://api.openai.com/v1/chat/completions`
    """
    api_key = request.values.get('apikey')
    organization = request.values.get('organization')
    user_id = request.values.get('uid')
    user_query = request.values.get('query')
    if user_id not in chat_completion_handles:
        new_chat_completion_handle = openai_wrapper.chat_completion_wrapper(api_key, organization)
        chat_completion_handles[user_id] = new_chat_completion_handle
    return chat_completion_handles[user_id].respond_chat_completion(user_query)

@app.route("/openai/embedding")
def embed_text():
    """
    Given a text input, return a vector representation (dense vector) using the model text-embedding-ada-002.
    This is a wrapper of `POST https://api.openai.com/v1/embeddings`
    """
    return "Dummy Response"

# Embed Endpoints
@app.route("/embedding/trip-plan")
def embed_trip_plan():
    """
    Given a trip plan, return its vector representation.
    """
    return "Dummy Response"

@app.route("/embedding/user-query")
def embed_user_query():
    """
    Given a user query, return its vector representation.
    """
    return "Dummy Response"


# Search Endpoints
@app.route("/lexical-search/trip-plans")
def lexical_search_trip_plans():
    """
    Given a user query, return the relevant trip plans using lexical search.
    """
    return "Dummy Response"

@app.route("/semantic-search/trip-plans")
def semantic_search_trip_plans():
    """
    Given a user query, return the relevant trip plans using semantic search.
    """
    return "Dummy Response"

@app.route("/search/trip-plans")
def hybrid_search_trip_plans():
    """
    Given a user query, return the relevant trip plans using hybrid search (combining lexical and semantic search).
    """
    return "Dummy Response"

@app.route("/search/get-generative-answer")
def get_generative_answer():
    """
    Return a generative answer from a user query.
    """
    return "Dummy Response"

@app.route("/search/initial-suggestions")
def get_initial_suggestions():
    """
    Get the initial suggestions when user first clicks into the search bar.
    """
    return "Dummy Response"

@app.route("/search/keyword-completions")
def get_keyword_completions():
    """
    Given a keyword, return the suggested keyword completions.
    """
    return "Dummy Response"

@app.route("/search/results")
def get_consolidated_search_results():
    """
    Return the consolidated responses by `search/trip-plans` and `search/get-generative-answer`.
    """
    return "Dummy Response"

@app.route("/search/compare-trip-plan")
def compare_trip_plan():
    """
    Compare a trip plan to a user query and highlight the similarities.
    """
    return "Dummy Response"


@app.route("/")
def index():
    return "Hello World."


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080
    app.run(host="0.0.0.0", port=PORT, debug=True)
