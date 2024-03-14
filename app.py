import streamlit as st
import clickhouse_connect
from openai import OpenAI
import os

st.title("MeowMunch Reviews")

client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


def find_similar(search_embedding):
    parameters = {
        'searchEmbedding': search_embedding
    }

    query = """
    FROM reviews2
    SELECT
    review, user,
    cosineDistance(
        embedding,
        {searchEmbedding:Array(Float(32))}
    ) AS score
    ORDER BY score
    LIMIT 5
    """

    return ch_client.query_df(query=query, parameters=parameters)

ch_client = clickhouse_connect.get_client(
    host=os.environ.get("CH_HOST"), 
    username='default', 
    password=os.environ.get("CH_PASSWORD"),
    secure=True
)

st.header("Popular phrases")

result = ch_client.query_df("""
WITH topArticles AS
    (
        SELECT tokens(review) AS textTokens
        FROM reviews2
    )
SELECT
    arrayJoin(if(length(textTokens) < 3, [textTokens], arrayShingles(textTokens, 3))) AS shingle,
    count()
FROM topArticles
WHERE numberOfStopWords(shingle) <= 1 AND not startsOrEndsWithStopWord(shingle)
GROUP BY ALL
ORDER BY count() DESC
LIMIT 10
""")
st.dataframe(result, hide_index=True)


st.header("Find similar reviews")

result = ch_client.query("""
SELECT review
FROM reviews2
""")

selected_review = st.selectbox(
    'Choose a review',
    [row[0] for row in result.result_rows]
)

with st.spinner('Wait for it...'):
    result = ch_client.query_df("""
    SELECT
        review,
        user,
        cosineDistance(embedding, getEmbedding({selectedReview:String})) AS score
    FROM reviews2
    ORDER BY score ASC
    LIMIT 10
    """, parameters={"selectedReview": selected_review})
    st.dataframe(result, hide_index=True)

st.header("Search reviews")
search_term = st.text_input('Search term')

if search_term:    
    with st.spinner('Wait for it...'):
        search_embedding = get_embedding(search_term)

        result = find_similar(search_embedding)
        st.dataframe(result, hide_index=True)
