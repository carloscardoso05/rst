<template>
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
        <relations-view 
          v-if="viewMode === 'relations'" 
          :document-relations="documentRelations" 
          @show-in-full-text="showInFullText"
        />
        <full-text-view 
          v-else 
          :text-chunks="textChunks"
          :document-relations="documentRelations"
          :active-relation-id="activeRelationId"
          :active-collapse-items="activeCollapseItems"
          @focus-relation="focusRelation"
        />
      </template>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import RelationsView from './RelationsView.vue'
import FullTextView from './FullTextView.vue'

interface Relation {
  id: number
  relname: string | null
  text: string
  parent_text: string
  relation?: {
    type: string
  }
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

const props = defineProps<{
  selectedDocument: string
  loading: boolean
  error: string | null
}>()

const emit = defineEmits<{
  (e: 'update:loading', loading: boolean): void
  (e: 'update:error', error: string | null): void
}>()

const viewMode = ref<'relations' | 'full'>('relations')
const documentRelations = ref<Relation[]>([])
const fullText = ref('')
const textChunks = ref<TextChunk[]>([])
const activeRelationId = ref<number | null>(null)
const activeCollapseItems = ref<number[]>([])

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

const loadDocument = async () => {
  if (!props.selectedDocument) return
  
  emit('update:loading', true)
  emit('update:error', null)
  
  try {
    const response = await axios.get<DocumentResponse>(`/files/${props.selectedDocument}`)
    documentRelations.value = response.data.intra_sentential_relations || []
    fullText.value = response.data.full_text || ''
    textChunks.value = createTextChunks(fullText.value, documentRelations.value)
    activeRelationId.value = null
    activeCollapseItems.value = []
  } catch (err) {
    emit('update:error', 'Failed to load document. Please try again.')
    console.error('Error fetching document:', err)
    documentRelations.value = []
    fullText.value = ''
    textChunks.value = []
  } finally {
    emit('update:loading', false)
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

watch(() => props.selectedDocument, loadDocument, { immediate: true })
</script>

<style scoped>
.document-view {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-message {
  padding: 20px;
}
</style>