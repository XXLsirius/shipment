<script setup lang="ts">
import DashboardLayout from "../components/DashboardLayout.vue";
import ContentHeader from "../components/ContentHeader.vue";
import { STATIC_URL, defaultMariner } from "../config";
import { Button, IconClose, IconAdd } from "daisyui-vue";
import { VNodeRef, computed, onMounted, ref } from "vue";
import gql from "graphql-tag";
import {
  IMariner,
  getQueryReturn,
  getUpdateQLData,
  getUpdateQLParams,
} from "../types";
import { useLazyQuery, useMutation, useQuery } from "@vue/apollo-composable";
import { watch } from "vue";

const fileInput = ref<HTMLInputElement | null>(null);

const props = defineProps<{
  id: string;
}>();

defineOptions({ layout: DashboardLayout });

const QL_GET_MARINER = gql`
  query ($pk : String!) {
    marinerById(pk : $pk) {
      mariner {
        ${getQueryReturn(defaultMariner)}
      }
    }
  }
`;

const QL_UPATE_MARINERS = gql`
  mutation (
    ${getUpdateQLParams(defaultMariner)}
  ) {
    updateMariner(
      data: {
        ${getUpdateQLData(defaultMariner)}
      }
    ) {
      ok
    }
  }
`;
console.log(`mutation (
    ${getUpdateQLParams(defaultMariner)}
  ) {
    updateMariner(
      data: {
        ${getUpdateQLData(defaultMariner)}
      }
    ) {
      ok
    }
  }`)
const QL_DELETE_MARINERS = gql`
  mutation ($pk: String!) {
    deleteMariner(pk: $pk) {
      ok
    }
  }
`;
const QL_GET_SHIPS = gql`
  query {
    allShips(pageSize: 10000, pageIndex: 0, searchParams: []) {
      ship {
        pk
        name
      }
    }
  }
`;
const { result: resultShips } = useQuery(QL_GET_SHIPS);

const ships = computed(() => {
  return resultShips.value
    ? resultShips.value.allShips.map((ship: any) => ship.ship)
    : [];
  [];
});

const { refetch } = useQuery(QL_GET_MARINER, {
  pk: props.id,
});

let item = ref<IMariner>(defaultMariner);

const duties = ['duty 1', 'duty 2', 'duty 3'];
// watch(result, () => console.log(result));
const { mutate: mutateUpdate } = useMutation(QL_UPATE_MARINERS);

const QL_UPLOAD = gql`
  mutation ($file: Upload!) {
    uploadFile(file: $file) {
      success
    }
  }
`;
let selectedFile:any;
const { mutate: mutateUpload } = useMutation(QL_UPLOAD);
let img_path = ref("");
const handleFileUploadBtn = ()=>{
  console.log('object :>> ',fileInput.value);
  fileInput.value?.click()

}

const handleFileUpload = ({target:{files=[]}})=>{
  if (!files.length) {
            return
          }
          mutateUpload({ file: files[0] })
          .then((res) => {
          
            img_path.value = "/static/uploads/"+files[0].name;
            console.log('uploaderesult :>> ', img_path);
            item.value.photoUris = img_path.value;
          }
              
            )
        .catch((err) => console.error(err));
}
const handleFileDelete = ()=>{
  img_path.value ="";
  item.value.photoUris = img_path.value;
  console.log('img_path.value :>> ', img_path.value);
}
onMounted(() => {
  console.log("props.id :>> ", props.id);
  if (props.id !== "new") {
    refetch({ pk: props.id })
      ?.then((res) => {
        console.log(res.data.marinerById);
        item.value = Object.assign({}, res.data.marinerById.mariner);
        img_path.value = item.value.photoUris
      })
      .catch((err) => console.error(err));
  }
});

const onCancel = () => {
  window.history.back();
};

const onSave = (event) => {
  event.preventDefault();
  console.log("item.value :>> ", item.value);
  if (item.value.shipPk && item.value.name) {

    mutateUpdate(item.value)
      .then(() => {
        console.log("successfully saved");
        window.history.back();
      })
      .catch((err) => console.error(err));
  }
};



const ImageMariner = STATIC_URL + "images/u1304.svg";
</script>

<template>
  <ContentHeader :icon="'pe-7s-users'">Mariner Edit</ContentHeader>

  <div class="">
    <div class="">
      <form @submit="(event) => onSave(event)">
        <div class="flex flex-wrap mt-3 px-4">
          <div class="relative flex-none w-72 h-96 relatvie">
            <div class="border-2 bg-gray-300 cursor-pointer">
              <img name="photo" class="object-contain w-72 h-96" :src="img_path==''?ImageMariner:img_path" @click="handleFileUploadBtn"/>
            </div>
            <input type="file" class="hidden" @change="handleFileUpload" ref="fileInput"/>
            <button
              type="button"
              class="absolute top-0 right-0 px-1 text-white hover:bg-gray-600 hover:opacity-30"
              @click="handleFileDelete"
            >
              <icon-close size="1em" />
            </button>
          </div>

          <div class="flex-initial mx-4">
            <div class="mb-2">
              <label
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Name</label
              >
              <input
                type="text"
                v-model="item.name"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-48 p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
              />
              <label
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Ship</label
              >
              <select
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
                v-model="item.shipPk"
              >
                <option v-for="ship in ships" :value="ship.pk">
                  {{ ship.name }}
                </option>
              </select>

              <label
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Birthday</label
              >
              <input
                type="date"
                v-model="item.birthday"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              />

              <label
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Duty</label
              >
              <select
                v-model="item.duty"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              >
                <option v-for="duty in duties">
                  {{ duty}}
                </option>
              </select>

              <label
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Registered</label
              >
              <input
                type="date"
                v-model="item.registerDate"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              />

              <div class="flex items-center">
                <input
                  type="checkbox"
                  v-model="item.isRetired"
                  class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                />
                <label
                  class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >Retired</label
                >
              </div>
              <input
                type="date"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
                :disabled="!item.isRetired"
                v-model="item.retiredDate"
              />
            </div>
          </div>
          <div class="flex-wrap">
            <div class="d-flex float-end">
              <button
                type="submit"
                class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
              >
                Save
              </button>
              <button
                type="button"
                @click="onCancel"
                class="py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>

        <div class="px-4 py-2">
          <div
            class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
          >
            <div class="text-2xl me-4">Mariner Particulars</div>

            <div class="mt-4 grid grid-cols-12 gap-4">
              <div class="md:col-span-4 col-span-6">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Job</label
                >
                <input
                  type="text"
                  v-model="item.job"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="md:col-span-4 col-span-6">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Daily fee</label
                >
                <input
                  type="number"
                  v-model="item.dailyFee"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="md:col-span-4"></div>
              <div class="col-start-1 md:col-span-4 col-span-6">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >P----</label
                >
                <input
                  type="text"
                  v-model="item.platoon"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="md:col-span-8 col-span-6">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Previous affiliation</label
                >
                <input
                  type="text"
                  v-model="item.prevAffilication"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="col-span-5">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Place of Born</label
                >
                <input
                  type="text"
                  v-model="item.placeBorn"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="col-span-5 col-5">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Place of Residence</label
                >
                <input
                  type="text"
                  v-model="item.placeResidence"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="col-span-2 sm:col-span-2">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Code</label
                >
                <input
                  type="text"
                  v-model="item.code"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="md:col-span-4 col-span-6">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Mobile Phone</label
                >
                <input
                  type="text"
                  v-model="item.mobilePhone"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="md:col-span-4 col-span-6">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Home Phone</label
                >
                <input
                  type="text"
                  v-model="item.homePhone"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="col-span-9">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Graduated</label
                >
                <input
                  type="text"
                  v-model="item.graduate"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="col-span-3">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >&nbsp;</label
                >
                <input
                  type="date"
                  v-model="item.graduateDate"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="md:col-span-4 col-span-6">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Qualification grade</label
                >
                <input
                  type="text"
                  v-model="item.qualGrade"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="md:col-span-4 col-span-6">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Boarded Years</label
                >
                <input
                  type="number"
                  v-model="item.boardedYears"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
              <div class="col-span-12">
                <label
                  class="block text-sm font-medium text-gray-900 dark:text-white"
                  >Note</label
                >
                <textarea
                  v-model="item.note"
                  type="text"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                />
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
