<template>
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
          <relation-card 
            :relation="example.relation" 
            :document="example.document"
            @show-in-text="$emit('show-in-text', example.document, example.relation.id)"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import RelationCard from './RelationCard.vue'

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

interface RelationExample {
  document: string
  relation: Relation
}

defineProps<{
  selectedRelationType: string
  selectedRelationName: string
  selectedSignalType: string
  selectedSignalSubtype: string
  relationExamples: RelationExample[]
  loading: boolean
  error: string | null
}>()

defineEmits<{
  (e: 'show-in-text', document: string, relationId: number): void
}>()
</script>

<style scoped>
.relation-examples {
  height: 100%;
  padding: 0;
}

.relations-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.no-relations {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}

.error-message {
  padding: 20px;
}
</style>