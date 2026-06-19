from pathlib import Path

import inspect
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import query
from app.db.database import get_db

router = APIRouter(prefix="/ui", tags=["ui"])

templates_dir = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

def render_template(request: Request, name: str, context: dict) -> HTMLResponse:
    template_response = templates.TemplateResponse
    params = inspect.signature(template_response).parameters
    if "request" in params:
        return template_response(request=request, name=name, context=context)
    return template_response(name=name, context=context)


@router.get("", response_class=HTMLResponse)
def ui_info_clusters(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    clusters_with_counts = query.get_info_clusters_recent_with_counts(db)
    unclustered_articles = query.get_articles_without_info_cluster(db)

    items: list[dict] = []
    for c, articles_count, thumb_url in clusters_with_counts:
        items.append(
            {
                "kind": "cluster",
                "date": c.updated_at,
                "obj": c,
                "articles_count": int(articles_count or 0),
                "thumb_url": thumb_url,
            }
        )
    for a in unclustered_articles:
        items.append({"kind": "article", "date": a.published_at, "obj": a})
    items.sort(key=lambda x: x["date"] or 0, reverse=True)

    return render_template(request, "pages/info_clusters.html", {"request": request, "items": items})


@router.get("/infos/{cluster_id}/articles", response_class=HTMLResponse)
def ui_info_cluster_articles_fragment(
    request: Request, cluster_id: int, db: Session = Depends(get_db)
) -> HTMLResponse:
    cluster = query.get_info_cluster_model_by_id(cluster_id, db)
    if not cluster:
        raise HTTPException(status_code=404, detail="InfoCluster not found")
    articles = query.get_articles_for_info_cluster(cluster_id, db)
    return render_template(
        request,
        "partials/cluster_articles.html",
        {"request": request, "cluster": cluster, "articles": articles},
    )
