<template>
  <div class="file-upload">
    <div 
      class="upload-area"
      @dragover.prevent
      @drop.prevent="handleDrop"
      :class="{ 'dragging': isDragging }"
    >
      <input
        type="file"
        ref="fileInput"
        @change="handleFileSelect"
        multiple
        accept=".rs3"
        class="file-input"
        style="display: none"
      />
      
      <div class="upload-content">
        <div class="upload-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <p class="upload-text">
          Drag and drop RS3 files here or
          <button class="upload-button" @click="triggerFileInput">
            browse files
          </button>
        </p>
        <p class="upload-hint">Supported format: .rs3</p>
      </div>
    </div>

    <div v-if="files.length > 0" class="file-list">
      <h3>Selected Files</h3>
      <ul>
        <li v-for="file in files" :key="file.name" class="file-item">
          <span class="file-name">{{ file.name }}</span>
          <button class="remove-button" @click="removeFile(file)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RS3Parser } from '../services/rs3Parser'
import type { RSTDocument } from '../types/Relation'

const props = defineProps<{
  onFilesParsed: (documents: RSTDocument[]) => void
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const files = ref<File[]>([])
const isDragging = ref(false)
const parser = new RS3Parser()

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files) {
    await handleFiles(Array.from(input.files))
  }
}

const handleDrop = async (event: DragEvent) => {
  isDragging.value = false
  if (event.dataTransfer?.files) {
    await handleFiles(Array.from(event.dataTransfer.files))
  }
}

const handleFiles = async (newFiles: File[]) => {
  const rs3Files = newFiles.filter(file => file.name.endsWith('.rs3'))
  files.value = [...files.value, ...rs3Files]
  
  try {
    const documents = await parser.parseRS3Files(rs3Files)
    props.onFilesParsed(documents)
  } catch (error) {
    console.error('Error parsing RS3 files:', error)
  }
}

const removeFile = (file: File) => {
  files.value = files.value.filter(f => f !== file)
}
</script>

<style scoped>
.file-upload {
  margin-bottom: 20px;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  background: #fff;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area.dragging {
  border-color: #2196f3;
  background: #e3f2fd;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.upload-icon {
  color: #666;
}

.upload-text {
  margin: 0;
  color: #666;
}

.upload-button {
  background: none;
  border: none;
  color: #2196f3;
  cursor: pointer;
  font-weight: 500;
  padding: 0;
}

.upload-button:hover {
  text-decoration: underline;
}

.upload-hint {
  margin: 0;
  font-size: 0.9em;
  color: #999;
}

.file-list {
  margin-top: 20px;
  background: #fff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.file-list h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
}

.file-list ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.file-item:last-child {
  border-bottom: none;
}

.file-name {
  font-size: 14px;
  color: #333;
}

.remove-button {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-button:hover {
  color: #f44336;
}
</style> 