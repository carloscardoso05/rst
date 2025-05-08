<template>
  <div v-if="documentRelations.length === 0" class="no-relations">
    <el-empty description="No relations found for this document" />
  </div>
  <div v-else class="relations-container">
    <div v-for="relation in documentRelations" :key="relation.id" class="relation-item">
      <relation-card 
        :relation="relation" 
        @show-in-text="$emit('show-in-full-text', relation.id)" 
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import RelationCard from './RelationCard.vue'

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
  documentRelations: Relation[]
}>()

defineEmits<{
  (e: 'show-in-full-text', relationId: number): void
}>()
</script>

<style scoped>
.relations-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.no-relations {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}
</style>