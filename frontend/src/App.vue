<template>
  <el-container class="layout-container">
    <el-header>
      <h1>RST Visualizer</h1>
    </el-header>
    <el-container>
      <el-aside width="300px">
        <el-tabs>
          <el-tab-pane label="Documents">
            <el-card class="document-list">
              <template #header>
                <div class="card-header">
                  <span>Documents</span>
                </div>
              </template>
              <el-menu
                :default-active="selectedDocument"
                @select="handleDocumentSelect"
              >
                <el-menu-item
                  v-for="doc in documents"
                  :key="doc"
                  :index="doc"
                >
                  {{ doc }}
                </el-menu-item>
              </el-menu>
              <div v-if="loading" class="loading-container">
                <el-icon class="is-loading"><Loading /></el-icon>
              </div>
            </el-card>
          </el-tab-pane>
          <el-tab-pane label="Relations">
            <el-card class="relation-types-list">
              <template #header>
                <div class="card-header">
                  <span>Relation Types</span>
                </div>
              </template>
              <el-menu
                :default-active="selectedRelationType"
                @select="handleRelationTypeSelect"
              >
                <el-menu-item
                  v-for="type in relationTypes"
                  :key="type"
                  :index="type"
                >
                  {{ type }}
                </el-menu-item>
              </el-menu>
              <div v-if="loading" class="loading-container">
                <el-icon class="is-loading"><Loading /></el-icon>
              </div>
            </el-card>
          </el-tab-pane>
          <el-tab-pane label="Grouped Relations">
            <el-card class="relation-groups-list">
              <template #header>
                <div class="card-header">
                  <span>Relation Groups</span>
                </div>
              </template>
              <div v-if="loading" class="loading-container">
                <el-icon class="is-loading"><Loading /></el-icon>
              </div>
              <div v-else-if="Object.keys(groupedRelations).length === 0" class="no-relations">
                <el-empty description="No relation groups found" />
              </div>
              <div v-else class="relation-groups">
                <el-collapse accordion>
                  <el-collapse-item 
                    v-for="(subtypes, signalType) in groupedRelations" 
                    :key="signalType"
                    :title="signalType"
                    :name="signalType"
                  >
                    <!-- Second level: Signal Subtype -->
                    <el-collapse accordion>
                      <el-collapse-item
                        v-for="(relations, signalSubtype) in subtypes"
                        :key="`${signalType}-${signalSubtype}`"
                        :title="signalSubtype"
                        :name="signalSubtype"
                      >
                        <!-- Third level: Relations -->
                        <el-menu class="relation-menu">
                          <el-menu-item
                            v-for="(count, relationName) in relations"
                            :key="`${signalType}-${signalSubtype}-${relationName}`"
                            :index="relationName"
                            @click="handleGroupedRelationSelect(signalType, signalSubtype, relationName)"
                          >
                            <span>{{ relationName }}</span>
                            <el-badge :value="count" class="relation-count" />
                          </el-menu-item>
                        </el-menu>
                      </el-collapse-item>
                    </el-collapse>
                  </el-collapse-item>
                </el-collapse>
              </div>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-aside>
      <el-main>
        <template v-if="selectedRelationType || selectedRelationName">
          <div class="relation-examples">
            <el-card v-loading="loading">
              <template #header>
                <div class="card-header">
                  <span>
                    {{selectedRelationName ? 
                      `Examples of "${selectedRelationName}" relation` + 
                      (selectedSignalType !== 'No Signal' ? 
                        ` with signal type "${selectedSignalType}"` +
                        (selectedSignalSubtype !== 'No Subtype' ? ` and subtype "${selectedSignalSubtype}"` : '')
                        : '')
                      : 
                      `Examples of "${selectedRelationType}" relation`
                    }}
                  </span>
                </div>
              </template>
              <div v-if="error" class="error-message">
                <el-alert
                  title="Error loading relation examples"
                  type="error"
                  :description="error"
                  show-icon
                  :closable="false"
                />
              </div>
              <div v-else-if="relationExamples.length === 0" class="no-relations">
                <el-empty description="No examples found for this relation type" />
              </div>
              <div v-else class="relations-container">
                <div v-for="example in relationExamples" :key="example.document + example.relation.id" class="relation-item">
                  <el-card class="relation-card">
                    <div class="relation-header">
                      <el-tag>{{ example.relation.relname }}</el-tag>
                      <span class="relation-type">{{ example.relation.relation?.type }}</span>
                      <el-tag size="small" type="info">{{ example.document }}</el-tag>
                    </div>
                    <div class="relation-content">
                      <div class="relation-text">{{ example.relation.text }}</div>
                      <div v-if="example.relation.parent_text" class="parent-text">
                        Parent: {{ example.relation.parent_text }}
                      </div>
                      <div v-if="example.relation.signals && example.relation.signals.length > 0" class="signals-container">
                        <div v-for="signal in example.relation.signals" :key="signal.id" class="signal-item">
                          <strong>Signal:</strong> Type: {{ signal.type }}, Subtype: {{ signal.subtype }}
                          <div v-if="signal.text" class="signal-text">Text: {{ signal.text }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="relation-actions">
                      <el-button 
                        type="primary" 
                        link 
                        @click="showInFullTextFromExample(example.document, example.relation.id)"
                      >
                        Show in text
                      </el-button>
                    </div>
                  </el-card>
                </div>
              </div>
            </el-card>
          </div>
        </template>
        <template v-else-if="selectedDocument">
          <div class="document-view">
            <el-card v-loading="loading">
              <template #header>
                <div class="card-header">
                  <span>{{ selectedDocument }}</span>
                  <el-radio-group v-model="viewMode" size="small">
                    <el-radio-button label="relations">Relations</el-radio-button>
                    <el-radio-button label="full">Full Text</el-radio-button>
                  </el-radio-group>
                </div>
              </template>
              <div v-if="error" class="error-message">
                <el-alert
                  title="Error loading document"
                  type="error"
                  :description="error"
                  show-icon
                  :closable="false"
                />
              </div>
              <template v-else>
                <div v-if="viewMode === 'relations'" class="relations-view">
                  <div v-if="documentRelations.length === 0" class="no-relations">
                    <el-empty description="No relations found for this document" />
                  </div>
                  <div v-else class="relations-container">
                    <div v-for="relation in documentRelations" :key="relation.id" class="relation-item">
                      <el-card class="relation-card">
                        <div class="relation-header">
                          <el-tag>{{ relation.relname }}</el-tag>
                          <span class="relation-type">{{ relation.relation?.type }}</span>
                        </div>
                        <div class="relation-content">
                          <div class="relation-text">{{ relation.text }}</div>
                          <div v-if="relation.parent_text" class="parent-text">
                            Parent: {{ relation.parent_text }}
                          </div>
                        </div>
                        <div class="relation-actions">
                          <el-button 
                            type="primary" 
                            link 
                            @click="showInFullText(relation.id)"
                          >
                            Show in text
                          </el-button>
                        </div>
                      </el-card>
                    </div>
                  </div>
                </div>
                <div v-else class="full-text-view">
                  <div class="text-content" ref="textContentRef">
                    <template v-for="(chunk, index) in textChunks" :key="index">
                      <span
                        v-if="chunk.type === 'relation'"
                        :class="{
                          'relation-highlight': true,
                          'active': chunk.relationId === activeRelationId
                        }"
                        :data-relation-id="chunk.relationId"
                        @click="focusRelation(chunk.relationId)"
                      >{{ chunk.text }}</span>
                      <template v-else>{{ chunk.text }}</template>
                    </template>
                  </div>
                  <el-divider>Relations</el-divider>
                  <div class="relations-list">
                    <el-collapse v-model="activeCollapseItems">
                      <el-collapse-item 
                        v-for="relation in documentRelations" 
                        :key="relation.id"
                        :title="relation.relname || 'Unnamed Relation'"
                        :name="relation.id"
                      >
                        <div 
                          class="relation-detail"
                          :class="{ 'active': relation.id === activeRelationId }"
                          @click="focusRelation(relation.id)"
                        >
                          <div class="relation-text">
                            <strong>Text:</strong> {{ relation.text }}
                          </div>
                          <div v-if="relation.parent_text" class="parent-text">
                            <strong>Parent:</strong> {{ relation.parent_text }}
                          </div>
                          <div v-if="relation.relation?.type" class="relation-type">
                            <strong>Type:</strong> {{ relation.relation.type }}
                          </div>
                        </div>
                      </el-collapse-item>
                    </el-collapse>
                  </div>
                </div>
              </template>
            </el-card>
          </div>
        </template>
        <div v-else class="no-selection">
          <el-empty description="Select a document or relation type to view details" />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { Loading, ArrowRight } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

interface Relation {
  id: number
  relname: string | null
  text: string
  parent_text: string
  relation?: {
    type: string
  }
  signals?: Signal[]
}

interface Signal {
  id: number
  source_id: number
  type: string
  subtype: string
  text: string
}

interface RelationExample {
  document: string
  relation: Relation
}

interface DocumentResponse {
  filename: string
  full_text: string
  intra_sentential_relations: Relation[]
}

interface TextChunk {
  type: 'text' | 'relation'
  text: string
  relationId?: number
}

interface GroupedRelations {
  [signalType: string]: {
    [signalSubtype: string]: {
      [relationName: string]: number
    }
  }
}

const documents = ref<string[]>([])
const selectedDocument = ref('')
const documentRelations = ref<Relation[]>([])
const relationTypes = ref<string[]>([])
const selectedRelationType = ref('')
const relationExamples = ref<RelationExample[]>([])
const groupedRelations = ref<GroupedRelations>({})
const selectedSignalType = ref('')
const selectedSignalSubtype = ref('')
const selectedRelationName = ref('')
const loading = ref(false)
const error = ref<string | null>(null)
const viewMode = ref<'relations' | 'full'>('relations')
const fullText = ref('')
const activeRelationId = ref<number | null>(null)
const activeCollapseItems = ref<number[]>([])
const textContentRef = ref<HTMLElement | null>(null)

const fetchDocuments = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('/files')
    documents.value = response.data
  } catch (err) {
    error.value = 'Failed to load documents. Please try again.'
    console.error('Error fetching documents:', err)
  } finally {
    loading.value = false
  }
}

const fetchRelationTypes = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('/files/relations/types')
    relationTypes.value = response.data
  } catch (err) {
    error.value = 'Failed to load relation types. Please try again.'
    console.error('Error fetching relation types:', err)
  } finally {
    loading.value = false
  }
}

const fetchGroupedRelations = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('/files/relations/grouped')
    groupedRelations.value = response.data
  } catch (err) {
    error.value = 'Failed to load relation groups. Please try again.'
    console.error('Error fetching relation groups:', err)
  } finally {
    loading.value = false
  }
}

const handleSignalTypeSelect = (type: string) => {
  selectedSignalType.value = type
  selectedSignalSubtype.value = ''
  selectedRelationName.value = ''
}

const handleSignalSubtypeSelect = (subtype: string) => {
  selectedSignalSubtype.value = subtype
  selectedRelationName.value = ''
}

const handleGroupedRelationSelect = async (type: string, subtype: string, relation: string) => {
  selectedSignalType.value = type
  selectedSignalSubtype.value = subtype
  selectedRelationName.value = relation
  selectedRelationType.value = ''
  selectedDocument.value = ''
  
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('/files/relations/grouped/examples', {
      params: {
        signal_type: type !== 'No Signal' ? type : null,
        signal_subtype: subtype !== 'No Subtype' ? subtype : null,
        relation_name: relation
      }
    })
    relationExamples.value = response.data
  } catch (err) {
    error.value = 'Failed to load relation examples. Please try again.'
    console.error('Error fetching relation examples:', err)
    relationExamples.value = []
  } finally {
    loading.value = false
  }
}

const createTextChunks = (fullText: string, relations: Relation[]): TextChunk[] => {
  // Create a sorted array of positions where relations appear in the text
  const positions: Array<{ start: number; end: number; relation: Relation }> = []
  
  relations.forEach(relation => {
    const index = fullText.indexOf(relation.text)
    if (index !== -1) {
      positions.push({
        start: index,
        end: index + relation.text.length,
        relation
      })
    }
  })
  
  // Sort positions by start index
  positions.sort((a, b) => a.start - b.start)
  
  const chunks: TextChunk[] = []
  let lastIndex = 0
  
  positions.forEach(pos => {
    // Add text before the relation if any
    if (pos.start > lastIndex) {
      chunks.push({
        type: 'text',
        text: fullText.slice(lastIndex, pos.start)
      })
    }
    
    // Add the relation
    chunks.push({
      type: 'relation',
      text: fullText.slice(pos.start, pos.end),
      relationId: pos.relation.id
    })
    
    lastIndex = pos.end
  })
  
  // Add remaining text if any
  if (lastIndex < fullText.length) {
    chunks.push({
      type: 'text',
      text: fullText.slice(lastIndex)
    })
  }
  
  return chunks
}

const textChunks = ref<TextChunk[]>([])

const handleDocumentSelect = async (filename: string): Promise<void> => {
  selectedDocument.value = filename
  selectedRelationType.value = ''
  loading.value = true
  error.value = null
  try {
    const response = await axios.get<DocumentResponse>(`/files/${filename}`)
    documentRelations.value = response.data.intra_sentential_relations || []
    fullText.value = response.data.full_text || ''
    textChunks.value = createTextChunks(fullText.value, documentRelations.value)
    activeRelationId.value = null
    activeCollapseItems.value = []
  } catch (err) {
    error.value = 'Failed to load document. Please try again.'
    console.error('Error fetching document:', err)
    documentRelations.value = []
    fullText.value = ''
    textChunks.value = []
    throw err // Re-throw the error so we can handle it in the calling function
  } finally {
    loading.value = false
  }
}

const showInFullTextFromExample = async (filename: string, relationId: number) => {
  try {
    // First load the document
    await handleDocumentSelect(filename)
    // Then switch to full text view and focus the relation
    nextTick(() => {
      showInFullText(relationId)
    })
  } catch (err) {
    // If there's an error loading the document, show an error message
    ElMessage.error('Failed to load document. Please try again.')
  }
}

const showInFullText = (relationId: number) => {
  viewMode.value = 'full'
  nextTick(() => {
    focusRelation(relationId)
  })
}

const focusRelation = (relationId: number) => {
  activeRelationId.value = relationId
  activeCollapseItems.value = [relationId]
  
  // Wait for the next tick to ensure the element is rendered
  nextTick(() => {
    const element = document.querySelector(`[data-relation-id="${relationId}"]`)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  })
}

const handleRelationTypeSelect = async (type: string) => {
  selectedRelationType.value = type
  selectedDocument.value = ''
  loading.value = true
  error.value = null
  try {
    const response = await axios.get(`/files/relations/examples/${type}`)
    relationExamples.value = response.data
  } catch (err) {
    error.value = 'Failed to load relation examples. Please try again.'
    console.error('Error fetching relation examples:', err)
    relationExamples.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDocuments()
  fetchRelationTypes()
  fetchGroupedRelations()
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
}

.el-header {
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.el-aside {
  background-color: #f5f7fa;
  padding: 20px;
  border-right: 1px solid #e4e7ed;
}

.document-list, .relation-types-list, .relation-groups-list {
  height: calc(100vh - 120px);
  overflow-y: auto;
  position: relative;
}

.loading-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.document-view, .relation-examples {
  height: 100%;
  padding: 0;
}

.relations-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.relation-card {
  margin-bottom: 10px;
}

.relation-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.relation-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.relation-text {
  font-weight: bold;
}

.parent-text {
  color: #666;
  font-size: 0.9em;
}

.signals-container {
  margin-top: 8px;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.signal-item {
  padding: 4px 0;
  font-size: 0.9em;
}

.signal-text {
  margin-top: 2px;
  color: #666;
}

.no-selection, .no-relations {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}

.error-message {
  padding: 20px;
}

.full-text-view {
  padding: 20px;
}

.text-content {
  white-space: pre-wrap;
  font-family: monospace;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  line-height: 1.6;
}

.relations-list {
  margin-top: 20px;
}

.relation-detail {
  cursor: pointer;
  padding: 12px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.relation-detail:hover {
  background-color: #f5f7fa;
}

.relation-detail.active {
  background-color: #ecf5ff;
  border: 1px solid #409EFF;
}

.relation-highlight {
  background-color: rgba(64, 158, 255, 0.1);
  border-radius: 4px;
  cursor: pointer;
  padding: 2px 4px;
  margin: -2px -4px;
  transition: background-color 0.2s ease;
}

.relation-highlight:hover {
  background-color: rgba(64, 158, 255, 0.2);
}

.relation-highlight.active {
  background-color: rgba(64, 158, 255, 0.3);
  outline: 2px solid #409EFF;
}

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-card) {
  height: 100%;
}

:deep(.el-tabs__content) {
  height: calc(100vh - 120px);
  overflow-y: auto;
}

:deep(.el-collapse-item__content) {
  padding-bottom: 12px;
}

.relation-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.relation-groups {
  padding: 10px 0;
}

.relation-menu {
  border-radius: 4px;
  margin-top: 8px;
}

.relation-count {
  margin-left: auto;
}

:deep(.el-collapse) {
  border: none;
}

:deep(.el-collapse-item__wrap) {
  border-bottom: none;
}

:deep(.el-collapse-item__header) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-collapse-item__header:hover) {
  color: #409EFF;
}

:deep(.el-menu-item) {
  height: 36px;
  line-height: 36px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
