import glob
import vectorstore
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders.blob_loaders import FileSystemBlobLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import website_to_kb as w2kb



def loadPdf(collecction, path_to_pdf):
    vs = vectorstore.getVectorStore(collection=collecction)
    loader = UnstructuredPDFLoader(path_to_pdf)
    data = loader.load()
    print(data)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0)
    docs = text_splitter.split_documents(data)
    w2kb.storeDocsInDb(vs, docs)


def loadPds(collection, path_to_pdfs):
    vs = vectorstore.getVectorStore(collection=collection)
    for pdfName in glob.glob(path_to_pdfs + "/*.pdf"):
        print("Doing " + pdfName)
        loader = UnstructuredPDFLoader(pdfName)
        data = loader.load()
        print(data)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=0)
        docs = text_splitter.split_documents(data)
        w2kb.storeDocsInDb(vs, docs)


if __name__ == "__main__":
    # loadPdf('appsec', 'asvs.pdf')
    loadPds('roadmaps', './roadmaps')