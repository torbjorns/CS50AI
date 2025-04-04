import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents) # Extract all links from the HTML file
            pages[filename] = set(links) - {filename} # Remove the filename from the links

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probabilities = dict()
    links = corpus[page]
    num_links = len(links)
    num_pages = len(corpus)

    if num_links == 0:
        # If no links, treat it as if it links to all pages (including itself)
        for p in corpus:
            probabilities[p] = 1 / num_pages
    else:
        for p in corpus:
            if p in links:
                probabilities[p] = damping_factor / num_links + (1 - damping_factor) / num_pages
            else:
                probabilities[p] = (1 - damping_factor) / num_pages

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize page rank values, each one starting at 0
    page_rank = {page: 0 for page in corpus}
    # Choose a random page to start
    page = random.choice(list(corpus.keys()))
    
    # Sample n pages
    for _ in range(n):
        # Increment the page rank of the current page, because we visited it
        page_rank[page] += 1
        # Get the next page according to the transition model
        probabilities = transition_model(corpus, page, damping_factor)
        # Choose the next page according to the probabilities
        page = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]
    
    for page in page_rank:
        # Normalize the page rank values, by dividing by the number of samples
        page_rank[page] /= n
    
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    # Initialize page rank values, each one starting at 1 / N
    page_rank = {page: 1 / num_pages for page in corpus}
    # Create a new dictionary to store the new page rank values
    new_page_rank = page_rank.copy()
    
    # Iterate until convergence - when the difference between the new and old page rank values is less than 0.001
    while True:
        for page in corpus:
            total = 0
            # iterate over all links in the corpus
            for link in corpus:
                # If the page links to the link, add the page rank of the link divided by the number of links in the link
                if page in corpus[link]:
                    total += page_rank[link] / len(corpus[link])
                # If the page doesn't link to any other page, add the page rank of the link divided by the number of pages
                if len(corpus[link]) == 0:
                    total += page_rank[link] / num_pages
            # Calculate the new page rank value for the page
            new_page_rank[page] = (1 - damping_factor) / num_pages + damping_factor * total
        
        # Check for convergence
        if all(abs(new_page_rank[page] - page_rank[page]) < 0.001 for page in page_rank):
            break
        
        # Update the page rank values
        page_rank = new_page_rank.copy()
    
    return page_rank


if __name__ == "__main__":
    main()
