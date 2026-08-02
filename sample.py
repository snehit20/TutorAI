print("LOADED CORRECT SAMPLE.PY")
store = {}
chain_cache = {}
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
def build_chain(pdfs, topic=None, use_web=True):
    from langchain_community.document_loaders import PyPDFLoader,WebBaseLoader
    import os
    import re
    from langchain_core.runnables import RunnablePassthrough,RunnableLambda,RunnableParallel
    from langchain_chroma import Chroma
    from langchain_core.output_parsers import StrOutputParser
    from langchain_groq import ChatGroq
    from dotenv import load_dotenv
    from langchain_core.prompts import PromptTemplate
    from tavily import TavilyClient
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    load_dotenv()
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    #memory 
    from langchain.chains import create_history_aware_retriever
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory 
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


    cache_key = (
    (topic or "no_topic")
    + "_"
    + "_".join(sorted(pdfs))
    + f"_web_{use_web}"
    )

    if cache_key in chain_cache:
        print("Using cached chain...")
        return chain_cache[cache_key]
    #Make Knowledge base

    #Pdf content
    docs = []
    for pdf in pdfs:
        loader = PyPDFLoader(f"Data/{pdf}")
        docs.extend(loader.load())
    
    for doc in docs:
        doc.metadata["source"] = "User"
        doc.metadata["priority"] = "More"

# Optional Web Search
    if use_web and topic:

        client = TavilyClient()

        response = client.search(
            query=topic,
            max_results=5
        )

        result = response["results"]

        metadata_lookup = {}

        for dic in result:

            metadata_lookup[dic["url"]] = {
                "source": "web",
                "url": dic["url"],
                "title": dic["title"],
                "score": dic["score"],
                "priority": "Less"
            }

        urls = list(metadata_lookup.keys())

        dc = []

        for i, url in enumerate(urls, start=1):

            print(f"Loading {i}/{len(urls)}: {url}")

            try:

                loader = WebBaseLoader(
                    web_path=[url],
                    requests_kwargs={"timeout": 10}
                )

                doc = loader.load()

                dc.extend(doc)

            except Exception as e:

                print(f"Skipped {url}")
                print(f"Reason: {e}")

        for d in dc:

            s_url = d.metadata["source"]
            d.metadata = metadata_lookup[s_url]

        for d in dc:

            text = d.page_content
            text = re.sub(r"\s+", " ", text)
            d.page_content = text

        docs.extend(dc)

    #chunking
    splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    #vector store
    vector_store = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=f"db/{topic}"
    )

    #retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10}
    )

    #MAIN model
    llm = ChatGroq(model="llama-3.3-70b-versatile",streaming=True)
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Given the chat history and the latest user question,
    rewrite the question so it can be understood without the chat history.

    Do NOT answer the question.
    Only rewrite it if necessary.
    Otherwise return it unchanged."""
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
    llm,
    retriever,
    contextualize_q_prompt
    )

    
    temp="""
        You are an AI Study Tutor.

    Your task is to answer the user's question using ONLY the provided context and conversation history.

    The context may contain information from two types of sources:

    1. User Notes

    * Identified by:
        Source: User
        Priority: More
    * These are the user's personal notes and should always be treated as the primary source of truth.

    2. Web Sources

    * Identified by:
        Source: Web
        URL
        Title
        Score
    * These sources should be used only to supplement, clarify, or expand upon information found in the user's notes.

    Rules:

    * Always prioritize information from User Notes over Web Sources.
    * If both User Notes and Web Sources contain relevant information, answer primarily from the User Notes and then add supporting information from Web Sources.
    * If the answer is not present in the User Notes but is available in the Web Sources, answer using the Web Sources.
    * Do not contradict User Notes with Web Sources.
    * Do not make up information that is not present in the provided context.
    * If the context does not contain enough information to answer the question, clearly state that the information is not available in the provided materials.
    * Use the conversation history to understand follow-up questions such as "explain that", "tell me more", "give an example", or similar references.
    * Do not rely on conversation history as a source of factual information. Use it only to understand what the user is referring to.
    * If the user's question is ambiguous, use the conversation history to infer the most likely meaning.
    * When useful, mention whether the information came from the user's notes or web resources.

    Previous Conversation:
    {chat_history}

    Context:
    {context}

    Question:
    {question}

    Answer:

    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", temp),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}")
    ])

    #fianl context

    def format_context(retrieved_docs):

        user_docs = [
            doc for doc in retrieved_docs
            if doc.metadata["source"] == "User"
        ]

        web_docs = [
            doc for doc in retrieved_docs
            if doc.metadata["source"] == "web"
        ]

        context = "=== USER NOTES ===\n\n"

        context += "\n\n".join(
            doc.page_content for doc in user_docs
        )

        context += "\n\n=== WEB SOURCES ===\n\n"

        context += "\n\n".join(
            doc.page_content for doc in web_docs
        )

        return context

    #chain
    p_chain = RunnableParallel({
        
        "context": (
    {
        "input": RunnableLambda(lambda x: x["question"]),
        "chat_history": RunnableLambda(
            lambda x: x.get("chat_history", [])
        ),
    }
        | history_aware_retriever
        | RunnableLambda(format_context)
    ),
        "question": RunnableLambda(lambda x: x["question"]),
        "chat_history": RunnableLambda(lambda x: x.get("chat_history", []))
    }


    )

    parser = StrOutputParser()

    def get_session_history(session_id):

        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()

        return store[session_id]

    final_chain = p_chain|prompt|llm|parser
    chain_with_history = RunnableWithMessageHistory(
    final_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
    )
    chain_cache[cache_key] = chain_with_history

    return chain_with_history



    
