<template>
  <div class="full-text-view">
    <div class="text-content">
      <template v-for="(chunk, index) in textChunks" :key="index">
        <span
          v-if="chunk.type === 'relation'"
          :class="{
            'relation-highlight': true,
            'active': chunk.relationId === activeRelationId
          }"
          :data-relation-id="chunk.relationId"
          @click="$emit('focus-relation', chunk.relationId)"
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
            @click="$emit('focus-relation', relation.id)"
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

<script setup lang="ts">
interface TextChunk {
  type: 'text' | 'relation'
  text: string
  relationId?: number
}

interface Relation {
  id: number
  relname: string | null
  text: string
  parent_text: string
  relation?: {
    type: string
  }
}

defineProps<{
  textChunks: TextChunk[]
  documentRelations: Relation[]
  activeRelationId: number | null
  activeCollapseItems: number[]
}>()

defineEmits<{
  (e: 'focus-relation', relationId: number): void
}>()
</script>

<style scoped>
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
</style>