<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useTableData } from "../../composables/useTableData";
import { Pagination, Input, Loading } from "daisyui-vue";
import { IShip, FnLoad, FnDelete } from "../../types";
import { IShipAndCert } from "../../pages/Ship.vue";
import { emit } from "process";

// props
const props = defineProps<{
  load_data: FnLoad<IShipAndCert>;
  forceReload: boolean;
}>();

const emits = defineEmits(["detail"]);

let page = ref<number>(1);
let size = ref<number>(10);
let page_count = ref<number>(0);
let will_load = ref<number>(0);

let searchNation = ref<string>("");
let searchCompany = ref<string>("");
let items = ref<Array<IShipAndCert>>([]);

const load = () => {
  props.load_data(
    page.value - 1,
    size.value,
    {},
    (data: IShipAndCert[], total_count) => {
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
  <div class="mb-2 pt-2">
    <div class="flex me-2">
      asdfasdf
      <label>&nbsp;</label>
      <Loading variant="ball" color="#4C51BF" />
      <div class="ml-auto flex items-center">
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
            class="px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Vessel
          </th>
          <th
            class="w-40 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            IMO / CS
          </th>

          <th
            class="w-40 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Length / Beam
          </th>
          <th
            class="w-40 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            DWT / GT
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
          <td
            class="px-4 py-2 border-b border-gray-200 cursor-pointer"
            @click="(event) => emits('detail', item)"
          >
            <div class="text-sm leading-5 text-gray-900 flex">
              <img
                :src="'/static/uploads/' + item.photoUris.split(';')[0]"
                class="w-20 h-16 me-4 border-1 border-gray-500 object-contain"
              />
              <span class="mt-5 text-lg font-medium">
                {{ item.name }}
              </span>
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.imoNumber }} <br />{{ item.callsign }}
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.length }} <br />{{ item.beam }}
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.deadWeight }} <br />{{ item.grossTonnage }}
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
