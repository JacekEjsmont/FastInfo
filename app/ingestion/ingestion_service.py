from app.db.database import SessionLocal
from app.db.models import Article
from app.ingestion.rss import fetch_rss_articles
from app.ingestion.parser import fetch_article_content
from app.ai.summary_service import create_article_summary
import json

def ingest_articles():
    db = SessionLocal()
    print("fetching articles...")
    rss_articles = fetch_rss_articles()

    print("ai summarizing processing...")
    for item in rss_articles:
        exists = db.query(Article).filter(Article.url == item["url"]).first()
        if exists:
            continue
        content = fetch_article_content(item["url"])
        print("title: ", item["title"])
        article_ai_data_raw_string = create_article_summary(content)
        article_ai_data = json.loads(article_ai_data_raw_string)
        if not article_ai_data:
            continue
        summary_pl = article_ai_data.get("summary_pl")
        if not summary_pl:
            continue

        article = Article(
            title=item["title"],
            summary_title=article_ai_data.get("title"),
            img=item["img_url"],
            content=content,
            summary_pl=summary_pl,
            source=item["source"],
            url=item["url"],
            topic=article_ai_data.get("topic"),
            claims=json.dumps(article_ai_data.get("claims")),
        )
        db.add(article)
        db.commit()
    db.close()
