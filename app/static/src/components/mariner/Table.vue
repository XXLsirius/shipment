<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useTableData } from "../../composables/useTableData";
import { Pagination, Input, Loading } from "daisyui-vue";
import { IMariner, FnLoad, FnDelete } from "../../types";
import { IMarinerAndCert } from "../../pages/Mariner.vue";
import { emit } from "process";

// props
const props = defineProps<{
  load_data: FnLoad<IMarinerAndCert>;
  forceReload: boolean;
  ships: Array<{ pk: string; name: string }>;
}>();

const emits = defineEmits(["detail"]);

let page = ref<number>(1);
let size = ref<number>(10);
let page_count = ref<number>(0);
let will_load = ref<number>(0);

let searchName = ref<string>("");
let searchShip = ref<string>("");
let items = ref<Array<IMarinerAndCert>>([]);
let img_path = ref<string>("");

const load = () => {
  props.load_data(
    page.value - 1,
    size.value,
    {
      searchName: searchName.value,
      searchShip: searchShip.value,
    },
    (data: IMarinerAndCert[], total_count) => {
      console.log("data :>> ", data);
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
  [page, size, searchShip, searchName, () => props.forceReload],
  (value, oldvalue) => {
    will_load.value++;
  }
);

onMounted(() => {
  will_load.value++;
});
</script>

<template>
  <div class="flex mb-2 pt-2">
    <div class="flex-initial me-2">
      <label
        for="searchName"
        class="block text-sm font-medium text-gray-900 dark:text-white"
        >Name</label
      >
      <input
        type="text"
        id="searchName"
        class="w-40 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-40 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        v-model="searchName"
        required
      />
    </div>
    <div class="flex-auto me-2">
      <label
        for="searchShip"
        class="block text-sm font-medium text-gray-900 dark:text-white"
        >Ship</label
      >
      <select
        id="pageSize"
        v-model="searchShip"
        class="w-40 ms-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-14 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        <option value="">All</option>
        <option v-for="ship in ships" :value="ship.pk">{{ ship.name }}</option>
      </select>
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
            class="w-10 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            #
          </th>
          <th
            class="px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Name
          </th>
          <th
            class="px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Ship
          </th>

          <th
            class="w-48 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Duty(Job)
          </th>
          <th
            class="w-48 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Certificate(Expire)
          </th>
        </tr>
      </thead>

      <tbody class="bg-white">
        <tr
          v-for="(item, index) in items"
          :key="index"
          :class="index % 2 ? 'bg-gray-200' : ''"
        >
          <td>
            {{ (page - 1) * size + index + 1 }}
          </td>
          <td
            class="px-4 py-2 border-b border-gray-200 cursor-pointer"
            @click="(event) => emits('detail', item)"
          >
            <div class="text-sm leading-5 text-gray-900 flex">
              <img :src="item.photoUris" class="w-10 h-10 rounded-full me-4" />
              <span class="mt-2">
                {{ item.name }}
              </span>
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.ship }}
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.duty }} <br />{{ item.job }}
            </div>
          </td>

          <td class="px-4 py-2 border-b border-gray-200">
            <div class="flex">
              <div class="grow text-sm leading-5 text-gray-900">
                {{
                  item.certificates.length > 0
                    ? item.certificates[item.certificates.length - 1].certtype
                        ?.name && ""
                    : ""
                }}
                ({{
                  item.certificates.length > 0
                    ? item.certificates[item.certificates.length - 1]
                        .issueExpireDate
                    : ""
                }})
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
