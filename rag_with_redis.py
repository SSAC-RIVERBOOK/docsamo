from langchain_community.vectorstores.redis import Redis
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional

from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="rag_with_redis0731"

loader = TextLoader("./folktales/춘향전1편.txt")
documents = loader.load()

text_splitter = CharacterTextSplitter(
    # 텍스트를 분할할 때 사용할 구분자를 지정합니다. 기본값은 "\n\n"입니다.
    # separator=" ",
    # 분할된 텍스트 청크의 최대 크기를 지정합니다.
    chunk_size=1000,
    # 분할된 텍스트 청크 간의 중복되는 문자 수를 지정합니다.
    chunk_overlap=100,
    # 텍스트의 길이를 계산하는 함수를 지정합니다.
    length_function=len,
    # 구분자가 정규식인지 여부를 지정합니다.
    is_separator_regex=False,
)

split_documents = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

rds = Redis.from_documents(documents=split_documents, embedding=embeddings, redis_url="redis://localhost:6379/0", index_name="chapter1")
retriever = rds.as_retriever()
result = retriever.invoke("춘향의 성격을 잘 드러내는 문서는?")
print(result)