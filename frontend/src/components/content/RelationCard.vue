<template>
  <el-card class="relation-card">
    <div class="relation-header">
      <el-tag>{{ relation.relname }}</el-tag>
      <span class="relation-type">{{ relation.relation?.type }}</span>
      <el-tag size="small" type="info" v-if="document">{{ document }}</el-tag>
    </div>
    <div class="relation-content">
      <div class="relation-text">{{ relation.text }}</div>
      <div v-if="relation.parent_text" class="parent-text">
        Parent: {{ relation.parent_text }}
      </div>
      <div v-if="relation.signals && relation.signals.length > 0" class="signals-container">
        <div v-for="signal in relation.signals" :key="signal.id" class="signal-item">
          <strong>Signal:</strong> Type: {{ signal.type }}, Subtype: {{ signal.subtype }}
          <div v-if="signal.text" class="signal-text">Text: {{ signal.text }}</div>
        </div>
      </div>
    </div>
    <div class="relation-actions">
      <el-button 
        type="primary" 
        link 
        @click="$emit('show-in-text')"
      >
        Show in text
      </el-button>
    </div>
  </el-card>
</template>

<script setup lang="ts">
interface Signal {
  id: number
  source_id: number
  type: string
  subtype: string
  text: string
}

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

defineProps<{
  relation: Relation
  document?: string
}>()

defineEmits<{
  (e: 'show-in-text'): void
}>()
</script>

<style scoped>
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

.relation-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
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
</style>