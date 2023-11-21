<script setup lang="ts">
import DashboardLayout from "../components/DashboardLayout.vue";
import ContentHeader from "../components/ContentHeader.vue";
import { STATIC_URL, defaultShip } from "../config";
import { Button, IconClose, IconAdd } from "daisyui-vue";
import { computed, onMounted, ref } from "vue";
import gql from "graphql-tag";
import {
  IShip,
  getQueryReturn,
  getUpdateQLData,
  getUpdateQLParams,
} from "../types";
import { useLazyQuery, useMutation, useQuery } from "@vue/apollo-composable";
import { watch } from "vue";

const props = defineProps<{
  id: string;
}>();

defineOptions({ layout: DashboardLayout });

const QL_GET_SHIP = gql`
  query ($pk : String!) {
    shipById(pk : $pk) {
      ship {
        ${getQueryReturn(defaultShip)}
      }
    }
  }
`;

const QL_UPATE_SHIPS = gql`
  mutation (
    ${getUpdateQLParams(defaultShip)}
  ) {
    updateShip(
      data: {
        ${getUpdateQLData(defaultShip)}
      }
    ) {
      ok
    }
  }
`;

const QL_DELETE_SHIPS = gql`
  mutation ($pk: String!) {
    deleteShip(pk: $pk) {
      ok
    }
  }
`;

const { refetch } = useQuery(QL_GET_SHIP, {
  pk: props.id,
});

let item = ref<IShip>(defaultShip);

// watch(result, () => console.log(result));
const { mutate: mutateUpdate } = useMutation(QL_UPATE_SHIPS);

onMounted(() => {
  console.log("props.id :>> ", props.id);
  if (props.id !== "new") {
    refetch({ pk: props.id })
      ?.then((res) => {
        console.log(res.data.shipById);
        item.value = Object.assign({}, res.data.shipById.ship);
      })
      .catch((err) => console.error(err));
  }
});

const ImageShip = STATIC_URL + "images/ship_preview.png";

const onCancel = () => {
  window.history.back();
};

const onSave = (event) => {
  if (event) event.preventDefault();

  console.log("item.value :>> ", item.value);
  mutateUpdate(item.value)
    .then(() => {
      console.log("successfully saved");
      window.history.back();
    })
    .catch((err) => console.error(err));
};

let testUris = ref<string>("download (2).jpg;Hadoop.jpg;skype.jpg");
let index = 0;
let uri = "";
let mainUri = ref<String>("");
const photoUris = computed(() => {
  let split = item.value.photoUris.split(";");
  if (split.length > 0) mainUri.value = split[0];
  return item.value.photoUris == "" ? [] : item.value.photoUris.split(";");
});

const handleEvent = (id) => {
  index = id;
  console.log("Select:id :>> ", id);
  if (id == photoUris.value.length) {
    fileInput.value?.click();
    return;
  }
  mainUri.value = photoUris.value[index];
};
const handleDelete = (id) => {
  // if(id == photoUris.value.length)
  // {
  //   fileInput.value?.click();
  //   return;
  // }
  // mainUri.value = photoUris.value[index];
  console.log("Delete:id :>> ", id);
  let tmpUris = "";
  for (let i = 0; i < photoUris.value.length; i++) {
    if (i != id) {
      if (tmpUris == "") tmpUris += photoUris.value[i];
      else tmpUris += ";" + photoUris.value[i];
    }
  }
  item.value.photoUris = tmpUris;
  index = 0;
  if (photoUris.value[0] != undefined) mainUri.value = photoUris.value[0];
};
let fileInput = ref<HTMLInputElement | null>(null);
let fileValue = ref(null);
const QL_UPLOAD = gql`
  mutation ($file: Upload!) {
    uploadFile(file: $file) {
      success
    }
  }
`;
const { mutate: mutateUpload } = useMutation(QL_UPLOAD);
const handleFileUpload = ({ target: { files = [] } }) => {
  if (!files.length) {
    return;
  }
  mutateUpload({ file: files[0] })
    .then((res) => {
      let filename = files[0].name;
      if (item.value.photoUris == "") item.value.photoUris += filename;
      else item.value.photoUris += ";" + filename;
      console.log("item.value.photoUris :>> ", item.value.photoUris);
      fileValue.value = null;
    })
    .catch((err) => console.error(err));
};
</script>

<template>
  <ContentHeader :icon="'pe-7s-helm'">Ship Edit</ContentHeader>

  <form @submit="(event) => onSave(event)">
    <div class="flex px-4 pt-2">
      <div class="flex">
        <div class="me-2">
          <label class="block text-sm font-medium text-gray-900 dark:text-white"
            >Vessel Name</label
          >
          <input
            type="text"
            class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-48 p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            v-model="item.name"
            required
          />
        </div>
        <div class="me-2">
          <label class="block text-sm font-medium text-gray-900 dark:text-white"
            >Registerd</label
          >
          <input
            type="date"
            class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-48 p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            v-model="item.registerdDate"
            required
          />
        </div>
        <div>
          <div class="flex">
            <input
              type="checkbox"
              v-model="item.isRemoved"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
            />
            <label
              class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Removed</label
            >
          </div>
          <input
            type="date"
            :disabled="!item.isRemoved"
            v-model="item.removedDate"
            class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
      </div>
      <div class="mx-6">
        <label class="block text-sm font-medium text-gray-900 dark:text-white"
          >&nbsp;</label
        >
        <div class="">
          <button
            type="submit"
            class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
          >
            Save
          </button>
          <button
            type="button"
            class="py-2 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
            @click="onCancel"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>

    <div class="px-4 py-2">Photos</div>
    <div class="flex flex-wrap px-4">
      <div class="relative flex-none w-96 h-72 mb-2 me-2">
        <div class="border-2 bg-gray-300 cursor-pointer">
          <img
            name="photo"
            class="object-contain w-96 h-72"
            :src="mainUri == '' ? ImageShip : '/static/uploads/' + mainUri"
          />
        </div>
      </div>

      <div class="flex-initial">
        <div class="grid grid-cols-3 gap-2">
          <div v-for="(uri, index) in photoUris" class="relative">
            <img
              class="w-32 h-24 bg-gray-300 object-contain cursor-pointer"
              :src="'/static/uploads/' + uri"
              @click="handleEvent(index)"
            />
            <button
              type="button"
              class="absolute top-0 right-0 px-1 text-white hover:bg-gray-600 hover:opacity-30"
              @click="handleDelete(index)"
            >
              <icon-close size="0.75em" />
            </button>
          </div>

          <div
            class="border border-dashed border-black flex cursor-pointer w-32 h-24"
            @click="handleEvent(photoUris.length)"
          >
            <input
              type="file"
              class="hidden"
              ref="fileInput"
              @change="handleFileUpload"
              :value="fileValue"
            />
            <icon-add class="m-auto" />
          </div>
        </div>
      </div>
    </div>

    <div class="px-4 py-2">
      <div
        class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
      >
        <div class="text-2xl me-4">Vessel Particulars</div>

        <div class="mt-4 grid grid-cols-12 gap-4">
          <div class="md:col-span-4 col-span-6">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Ship type</label
            >
            <input
              type="text"
              v-model="item.shipType"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="md:col-span-8 col-span-6"></div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Year of Build</label
            >
            <input
              v-model="item.buildYear"
              type="text"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Flag</label
            >
            <input
              type="text"
              v-model="item.flag"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Homeport</label
            >
            <input
              type="text"
              v-model="item.homeport"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Reg. Number</label
            >
            <input
              type="text"
              v-model="item.regNumber"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Callsign</label
            >
            <input
              type="text"
              v-model="item.callsign"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >IMO Number</label
            >
            <input
              type="text"
              v-model="item.imoNumber"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Gross Tonnage (t)</label
            >
            <input
              v-model="item.grossTonnage"
              type="number"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Net Tonnage (t)</label
            >
            <input
              type="number"
              v-model="item.grossTonnage"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >DeadWeight (t)</label
            >
            <input
              type="number"
              v-model="item.deadWeight"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Length (m)</label
            >
            <input
              type="number"
              v-model="item.length"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Beam (m)</label
            >
            <input
              type="number"
              v-model="item.beam"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Depth (m)</label
            >
            <input
              type="number"
              v-model="item.depth"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-4">
            <label
              class="block text-sm font-medium text-gray-900 dark:text-white"
              >Draught (m)</label
            >
            <input
              type="number"
              v-model="item.draught"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div class="col-span-12">
            <p>Note</p>
            <textarea
              name="note"
              type="text"
              v-model="item.note"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
        </div>
      </div>
    </div>
  </form>
</template>
<style></style>
