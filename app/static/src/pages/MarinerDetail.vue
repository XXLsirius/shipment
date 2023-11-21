<script setup lang="ts">
import DashboardLayout from "../components/DashboardLayout.vue";

import ContentHeader from "../components/ContentHeader.vue";
import { STATIC_URL, defaultCertificate, defaultMariner } from "../config";
import { Button, IconClose, IconAdd } from "daisyui-vue";
import { computed, onMounted, ref } from "vue";
import gql from "graphql-tag";
import { IMariner, getQueryReturn } from "../types";
import { useQuery } from "@vue/apollo-composable";
import { router } from "@inertiajs/core";
import { IMarinerAndCert } from "./Mariner.vue";

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
      certificates {
        ${getQueryReturn(defaultCertificate)}
      }
    }
  }
`;

const { refetch } = useQuery(QL_GET_MARINER, {
  pk: props.id,
});

let item = ref<IMarinerAndCert>({
  ...defaultMariner,
  certificates: [],
  ship: "",
});

let img_path = ref<string>("");

// watch(result, () => console.log(result)

onMounted(() => {
  if (props.id !== "new") {
    refetch({ pk: props.id })
      ?.then((res) => {
        console.log(res.data.marinerById);
        item.value = Object.assign({}, res.data.marinerById.mariner, {
          certificates: res.data.marinerById.certificates,
        });
        
        img_path.value= item.value.photoUris;

      })
      .catch((err) => console.error(err));
  }
});

const onCancel = () => {
  window.history.back();
};

const onEdit = () => {
  console.log("item.value :>> ", item.value);
  router.get("/mariner/edit", { id: item.value.pk });
};

const ImageMariner = STATIC_URL + "images/u1304.svg";
</script>

<template>
  <ContentHeader :icon="'pe-7s-users'">Mariner Detail</ContentHeader>

  <div class="flex flex-wrap mt-3 px-4">
    <div class="flex-none w-72 h-96">
      <div class="border-2 bg-gray-300 cursor-pointer">
        <img name="photo" class="object-contain w-72 h-96"  :src="img_path==''?ImageMariner:img_path"/>
      </div>
      <input type="file" class="hidden" />
    </div>

    <div class="flex-1 mx-4">
      <div class="flex">
        <div class="flex-auto">
          <p class="text-4xl pb-4 font-bold">Person Name</p>
          <p class="text-xl py-1 text-gray-500">
            Birthday: {{ item.birthday }}
          </p>
          <p class="text-xl py-1 text-gray-500">Mariner: {{ item.name }}</p>
          <p class="text-xl py-1 text-gray-500">Duty: {{ item.duty }}</p>
          <p class="text-xl py-1 text-gray-500">
            Registered: {{ item.registerDate }}
          </p>
          <p class="text-xl py-1 text-gray-500">
            Retired: {{ item.isRetired ? item.retiredDate : "-" }}
          </p>
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
            @click="onCancel"
            type="button"
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
  </div>

  <div class="px-4 py-2">
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="text-2xl me-4 mb-4 uppercase">Mariner Particulars</div>

      <table class="min-w-full">
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
            <td class="px-4 py-2 border-b border-gray-200">Job</td>
            <td class="px-4 py-2 border-b border-gray-200">{{item.job}}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">Daily fee</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.dailyFee }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">P----</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.platoon }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">
              Previous affiliation
            </td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.prevAffilication }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">Place of Born</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.placeBorn }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">
              Place of Residence
            </td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.placeResidence }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">Code</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.code }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">Mobile Phone</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.mobilePhone }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">Home Phone</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.homePhone }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">Graduated</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.graduate }}</td>
          </tr>
          <tr>
            <td class="px-4 py-2 border-b border-gray-200">
              Qualification grade
            </td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.qualGrade }}</td>
          </tr>
          <tr class="bg-gray-200">
            <td class="px-4 py-2 border-b border-gray-200">Boarded Years</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ item.boardedYears }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="px-4 py-2">
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="text-2xl me-4 mb-4 uppercase">Personal Certificates</div>

      <table class="min-w-full">
        <thead>
          <tr class="bg-sky-950 text-white">
            <th
              class="w-48 px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left border-b border-gray-200"
            >
              Name
            </th>
            <th
              class="px-4 py-2 text-xs font-medium leading-4 tracking-wider border-b border-gray-200"
            >
              Number
            </th>
            <th
              class="w-20 px-4 py-2 text-xs font-medium leading-4 tracking-wider border-b border-gray-200"
            >
              Issue
            </th>
            <th
              class="w-20 px-4 py-2 text-xs font-medium leading-4 tracking-wider border-b border-gray-200"
            >
              Expire
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cert in item.certificates">
            <td class="px-4 py-2 border-b border-gray-200">
              {{ cert.certtype?.name }}
            </td>
            <td class="px-4 py-2 border-b border-gray-200">{{ cert.issueId }}</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ cert.issueDate }}</td>
            <td class="px-4 py-2 border-b border-gray-200">{{ cert.issueExpireDate }}</td>
          </tr>
          
        </tbody>
      </table>
    </div>
  </div>
</template>
