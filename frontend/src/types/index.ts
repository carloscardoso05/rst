export interface Signal {
  id: number
  source_id: number
  type: string
  subtype: string
  text: string
}

export interface Relation {
  id: number
  relname: string | null
  text: string
  parent_text: string
  relation?: {
    type: string
  }
  signals?: Signal[]
}

export interface RelationExample {
  document: string
  relation: Relation
}

export interface DocumentResponse {
  filename: string
  full_text: string
  intra_sentential_relations: Relation[]
}

export interface TextChunk {
  type: 'text' | 'relation'
  text: string
  relationId?: number
}

export interface GroupedRelations {
  [signalType: string]: {
    [signalSubtype: string]: {
      [relationName: string]: number
    }
  }
}