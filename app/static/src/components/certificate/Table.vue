<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useTableData } from "../../composables/useTableData";
import { Pagination, Input, Loading } from "daisyui-vue";
import { ICertificate, FnLoad, FnDelete } from "../../types";
import { ICertificateAndCert } from "../../pages/Certificate.vue";
import { emit } from "process";

// props
const props = defineProps<{
  load_data: FnLoad<ICertificateAndCert>;
  forceReload: boolean;
  ships: Array<{ pk: string; name: string }>;
  certtypes: Array<{ pk: string; name: string }>;
  kind: number;
}>();

const emits = defineEmits(["detail"]);

let page = ref<number>(1);
let size = ref<number>(10);
let page_count = ref<number>(0);
let will_load = ref<number>(0);

let searchCerttype = ref<string>("");
let searchShip = ref<string>("");
let searchDepartment = ref<string>("");
let searchMariner = ref<string>("");

let items = ref<Array<ICertificateAndCert>>([]);

const load = () => {
  props.load_data(
    page.value - 1,
    size.value,
    {
      searchCerttype: searchCerttype.value,
      searchDepartment: searchDepartment.value,
      searchShip: searchShip.value,
      searchMariner: searchMariner.value,
    },
    (data: ICertificateAndCert[], total_count) => {
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
  [
    page,
    size,
    searchShip,
    searchCerttype,
    searchDepartment,
    searchMariner,
    () => props.forceReload,
    () => props.kind,
  ],
  (value, oldvalue) => {
    will_load.value++;
  }
);

onMounted(() => {
  will_load.value++;
});

const departments = ["department 1", "department 2", "department 3"];
</script>

<template>
  <div class="flex mb-2 pt-4">
    <div class="flex-initial me-2">
      <label class="block text-sm font-medium text-gray-900 dark:text-white"
        >Department</label
      >
      <select
        v-model="searchDepartment"
        class="w-40 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-14 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        <option value="">All</option>
        <option v-for="depart in departments">{{ depart }}</option>
      </select>
    </div>
    <div class="me-2">
      <label class="block text-sm font-medium text-gray-900 dark:text-white"
        >Certificate</label
      >
      <select
        v-model="searchCerttype"
        class="w-40 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-14 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        <option value="">All</option>
        <option v-for="certtype in certtypes" :value="certtype.pk">
          {{ certtype.name }}
        </option>
      </select>
    </div>
    <div class="me-2">
      <label class="block text-sm font-medium text-gray-900 dark:text-white"
        >Ship</label
      >
      <select
        id="pageSize"
        v-model="searchShip"
        class="w-40 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-14 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        <option value="">All</option>
        <option v-for="ship in ships" :value="ship.pk">{{ ship.name }}</option>
      </select>
    </div>
    <div class="me-2" v-if="kind == 1">
      <label
        for="searchName"
        class="block text-sm font-medium text-gray-900 dark:text-white"
        >Person</label
      >
      <input
        type="text"
        id="searchName"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-40 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        v-model="searchMariner"
        required
      />
    </div>
    <div class="m-auto"></div>
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
            class="w-32 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Department
          </th>
          <th
            class="px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Certificate / ID
          </th>

          <th
            class="w-32 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Ship
          </th>
          <th
            v-if="kind == 1"
            class="w-32 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Person
          </th>
          <th
            class="w-48 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Issue / Expiration Date
          </th>
          <th
            class="w-32 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Price / Reg.Fee
          </th>
          <th
            class="w-48 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
          >
            Account / Amount
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
            class="px-4 py-2 border-b border-gray-200"
            @click="(event) => emits('detail', item)"
          >
            <div class="text-sm leading-5 text-gray-900">
              <img />
              {{ item.issueDepartment }}
            </div>
          </td>

          <td class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.certtype?.name }} <br />{{ item.issueId }}
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.ship }}
            </div>
          </td>
          <td v-if="kind == 1" class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.mariner }}
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.issueDate }} <br />{{ item.issueExpireDate }}
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="grow text-sm leading-5 text-gray-900">
              {{ item.issuePrice }} <br />{{ item.issueRegfee }}
            </div>
          </td>
          <td class="px-4 py-2 border-b border-gray-200">
            <div class="flex">
              <div class="grow text-sm leading-5 text-gray-900">
                <div class="grow text-sm leading-5 text-gray-900">
                  {{ item.issueAccount }} <br />{{ item.issueAmount }}
                </div>
              </div>
              <div class="flex-auto flex flex-row-reverse">
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
