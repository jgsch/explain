import logging
import os
import sys
from contextlib import contextmanager

from rich.logging import RichHandler


def setup_logging(verbose: bool = False):
    handler = RichHandler(
        show_path=False,
        omit_repeated_times=False,
        log_time_format="[%H:%M:%S]",
        markup=True,
    )

    for package in [
        "arxiv",
        "urllib3",
        "sentence_transformers",
        "httpcore",
        "httpx",
    ]:
        logging.getLogger(package).propagate = False

    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG if verbose else logging.INFO,
        handlers=[handler],
    )


@contextmanager
def no_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout, sys.stdout = sys.stdout, devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
