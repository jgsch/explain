# Explain

`explain` is a CLI utility that leverages Large Language Models (LLM) and
vector database to provide comprehensive yet accessible explanations for
research papers. It tries to simplifie academic comprehension, transforming
complex concepts into easy-to-understand language, making scientific research
accessible to a broad audience.

Please note that `explain` is an early-stage and experimental utility. While
it aims to simplify complex academic concepts, the accuracy and depth of
explanations may vary due to its developmental stage and the inherent limitations
of AI technology.

## Setup

- setup conda environment:
  ```bash
  conda create -n explain python=3.10 -y
  conda activate explain
  conda install -y cudatoolkit
  pip install -e .
  ```

- when developing, setup git hooks:
  ```bash
  pre-commit install
  ```

## Usage

```
Usage: explain [OPTIONS] URL

  Explain Arxiv paper with Large Langage Model.

Options:
  -p, --prompt TEXT               Optional prompt to guide the explanation.
  -u, --understanding [BASIC|INTERMEDIATE|ADVANCED]
                                  Level of understanding desired
  --chatbot-model-name TEXT       Model name for the chatbot.
  --embeddings-model-name TEXT    Model name for generating embeddings.
  -v, --verbose                   Enable verbose output.
  --help                          Show this message and exit.
```


## Example

```bash
explain https://arxiv.org/abs/2112.14777
````

```
Ionization of Gravitational Atoms by Daniel Baumann et al., published in  arXiv preprint server
on June 6th, 2022, provides a comprehensive overview  of how electromagnetic radiation could
potentially affect the dynamics of compact objects such as neutron stars and black holes through
interactions with surrounding matter. Specifically, it discusses the possibility of creating
"gravitational atoms" - dense regions of charged particles near the event horizon of a black hole
 - which would emit detectable signals via processes involving light and other forms of
electromagnetic radiation.

The key objective of the research described in the paper is to understand better the physical
mechanisms behind the creation of gravitational atoms and how they might influence the motion
of matter close to the event horizon of a black hole. By combining theoretical modeling with
numerical simulations, researchers hope to gain insight into the nature of spacetime near
extreme conditions and test various predictions made by general relativity. Additionally, the
discovery of gravitational atoms has important practical applications related to detecting
gravitational waves generated during the merger of two black holes or neutron star collisions.
Therefore, studying the properties of gravitational atoms offers significant potential benefits
beyond pure academic curiosity alone.
```
