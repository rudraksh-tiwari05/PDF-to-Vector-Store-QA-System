import os
from langchain.vectorstores.cassandra import cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import cassio
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load sensitive information from environment variables
Astra_db_app_token = os.getenv('ASTRA_DB_APP_TOKEN')
Astra_db_id = os.getenv('ASTRA_DB_ID')
open_Api_Key = os.getenv('OPEN_API_KEY')
pdf_file_path = os.getenv('PDF_FILE_PATH', 'path/to/your/file.pdf')

# Ensure all necessary environment variables are set
if not all([Astra_db_app_token, Astra_db_id, open_Api_Key, pdf_file_path]):
    logger.error("Please set the required environment variables: ASTRA_DB_APP_TOKEN, ASTRA_DB_ID, OPEN_API_KEY, PDF_FILE_PATH")
    exit(1)

def read_pdf(file_path):
    try:
        pdf_reader = PdfReader(file_path)
        raw_text = ''
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                raw_text += content
        return raw_text
    except Exception as e:
        logger.error(f"Failed to read PDF file: {e}")
        return ''

def init_cassio():
    try:
        cassio.init(token=Astra_db_app_token, database_id=Astra_db_id)
    except Exception as e:
        logger.error(f"Failed to initialize cassio: {e}")
        exit(1)

def main():
    init_cassio()

    raw_text = read_pdf(pdf_file_path)
    if not raw_text:
        logger.error("No text extracted from the PDF file.")
        return

    llm = OpenAI(openai_api_key=open_Api_Key)
    embedding = OpenAIEmbeddings(openai_api_key=open_Api_Key)

    astra_vector_store = cassandra(
        embedding=embedding,
        table_name='qa_mini_demo',
        session=None,
        keyspace=None,
    )

    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    try:
        astra_vector_store.add_texts(texts[:50])
        logger.info(f"Inserted {len(texts[:50])} headlines")
    except Exception as e:
        logger.error(f"Failed to insert texts into the vector store: {e}")
        return

    astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

    first_question = True
    while True:
        query_text = input("\n Enter your question (or type 'quit' to exit): ").strip() if first_question else input("\n What's your next question (or type 'quit' to exit): ").strip()

        if query_text.lower() == 'quit':
            break
        if query_text == '':
            continue

        first_question = False

        logger.info(f"Question: '{query_text}'")
        try:
            answer = astra_vector_index.query(query_text, llm=LLM).strip()
            logger.info(f"Answer: '{answer}'")
        except Exception as e:
            logger.error(f"Failed to get answer: {e}")
            continue

        logger.info('First Document By Relevance:')
        try:
            for doc, score in astra_vector_store.similarity_search_with_score(query_text, k=4):
                logger.info(f" [{score:.4f}] '{doc.page_content[:84]}...'")
        except Exception as e:
            logger.error(f"Failed to search for similar documents: {e}")

if __name__ == '__main__':
    main()
