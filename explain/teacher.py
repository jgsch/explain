import logging
import tempfile
import textwrap
import time
import warnings
from enum import Enum

import torch
import transformers
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant

from explain import utils
from explain.paper import get_paper

warnings.filterwarnings("ignore")

log = logging.getLogger("teacher")


class Understanding(Enum):
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3


class Teacher:
    def __init__(
        self,
        chatbot_model_name: str = "togethercomputer/RedPajama-INCITE-Chat-3B-v1",
        embeddings_model_name: str = "hkunlp/instructor-xl",
        verbose: bool = True,
    ):
        utils.setup_logging(verbose)

        self.embeddings = self._get_embeddings(embeddings_model_name)
        self.llm = self._get_llm(chatbot_model_name)

    def _get_embeddings(self, model_name: str):
        start = time.time()

        with utils.no_stdout():
            embeddings = HuggingFaceInstructEmbeddings(
                model_name=model_name,
                model_kwargs={"device": "cuda"},
            )

        log.debug(f"Embeddings model loaded (in {time.time() - start:.2f} secs)")

        return embeddings

    def _get_llm(self, model_name: str):
        start = time.time()

        tokenizer = transformers.AutoTokenizer.from_pretrained(model_name, fast=True)

        streamer = transformers.TextStreamer(tokenizer, skip_prompt=True)

        with utils.no_stdout():
            model = transformers.AutoModelForCausalLM.from_pretrained(
                model_name,
                load_in_8bit=True,
                torch_dtype=torch.float16,
                device_map="auto",
            )

        pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            streamer=streamer,
            max_length=2048,
            temperature=0,
            top_p=0.95,
            repetition_penalty=1.15,
        )

        log.debug(f"LLM loaded (in {time.time() - start:.2f} secs)")

        return HuggingFacePipeline(pipeline=pipeline)

    def explain(
        self,
        url: str,
        understanding: Understanding = Understanding.BASIC,
        prompt: str | None = None,
    ):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as temp:
            paper = get_paper(url, temp.name)
            log.debug(f"paper title: {paper.title}")

            document = PyPDFLoader(temp.name).load()
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            doc = splitter.split_documents(document)
            log.debug("paper splitted")

        vector_store = Qdrant.from_documents(
            doc,
            self.embeddings,
            location=":memory:",
            collection_name="explain",
        )
        retriever = vector_store.as_retriever()
        log.debug("paper loaded in database")

        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False,
        )

        if prompt is None:
            understanding = understanding.name.lower()  # type: ignore
            log.debug(f"target understanding of the topic: {understanding}")

            prompt = f"""
            I'd like a detailed explanation of the research paper titled '{paper.title}'.

            My current understanding of the subject is {understanding}. Please tailor the
            explanation to this level.

            Could you provide the following:
            1. Information about the authors and their affiliations
            2. A summary of the abstract
            3. Key objectives of the research
            4. The methodology used
            5. The findings/results of the paper
            6. The conclusion and implications of the study

            Any critiques or points of discussion that are noteworthy. In particular,
            if there are any unique or novel techniques or concepts introduced in this
            paper, please elaborate on those.
            """
            prompt = textwrap.dedent(prompt)

        log.debug(f"prompt:\n{prompt}")

        qa(prompt)


if __name__ == "__main__":
    teacher = Teacher()
    teacher.explain("https://arxiv.org/abs/2112.14777")
