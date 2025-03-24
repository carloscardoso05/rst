export interface Relation {
  name: string;
  type: string;
}

export interface Node {
  id: number;
  parentId: number | null;
  relname: string | null;
  children: Node[];
}

export interface RSTDocument {
  relations: Relation[];
  nodes: Node[];
  rootNode: Node;
} 