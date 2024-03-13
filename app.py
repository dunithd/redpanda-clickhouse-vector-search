import streamlit as st
import clickhouse_connect
from openai import OpenAI
import os

st.title("MeowMunch Reviews")

# client = OpenAI()

# def get_embedding(text, model="text-embedding-3-small"):
#    text = text.replace("\n", " ")
#    return client.embeddings.create(input = [text], model=model).data[0].embedding


# def find_similar(search_term):
#     parameters = {
#         'searchEmbedding': get_embedding(search_term)
#     }

#     query = """
#     FROM reviews2
#     SELECT
#     review, user,
#     cosineDistance(
#         embedding,
#         {searchEmbedding:Array(Float(32))}
#     ) AS score
#     ORDER BY score
#     LIMIT 5
#     """

#     return ch_client.query(query=query, parameters=parameters)

ch_client = clickhouse_connect.get_client(
    host=os.environ.get("CH_HOST"), 
    username='default', 
    password=os.environ.get("CH_PASSWORD"),
    secure=True
)

# result = ch_client.query('SELECT * FROM reviews2 LIMIT 1')

# print(result.column_names)
# print(result.result_rows)

# result = find_similar("small portions")
# for row in result.result_rows:
#     print(row)

result = ch_client.query("""
SELECT review
FROM reviews2
""")

selected_review = st.selectbox(
    'Choose a review',
    [row[0] for row in result.result_rows]
)


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