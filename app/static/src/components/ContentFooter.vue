<script setup>
import { ref } from "vue";
const company = ref("Company Name");
const contact = ref("Contact");
</script>

<template>
  <footer class="bg-white dark:bg-gray-800">
    <div
      class="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between"
    >
      <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400"
        >© 2023
        <a href="https://flowbite.com/" class="hover:underline">Shipment™</a>.
        All Rights Reserved.
      </span>
    </div>
  </footer>
</template>
<style></style>
