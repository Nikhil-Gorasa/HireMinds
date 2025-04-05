<template>
  <div class="bg-gray-50">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <div class="absolute inset-y-0 h-full w-full" aria-hidden="true">
        <div class="relative h-full">
          <svg class="absolute right-full transform translate-y-1/3 translate-x-1/4 md:translate-y-1/2 sm:translate-x-1/2 lg:translate-x-full" width="404" height="784" fill="none" viewBox="0 0 404 784">
            <defs>
              <pattern id="e229dbec-10e9-49ee-8ec3-0286ca089edf" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                <rect x="0" y="0" width="4" height="4" class="text-gray-200" fill="currentColor" />
              </pattern>
            </defs>
            <rect width="404" height="784" fill="url(#e229dbec-10e9-49ee-8ec3-0286ca089edf)" />
          </svg>
          <svg class="absolute left-full transform -translate-y-3/4 -translate-x-1/4 sm:-translate-x-1/2 md:-translate-y-1/2 lg:-translate-x-3/4" width="404" height="784" fill="none" viewBox="0 0 404 784">
            <defs>
              <pattern id="d2a68204-c383-44b1-b99f-42ccff4e5365" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                <rect x="0" y="0" width="4" height="4" class="text-gray-200" fill="currentColor" />
              </pattern>
            </defs>
            <rect width="404" height="784" fill="url(#d2a68204-c383-44b1-b99f-42ccff4e5365)" />
          </svg>
        </div>
      </div>

      <div class="relative pt-6 pb-16 sm:pb-24">
        <div class="mt-16 mx-auto max-w-7xl px-4 sm:mt-24 sm:px-6">
          <div class="text-center">
            <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
              <span class="block">Hack the Future:</span>
              <span class="block text-indigo-600">A Gen AI Sprint Powered by Data</span>
            </h1>
            <p class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              Enhancing Job Screening with AI and Data Intelligence - Accenture Hackathon 2024
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Problem Statement Section -->
    <div class="relative bg-white py-16 sm:py-24">
      <div class="lg:mx-auto lg:max-w-7xl lg:px-8 lg:grid lg:grid-cols-2 lg:gap-24 lg:items-start">
        <div class="relative sm:py-16 lg:py-0">
          <div class="relative mx-auto max-w-md px-4 sm:max-w-3xl sm:px-6 lg:px-0 lg:max-w-none lg:py-20">
            <!-- Gradient background -->
            <div class="relative rounded-2xl shadow-xl overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-600 opacity-90"></div>
              <div class="relative px-8 py-10">
                <blockquote class="mt-8">
                  <div class="relative text-lg font-medium text-white md:flex-grow">
                    <p class="relative">
                      Current recruitment processes face challenges in efficiently screening large volumes of applications while ensuring fair and accurate candidate evaluation. Our solution leverages AI to transform this process.
                    </p>
                  </div>
                </blockquote>
              </div>
            </div>
          </div>
        </div>

        <div class="relative mx-auto max-w-md px-4 sm:max-w-3xl sm:px-6 lg:px-0">
          <div class="pt-12 sm:pt-16 lg:pt-20">
            <h2 class="text-3xl text-gray-900 font-extrabold tracking-tight sm:text-4xl">
              The Challenge
            </h2>
            <div class="mt-6 text-gray-500 space-y-6">
              <p class="text-lg">
                In today's competitive job market, HR teams face several challenges:
              </p>
              <ul class="list-disc pl-5 space-y-2">
                <li>Manual screening of numerous CVs is time-consuming and inefficient</li>
                <li>Inconsistent evaluation criteria across different recruiters</li>
                <li>Risk of overlooking qualified candidates</li>
                <li>Difficulty in matching candidate skills with job requirements</li>
                <li>Need for objective and data-driven decision making</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Solution Section -->
    <div class="bg-indigo-50 py-16 sm:py-24">
      <div class="relative">
        <div class="lg:mx-auto lg:max-w-7xl lg:px-8 lg:grid lg:grid-cols-2 lg:gap-24 lg:items-start">
          <div class="relative sm:py-16 lg:py-0">
            <div class="relative mx-auto max-w-md px-4 sm:max-w-3xl sm:px-6 lg:px-0 lg:max-w-none lg:py-20">
              <h2 class="text-3xl text-gray-900 font-extrabold tracking-tight sm:text-4xl">
                Our Solution: HireMinds
              </h2>
              <div class="mt-6 text-gray-500 space-y-6">
                <p class="text-lg">
                  HireMinds is an AI-powered recruitment platform that revolutionizes the hiring process through:
                </p>
                <ul class="list-disc pl-5 space-y-2">
                  <li>Automated CV analysis and scoring</li>
                  <li>Intelligent skill matching with job requirements</li>
                  <li>Data-driven candidate evaluation</li>
                  <li>Standardized assessment criteria</li>
                  <li>Real-time insights and recommendations</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="relative mx-auto max-w-md px-4 sm:max-w-3xl sm:px-6 lg:px-0">
            <div class="pt-12 sm:pt-16 lg:pt-20">
              <div class="mt-6 text-gray-500 space-y-6">
                <div class="bg-white shadow-lg rounded-lg overflow-hidden">
                  <div class="px-6 py-8">
                    <h3 class="text-xl font-semibold text-gray-900 mb-4">Getting Started</h3>
                    <p class="text-gray-600 mb-6">
                      To use HireMinds with full functionality, follow these steps:
                    </p>
                    <ol class="list-decimal pl-5 space-y-3 text-gray-600">
                      <li>Clone the repository:
                        <code class="block bg-gray-50 p-2 mt-2 rounded text-sm">
                          git clone https://github.com/Nikhil-Gorasa/HireMinds
                        </code>
                      </li>
                      <li>Install dependencies and set up the environment</li>
                      <li>Run the application locally with Ollama integration</li>
                    </ol>
                    <div class="mt-6">
                      <a href="https://github.com/Nikhil-Gorasa/HireMinds" class="text-indigo-600 hover:text-indigo-500 font-medium">
                        View Full Installation Guide →
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="bg-white py-16 sm:py-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-indigo-600 font-semibold tracking-wide uppercase">Features</h2>
          <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Intelligent Recruitment Made Simple
          </p>
        </div>

        <div class="mt-10">
          <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Automated CV Analysis</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                Process multiple CVs simultaneously with AI-powered analysis and scoring.
              </dd>
            </div>

            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Skill Matching</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                Advanced algorithms to match candidate skills with job requirements.
              </dd>
            </div>

            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Real-time Processing</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                Get instant analysis and recommendations for candidate profiles.
              </dd>
            </div>

            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Data Analytics</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                Comprehensive analytics and insights for better decision making.
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script> 