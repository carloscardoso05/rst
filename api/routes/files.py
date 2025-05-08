from fastapi import APIRouter, Depends
from typing import List, Dict, Any

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
) -> Dict:
    doc = repo.documents[filename]
    return {
        "filename": doc.get_filename(),
        "full_text": doc.get_full_text(),
        "intra_sentential_relations": doc.intra_sentential_relations
    }


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


@router.get("/relations/grouped")
def get_grouped_relations(
    repo: DocumentsRepository = Depends(create_documents_repository)
) -> Dict[str, Any]:
    """
    Returns relations grouped by signal type, subtype, and relation name.
    """
    grouped_relations = {}
    
    for doc in repo.documents.values():
        for node in doc.intra_sentential_relations:
            if node.relname and hasattr(node, 'signals') and node.signals:
                for signal in node.signals:
                    signal_type = signal.type or "No Type"
                    signal_subtype = signal.subtype or "No Subtype"
                    relation_name = node.relname
                    
                    # Create the nested structure if it doesn't exist
                    if signal_type not in grouped_relations:
                        grouped_relations[signal_type] = {}
                        
                    if signal_subtype not in grouped_relations[signal_type]:
                        grouped_relations[signal_type][signal_subtype] = {}
                        
                    if relation_name not in grouped_relations[signal_type][signal_subtype]:
                        grouped_relations[signal_type][signal_subtype][relation_name] = 0
                        
                    # Increment the count
                    grouped_relations[signal_type][signal_subtype][relation_name] += 1
            elif node.relname:
                # Handle nodes without signals
                signal_type = "No Signal"
                signal_subtype = "No Signal"
                relation_name = node.relname
                
                if signal_type not in grouped_relations:
                    grouped_relations[signal_type] = {}
                    
                if signal_subtype not in grouped_relations[signal_type]:
                    grouped_relations[signal_type][signal_subtype] = {}
                    
                if relation_name not in grouped_relations[signal_type][signal_subtype]:
                    grouped_relations[signal_type][signal_subtype][relation_name] = 0
                    
                grouped_relations[signal_type][signal_subtype][relation_name] += 1
    
    return grouped_relations


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


@router.get("/relations/grouped/examples")
def get_grouped_relation_examples(
    signal_type: str = None,
    signal_subtype: str = None, 
    relation_name: str = None,
    repo: DocumentsRepository = Depends(create_documents_repository)
) -> List[Dict]:
    """
    Returns examples of relations filtered by signal type, subtype, and/or relation name.
    Parameters are optional for flexible filtering.
    """
    examples = []
    for doc in repo.documents.values():
        for node in doc.intra_sentential_relations:
            # Skip nodes without the specified relation name if provided
            if relation_name and node.relname != relation_name:
                continue
                
            # If no signal filters are specified, or the node has signals that match the filters
            match = False
            if not signal_type and not signal_subtype:
                # No signal filters, so we include this node
                match = True
            elif hasattr(node, 'signals') and node.signals:
                for signal in node.signals:
                    # Check if signal matches the filters
                    if (signal_type is None or signal.type == signal_type) and \
                       (signal_subtype is None or signal.subtype == signal_subtype):
                        match = True
                        break
            
            if match:
                examples.append({
                    "document": doc.get_filename(),
                    "relation": node
                })
                if len(examples) >= 5:  # Limit to 5 examples
                    break
    
    return examples
