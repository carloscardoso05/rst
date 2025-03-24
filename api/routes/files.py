from fastapi import APIRouter, Depends

from db.documents_repository import (
    DocumentsRepository,
    create_documents_repository,
    Document,
)

router = APIRouter()


@router.get("/")
def get_files(
    repo: DocumentsRepository = Depends(create_documents_repository),
) -> list[str]:
    return [document.get_filename() for document in repo.documents.values()]


@router.get("/{filename}")
def get_file_by_id(
    filename: str, repo: DocumentsRepository = Depends(create_documents_repository)
) -> Document:
    return repo.documents[filename]
