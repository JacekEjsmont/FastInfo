from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import query
from app.ai_evaluation import evaluation_service, evaluation_by_chunks

router = APIRouter(prefix="/evaluation")

@router.post("/evaluate_articles_faithfulness")
def evaluate_articles_faithfulness(db: Session = Depends(get_db)):
    evaluation_service.evaluate_articles_faithfulness(db)
    return {"status": "Faithfulness evaluation finished."}

# @router.post("/evaluate_articles_by_chunks")
# def evaluate_articles_by_chunks(db: Session = Depends(get_db)):
#     evaluation_by_chunks.evaluate_articles(db)
#     return {"status": "Evaluation finished."}

@router.get("/get_all_evaluations")
def get_evaluations(db: Session = Depends(get_db)):
    return query.get_all_articles_evaluations(db)

@router.get("/get_false_evaluations")
def get_false_evaluations(db: Session = Depends(get_db)):
    return query.get_false_evaluations(db)

@router.get("/get_faithfulness_score")
def get_faithfulness_score(db: Session = Depends(get_db)):
    all_evals_count =  query.get_all_articles_evaluations_count(db)
    if all_evals_count <= 0:
        return "Nothing evaluated yet"
    all_articles_count = query.get_all_articles_count(db)
    false_evals = query.get_false_evaluations(db)
    false_percent = len(false_evals) / all_evals_count
    return {"correct_summaries_score": 1 - false_percent, "false_summaries_score": false_percent, "evaluated_summaries_quantity": f"{all_evals_count} from {all_articles_count}"}

