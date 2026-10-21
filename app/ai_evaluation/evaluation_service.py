from app.ai_evaluation import judge_model, judge_model_bielik
from app.ai.summary_to_factual_statements import transform_summary_to_factual_statements
from app.db import query
from app.db.models import ArticleEvaluation
from app.ingestion.parser import fetch_article_content
import json

ARTICLE_CONTENT_NOT_FULL_IN_RP = "Czytaj dalej już od"
BIELIK = "bielik"
GPT = "gpt"

def evaluate_articles_faithfulness(db):
    print("Evaluating articles faithfulness")
    articles_not_evaluated_yet = query.get_articles_not_evaluated_yet(db)
    articles_evals = evaluate_articles(model=GPT, articles=articles_not_evaluated_yet)
    save_evals(db, articles_evals)
    print(f"Finished evaluation of {len(articles_evals)} articles.")

def evaluate_articles(model, articles):
    """:return list of articles evaluation in format: [{article.id: judge_result}]"""
    articles_not_able_to_evaluate = []
    evaluated_articles = []
    for article in articles:
        article_content = fetch_article_content(article.url)
        if ARTICLE_CONTENT_NOT_FULL_IN_RP in article_content and "rp.pl" in article.url:
            articles_not_able_to_evaluate.append(
                {"id": article.id, "summary_title": article.summary_title,
                 "reason": "Missing full content of article."})
            continue
        summary_as_statements = transform_summary_to_factual_statements(article.summary_pl)
        all_statements = json.loads(article.claims) + json.loads(summary_as_statements)
        judge_result_raw_string = evaluate_summary_and_claims(model, all_statements, article_content)
        judge_result = json.loads(judge_result_raw_string)
        evaluated_articles.append({article.id: judge_result})
    print("Articles that could not be evaluated: ", articles_not_able_to_evaluate)
    return evaluated_articles

def save_evals(db, articles_evals):
    for article_id in articles_evals:
        judge_result = articles_evals[article_id]
        model_eval_data = None
        is_evaluation_positive = True
        for claim_eval in judge_result:
            if claim_eval.get("potwierdzone") == "nie":
                is_evaluation_positive = False
                model_eval_data = judge_result
                break
            if claim_eval.get("potwierdzone") == "nie wiem":
                is_evaluation_positive = None
                model_eval_data = judge_result
                break
        article_eval = ArticleEvaluation(
            article_id=article_id,
            model_evaluation=model_eval_data,
            is_model_evaluation_positive=is_evaluation_positive,
        )
        db.add(article_eval)
        db.commit()
def evaluate_summary_and_claims(model, statements, article_content):
    judge_result_raw = ""
    if model == BIELIK:
        judge_result_raw = judge_model_bielik.judge_article_faithfulness(article_content, statements)
    elif model == GPT:
        judge_result_raw = judge_model.judge_article_faithfulness(article_content, statements)
    return judge_result_raw