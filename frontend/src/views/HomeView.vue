<template>
  <AppLayout>
    <template #sidebar>
      <DocumentsSidebar />
    </template>
    
    <div v-if="isLoading" class="flex items-center justify-center min-h-screen">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
    
    <div v-else-if="error" class="alert alert-error">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      <span>{{ error }}</span>
    </div>
    
    <div v-else>
      <h1 class="text-3xl font-bold mb-6">Welcome to RST Visualizer</h1>
      
      <div class="card bg-base-200 shadow-xl">
        <div class="card-body">
          <h2 class="card-title">Get Started</h2>
          <p>Select a document from the sidebar to view its RST structure.</p>
          <p class="mt-2">Or explore the relations by type using the Relations Explorer.</p>
          
          <div class="card-actions justify-end mt-4">
            <RouterLink to="/relations" class="btn btn-primary">
              Relations Explorer
            </RouterLink>
          </div>
        </div>
      </div>
      
      <div class="mt-6">
        <h2 class="text-2xl font-bold mb-4">Available Documents ({{ documents.length }})</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="doc in documents" :key="doc" class="card bg-base-100 shadow-sm hover:shadow-md transition-shadow">
            <div class="card-body">
              <h3 class="card-title">{{ doc }}</h3>
              <div class="card-actions justify-end">
                <RouterLink :to="`/document/${encodeURIComponent(doc)}`" class="btn btn-primary btn-sm">
                  View Document
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import AppLayout from '@/components/layout/AppLayout.vue';
import DocumentsSidebar from '@/components/layout/DocumentsSidebar.vue';
import { useDocumentStore } from '@/stores/document';

const documentStore = useDocumentStore();

const documents = computed(() => documentStore.documents);
const isLoading = computed(() => documentStore.isLoading);
const error = computed(() => documentStore.error);

onMounted(async () => {
  if (!documentStore.hasDocuments) {
    await documentStore.fetchDocuments();
  }
});
</script>