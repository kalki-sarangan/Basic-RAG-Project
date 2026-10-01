import math
import json
from foundry_local_sdk import Configuration, FoundryLocalManager

# Calculating the cosine similarity between two vectors.
def cosine_similarity(vec_a, vec_b):
    dot_product = sum(x * y for x, y in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(y * y for y in vec_b))
    return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0.0

# Find research papers and the scores of the 5 most relevant papers.
def find_relevant_papers(query_embedding, abstract_embeddings, num_papers = 5):
    scores = []
    for i, embedding in enumerate(abstract_embeddings):
        score = cosine_similarity(query_embedding, embedding)
        scores.append((i, score))
    scores.sort(key = lambda x: x[1], reverse = True)
    return scores[:num_papers]

def main():
    # Initializing the SDK
    config = Configuration(app_name = "research_paper_fetcher")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Loading the embedding model
    embedding_model = manager.catalog.get_model("qwen3-embedding-0.6b")
    embedding_model.download()
    embedding_model.load()
    embedding_client = embedding_model.get_embedding_client()

    # Loading the chat model
    chat_model = manager.catalog.get_model("qwen2.5-0.5b")
    chat_model.download()
    chat_model.load()
    chat_client = chat_model.get_chat_client()

    # Load the research papers from the JSON file
    with open("research_papers.json", "r") as file:
        research_papers = json.load(file)

    # Create a list to store the abstracts of the papers
    abstracts = [paper["abstract"] for paper in research_papers]

    # Embedding the abstracts using the embedding model
    abstract_embeddings = []
    for i in range(0, len(abstracts), 10):
        response = embedding_client.generate_embeddings(abstracts[i: min(i + 10, len(abstracts))])
        abstract_embeddings.extend(item.embedding for item in response.data)
    print(f"Embedded {len(abstract_embeddings)} abstracts.")

    print("Enter your question to find relevant research papers:\n")
    print("Type 'exit' to quit the program.\n")
    while True:
        query = input("Question: ").strip()
        if not query or query.lower() == "exit":
            print("Exiting the program.")
            break

        # Embedding the user's question
        query_response = embedding_client.generate_embedding(query)
        query_embedding = query_response.data[0].embedding

        # Retrieving the most relevant research papers based on the user's question
        results = find_relevant_papers(query_embedding, abstract_embeddings)
        context = "\n".join(f"Abstract: {research_papers[i]['abstract']}\n" for i, _ in results)

        # Building prompt with retrieved papers
        messages = [
            {"role": "system",
            "content": (
                "You are a RAG assistant that provides answers based on the context of the research papers provided."
                "If the context doesn't contain enough information to answer the question, inform the user 'The provided abstracts do not contain enough information to answer this.'"
                "Do not invent papers, datasets, dates, benchmarks, authors, or results.'\n\n"
                f"Context:\n{context}"
                )
                        },
            {"role": "user", "content": query}
        ]

        # Chat model's response
        print("Answer: ", end = "", flush = True)
        for chunk in chat_client.complete_streaming_chat(messages):

            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content
            if content:
                print(content, end = "", flush = True)
        print("\n")

    # Clean up
    embedding_model.unload()
    chat_model.unload()
    print("Unloaded models.")

if __name__ == "__main__":
    main()