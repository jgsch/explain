from urllib.parse import urlparse

import arxiv


def get_paper_id(url: str) -> str:
    """Extracts the arxiv paper id from the given arxiv URL.

    Args:
        url (str): The URL of the arxiv paper from which to extract the paper id.

    Returns:
        str: The arxiv paper id.

    Raises:
        ValueError: If the provided URL does not have the correct arxiv.org domain.
    """

    parsed_url = urlparse(url)
    if parsed_url.netloc != "arxiv.org":
        raise ValueError(
            f"The provided URL '{url}' is not valid. Please ensure it originates from "
            + "'arxiv.org' and follows this format: 'https://arxiv.org/abs/<PAPER_ID>'."
        )

    id = parsed_url.path.split("/")[-1]
    if id.endswith(".pdf"):
        id = id[:-4]

    return id


def get_paper(url: str, destination: str) -> arxiv.Result:
    """Downloads the arxiv paper associated with the given id.

    Args:
        id (str): The arxiv id of the paper to download.
        destination (str): The location where the downloaded paper should be saved.

    Returns:
        arxiv.Result: An object representing the downloaded arxiv paper.

    Raises:
        ValueError: If the provided id is not associated with an arxiv paper.
    """

    id = get_paper_id(url)

    try:
        paper = next(arxiv.Search(id_list=[id]).results())
    except arxiv.arxiv.HTTPError:
        raise ValueError(
            f"The provided arxiv id '{id}' does not correspond to any "
            + "known papers. Please verify the id and try again."
        )

    paper.download_pdf(filename=destination)

    return paper
