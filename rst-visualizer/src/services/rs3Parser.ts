import { XMLParser } from 'fast-xml-parser'
import type { Relation, Node, RSTDocument } from '../types/Relation'

export class RS3Parser {
  private parser: XMLParser

  constructor() {
    this.parser = new XMLParser({
      ignoreAttributes: false,
      attributeNamePrefix: '@_'
    })
  }

  parseRS3File(content: string): RSTDocument {
    const parsed = this.parser.parse(content)
    const rst = parsed.rst

    // Parse relations
    const relations: Relation[] = rst.header.relations.rel.map((rel: any) => ({
      name: rel['@_name'],
      type: rel['@_type']
    }))

    // Parse nodes
    const nodes: Node[] = []
    const rootNode = this.parseNode(rst.body, null, nodes)

    return {
      relations,
      nodes,
      rootNode
    }
  }

  private parseNode(element: any, parentId: number | null, nodes: Node[]): Node {
    const id = nodes.length + 1
    const node: Node = {
      id,
      parentId,
      relname: element['@_relname'] || null,
      children: []
    }

    nodes.push(node)

    // Parse children
    if (element.segment) {
      const segments = Array.isArray(element.segment) ? element.segment : [element.segment]
      segments.forEach((segment: any) => {
        const childNode = this.parseNode(segment, id, nodes)
        node.children.push(childNode)
      })
    }

    return node
  }

  async parseRS3Files(files: File[]): Promise<RSTDocument[]> {
    const documents: RSTDocument[] = []

    for (const file of files) {
      const content = await file.text()
      const document = this.parseRS3File(content)
      documents.push(document)
    }

    return documents
  }
} 