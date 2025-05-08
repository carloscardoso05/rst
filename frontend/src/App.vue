<template>
  <el-container class="layout-container">
    <app-header />
    <el-container>
      <el-aside width="300px">
        <el-tabs>
          <el-tab-pane label="Documents">
            <documents-list
              :selected-document="selectedDocument"
              :loading="loading"
              @select-document="handleDocumentSelect"
            />
          </el-tab-pane>
          <el-tab-pane label="Relations">
            <relation-types-list
              :selected-relation-type="selectedRelationType"
              :loading="loading"
              @select-relation-type="handleRelationTypeSelect"
            />
          </el-tab-pane>
          <el-tab-pane label="Grouped Relations">
            <grouped-relations-list
              :selected-signal-type="selectedSignalType"
              :selected-signal-subtype="selectedSignalSubtype"
              :loading="loading"
              @select-grouped-relation="handleGroupedRelationSelect"
              @select-signal-type="handleSignalTypeSelect"
              @select-signal-subtype="handleSignalSubtypeSelect"
            />
          </el-tab-pane>
        </el-tabs>
      </el-aside>
      <el-main>
        <template v-if="selectedRelationType || selectedRelationName">
          <relation-examples
            :selected-relation-type="selectedRelationType"
            :selected-relation-name="selectedRelationName"
            :selected-signal-type="selectedSignalType"
            :selected-signal-subtype="selectedSignalSubtype"
            :relation-examples="relationExamples"
            :loading="loading"
            :error="error"
            @show-in-text="showInFullTextFromExample"
          />
        </template>
        <template v-else-if="selectedDocument">
          <document-view
            :selected-document="selectedDocument"
            :loading="loading"
            :error="error"
            @update:loading="loading = $event"
            @update:error="error = $event"
          />
        </template>
        <div v-else class="no-selection">
          <el-empty description="Select a document or relation type to view details" />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { RelationExample } from './types'
import AppHeader from './components/AppHeader.vue'
import DocumentsList from './components/sidebar/DocumentsList.vue'
import RelationTypesList from './components/sidebar/RelationTypesList.vue'
import GroupedRelationsList from './components/sidebar/GroupedRelationsList.vue'
import RelationExamples from './components/content/RelationExamples.vue'
import DocumentView from './components/content/DocumentView.vue'

// State for document and relation data
const selectedDocument = ref('')
const selectedRelationType = ref('')
const selectedSignalType = ref('')
const selectedSignalSubtype = ref('')
const selectedRelationName = ref('')
const relationExamples = ref<RelationExample[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const handleDocumentSelect = (document: string) => {
  selectedDocument.value = document
  selectedRelationType.value = ''
  selectedRelationName.value = ''
  selectedSignalType.value = ''
  selectedSignalSubtype.value = ''
  error.value = null
}

const handleRelationTypeSelect = async (type: string) => {
  selectedRelationType.value = type
  selectedDocument.value = ''
  loading.value = true
  error.value = null
  try {
    const response = await axios.get(`/files/relations/examples/${type}`)
    relationExamples.value = response.data
  } catch (err) {
    error.value = 'Failed to load relation examples. Please try again.'
    console.error('Error fetching relation examples:', err)
    relationExamples.value = []
  } finally {
    loading.value = false
  }
}

const handleSignalTypeSelect = (type: string) => {
  selectedSignalType.value = type
  selectedSignalSubtype.value = ''
  selectedRelationName.value = ''
}

const handleSignalSubtypeSelect = (subtype: string) => {
  selectedSignalSubtype.value = subtype
  selectedRelationName.value = ''
}

const handleGroupedRelationSelect = async (type: string, subtype: string, relation: string) => {
  // Create local variables for loading state to avoid triggering sidebar re-render
  let isLoading = true;
  let localError = null;
  let results = [];
  
  try {
    const response = await axios.get('/files/relations/grouped/examples', {
      params: {
        signal_type: type !== 'No Signal' ? type : null,
        signal_subtype: subtype !== 'No Subtype' ? subtype : null,
        relation_name: relation
      }
    });
    results = response.data;
  } catch (err) {
    localError = 'Failed to load relation examples. Please try again.';
    console.error('Error fetching relation examples:', err);
  } finally {
    isLoading = false;
  }
  
  // Only update state variables after the request is complete
  // This batches our reactive updates to minimize re-renders
  nextTick(() => {
    // First update the main content area data
    relationExamples.value = results;
    error.value = localError;
    
    // Then update the selection state
    selectedRelationName.value = relation;
    selectedSignalType.value = type;
    selectedSignalSubtype.value = subtype;
    selectedRelationType.value = '';
    selectedDocument.value = '';
    
    // Finally update the loading state last to avoid flickering
    loading.value = false;
  });
  
  // Show loading state immediately but only in the main content area
  loading.value = true;
}

const showInFullTextFromExample = async (filename: string, relationId: number) => {
  try {
    loading.value = true;
    
    // Set the document
    selectedDocument.value = filename
    selectedRelationType.value = ''
    selectedRelationName.value = ''
    selectedSignalType.value = ''
    selectedSignalSubtype.value = ''
    
    // This will trigger document loading and then we can focus the relation
    // in the DocumentView component
    
  } catch (err) {
    // If there's an error loading the document, show an error message
    ElMessage.error('Failed to load document. Please try again.')
    console.error('Error showing relation in full text:', err)
  } finally {
    loading.value = false;
  }
}
</script>

<style>
.layout-container {
  height: 100vh;
  width: 100vw;
}

.el-aside {
  background-color: #f5f7fa;
  padding: 20px;
  border-right: 1px solid #e4e7ed;
}

:deep(.el-tabs__content) {
  height: calc(100vh - 120px);
  overflow-y: auto;
}

.no-selection {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}
</style>
