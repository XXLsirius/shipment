<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useTableData } from "../../composables/useTableData";
import { Pagination, Input, Loading } from "daisyui-vue";
import { ICharterer, FnLoad, FnDelete } from "../../types";

// props
const props = defineProps<{
  load_data: FnLoad<ICharterer>;
  forceReload: boolean;
}>();

let page = ref<number>(1);
let size = ref<number>(10);
let page_count = ref<number>(0);
let will_load = ref<number>(0);

let searchNation = ref<string>("");
let searchCompany = ref<string>("");
let items = ref<Array<ICharterer>>([]);

const load = () => {
  props.load_data(
    page.value - 1,
    size.value,
    { nation: searchNation.value, company: searchCompany.value },
    (data: ICharterer[], total_count) => {
      will_load.value = 0;
      items.value = data;
      if (total_count) {
        let count = Math.ceil(total_count / size.value);
        if (count < page.value) {
          page.value = Math.max(1, count);
        }
        page_count.value = count;
      }
    }
  );
};

watch(will_load, (cur, old) => {
  if (cur == 0) return;
  const timeoutId = setTimeout(() => {
    load();
  }, 200);
});

watch(
  [page, size, searchCompany, searchNation, () => props.forceReload],
  (value, oldvalue) => {
    will_load.value++;
  }
);

onMounted(() => {
  will_load.value++;
});
</script>

<template>
  <div class="flex mb-2 pt-4">
    <div class="flex-initial me-2">
      <label
        for="searchCompany"
        class="block text-sm font-medium text-gray-900 dark:text-white"
        >Company</label
      >
      <input
        type="text"
        id="searchCompany"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-40 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        v-model="searchCompany"
        required
      />
    </div>
    <div class="flex-auto me-2">
      <label
        for="searchNation"
        class="block text-sm font-medium text-gray-900 dark:text-white"
        >Nation</label
      >
      <input
        type="text"
        id="searchNation"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-40 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        v-model="searchNation"
        required
      />
    </div>

    <div class="flex-none me-2">
      <label>&nbsp;</label>
      <div class="flex items-center">
        <label
          for="pageSize"
          class="block text-sm font-medium text-gray-900 dark:text-white"
          >Show</label
        >
        <select
          id="pageSize"
          v-model="size"
          class="ms-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-14 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        >
          <option selected>5</option>
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="30">30</option>
          <option value="50">50</option>
        </select>
        <label
          class="ms-2 block text-sm font-medium text-gray-900 dark:text-white"
          >entries</label
        >
      </div>
    </div>
  </div>
  <div class="overflow-x-auto">
    <table class="min-w-full">
      <thead>
        <tr class="bg-sky-950 text-white">
          <th
            class="px-4 py-2 text-xs w-10 font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            #
          </th>
          <th
            class="px-4 py-2 text-xs w-48 font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Company
          </th>
          <th
            class="px-4 py-2 text-xs w-48 font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Nation
          </th>
          <th
            class="px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Phone
          </th>
          <th
            class="px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Email
          </th>
        </tr>
      </thead>

      <tbody class="bg-white">
        <tr
          v-for="(item, index) in items"
          :key="index"
          :class="index % 2 ? 'bg-gray-200' : ''"
        >
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                {{ (page - 1) * size + index + 1 }}
              </div>
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="text-sm leading-5 text-gray-900">
              {{ item.company }}
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="text-sm leading-5 text-gray-900">
              {{ item.nation }}
            </div>
          </td>

          <td class="px-4 py-2 border-b border-gray-200">
            <div class="text-sm leading-5 text-gray-900">
              {{ item.phone }}
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="flex">
              <div class="grow text-sm leading-5 text-gray-900">
                {{ item.email }}
              </div>
              <div class="flex-auto flex flex-row-reverse">
                <button
                  type="button"
                  class="flex-end btn pe-7s-close-circle text-xl font-bold hover:text-blue-700"
                  @click="($event) => $emit('delete', item)"
                />
                <button
                  class="flex-end btn pe-7s-pen text-xl font-bold hover:text-blue-700 px-2"
                  @click="$emit('edit', item)"
                />
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="flex">
    <div class="grow"></div>
    <Pagination class="flex-none m-1" :total="page_count" v-model="page" />
  </div>
</template>
