import os
import requests

from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_community.document_loaders import (
    unstructured,
    UnstructuredAPIFileLoader,
)

from langchain_voyageai import VoyageAIEmbeddings



def embed_document(file):
    elements = unstructured.get_elements_from_api(
        file_path=file,
        api_key=os.getenv("UNSTRUCTURED_API_KEY"),
        api_url=os.getenv("UNSTRUCTURED_API_URL"),
        strategy='hi_res',
        pdf_infer_table_structure=True
    )

    astra_db_store = AstraDBVectorStore(
    collection_name="financial_reports",
    embedding=VoyageAIEmbeddings(voyage_api_key=os.getenv("VOYAGE_API_KEY"), model='voyage-large-2-instruct'),
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT")
    )

    documents = []
    current_doc = None

    for el in elements:
        if el.category in ["Header", "Footer"]:
            continue # skip these
        if el.category == "Title":
            if current_doc is not None:
                documents.append(current_doc)
            current_doc = None
        if not current_doc:
            current_doc = Document(page_content="", metadata=el.metadata.to_dict())
        current_doc.page_content += el.metadata.text_as_html if el.category == "Table" else el.text
        if el.category == "Table":
            if current_doc is not None:
                documents.append(current_doc)
            current_doc = None
    
    astra_db_store.add_documents(documents)

def embed_all(data_folder):
    for file in os.listdir(data_folder):
        embed_document(os.path.join(data_folder, file))
        print(f"Uploaded file {os.path.join(data_folder, file)}")
    print("Done")



if __name__=='__main__':
    load_dotenv()
    embed_all('/Users/justin/Desktop/Everything/Code/financial-reasoning/data')





    