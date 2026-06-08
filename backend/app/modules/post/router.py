from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.dependencies import get_current_user
from . import schemas, service

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=list[schemas.PostResponse])
def list_posts(db: Session = Depends(get_db)):
    return service.get_posts(db)

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return service.create_post(db, post_data, author_id=current_user.id)