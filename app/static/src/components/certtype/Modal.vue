<script setup lang="ts">
import {
  ModalBase,
  ModalBody,
  ModalTitle,
  ModalAction,
  Button,
} from "daisyui-vue";

import { ICertType } from "../../types";
import { ref, watch } from "vue";

const props = defineProps<{
  open: boolean;
  data?: ICertType | null;
}>();

const item = ref<ICertType>({
  pk: "",
  name: "",
  agency: "",
  note: "",
  kind: 0,
});

watch(
  () => props.data,
  (cur, old) => {
    console.log("cur :>> ", cur);
    if (cur !== null) item.value = Object.assign({}, cur);
    else
      item.value = {
        pk: "",
        name: "",
        agency: "",
        note: "",
        kind: 0,
      };
  }
);

const emits = defineEmits(["close"]);
const onClose = (action: string, event: Event) => {
  if (event) event.preventDefault();
  emits("close", action, item.value);
};
</script>

<template>
  <ModalBase :open="open" :onClose="($event) => onClose('cancel')">
    <ModalTitle :onClose="($event) => onClose('cancel')">
      Type of Certificate
    </ModalTitle>
    <form @submit="($event) => onClose('save', $event)">
      <ModalBody>
        <div>
          <label
            for="name"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >Name</label
          >
          <input
            type="text"
            id="name"
            class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
            v-model="item.name"
          />
        </div>

        <div>
          <label
            for="agency"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >Issuing Agency</label
          >
          <input
            type="text"
            id="agency"
            class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
            v-model="item.agency"
          />
        </div>

        <div>
          <label
            for="note"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >Note</label
          >
          <textarea
            id="note"
            rows="4"
            class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Leave a comment..."
            v-model="item.note"
          ></textarea>
        </div>
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
          @click="onClose('cancel')"
        >
          Cancel
        </button>
      </ModalAction>
    </form>
  </ModalBase>
</template>
