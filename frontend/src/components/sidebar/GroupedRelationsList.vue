<template>
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
      <el-collapse 
        accordion
        v-model="expandedSignalTypes"
        @change="handleCollapseChange"
      >
        <el-collapse-item 
          v-for="(subtypes, signalType) in groupedRelations" 
          :key="signalType"
          :title="signalType"
          :name="signalType"
        >
          <!-- Second level: Signal Subtype -->
          <el-collapse 
            accordion
            v-model="expandedSubtypes[signalType]"
            @change="keys => handleSubtypeCollapseChange(signalType, keys)"
          >
            <el-collapse-item
              v-for="(relations, signalSubtype) in subtypes"
              :key="`${signalType}-${signalSubtype}`"
              :title="signalSubtype"
              :name="signalSubtype"
              class="subtype-item"
            >
              <!-- Third level: Relations -->
              <el-menu class="relation-menu">
                <el-menu-item
                  v-for="(count, relationName) in relations"
                  :key="`${signalType}-${signalSubtype}-${relationName}`"
                  :index="relationName"
                  @click="handleGroupedRelationSelect(signalType, signalSubtype, relationName)"
                  class="relation-menu-item"
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import axios from 'axios'

interface GroupedRelations {
  [signalType: string]: {
    [signalSubtype: string]: {
      [relationName: string]: number
    }
  }
}

defineProps<{
  selectedSignalType: string;
  selectedSignalSubtype: string;
  loading: boolean;
}>()

const emit = defineEmits<{
  (e: 'select-grouped-relation', type: string, subtype: string, relation: string): void;
  (e: 'select-signal-type', type: string): void;
  (e: 'select-signal-subtype', subtype: string): void;
}>()

const groupedRelations = ref<GroupedRelations>({})
const expandedSignalTypes = ref<string[]>([])
const expandedSubtypes = ref<{[key: string]: string[]}>({})

const handleCollapseChange = (keys: string[]) => {
  expandedSignalTypes.value = keys
}

const handleSubtypeCollapseChange = (signalType: string, keys: string[]) => {
  if (!expandedSubtypes.value[signalType]) {
    expandedSubtypes.value[signalType] = []
  }
  expandedSubtypes.value[signalType] = keys
}

const handleGroupedRelationSelect = (type: string, subtype: string, relation: string) => {
  emit('select-grouped-relation', type, subtype, relation)
}

const fetchGroupedRelations = async () => {
  try {
    const response = await axios.get('/files/relations/grouped')
    groupedRelations.value = response.data
  } catch (err) {
    console.error('Error fetching relation groups:', err)
  }
}

onMounted(() => {
  fetchGroupedRelations()
})
</script>

<style scoped>
.relation-groups-list {
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

.relation-groups {
  padding: 10px 0;
}

.no-relations {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
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

/* Indentation styles for the hierarchy */
.subtype-item :deep(.el-collapse-item__header) {
  padding-left: 15px;
  font-size: 0.95em;
}

.relation-menu-item {
  padding-left: 15px !important;
  font-size: 0.9em;
}
</style>