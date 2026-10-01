import arxiv
import json

client = arxiv.Client()

search = arxiv.Search(
    query = "abs:Transformers AND cat:cs.*",
    max_results = 50,
    sort_by = arxiv.SortCriterion.SubmittedDate,
    sort_order = arxiv.SortOrder.Descending
)

research_papers = []

for r in client.results(search):
    research_papers.append({
        "title": r.title,
        "authors": [author.name for author in r.authors],
        "published": r.published.strftime("%Y-%m-%d"),
        "abstract": r.summary,
        "pdf_url": r.pdf_url
    })

with open("research_papers.json", "w") as file:
    json.dump(research_papers, file, indent = 2)

print(f"Saved {len(research_papers)} research papers to research_papers.json")