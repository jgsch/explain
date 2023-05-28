import click

from explain.teacher import Teacher, Understanding


def create_cli():
    @click.command()
    @click.argument("url")
    @click.option(
        "-p", "--prompt", type=str, help="Optional prompt to guide the explanation."
    )
    @click.option(
        "-u",
        "--understanding",
        type=click.Choice([u.name for u in Understanding], case_sensitive=False),
        help="Level of understanding desired",
    )
    @click.option(
        "--chatbot-model-name",
        type=str,
        default="togethercomputer/RedPajama-INCITE-Chat-3B-v1",
        help="Model name for the chatbot.",
    )
    @click.option(
        "--embeddings-model-name",
        type=str,
        default="hkunlp/instructor-xl",
        help="Model name for generating embeddings.",
    )
    @click.option(
        "-v", "--verbose", is_flag=True, default=False, help="Enable verbose output."
    )
    def cli(
        url, prompt, understanding, chatbot_model_name, embeddings_model_name, verbose
    ):
        """Explain Arxiv paper with Large Langage Model."""
        teacher = Teacher(chatbot_model_name, embeddings_model_name, verbose=verbose)
        teacher.explain(url, understanding, prompt)

    return cli
