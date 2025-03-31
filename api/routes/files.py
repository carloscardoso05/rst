from fastapi import APIRouter, Depends
from typing import List, Dict

from db.documents_repository import (
    DocumentsRepository,
    create_documents_repository,
    Document,
)

router = APIRouter()


@router.get("")
def get_files(
    repo: DocumentsRepository = Depends(create_documents_repository),
) -> list[str]:
    return [document.get_filename() for document in repo.documents.values()]


@router.get("/{filename}")
def get_file_by_id(
    filename: str, repo: DocumentsRepository = Depends(create_documents_repository)
) -> Document:
    return repo.documents[filename]


@router.get("/relations/types")
def get_relation_types(
    repo: DocumentsRepository = Depends(create_documents_repository)
) -> List[str]:
    relation_types = set()
    for doc in repo.documents.values():
        for relation in doc.intra_sentential_relations:
            if relation.relname:
                relation_types.add(relation.relname)
    return sorted(list(relation_types))


@router.get("/relations/examples/{relation_type}")
def get_relation_examples(
    relation_type: str, repo: DocumentsRepository = Depends(create_documents_repository)
) -> List[Dict]:
    examples = []
    for doc in repo.documents.values():
        for relation in doc.intra_sentential_relations:
            if relation.relname == relation_type:
                examples.append({
                    "document": doc.get_filename(),
                    "relation": relation
                })
                if len(examples) >= 5:  # Limit to 5 examples per type
                    break
    return examples
