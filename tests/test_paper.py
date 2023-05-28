from argparse import Namespace

import pytest
from arxiv import arxiv

from explain.paper import get_paper, get_paper_id


def test_get_arxiv_id_abs():
    """Test when the url is in the correct format and doesn't end in .pdf."""
    url = "https://arxiv.org/abs/2103.00027"
    assert get_paper_id(url) == "2103.00027"


def test_get_arxiv_id_pdf():
    """Test when the url is in the correct format and ends in .pdf."""
    url = "https://arxiv.org/pdf/2103.00027.pdf"
    assert get_paper_id(url) == "2103.00027"


def test_get_arxiv_id_wrong_domain():
    """Test when the url is not an arxiv.org url."""
    with pytest.raises(ValueError):
        get_paper_id("https://example.com/abs/2103.00027")


def test_get_arvix_paper(mocker):
    """Test for the 'get_arvix_paper' function when the provided id is valid."""

    id = 303

    mocker.patch(
        "arxiv.arxiv.Search.results", return_value=iter([arxiv.Result(entry_id=id)])
    )
    mocker.patch("arxiv.arxiv.Result.download_pdf")

    url = "https://arxiv.org/abs/2103.00027"
    result = get_paper(url, "./papers")

    assert result.entry_id == id


def test_get_arvix_paper_invalid_id(mocker):
    """Test for the 'get_arvix_paper' function when the provided id is invalid."""

    mock_results = mocker.patch("arxiv.arxiv.Search.results")
    feed = Namespace(status="mock", bozo=False, entries=[])
    mock_results.side_effect = arxiv.HTTPError("mock", "mock", feed)

    with pytest.raises(ValueError):
        get_paper("invalid_id", "./papers")
