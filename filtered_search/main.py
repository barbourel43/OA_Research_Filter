import click
import requests
from datetime import datetime
import sys  # Make sure to import sys


@click.command()
@click.option(
    "--keyword",
    prompt="Enter the keyword",
    help="Keyword to search for in OpenAlex works.",
)
@click.option(
    "--year",
    default=2000,
    type=int,
    prompt="Enter the publication year filter",
    help="Filter works to those published on or after this year.",
)
def fetch_top_cited_works(keyword, year):
    """
    Fetches works from OpenAlex based on a keyword, filters them by publication year,
    and returns a list of the top ten most cited works based on citations per year,
    post the specified year.
    """
    # Encode the keyword to handle URL encoding issues
    keyword_encoded = requests.utils.quote(keyword)
    # Prepare the API request URL
    url = f"https://api.openalex.org/works?search={keyword_encoded}&per_page=200"

    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        all_works = response.json()["results"]

        # Get the current year
        current_year = datetime.now().year

        # Filter works based on the publication year and calculate citations per year
        filtered_works = []
        for work in all_works:
            pub_year = work.get("publication_year", current_year)
            if pub_year >= year:
                citations = work.get("cited_by_count", 0)
                years_since_published = max(
                    current_year - pub_year, 1
                )  # Avoid division by zero
                citations_per_year = citations / years_since_published
                filtered_works.append((work, citations_per_year))

        # Sort the filtered works by citations per year in descending order
        filtered_works.sort(key=lambda x: x[1], reverse=True)

        # Display the top ten most cited works
        click.echo(
            f"Top 10 Most Cited Works related to '{keyword}' from {year} onwards, ranked by citations per year:\n"
        )
        for index, (work, citations_per_year) in enumerate(
            filtered_works[:10], start=1
        ):
            title = work.get("display_name", "No Title Available")
            citations = work.get("cited_by_count", 0)
            pub_year = work.get("publication_year", "Year Not Available")
            click.echo(
                f"{index}. {title} - Citations: {citations} (Citations/Year: {citations_per_year:.2f}), Year: {pub_year}\n"
            )
    except requests.HTTPError as e:
        click.echo(f"HTTP Error: {e}")
        sys.exit(1)  # Exit with status 1 on HTTP errors
    except requests.RequestException as e:
        click.echo(f"Request failed: {e}")
        sys.exit(1)  # Exit with status 1 on other request-related errors


if __name__ == "__main__":
    fetch_top_cited_works()
