<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">HireMinds</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="border-4 border-dashed border-gray-200 rounded-lg h-96 p-4">
          <h2 class="text-2xl font-semibold mb-4">Welcome to HireMinds</h2>
          <p class="text-gray-600 mb-4">
            This is a frontend-only deployment. To use the full application with AI features:
          </p>
          <ol class="list-decimal list-inside space-y-2 text-gray-600">
            <li>Clone the repository from GitHub</li>
            <li>Install Ollama locally</li>
            <li>Run the full application with backend support</li>
          </ol>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script> 