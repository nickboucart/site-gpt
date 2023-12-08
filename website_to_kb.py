import logging
from urllib.parse import urlparse
import more_itertools
from langchain.document_loaders import UnstructuredURLLoader
from sitemapgrabber import getAllURLsForAWebsite
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models.ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
import vectorstore

model = "mistral"
rag_prompt_template = '''<s>[INST]<<SYS>> You are an professional assistant for question-answering tasks. Answer the question below only using the provided context. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.<</SYS>>
[Contex]t: {context} 
[Question]: {question} 
Answer: [/INST]'''

rag_prompt = PromptTemplate.from_template(rag_prompt_template)

llm = ChatOllama(model=model)
# vectorstore = vectorstore.getVectorStore()


def storeDocsInDb(db, docs):
    logging.info("storing {len(docs)} documents")
    db.add_documents(docs)
    db.persist()


def loadSplitandStoreUrls(db, urls):
    loaders = UnstructuredURLLoader(urls=urls, show_progress_bar=True)
    data = loaders.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0)
    docs = text_splitter.split_documents(data)
    storeDocsInDb(db, docs)


def loadEntireWebsite(db, website, progress):
    urls = getAllURLsForAWebsite(website)
    progress(0, desc="starting download of website...")
    for u in progress.tqdm(more_itertools.batched(urls, 20), desc="Downloading pages of the website"):
        loadSplitandStoreUrls(db, u)
    return "fetched website"


def storeWebsiteInDb(website, progress):
    db = vectorstore.getVectorStore(urlparse(website).netloc)
    return loadEntireWebsite(db, website, progress)


def questionAndAnswer(website, question):
    db = vectorstore.getVectorStore(urlparse(website).netloc)
    rag_chain = {"context": db.as_retriever(
    ), "question": RunnablePassthrough()} | rag_prompt | llm
    return rag_chain.invoke(question)

def pdfQuestion(pdfCollection, question):
    db = vectorstore.getVectorStore(pdfCollection)
    rag_chain = {"context": db.as_retriever(
    ), "question": RunnablePassthrough()} | rag_prompt | llm  
    return rag_chain.invoke(question)
