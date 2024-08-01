from langchain_community.vectorstores.redis import Redis
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# rds = Redis.from_existing_index(embedding=embeddings, index_name="chapter1", schema=)
rds = Redis(
    redis_url="redis://localhost:6379/0", index_name="chapter1", embedding=embeddings
)
retriever = rds.as_retriever()
result = retriever.invoke("핵심 사건이 담겨있는 문서는?")
print(result)
