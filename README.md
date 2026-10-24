# LLM Training Framework: Hands-on Notebooks, Apps and Reading List for Large Language Models

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Hugging Face Transformers](https://img.shields.io/badge/Transformers-FFD21E?logo=huggingface&logoColor=black)](https://github.com/huggingface/transformers)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI_API-412991?logo=openai&logoColor=white)](https://platform.openai.com/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/R0b0t-Maker/LLM-Training-Framework/blob/main/src/Transformers_T1.ipynb)

This repository is a hands-on workspace for learning and prototyping with large language models (LLMs). It contains Google Colab notebooks covering Hugging Face Transformers pipelines, the OpenAI and Gemini APIs, LangChain (prompts, caching, agents, Pinecone retrieval), LlamaIndex and NVIDIA NeMo text-to-speech, a few small Python apps (voice chatbots, a Streamlit chat UI, an image scraper), and a curated folder of foundational LLM papers. Model training and fine-tuning tooling is planned but not yet implemented.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Notebooks](#notebooks)
- [Applications](#applications)
- [Reading List](#reading-list)
- [Roadmap](#roadmap)
- [Evaluation](#evaluation)
- [License](#license)
- [Citation](#citation)

## Overview

The material is organised around four themes:
1. **Model libraries**: Hugging Face `pipeline` tasks (sentiment, emotion classification, summarisation, paraphrasing, conversation, question answering) and open models such as GPT-Neo and GPT-J.
2. **LLM APIs and frameworks**: OpenAI chat completions, Google Gemini through LangChain, LangChain chains and agents, Pinecone vector search, LlamaIndex and Jupyter AI magics.
3. **Applications**: voice assistants built on speech recognition, OpenAI and `pyttsx3`, a Streamlit custom-ChatGPT interface and a Bing image scraper.
4. **Literature**: PDFs of key LLM and NLP papers (Transformers, GPT-3, RAG, ReAct, LoRA, QLoRA, ZeRO and surveys).

Most notebooks were written for Google Colab and read API keys from a `.env` file on Google Drive.

## Key Features
- **Transformers tutorial**: step-by-step pipelines for sentiment analysis, GoEmotions classification, BART summarisation, Pegasus paraphrasing and BlenderBot conversation, with Gradio demos.
- **LangChain walkthrough**: in-memory and SQLite LLM caching, streaming, `PromptTemplate` and `ChatPromptTemplate`, chains, and a ReAct agent with Python REPL, DuckDuckGo and Wikipedia tools.
- **Retrieval-augmented generation**: text splitting, OpenAI embeddings (dimension 1536), embedding cost estimation and Pinecone index creation and querying.
- **Gemini with LangChain**: chat, system prompts, streaming, multimodal input with `gemini-pro-vision` and safety settings.
- **LlamaIndex**: indexing a web page with `SimpleWebPageReader` and `VectorStoreIndex` and querying it.
- **Document assistant**: extracting text from PDFs with PyMuPDF, answering template questions with a question-answering pipeline and writing a filled PDF.
- **Text-to-speech**: NVIDIA NeMo FastPitch + HiFi-GAN synthesis to WAV.
- **Voice chatbot apps**: Tkinter GUIs that listen, query `gpt-3.5-turbo` asynchronously and speak the answer.

## Installation

Clone the repository:
```bash
git clone https://github.com/R0b0t-Maker/LLM-Training-Framework.git
cd LLM-Training-Framework
```

There is no `requirements.txt`. Each notebook installs its own packages in its first cells. For the Python apps in `src/`:
```bash
pip install openai SpeechRecognition pyaudio pyttsx3            # voice chatbots (main*.py)
pip install streamlit streamlit-chat langchain langchain-openai python-dotenv   # Streamlit chat app
pip install requests beautifulsoup4 streamlit pillow             # image scrapers
```

Set the API keys you need as environment variables or in a local `.env` file that is not committed:
```bash
OPENAI_API_KEY=...
GOOGLE_API_KEY=...      # Gemini notebook
PINECONE_API_KEY=...    # Pinecone notebook
```

<!-- TODO: add a requirements.txt; make main*.py read OPENAI_API_KEY from the environment instead of a constant. -->

## Usage

Open a notebook in Google Colab (badge above) or Jupyter:
```bash
jupyter notebook src/Transformers_T1.ipynb
```
Notebooks that use paid APIs expect a `.env` file; update the `load_dotenv(...)` path to your own location.

Run the voice chatbot (set the key inside the script first, see the TODO above):
```bash
python src/main-v003.py
```

Run the Streamlit chat interface:
```bash
streamlit run src/project_streamlit_custom_chatgpt.py
```

Run the image scraper GUI:
```bash
streamlit run src/webscrapperGUI.py
```

## Code Structure
- **`src/`**: notebooks and scripts.
  - Notebooks: `Transformers_T1.ipynb`, `LLM.ipynb`, `T1_OpenAI_API.ipynb`, `chatbot_LangChain.ipynb`, `chatbot_LangChain_Pinecone.ipynb`, `Chatbot_LangChain_Gemini.ipynb`, `LLAMA.ipynb`, `jupyter_ai.ipynb`, `Assistant_v001.ipynb`, `TTS_v001.ipynb`.
  - Voice chatbot apps: `main.py`, `main-v001.py`, `main-v002.py`, `main-v003.py` (latest, commented, themed Tkinter UI).
  - `interface-v001.py`: Tkinter questionnaire for building a user profile for a companion assistant.
  - `project_streamlit_custom_chatgpt.py`: Streamlit chat app with a configurable system role.
  - `wbescrapper.py`, `webscrapperGUI.py`: download images for a search term from Bing (command line and Streamlit GUI with ZIP download).
- **`documents/LLM-papers/`**: 11 numbered papers and guides on LLMs.
- **`documents/useful-paper/`**: 9 further papers (LoRA, QLoRA, ZeRO, GPT-1, embeddings survey and others).
- **`LICENSE`**: MIT licence.

## Notebooks

| Notebook | Content |
| --- | --- |
| `Transformers_T1.ipynb` | Transformers basics: `distilbert-base-uncased-finetuned-sst-2-english` sentiment, `SamLowe/roberta-base-go_emotions`, `facebook/bart-large-cnn` summarisation, `tuner007/pegasus_paraphrase`, `facebook/blenderbot-400M-distill` chatbot and Gradio apps that combine chat with sentiment |
| `LLM.ipynb` | Text generation with open models (GPT-2, GPT-Neo 1.3B, GPT-J 6B) through the `text-generation` pipeline |
| `T1_OpenAI_API.ipynb` | OpenAI chat completions with `gpt-3.5-turbo` and the effect of `max_tokens`, `n` and `temperature` |
| `chatbot_LangChain.ipynb` | LangChain with OpenAI chat models: in-memory and SQLite caching, streaming, prompt templates, `LLMChain`, and a ReAct agent with Python REPL, DuckDuckGo and Wikipedia tools |
| `chatbot_LangChain_Pinecone.ipynb` | Pinecone index management, namespaces, text splitting, OpenAI embeddings, embedding cost, `RetrievalQA` over a text file and spoken answers with Coqui TTS |
| `Chatbot_LangChain_Gemini.ipynb` | `langchain_google_genai` with `gemini-pro` and `gemini-pro-vision`, system prompts, streaming and safety settings |
| `LLAMA.ipynb` | LlamaIndex: load a web page, build a vector index and query it with an OpenAI LLM |
| `jupyter_ai.ipynb` | Jupyter AI `%ai` magics with OpenAI models |
| `Assistant_v001.ipynb` | PDF form filling: find empty fields in a template PDF, answer them from an information PDF with a QA pipeline, export with FPDF |
| `TTS_v001.ipynb` | NeMo `tts_en_fastpitch` + `tts_en_hifigan` speech synthesis |

## Applications

**Voice chatbot (`src/main-v003.py`)**: a Tkinter window with start and stop buttons. A background thread captures microphone audio, transcribes it with Google speech recognition, sends the text to `gpt-3.5-turbo` through the asynchronous OpenAI client, shows the reply in a scrolling text area and speaks it with `pyttsx3`. Listening repeats every second while active. `main.py`, `main-v001.py` and `main-v002.py` are earlier versions of the same app.

**Custom ChatGPT (`src/project_streamlit_custom_chatgpt.py`)**: a Streamlit page with a sidebar for a system role and a user message, using LangChain's `ChatOpenAI` (`gpt-3.5-turbo`, temperature 0.5) and keeping the conversation in `st.session_state`.

**Image scraper (`src/wbescrapper.py`, `src/webscrapperGUI.py`)**: queries Bing Images for a subject, downloads the requested number of images into `images/`, records their source URLs, and in the GUI version offers the images as a ZIP download. Check the terms of use of the source site before scraping.

## Reading List

`documents/LLM-papers/` contains, in reading order:
0. A Compact Guide to LLMs
1. Attention Is All You Need (2017)
2. Language Models are Few-Shot Learners (2020)
3. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (2020)
4. Towards Reasoning in Large Language Models: A Survey (2023)
5. Lost in the Middle: How Language Models Use Long Contexts (2024)
6. ReAct: Synergizing Reasoning and Acting in Language Models
7. A Survey of Large Language Models
8. Large Language Models: A Survey
9. Finetuned Language Models are Zero-Shot Learners
10. Zero-Shot Learning Through Cross-Modal Transfer

`documents/useful-paper/` adds LoRA, QLoRA, ZeRO, "Textbooks Are All You Need", a survey of text representation and embedding techniques, the original GPT language-understanding paper, and second copies of the Transformer, GPT-3 and LLM survey papers.

<!-- TODO: remove duplicate PDFs and consider linking to arXiv instead of redistributing the files. -->

## Roadmap

The following components are planned and not yet in the repository:
- **Data preprocessing**: scripts to clean and prepare datasets for LLM training.
- **Training and fine-tuning**: a configurable trainer and fine-tuning scripts for pre-trained models on custom data.
- **Evaluation metrics**: custom metrics for output quality, efficiency and adaptiveness.
- **Advanced techniques**: reinforcement learning, prompt tuning and transfer learning for domain-specific knowledge.

## Evaluation

The repository does not contain model training or benchmark results. The notebooks demonstrate inference and API usage; the only quantitative outputs are API token counts and embedding cost estimates in `chatbot_LangChain_Pinecone.ipynb`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details. The papers in `documents/` remain the property of their respective authors and publishers and are not covered by this licence.

## Citation

If you find this repository helpful in your research, please cite:

**LLM Training Framework: Hands-on Notebooks, Apps and Reading List for Large Language Models**
Rasoul Sadeghian, December 2023

```bibtex
@misc{sadeghian2023llmtraining,
  author       = {Sadeghian, Rasoul},
  title        = {LLM Training Framework: Hands-on Notebooks, Apps and Reading List for Large Language Models},
  year         = {2023},
  month        = {dec},
  howpublished = {\url{https://github.com/R0b0t-Maker/LLM-Training-Framework}}
}
```
