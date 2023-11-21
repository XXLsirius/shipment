<script setup lang="ts">
import {
  ModalBase,
  ModalBody,
  ModalTitle,
  ModalAction,
  Button,
} from "daisyui-vue";

const props = defineProps<{
  open: boolean;
}>();

const emits = defineEmits(["close"]);
const onClose = (action: string, event: Event) => {
  if (event) event.preventDefault();
  emits("close", action);
};
</script>

<template>
  <ModalBase :open="open" :onClose="(event) => onClose('cancel', event)">
    <ModalTitle :onClose="(event) => onClose('cancel', event)"> Delete </ModalTitle>
    <form @submit="(event) => onClose('save', event)">
      <ModalBody>
        <div class="text-lg"><slot/></div>
      </ModalBody>

      <ModalAction>
        <button
          type="submit"
          class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
        >
          OK
        </button>
        <button
          type="button"
          class="py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
          @click="(event) => onClose('cancel', event)"
        >
          Cancel
        </button>
      </ModalAction>
    </form>
  </ModalBase>
</template>
