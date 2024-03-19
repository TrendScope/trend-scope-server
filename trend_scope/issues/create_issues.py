from openai import OpenAI
import scopuscaller as sc
import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from bertopic import BERTopic

from trend_scope.trend_scope.settings import BASE_DIR
from trend_scope.trend_scope.settings import env

csv_directory = os.path.join(BASE_DIR, 'issues')
api_key = env('SCOPOS_KEY')
openai_api_key = env('OPENAI_KEY')

client = OpenAI(api_key=openai_api_key)


def preprocessing(df):
    df = df.dropna(how='any', subset=['abstract'])
    return df


def apply_processing_text(text, command):
    content = f"{text} {command}"
    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a summarizer."},
            {"role": "user", "content": content},
        ]
    )

    processing_text = response.choices[0].message.content.strip()
    return processing_text


def bertopic_analysis(df):
    topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
    topics = topic_model.fit_transform(df['abstract'])

    # 토픽의 주요 단어 출력
    top_n_words = topic_model.get_topic_info()

    print(top_n_words['Name'].tolist())
    return top_n_words['Name'].tolist()
    # top_n_words.to_csv(os.path.join(csv_directory, 'bertopic_result.csv'), index=False)


def rag_analysis(text, keywords):
    vectorstore = DocArrayInMemorySearch.from_texts(
        [text],
        embedding=OpenAIEmbeddings(openai_api_key=openai_api_key))

    retriever = vectorstore.as_retriever()

    template = """Answer the question based only on the following context, and
    Strictly Use ONLY the following pieces of context to answer the question at the end:
    {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    model = ChatOpenAI(openai_api_key=openai_api_key)

    output_parser = StrOutputParser()

    setup_and_retrieval = RunnableParallel(
        {"context": retriever,
         "question": RunnablePassthrough()
         }
    )

    chain = setup_and_retrieval | prompt | model | output_parser

    result = chain.invoke(
        str(keywords) +
        ", 지금 키워드 리스트를 전달했는데 이 키워드를 바탕으로 2024년에 유행할 이머징 이슈 키워드랑 주제 알려줘. 키워드끼리 리스트, 주제끼리 리스트에 담아서 최종적으로 결과 리스트를 만들어 전달해줘.")
    return result


def create_issues(keywords):
    df = sc.get_titles(api_key, keywords, 2023)
    df = sc.get_abstracts(df)

    # 전처리
    df = preprocessing(df)

    # BERTopic
    keywords = bertopic_analysis(df)

    # RAG 분석
    rag_result = rag_analysis(df['abstract'].iloc[0], keywords)
    print(rag_result)
