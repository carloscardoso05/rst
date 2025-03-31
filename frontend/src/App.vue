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
        </el-tabs>
      </el-aside>
      <el-main>
        <template v-if="selectedRelationType">
          <div class="relation-examples">
            <el-card v-loading="loading">
              <template #header>
                <div class="card-header">
                  <span>Examples of "{{ selectedRelationType }}" relation</span>
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
                </div>
              </template>
              <div v-if="error" class="error-message">
                <el-alert
                  title="Error loading relations"
                  type="error"
                  :description="error"
                  show-icon
                  :closable="false"
                />
              </div>
              <div v-else-if="documentRelations.length === 0" class="no-relations">
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
                  </el-card>
                </div>
              </div>
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
import { ref, onMounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import axios from 'axios'

interface Relation {
  id: number
  relname: string | null
  text: string
  parent_text: string
  relation?: {
    type: string
  }
}

interface RelationExample {
  document: string
  relation: Relation
}

const documents = ref<string[]>([])
const selectedDocument = ref('')
const documentRelations = ref<Relation[]>([])
const relationTypes = ref<string[]>([])
const selectedRelationType = ref('')
const relationExamples = ref<RelationExample[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

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

const handleDocumentSelect = async (filename: string) => {
  selectedDocument.value = filename
  selectedRelationType.value = ''
  loading.value = true
  error.value = null
  try {
    const response = await axios.get(`/files/${filename}`)
    documentRelations.value = response.data.intra_sentential_relations || []
  } catch (err) {
    error.value = 'Failed to load document relations. Please try again.'
    console.error('Error fetching document relations:', err)
    documentRelations.value = []
  } finally {
    loading.value = false
  }
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

.document-list, .relation-types-list {
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
</style>
