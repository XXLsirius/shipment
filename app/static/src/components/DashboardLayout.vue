<script setup lang="ts">
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'
import ContentFooter from './ContentFooter.vue';
</script>

<template>
  <div class="flex h-screen bg-gray-200 font-roboto">
    <Sidebar />

    <div class="flex-1 flex flex-col overflow-hidden">
      <Header />
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-200">
          <slot />
      </main>
      <ContentFooter />
    </div>
  </div>
</template>
