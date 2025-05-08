<template>
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import axios from 'axios'

defineProps<{
  selectedDocument: string;
  loading: boolean;
}>()

const emit = defineEmits<{
  (e: 'select-document', document: string): void
}>()

const documents = ref<string[]>([])

const handleDocumentSelect = (document: string) => {
  emit('select-document', document)
}

const fetchDocuments = async () => {
  try {
    const response = await axios.get('/files')
    documents.value = response.data
  } catch (err) {
    console.error('Error fetching documents:', err)
  }
}

onMounted(() => {
  fetchDocuments()
})
</script>

<style scoped>
.document-list {
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

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-card) {
  height: 100%;
}
</style>