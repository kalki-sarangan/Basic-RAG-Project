import arxiv
import json

client = arxiv.Client()

# Arxiv search filters to filter 50 recent research papers related to Transformers in the field of computer science
search = arxiv.Search(
    query = "abs:Transformers AND cat:cs.*",
    max_results = 50,
    sort_by = arxiv.SortCriterion.SubmittedDate,
    sort_order = arxiv.SortOrder.Descending
)

# List to store some information about the selected research papers
research_papers = []

# Loop through the results of the search and add relevant information about a paper to the list of research papers
for r in client.results(search):
    research_papers.append({
        "title": r.title,
        "authors": [author.name for author in r.authors],
        "published": r.published.strftime("%Y-%m-%d"),
        "abstract": r.summary,
        "pdf_url": r.pdf_url
    })

# Save the list of information regarding research papers to a JSON file
with open("research_papers.json", "w") as file:
    json.dump(research_papers, file, indent = 2)

print(f"Saved {len(research_papers)} research papers to research_papers.json")