import glob
import os
from typing import List, Self

from pydantic import BaseModel, computed_field, model_validator

from core.elements import Node, RS3Parser


def find_files_by_name(name: str, directory: str) -> List[str]:
    return glob.glob(f"{directory}/**/{name}.rs3", recursive=True)


def get_all_files(path: str) -> List[str]:
    if not os.path.isdir(path):
        raise NotADirectoryError()
    files = find_files_by_name("*", path)
    return files


class Document(BaseModel):
    file_path: str
    intra_sentential_relations: list[Node] = []

    @property
    @computed_field
    def filename(self) -> str:
        return self.get_filename()

    def get_filename(self) -> str:
        return os.path.basename(self.file_path)

    @model_validator(mode="after")
    def check_file_exists(self) -> Self:
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f'Document at "{self.file_path}" does not exist')
        return self


def document_from_file(file_path: str) -> Document:
    relations = RS3Parser(file_path).get_intra_sentential_relations()
    return Document(file_path=file_path, intra_sentential_relations=relations)


class DocumentsRepository:
    documents: dict[str, Document]

    def __init__(self):
        self.documents = {
            document.get_filename(): document
            for document in [
                document_from_file(file) for file in get_all_files("documents")
            ]
        }


def create_documents_repository() -> DocumentsRepository:
    return DocumentsRepository()
