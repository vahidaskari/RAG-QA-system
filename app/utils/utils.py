import logging
import os
import uuid
import sys

# use pysqlite
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import magic

from app.config.settings import settings
from app.exceptions import (
    FileSizeError,
    TooManyFilesError,
    FileTypeError,
    InternalServerError,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define embedding model for chroma embeddings
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)


async def save_files(documents) -> list:
    """check size and type of files and save them in specified path"""

    if len(documents) > 5:
        raise TooManyFilesError()

    if not os.path.exists(settings.FILE_STORE_PATH):
        # check path exist; if not create it
        os.makedirs(settings.FILE_STORE_PATH)

    paths = []
    for document in documents:
        if document.size > 50000000:  # 50 MB
            raise FileSizeError()

        buffer = await document.read()

        # check file type
        file_format = magic.from_buffer(buffer, mime=True)
        if file_format not in ["application/pdf"]:
            # TODO support more file types
            raise FileTypeError()

        # change name to random id to prevent overwrite existing files
        document_name = str(uuid.uuid4()) + ".pdf"
        file_path = os.path.join(settings.FILE_STORE_PATH, document_name)
        try:
            with open(file_path, "wb") as f:
                f.write(buffer)
            paths.append(file_path)
        except Exception as e:
            logger.error("Error in utils.save_files: %s", e)
            raise InternalServerError() from e
    return paths


async def extract_text(file_paths: list) -> list:
    """combine all files texts together and returns them as a list (modify if seprating files contexts matter)"""

    data = []
    for file_path in file_paths:
        loader = PyMuPDFLoader(file_path)
        pages = loader.load()
        data.extend(pages)
    # TODO remove files from disk if not needed
    return data


async def save_in_chroma(data: list) -> str:
    """
    assign document_id to chunks metadata and add them to chromadb
    returns generated document_id
    """

    document_id = str(uuid.uuid4())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(data)

    for chunk in chunks:
        chunk.metadata["document_id"] = document_id

    Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=settings.CHROMA_PATH,
    )
    return document_id


async def query_chroma(query: str, document_id: str) -> list:
    """search chroma with document_id for user question and returns list of resluts"""

    chroma_db = Chroma(
        persist_directory=settings.CHROMA_PATH,
        embedding_function=embeddings,
    )

    chroma_docs = chroma_db.similarity_search_with_score(
        query=query, k=5, filter={"document_id": document_id}
    )
    return chroma_docs


async def request_llm(context: str, question: str) -> str:
    """format the prompt based on question and context and returns llm answer"""

    # TODO check and improve prompt
    PROMPT_TEMPLATE = """
    Answer the QUESTION using only the provided CONTEXT information. 
    Base your answer solely on the information given; do not use prior knowledge or external references.
    Provide a detailed and accurate response, but keep it concise and focused.
    If the CONTEXT does not provide enough information to answer, state: "The provided context does not contain sufficient information to answer the question."
    
    CONTEXT:
    {context}
    
    QUESTION:
    {question}
    """

    context_text = "\n\n".join([doc.page_content for doc, _score in context])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question)
    model = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY)
    response_text = model.predict(prompt)
    return response_text
