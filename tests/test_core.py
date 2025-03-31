import os
import pytest
from core.elements import RS3Parser

def test_rs3_parser():
    # Test file path
    test_file = "documents/00a-Treinamento/Cluster 1/D1_C1_Folha_04-08-2006_07h42 (1) - Ewerson Dantas.rs3"
    
    # Test that file exists
    assert os.path.exists(test_file), f"Test file {test_file} does not exist"
    
    # Create parser
    parser = RS3Parser(test_file)
    
    # Test basic functionality
    assert parser.root_node is not None, "Root node should not be None"
    assert len(parser.nodes) > 0, "Should have at least one node"
    assert len(parser.segments) > 0, "Should have at least one segment"
    
    # Test text extraction
    text = parser.get_text()
    assert isinstance(text, str), "get_text() should return a string"
    assert len(text) > 0, "Text should not be empty"
    
    # Test tokens
    tokens = parser.get_tokens()
    assert isinstance(tokens, list), "get_tokens() should return a list"
    assert len(tokens) > 0, "Should have at least one token"
    
    # Test relations
    relations = parser.get_intra_sentential_relations()
    assert isinstance(relations, list), "get_intra_sentential_relations() should return a list"
    
    # Test relation counting
    relation_counts = parser.count_intra_sentential_relations()
    assert isinstance(relation_counts, dict), "count_intra_sentential_relations() should return a dict"
    
    # Test segment sorting
    sorted_segments = parser.get_sorted_segments()
    assert isinstance(sorted_segments, list), "get_sorted_segments() should return a list"
    assert len(sorted_segments) > 0, "Should have at least one segment"
    
    # Test that segments are properly ordered
    for i in range(len(sorted_segments) - 1):
        assert sorted_segments[i].order <= sorted_segments[i + 1].order, "Segments should be in order" 