<template>
  <div class="relation-visualizer">
    <div class="controls">
      <div class="filter-section">
        <h3>Filter Relations</h3>
        <div class="filter-options">
          <label>
            <input type="checkbox" v-model="showRST" />
            RST Relations
          </label>
          <label>
            <input type="checkbox" v-model="showMultinuc" />
            Multinuclear Relations
          </label>
        </div>
      </div>
      
      <div class="search-section">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search relations..."
          class="search-input"
        />
      </div>
    </div>

    <div class="visualization-container">
      <div class="relations-grid">
        <div 
          v-for="group in filteredRelationGroups" 
          :key="group.type"
          class="relation-group"
        >
          <h3>{{ group.type }}</h3>
          <div class="relations-list">
            <div 
              v-for="relation in group.relations" 
              :key="relation.name"
              class="relation-item"
              :class="{ 'highlighted': isHighlighted(relation) }"
              @click="selectRelation(relation)"
            >
              <span class="relation-name">{{ relation.name }}</span>
              <span class="relation-count" v-if="relation.count">
                ({{ relation.count }})
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="relation-details" v-if="selectedRelation">
        <h3>Relation Details</h3>
        <div class="details-content">
          <p><strong>Name:</strong> {{ selectedRelation.name }}</p>
          <p><strong>Type:</strong> {{ selectedRelation.type }}</p>
          <p><strong>Count:</strong> {{ selectedRelation.count }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Relation } from '../types/Relation'

const props = defineProps<{
  relations: Relation[]
}>()

const showRST = ref(true)
const showMultinuc = ref(true)
const searchQuery = ref('')
const selectedRelation = ref<Relation | null>(null)

const filteredRelationGroups = computed(() => {
  const groups = {
    'RST Relations': [] as (Relation & { count?: number })[],
    'Multinuclear Relations': [] as (Relation & { count?: number })[]
  }

  props.relations.forEach(relation => {
    if (relation.type === 'rst' && showRST.value) {
      groups['RST Relations'].push(relation)
    } else if (relation.type === 'multinuc' && showMultinuc.value) {
      groups['Multinuclear Relations'].push(relation)
    }
  })

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    Object.keys(groups).forEach(key => {
      groups[key] = groups[key].filter(relation => 
        relation.name.toLowerCase().includes(query)
      )
    })
  }

  return Object.entries(groups)
    .filter(([_, relations]) => relations.length > 0)
    .map(([type, relations]) => ({ type, relations }))
})

const isHighlighted = (relation: Relation) => {
  return selectedRelation.value?.name === relation.name
}

const selectRelation = (relation: Relation) => {
  selectedRelation.value = relation
}
</script>

<style scoped>
.relation-visualizer {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  gap: 20px;
  align-items: center;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-options {
  display: flex;
  gap: 15px;
}

.search-section {
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.visualization-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.relations-grid {
  display: grid;
  gap: 20px;
}

.relation-group {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
}

.relation-group h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 18px;
}

.relations-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}

.relation-item {
  background: white;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.relation-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.relation-item.highlighted {
  background: #e3f2fd;
  border: 2px solid #2196f3;
}

.relation-name {
  font-weight: 500;
}

.relation-count {
  color: #666;
  font-size: 0.9em;
}

.relation-details {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.relation-details h3 {
  margin: 0 0 15px 0;
  color: #333;
}

.details-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.details-content p {
  margin: 0;
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  border-bottom: 1px solid #eee;
}

.details-content p:last-child {
  border-bottom: none;
}
</style> 