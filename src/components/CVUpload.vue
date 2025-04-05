<template>
  <div class="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
    <div class="relative py-3 sm:max-w-xl sm:mx-auto">
      <div class="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
        <div class="max-w-md mx-auto">
          <div class="divide-y divide-gray-200">
            <div class="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
              <h2 class="text-2xl font-bold mb-8 text-center text-gray-900">CV Analysis</h2>
              
              <!-- Job Description -->
              <div class="mb-6">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Job Description
                </label>
                <textarea
                  v-model="jobDescription"
                  rows="4"
                  class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Paste job description here..."
                ></textarea>
              </div>

              <!-- CV Upload -->
              <div class="mt-6">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Upload CVs
                </label>
                <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                  <div class="space-y-1 text-center">
                    <svg
                      class="mx-auto h-12 w-12 text-gray-400"
                      stroke="currentColor"
                      fill="none"
                      viewBox="0 0 48 48"
                    >
                      <path
                        d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                    </svg>
                    <div class="flex text-sm text-gray-600">
                      <label
                        for="file-upload"
                        class="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500"
                      >
                        <span>Upload files</span>
                        <input
                          id="file-upload"
                          type="file"
                          multiple
                          accept=".pdf"
                          class="sr-only"
                          @change="handleFileUpload"
                        >
                      </label>
                      <p class="pl-1">or drag and drop</p>
                    </div>
                    <p class="text-xs text-gray-500">PDF up to 10MB</p>
                  </div>
                </div>
              </div>

              <!-- Selected Files -->
              <div v-if="selectedFiles.length > 0" class="mt-4">
                <h3 class="text-sm font-medium text-gray-700">Selected Files:</h3>
                <ul class="mt-2 divide-y divide-gray-200">
                  <li v-for="file in selectedFiles" :key="file.name" class="py-2 flex items-center justify-between">
                    <span class="text-sm text-gray-500">{{ file.name }}</span>
                    <button
                      @click="removeFile(file)"
                      class="text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </li>
                </ul>
              </div>

              <!-- Analysis Button -->
              <div class="mt-8">
                <button
                  @click="analyzeFiles"
                  :disabled="!canAnalyze"
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                  Analyze CVs
                </button>
              </div>

              <!-- Results -->
              <div v-if="results.length > 0" class="mt-8">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Analysis Results</h3>
                <div class="space-y-4">
                  <div v-for="result in results" :key="result.filename" class="bg-gray-50 p-4 rounded-lg">
                    <h4 class="font-medium text-gray-900">{{ result.filename }}</h4>
                    <div class="mt-2">
                      <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-500">Match Score:</span>
                        <span class="text-sm font-medium text-gray-900">{{ result.match_score }}%</span>
                      </div>
                      <div class="mt-2">
                        <div class="w-full bg-gray-200 rounded-full h-2">
                          <div
                            class="bg-indigo-600 h-2 rounded-full"
                            :style="{ width: result.match_score + '%' }"
                          ></div>
                        </div>
                      </div>
                    </div>
                    <div class="mt-4">
                      <h5 class="text-sm font-medium text-gray-900">Key Skills:</h5>
                      <div class="mt-2 flex flex-wrap gap-2">
                        <span
                          v-for="skill in result.skills"
                          :key="skill"
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
                        >
                          {{ skill }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import axios from 'axios'

export default {
  name: 'CVUpload',
  setup() {
    const jobDescription = ref('')
    const selectedFiles = ref([])
    const results = ref([])
    const isLoading = ref(false)

    const canAnalyze = computed(() => {
      return jobDescription.value.trim() !== '' && selectedFiles.value.length > 0
    })

    const handleFileUpload = (event) => {
      const files = Array.from(event.target.files)
      selectedFiles.value = [...selectedFiles.value, ...files]
    }

    const removeFile = (file) => {
      selectedFiles.value = selectedFiles.value.filter(f => f !== file)
    }

    const analyzeFiles = async () => {
      if (!canAnalyze.value) return

      isLoading.value = true
      const formData = new FormData()
      formData.append('job_description', jobDescription.value)
      selectedFiles.value.forEach(file => {
        formData.append('cvs', file)
      })

      try {
        // This would normally point to your backend API
        // For demo purposes, we'll simulate a response
        // const response = await axios.post('/api/analyze', formData)
        // results.value = response.data
        
        // Simulated response for demo
        results.value = selectedFiles.value.map(file => ({
          filename: file.name,
          match_score: Math.floor(Math.random() * 40) + 60,
          skills: ['Python', 'JavaScript', 'React', 'Machine Learning', 'Data Analysis'].sort(() => Math.random() - 0.5).slice(0, 3)
        }))
      } catch (error) {
        console.error('Error analyzing CVs:', error)
        alert('Error analyzing CVs. Please try again.')
      } finally {
        isLoading.value = false
      }
    }

    return {
      jobDescription,
      selectedFiles,
      results,
      isLoading,
      canAnalyze,
      handleFileUpload,
      removeFile,
      analyzeFiles
    }
  }
}
</script> 