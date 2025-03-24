<template>
  <div class="app">
    <header>
      <h1>RST Relations Visualizer</h1>
    </header>
    <main>
      <FileUpload @files-parsed="handleFilesParsed" />
      <div v-if="rstService" class="visualization-section">
        <RelationVisualizer :relations="relations" />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import RelationVisualizer from './components/RelationVisualizer.vue'
import FileUpload from './components/FileUpload.vue'
import { RSTService } from './services/rstService'
import type { Relation, RSTDocument } from './types/Relation'

const rstService = ref<RSTService | null>(null)
const relations = ref<Relation[]>([])

const handleFilesParsed = async (documents: RSTDocument[]) => {
  rstService.value = new RSTService()
  await rstService.value.loadDocuments(documents)
  
  // Get relation stats and update the relations array
  const stats = rstService.value.getRelationStats()
  relations.value = Array.from(stats.entries()).map(([name, data]) => ({
    name,
    type: data.type,
    count: data.count
  }))
}
</script>

<style>
.app {
  min-height: 100vh;
  background: #f8f9fa;
}

header {
  background: #fff;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  margin-bottom: 20px;
}

header h1 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

main {
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.visualization-section {
  margin-top: 20px;
}
</style> 