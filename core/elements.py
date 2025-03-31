from collections import Counter
import os
import re
from typing import Optional, cast
from xml.etree import ElementTree

from pydantic import BaseModel, ConfigDict, Field, computed_field


class RS3Parser:
    relations: dict[str, "Relation"]
    nodes: dict[int, "Node"]
    segments: dict[int, "Segment"]
    groups: dict[int, "Group"]
    signals: dict[int, "Signal"]
    root_node: "Node"

    def get_sorted_segments(self) -> list["Segment"]:
        return list(sorted(self.segments.values(), key=lambda s: s.order))

    def count_intra_sentential_relations(self) -> dict[str, int]:
        nodes = self.get_intra_sentential_relations()
        counting = dict(Counter(map(lambda node: node.relname, nodes)))
        return counting

    def get_intra_sentential_relations(self) -> list["Node"]:
        return list(filter(self.to_count, self.nodes.values()))

    def get_tokens(self) -> list[str]:
        return self.root_node.get_tokens()

    def get_tokens_dict(self) -> dict[int, str]:
        return {id + 1: token for id, token in enumerate(self.get_tokens())}

    def get_tokens_ids(self) -> list[int]:
        return list(self.get_tokens_dict().keys())

    def get_text(self) -> str:
        return self.root_node.get_text()

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Document at "{file_path}" does not exist')

        root_element = ElementTree.parse(file_path).getroot()
        self.relations = {
            relation.name: relation
            for relation in [
                Relation.from_element(rel, self)
                for rel in root_element.findall("header/relations/rel")
            ]
        }
        self.segments = {
            segment.id: segment
            for segment in [
                Segment.from_element(segment, self, order)
                for order, segment in enumerate(root_element.findall("body/segment"))
            ]
        }
        self.groups = {
            group.id: group
            for group in [
                Group.from_element(group, self)
                for group in root_element.findall("body/group")
            ]
        }
        self.nodes = cast(dict[int, Node], self.groups) | cast(
            dict[int, Node], self.segments
        )
        self.signals = {
            id: Signal.from_element(signal, id, self)
            for id, signal in enumerate(root_element.findall("body/signals/signal"))
        }
        self.root_node = [node for node in self.nodes.values() if node.is_root()][0]

        sentence_id = 1
        initial_token_id = 1
        for segment in self.get_sorted_segments():
            segment.sentence_id = sentence_id
            segment.initial_token_id = initial_token_id
            if re.match(r".*[.? !]\s*[\'\"]?\s*", segment.get_tokens()[-1]):
                sentence_id += 1
            initial_token_id += len(segment.get_tokens())
            
        for signal in self.signals.values():
            self.nodes[signal.source_id].signals.append(signal)

    def to_count(self, node: "Node") -> bool:
        # Quando a relname de um nó é None, significa que é a raiz da árvore
        if node.relname == "span" or node.relname is None:
            return False
        if node.is_multinuclear():
            if node.relname == "same-unit":
                return node.get_siblings_of_same_relation()[0] == node
            else:  # contrast, sequence ou list
                index = [
                    node.id for node in node.get_siblings_of_same_relation()
                ].index(node.id)
                if index + 1 == len(node.get_siblings_of_same_relation()):
                    return False
                node_on_right = node.get_siblings_of_same_relation()[index + 1]
                return node.get_sentences_ids() == node_on_right.get_sentences_ids()
        return self.are_of_same_sentence([node.get_parent(), node])

    def are_of_same_sentence(self, nodes: list[Optional["Node"]]) -> bool:
        segments: list[Segment] = []
        nodes = list(filter(lambda n: n is not None, nodes))
        for node in nodes:
            if isinstance(node, Group):
                segments.extend(node.get_deep_children_segments())
            elif isinstance(node, Segment):
                segments.append(node)
        if len(segments) <= 1:
            return True
        sentence_id = segments[0].sentence_id
        for segment in segments[1:]:
            if sentence_id != segment.sentence_id:
                return False
        return True


class Relation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    type: str
    parser: RS3Parser = Field(exclude=True)

    @classmethod
    def from_element(
        cls, element: ElementTree.Element, parser: RS3Parser
    ) -> "Relation":
        return Relation(
            name=str(element.get("name")),
            type=str(element.get("type")),
            parser=parser,
        )


class Node(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    parent_id: int | None
    relname: str | None
    signals: list["Signal"] = Field(default_factory=list)
    parser: RS3Parser = Field(exclude=True)

    def is_multinuclear(self) -> bool:
        return self.relname in [
            "sequence",
            "same-unit",
            "list",
            "contrast",
            "joint",
            "other-rel",
            None,
        ]

    def get_sentences_ids(self) -> set[int]:
        sentences: list[int] = []
        for segment in self.get_deep_children_segments():
            sentences.append(segment.sentence_id)
        return set(sentences)

    def is_root(self) -> bool:
        return self.parent_id is None and self.relname is None

    def get_parent(self) -> Optional["Node"]:
        if self.parent_id is None:
            return None
        return self.parser.nodes[self.parent_id]

    def get_children(self) -> list["Node"]:
        return [
            node for node in self.parser.nodes.values() if node.parent_id == self.id
        ]

    def get_siblings(self) -> list["Node"]:
        return [
            node
            for node in self.parser.nodes.values()
            if node.parent_id == self.parent_id
        ]

    def get_siblings_of_same_relation(self) -> list["Node"]:
        return [node for node in self.get_siblings() if node.relname == self.relname]

    def get_relation(self) -> Relation | None:
        if self.relname is None:
            return None
        return self.parser.relations[self.relname]

    @computed_field
    def relation(self) -> Relation | None:
        return self.get_relation()

    def get_deep_children_segments(self) -> list["Segment"]:
        segments: list[Segment] = []
        if isinstance(self, Segment):
            segments.append(self)
        for child in self.get_children():
            segments.extend(child.get_deep_children_segments())
        return list(sorted(segments, key=lambda s: s.order))

    def get_tokens(self) -> list[str]:
        tokens: list[str] = []
        for segment in self.get_deep_children_segments():
            tokens.extend(segment.inner_text.split())
        return tokens

    def get_text(self) -> str:
        return " ".join(self.get_tokens())

    @computed_field
    def parent_text(self) -> str:
        return self.get_parent().get_text()

    @computed_field
    def text(self) -> str:
        return self.get_text()


class Signal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    source_id: int
    type: str
    subtype: str
    tokens_ids: list[int]
    parser: RS3Parser = Field(exclude=True)

    def get_tokens(self) -> list[str]:
        tokens_dict = self.parser.get_tokens_dict()
        result = []
        for id in self.tokens_ids:
            if id in tokens_dict:
                result.append(tokens_dict[id])
        return result

    def get_text(self) -> str:
        return " ".join(self.get_tokens())

    def get_source(self) -> Node:
        return self.parser.nodes[self.source_id]

    @computed_field
    def text(self) -> str:
        return self.get_text()

    @classmethod
    def from_element(
        cls, element: ElementTree.Element, id: int, parser: RS3Parser
    ) -> "Signal":
        return Signal(
            id=id,
            source_id=int(str(element.get("source"))),
            type=str(element.get("type")),
            subtype=str(element.get("subtype")),
            tokens_ids=[int(token) for token in str(element.get("tokens")).split(",")]
            if element.get("tokens")
            else [],
            parser=parser,
        )


class Segment(Node):
    order: int
    inner_text: str
    initial_token_id: int = Field(init=False, default=-1)
    sentence_id: int = Field(init=False, default=-1)

    @classmethod
    def from_element(
        cls, element: ElementTree.Element, parser: RS3Parser, order: int
    ) -> "Segment":
        id: int = int(str(element.get("id")))
        parent_id: int | None = (
            int(str(element.get("parent")))
            if element.get("parent") is not None
            else None
        )
        relname: str | None = (
            str(element.get("relname")) if element.get("relname") is not None else None
        )
        return Segment(
            id=id,
            parent_id=parent_id,
            relname=relname,
            inner_text=element.text or "",
            parser=parser,
            order=order,
        )


class Group(Node):
    type: str

    @classmethod
    def from_element(
        cls,
        element: ElementTree.Element,
        parser: RS3Parser,
    ) -> "Group":
        id: int = int(str(element.get("id")))
        parent_id: int | None = (
            int(str(element.get("parent")))
            if element.get("parent") is not None
            else None
        )
        relname: str | None = (
            str(element.get("relname")) if element.get("relname") is not None else None
        )
        return Group(
            id=id,
            parent_id=parent_id,
            relname=relname,
            type=str(element.get("type")),
            parser=parser,
        )


if __name__ == "__main__":
    file = "documents/05-Quinta rodada (28-06 - 04-07)/Cluster 29/D1_C29_Folha_16-07-2007_JacksonSouza.rs3"
    parser = RS3Parser(file)
    print(parser.get_intra_sentential_relations())
