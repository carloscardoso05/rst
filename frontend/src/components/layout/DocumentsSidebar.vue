<template>
  <ul class="menu p-4 w-80 min-h-full bg-base-200 text-base-content">
    <li class="menu-title">Documents</li>
    <li v-for="doc in documents" :key="doc">
      <RouterLink :to="`/document/${encodeURIComponent(doc)}`" :class="{ 'active': isActive(doc) }">{{ doc }}</RouterLink>
    </li>
    <li class="menu-title mt-4">Relations</li>
    <li>
      <RouterLink to="/relations">Relations Explorer</RouterLink>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useDocumentStore } from '@/stores/document';

const documentStore = useDocumentStore();
const route = useRoute();

const documents = computed(() => documentStore.documents);

onMounted(async () => {
  if (!documentStore.hasDocuments) {
    await documentStore.fetchDocuments();
  }
});

function isActive(doc: string): boolean {
  return route.params.filename === doc;
}
</script>
