<script setup lang="ts">
import DashboardLayout from "../components/DashboardLayout.vue";


import ContentHeader from "../components/ContentHeader.vue";
import { STATIC_URL, defaultCertificate, defaultShip } from "../config";
import { Button, IconClose, IconAdd } from "daisyui-vue";
import {computed, onMounted, ref } from "vue";
import gql from "graphql-tag";
import {
  IShip,
  getQueryReturn,
} from "../types";
import { useQuery } from "@vue/apollo-composable";
import { router } from "@inertiajs/core";
import { IShipAndCert } from "./Ship.vue";

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
      certificates {
        ${getQueryReturn(defaultCertificate)}
      }
    }
  }
`;

const { refetch } = useQuery(QL_GET_SHIP, {
  pk: props.id,
});

let item = ref<IShipAndCert>({...defaultShip, certificates: []});

// watch(result, () => console.log(result)

const ImageShip = STATIC_URL + 'images/ship_preview.png';
const ImageAdd = STATIC_URL + 'images/ship-plus.png';
onMounted(() => {
  console.log("props.id :>> ", props.id);
  if (props.id !== "new") {
    refetch({ pk: props.id })
      ?.then((res) => {

        console.log(res.data.shipById)
        item.value = Object.assign({},res.data.shipById.ship, {certificates : res.data.shipById.certificates});
      })
      .catch((err) => console.error(err));
  }
});


const onCancel = () => {
  window.history.back();
};

const onEdit = () => {
  console.log("item.value :>> ", item.value);
  router.get('/ship/edit', {id : item.value.pk});
};

const certificate = computed(() => {
  return item.value.certificates.length > 0 ? item.value.certificates[item.value.certificates.length - 1] : undefined;
})

//let testUris = "download (2).jpg;Hadoop.jpg;skype.jpg"
let index = 0;
let uri = "";
let mainUri = ref<String>("");
  const photoUris = computed(() => {
  let split = item.value.photoUris.split(";");
  if(split.length>0) mainUri.value=split[0];
  return (item.value.photoUris=="")
    ?[]: item.value.photoUris.split(";")
     ;
});

const handleEvent=(id)=>{
  index= id;
  console.log('index :>> ', index);
  mainUri.value = photoUris.value[index];
}

</script>

<template>
  <ContentHeader :icon="'pe-7s-helm'">Ship Detail</ContentHeader>

  <div class="flex-1 mx-4 mt-4">
    <div class="flex">
      <div class="flex-auto">
        <p class="text-4xl pb-4 font-bold">CMA CGM TROCADERO</p>
        <p class="text-xl py-1 text-gray-500">Registerd: {{ item.registerdDate }}</p>
        <p class="text-xl py-1 text-gray-500">
          Certificate: {{certificate ? certificate.certtype?.name && "" : ""}} (to {{ certificate ? certificate.issueExpireDate : "" }})
        </p>
        <p class="text-xl py-1 text-gray-500">Rmoved: {{item.isRemoved ? item.removedDate : "-"}}</p>
      </div>
      <div>
        <button
          type="button"
          class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
          @click="onEdit"
        >
          Edit
        </button>
        <button
          type="button"
          @click="onCancel"
          class="py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-200 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
        >
          Back
        </button>
      </div>
    </div>

    <div class="">
      {{ item.note }}
    </div>
  </div>

  <div class="flex flex-wrap px-4">
    <div class="flex-none w-96 h-72 mb-2 me-2">
      <div class="bg-gray-300 cursor-pointer">
        <img name="photo" class="object-contain w-96 h-72" :src="mainUri=='' ? ImageShip: '/static/uploads/'+mainUri" />
      </div>
    </div>

    <div class="">
      <div class="grid grid-cols-3 gap-2">
        <div v-for="(uri,index) in photoUris" class="relative">
          <img
            class="w-32 h-24 bg-gray-300 object-contain cursor-pointer"
            :src="'/static/uploads/'+uri"
            @click="handleEvent(index)"
          />
        </div>
        <input type="file" class="hidden" />
      </div>
    </div>
  </div>

  <div class="px-4 py-2">
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="text-2xl me-4">Vessel Particulars</div>

      <table class="mt-4 min-w-full">
        <thead>
          <tr class="bg-sky-950 text-white">
            <th
              class="w-48 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
            >
              Item
            </th>
            <th
              class="px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
            >
              Value
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">Ship type</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.shipType }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">Year of Built</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.buildYear }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">Flag</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.flag }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">
              Homeport
            </td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.homeport }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">Reg. Number</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.regNumber }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">
              Callsign
            </td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.callsign }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">IMO Number</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.imoNumber }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">Gross Tonnage (t)</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.grossTonnage }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">Net Tonnage (t)</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.grossTonnage }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">Deadweight (t)</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.deadWeight }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">
              Length (m)
            </td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.length }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">Beam (m)</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.beam }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">Depth (m)</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.depth }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">Draught (m)</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.draught }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
