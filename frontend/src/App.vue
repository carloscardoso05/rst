<template>
  <el-container class="layout-container">
    <el-header>
      <h1>RST Visualizer</h1>
    </el-header>
    <el-container>
      <el-aside width="300px">
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
      </el-aside>
      <el-main>
        <div v-if="selectedDocument" class="document-view">
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
        <div v-else class="no-selection">
          <el-empty description="Select a document to view its relations" />
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

const documents = ref<string[]>([])
const selectedDocument = ref('')
const documentRelations = ref<Relation[]>([])
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

const handleDocumentSelect = async (filename: string) => {
  selectedDocument.value = filename
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

onMounted(() => {
  fetchDocuments()
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

.document-list {
  height: calc(100vh - 60px);
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

.document-view {
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
</style>
