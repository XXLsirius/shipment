<script setup lang="ts">
const props = defineProps<{icon: string }>();
</script>
<template>
  <div class="bg-white border-2 border-b-gray-200 shadow dark:bg-gray-800">
    <div
      class="w-full max-w-screen-xl p-4 flex items-center"
    >
      <i
        class="text-2xl w-16 h-16 p-5 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
        :class="icon"
      ></i>
      <div class="px-4">
        <div class="text-3xl uppercase" style="color: #b9cf25"><slot/></div>
        <div class="text-sm">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean
          euismodbibendum laoreet. Proin gravida dolor sit amet lacus accumsan
          et viverrajusto commodo.
        </div>
      </div>
    </div>
  </div>
</template>

<style>
h1 {
  color: #b9cf25;
}
</style>
