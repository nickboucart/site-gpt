Some experiments with (open source) llm's

I use ollama to run llms' locally.

To try things out, I use pyenv to install python and use a virtual environment to manage dependancies.

Install requirements

```bash
pip install -r requirements.txt

```

Run the demo webfrontend

```bash
python web.py

```

This will run a gradio webapp.

There's two tabs:
1. website checker: fill out a website, let the app download the entire website based on their sitemap.xml, split and generate embeddings and store them in a local chroma db. Once done, use the website as a RAG-based Q&A bot
1. pdf bot: similar as the other demo, use the loadPDFs.py script to load all PDFs in a directory and use RAG-based Q&A