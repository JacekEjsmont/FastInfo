from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime

info_clusters_articles = Table(
    "info_clusters_articles",
    Base.metadata,
    Column("infocluster_id", Integer, ForeignKey("infoclusters.id")),
    Column("article_id", Integer, ForeignKey("articles.id")),
)

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    summary_title = Column(String)
    img = Column(String)
    content = Column(Text)
    summary_pl = Column(Text)
    summary_eng = Column(Text)
    source = Column(String)
    url = Column(String, unique=True)
    published_at = Column(DateTime, default=datetime.datetime.utcnow)
    actors = Column(Text)
    locations = Column(Text)
    topic = Column(Text)
    claims = Column(Text)
    uncertainties = Column(Text)
    published = Column(Boolean, default=None)
    infoclusters  = relationship("InfoCluster", secondary="info_clusters_articles", back_populates="articles")


class InfoCluster(Base):
    __tablename__ = "infoclusters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    articles = relationship("Article", secondary="info_clusters_articles", back_populates="infoclusters")
    summary = Column(Text, nullable=True)

class ArticleEvaluation(Base):
    __tablename__ = "articleevaluations"
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    model_evaluation = Column(Text)
    is_model_evaluation_positive = Column(Boolean, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)