#
# from app.db import query
# from app.ai_evaluation import judge_model_bielik
# from app.ai_evaluation import judge_model
# from app.ingestion.parser import fetch_article_content
# from app.ai.summary_to_factual_statements import transform_summary_to_factual_statements
# from langchain_openai import OpenAIEmbeddings
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_text_splitters import CharacterTextSplitter
# import chromadb
# from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
# import json
# import os
# from dotenv import load_dotenv
#
# # todo WORKING AS POC BUT RESULTS OF EVALUATION BY CHUNKS NOT SATISFYING. WAITING FOR FURTHER DEVELOPMENT.
#
# load_dotenv()
# OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
# embedding_model = OpenAIEmbeddings(api_key=OPEN_AI_KEY, model='text-embedding-3-small')
#
# global collection
#
# def prep_chroma():
#     client = chromadb.PersistentClient(path="/embeddingsForEval")
#     global collection
#     collection = client.get_or_create_collection(
#         name="embeddings_for_eval",
#         embedding_function=OpenAIEmbeddingFunction(model_name="text-embedding-3-small", api_key=OPEN_AI_KEY)
#     )
#     print("Preparing chroma...")
# prep_chroma()
#
# def semantic_chunk_of_article(text):
#
#     semantic_splitter = SemanticChunker(
#         embeddings=embedding_model,
#         breakpoint_threshold_type="gradient",
#         breakpoint_threshold_amount=0.1
#     )
#     chunks = semantic_splitter.split_text(text)
#     return chunks
#
# def split_text(text):
#     from langchain_text_splitters import CharacterTextSplitter
#     text_splitter = CharacterTextSplitter(
#         separator='\n',
#         chunk_size=500,
#         chunk_overlap=50
#     )
#     return text_splitter.split_text(text)
#
# def embedd_chunks(chunks, article_id, article_topic):
#     ids = []
#     documents = []
#     metadata = []
#     for i, chunk in enumerate(chunks):
#         ids.append(str(article_id) + "-" + str(i))
#         documents.append(chunk)
#         metadata.append({"article_id": article_id, "topic": article_topic})
#     collection.add(ids=ids, documents=documents, metadatas=metadata)
#
# def get_top_3_chunks(statement, article_id):
#     result = collection.query(
#         query_texts=[statement],
#         n_results=3,
#         where={"article_id": article_id}
#     )
#     return result['documents'][0]
#
# def evaluate_statements_faithfulness(all_statements, article_id):
#     full_eval=[]
#     eval_false = False
#     for statement in all_statements:
#         best_matching_text = get_top_3_chunks(statement, article_id)
#         judge_result_raw = judge_model_bielik.judge_article_faithfulness_for_one_statement(best_matching_text, statement)
#         judge_result = json.loads(judge_result_raw.strip())
#         if judge_result.get("potwierdzone") == "nie":
#             print(judge_result)
#             eval_false = True
#         judge_result["zdanie"] = statement
#         full_eval.append(judge_result)
#     if eval_false:
#         print(full_eval)
#
# def evaluate_articles(db):
#     ARTICLE_CONTENT_NOT_FULL_IN_RP = "Czytaj dalej już od"
#     articles_not_evaluated_yet = query.get_articles_not_evaluated_yet(db)
#     articles_not_able_to_evaluate = []
#     for article in articles_not_evaluated_yet:
#         print("Evaluating article: ", str(article.id) + " " + article.summary_title)
#         article_content = fetch_article_content(article.url)
#         if ARTICLE_CONTENT_NOT_FULL_IN_RP in article_content and "rp.pl" in article.url:
#             articles_not_able_to_evaluate.append(
#                 {"id":article.id, "summary_title":article.summary_title, "reason": "Missing full content of article."})
#             continue
#         article_content_chunks = split_text(article_content)
#         embedd_chunks(article_content_chunks, article.id, article.topic)
#         summary_as_statements = transform_summary_to_factual_statements(article.summary_pl)
#         all_statements = json.loads(article.claims) + json.loads(summary_as_statements)
#         evaluate_statements_faithfulness(all_statements, article.id)
#     print("articles_not_able_to_evaluate", articles_not_able_to_evaluate)
