<template>
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import axios from 'axios'

defineProps<{
  selectedRelationType: string;
  loading: boolean;
}>()

const emit = defineEmits<{
  (e: 'select-relation-type', type: string): void
}>()

const relationTypes = ref<string[]>([])

const handleRelationTypeSelect = (type: string) => {
  emit('select-relation-type', type)
}

const fetchRelationTypes = async () => {
  try {
    const response = await axios.get('/files/relations/types')
    relationTypes.value = response.data
  } catch (err) {
    console.error('Error fetching relation types:', err)
  }
}

onMounted(() => {
  fetchRelationTypes()
})
</script>

<style scoped>
.relation-types-list {
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