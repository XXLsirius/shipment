<script setup lang="ts">
import {
  ModalBase,
  ModalBody,
  ModalTitle,
  ModalAction,
  Button,
} from "daisyui-vue";

import { ICharterer } from "../../types";
import { ref, watch } from "vue";
import gql from "graphql-tag";
import { useQuery } from "@vue/apollo-composable";

export interface ICertAddInfo {
  certtypePk: string;
  shipPk: string;
  marinerPk: string;
}

const props = defineProps<{
  kind: number;
  open: boolean;
  certtypes: Array<{ pk: string; name: string, kind : number }>;
  ships: Array<{ pk: string; name: string }>;
}>();

const item = ref<ICertAddInfo>({
  certtypePk: "",
  shipPk: "",
  marinerPk: "",
});

const mariners = ref<Array<{ pk: string; name: string }>>([]);
const QL_GET_MARINERS = gql`
  query ($ship: String!) {
    allMariners(
      pageSize: 1000
      pageIndex: 0
      searchParams: [{ key: "shipPk", value: $ship, op: "equal" }]
    ) {
      mariner {
        pk
        name
      }
    }
  }
`;

const { refetch } = useQuery(QL_GET_MARINERS, {
  ship: "",
});

watch(
  () => props,
  () => {
    item.value = {
      certtypePk: "",
      shipPk: "",
      marinerPk: "",
    };
  }
);

const emits = defineEmits(["close"]);

const onClose = (event: Event) => {
  event.preventDefault();
  emits("close", "cancel", item.value);
};

const onSave = (event: Event) => {
  event.preventDefault();

  emits("close", "save", item.value);
};

const onSelectShip = (event: Event) => {
  const ship = item.value.shipPk;

  refetch({ ship })?.then((res) => {
    mariners.value = res.data.allMariners.map((_ : any) => _.mariner);
    item.value.marinerPk = mariners.value.length > 0 ? mariners.value[0].pk : "";
  });
};
</script>

<template>
  <ModalBase :open="open" :onClose="onClose">
    <ModalTitle :onClose="onClose"> Type of Certificate </ModalTitle>
    <form @submit="onSave">
      <ModalBody>
        <div>
          <label
            for="certificate"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >Certificate</label
          >
          <select
            id="certificate"
            v-model="item.certtypePk"
            class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
          >
            <option v-for="certtype of certtypes.filter(cert => cert.kind == kind)" :value="certtype.pk">
              {{ certtype.name }}
            </option>
          </select>
        </div>

        <div>
          <label
            for="ship"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >Ship</label
          >
          <select
            id="certificate"
            v-model="item.shipPk"
            @change="onSelectShip"
            class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
          >
            <option v-for="ship of ships" :value="ship.pk">
              {{ ship.name }}
            </option>
          </select>
        </div>

        <div v-if="kind == 1">
          <label
            for="ship"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >Mariner</label
          >
          <select
            id="certificate"
            v-model="item.marinerPk"
            class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
          >
            <option v-for="mariner of mariners" :value="mariner.pk">
              {{ mariner.name }}
            </option>
          </select>
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
          @click="onClose"
        >
          Cancel
        </button>
      </ModalAction>
    </form>
  </ModalBase>
</template>
