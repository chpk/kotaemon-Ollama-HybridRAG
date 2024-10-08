# kotaemon + Ollama: HybridRAG (File + GraphRAG)

An open-source clean & customizable RAG UI for chatting with your documents. Built with both end users and
developers in mind.

![Preview](https://raw.githubusercontent.com/Cinnamon/kotaemon/main/docs/images/preview-graph.png)

## Introduction

This project serves as a functional RAG UI for both end users who want to do QA on their
documents and developers who want to build their own RAG pipeline.

- For end users:
  - A clean & minimalistic UI for RAG-based QA.
  - Supports LLM API providers (OpenAI, AzureOpenAI, Cohere, etc) and local LLMs
    (via `ollama` and `llama-cpp-python`).
  - Easy installation scripts.
- For developers:
  - A framework for building your own RAG-based document QA pipeline.
  - Customize and see your RAG pipeline in action with the provided UI (built with <a href='https://github.com/gradio-app/gradio'>Gradio <img src='https://img.shields.io/github/stars/gradio-app/gradio'></a>).
  - If you use Gradio for development, check out our theme here: [kotaemon-gradio-theme](https://github.com/lone17/kotaemon-gradio-theme).

```yml
+----------------------------------------------------------------------------+
| End users: Those who use apps built with `kotaemon`.                       |
| (You use an app like the one in the demo above)                            |
|     +----------------------------------------------------------------+     |
|     | Developers: Those who built with `kotaemon`.                   |     |
|     | (You have `import kotaemon` somewhere in your project)         |     |
|     |     +----------------------------------------------------+     |     |
|     |     | Contributors: Those who make `kotaemon` better.    |     |     |
|     |     | (You make PR to this repo)                         |     |     |
|     |     +----------------------------------------------------+     |     |
|     +----------------------------------------------------------------+     |
+----------------------------------------------------------------------------+
```

## Installation

### For developers (ONLY Local LLMs)

### Ollama OpenAI compatible server (recommended)

Install [ollama](https://github.com/ollama/ollama) and start the application.

Pull your model (e.g):

```
ollama pull mistral-nemo:12b-instruct-2407-q5_K_M
ollama pull nomic-embed-text:latest
```

#### System requirements

1. Python >=3.11

##### If you would like to process files other than .pdf, .html, .mhtml, and .xlsx documents

You will need to install the system dependencies of [unstructured](https://docs.unstructured.io/open-source/installation/full-installation#full-installation). The installations vary by operating system, so please go to the link and follow the instructions there.

#### Without Docker/native installation (recommended)

- Clone and install required packages on a fresh python environment.

```shell
# optional (setup env)
conda create -n kotaemon python=3.11
conda activate kotaemon

# clone this repo
git clone https://github.com/Cinnamon/kotaemon
cd kotaemon

pip install -e "libs/kotaemon[all]"
pip install -e "libs/ktem"

```

- Refer to the .env and settings.yaml files in the ./extras/ folder of this project. Modify these files accordingly based on your requirements.

The .env file is there to serve use cases where users want to pre-config the models before starting up the app (e.g. deploy the app on HF hub). The file will only be used to populate the db once upon the first run, it will no longer be used in consequent runs.

- (Optional) To enable in-browser PDF_JS viewer, download [PDF_JS_DIST](https://github.com/mozilla/pdf.js/releases/download/v4.0.379/pdfjs-4.0.379-dist.zip) and extract it to `libs/ktem/ktem/assets/prebuilt`

<img src="https://raw.githubusercontent.com/Cinnamon/kotaemon/main/docs/images/pdf-viewer-setup.png" alt="pdf-setup" width="300">

- Start the web server:

```shell
python app.py
```

The app will be automatically launched in your browser.

Default username / password are: `admin` / `admin`. You can setup additional users directly on the UI.

![Chat tab](https://raw.githubusercontent.com/Cinnamon/kotaemon/main/docs/images/chat-tab.png)

- Check the Resources tab and LLMs and Embeddings and ensure that your `api_key` value is set correctly from your `.env`. file. If it is not set, you can set it here.

## Setup local models (for local / private RAG)

See [Local model setup](docs/local_model.md).

## Customize your application

By default, all application data are stored in `./ktem_app_data` folder. You can backup or copy this folder to move your installation to a new machine.

For advance users or specific use-cases, you can customize those files:

- `flowsettings.py`
- `.env`

### `flowsettings.py`

This file contains the configuration of your application. You can use the example
[here](flowsettings.py) as the
starting point.

<details>

<summary>Notable settings</summary>

```
# setup your preferred document store (with full-text search capabilities)
KH_DOCSTORE=(Elasticsearch | LanceDB | SimpleFileDocumentStore)

# setup your preferred vectorstore (for vector-based search)
KH_VECTORSTORE=(ChromaDB | LanceDB | InMemory | Qdrant)

# Enable / disable multimodal QA
KH_REASONINGS_USE_MULTIMODAL=True

# Setup your new reasoning pipeline or modify existing one.
KH_REASONINGS = [
    "ktem.reasoning.simple.FullQAPipeline",
    "ktem.reasoning.simple.FullDecomposeQAPipeline",
    "ktem.reasoning.react.ReactAgentPipeline",
    "ktem.reasoning.rewoo.RewooAgentPipeline",
]
)
```

</details>

### `.env`

This file provides another way to configure your models and credentials.

<details markdown>

<summary>Configure model via the .env file</summary>

Alternatively, you can configure the models via the `.env` file with the information needed to connect to the LLMs. This file is located in
the folder of the application. If you don't see it, you can create one.

Currently, the following providers are supported:

#### OpenAI

In the `.env` file, set the `OPENAI_API_KEY` variable with your OpenAI API key in order
to enable access to OpenAI's models. There are other variables that can be modified,
please feel free to edit them to fit your case. Otherwise, the default parameter should
work for most people.

```shell
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=<your OpenAI API key here>
OPENAI_CHAT_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDINGS_MODEL=text-embedding-ada-002
```

#### Azure OpenAI

For OpenAI models via Azure platform, you need to provide your Azure endpoint and API
key. Your might also need to provide your developments' name for the chat model and the
embedding model depending on how you set up Azure development.

```shell
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-35-turbo
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT=text-embedding-ada-002
```

#### Local models

##### Using ollama OpenAI compatible server

Install [ollama](https://github.com/ollama/ollama) and start the application.

Pull your model (e.g):

```
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

Set the model names on web UI and make it as default.

![Models](https://raw.githubusercontent.com/Cinnamon/kotaemon/main/docs/images/models.png)

##### Using GGUF with llama-cpp-python

You can search and download a LLM to be ran locally from the [Hugging Face
Hub](https://huggingface.co/models). Currently, these model formats are supported:

- GGUF

You should choose a model whose size is less than your device's memory and should leave
about 2 GB. For example, if you have 16 GB of RAM in total, of which 12 GB is available,
then you should choose a model that takes up at most 10 GB of RAM. Bigger models tend to
give better generation but also take more processing time.

Here are some recommendations and their size in memory:

- [Qwen1.5-1.8B-Chat-GGUF](https://huggingface.co/Qwen/Qwen1.5-1.8B-Chat-GGUF/resolve/main/qwen1_5-1_8b-chat-q8_0.gguf?download=true):
  around 2 GB

Add a new LlamaCpp model with the provided model name on the web uI.

</details>

## Adding your own RAG pipeline

#### Custom reasoning pipeline

First, check the default pipeline implementation in
[here](libs/ktem/ktem/reasoning/simple.py). You can make quick adjustment to how the default QA pipeline work.

Next, if you feel comfortable adding new pipeline, add new `.py` implementation in `libs/ktem/ktem/reasoning/` and later include it in `flowssettings` to enable it on the UI.

#### Custom indexing pipeline

Check sample implementation in `libs/ktem/ktem/index/file/graph`

(more instruction WIP).

## Developer guide

Please refer to the [Developer Guide](https://cinnamon.github.io/kotaemon/development/)
for more details.

## Star History

<a href="https://star-history.com/#Cinnamon/kotaemon&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Cinnamon/kotaemon&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Cinnamon/kotaemon&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Cinnamon/kotaemon&type=Date" />
 </picture>
</a>
