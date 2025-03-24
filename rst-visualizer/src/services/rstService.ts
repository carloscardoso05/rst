import type { Relation, Node, RSTDocument } from '../types/Relation'

export class RSTService {
  private documents: RSTDocument[] = []

  async loadDocuments(documents: RSTDocument[]) {
    this.documents = documents
  }

  getRelationStats(): Map<string, { count: number; type: string }> {
    const stats = new Map<string, { count: number; type: string }>()

    this.documents.forEach(doc => {
      doc.relations.forEach(relation => {
        const current = stats.get(relation.name) || { count: 0, type: relation.type }
        stats.set(relation.name, {
          count: current.count + 1,
          type: relation.type
        })
      })
    })

    return stats
  }

  getRelationHierarchy(): Node[] {
    return this.documents.map(doc => doc.rootNode)
  }

  getRelationGroups(): { type: string; relations: Relation[] }[] {
    const groups = new Map<string, Relation[]>()

    this.documents.forEach(doc => {
      doc.relations.forEach(relation => {
        if (!groups.has(relation.type)) {
          groups.set(relation.type, [])
        }
        const group = groups.get(relation.type)!
        if (!group.find(r => r.name === relation.name)) {
          group.push(relation)
        }
      })
    })

    return Array.from(groups.entries()).map(([type, relations]) => ({
      type,
      relations
    }))
  }

  getRelationUsage(node: Node): { relation: Relation; count: number }[] {
    const usage = new Map<string, { relation: Relation; count: number }>()

    const traverse = (node: Node) => {
      if (node.relname) {
        const current = usage.get(node.relname) || {
          relation: { name: node.relname, type: 'unknown' },
          count: 0
        }
        usage.set(node.relname, {
          ...current,
          count: current.count + 1
        })
      }

      node.children.forEach(traverse)
    }

    traverse(node)
    return Array.from(usage.values())
  }

  getRelationDistribution(): { type: string; count: number }[] {
    const distribution = new Map<string, number>()

    this.documents.forEach(doc => {
      doc.relations.forEach(relation => {
        const current = distribution.get(relation.type) || 0
        distribution.set(relation.type, current + 1)
      })
    })

    return Array.from(distribution.entries()).map(([type, count]) => ({
      type,
      count
    }))
  }
} 