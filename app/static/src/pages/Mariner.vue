<script setup lang="ts">
import { ref } from "vue";

import DashboardLayout from "../components/DashboardLayout.vue";
import ContentHeader from "../components/ContentHeader.vue";

import Table from "../components/mariner/Table.vue";

import DeleteModal from "../components/DeleteModal.vue";

import {
  FnLoad,
  IMariner,
  getUpdateQLParams,
  getQueryReturn,
  ICertificate
} from "../types";

import { defaultCertificate, defaultMariner } from "../config";
import { Button, IconAdd } from "daisyui-vue";
import { useMutation, useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { getUpdateQLData } from "../types";
import { router } from "@inertiajs/core";
import { computed } from "@vue/reactivity";


export type IMarinerAndCert = IMariner & {
  certificates: ICertificate[],
  ship: string
} 

defineOptions({ layout: DashboardLayout });

let forceReload = ref<boolean>(false);

const QL_GET_MARINERS = gql`
  query ($page: Int!, $size: Int!, $modelName: String!, $searchName : String!, $searchShip : String!) {
    allMariners(pageSize: $size, pageIndex: $page, searchParams: [
      {
        key : "name",
        value: $searchName,
        op: "contains"
      },
      {
        key : "shipPk",
        value: $searchShip,
        op: "equal"
      }
    ]) {
      mariner {
        ${getQueryReturn(defaultMariner)}
      }
      certificates {
        ${getQueryReturn(defaultCertificate)}
      }
      ship {
        name
      }
    }
    totalCount(modelName: $modelName, searchParams: [])
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
// watch(result, () => console.log(result));
const { mutate } = useMutation(QL_UPATE_MARINERS);

const { mutate: mutateDelete } = useMutation(QL_DELETE_MARINERS);

const { refetch } = useQuery(QL_GET_MARINERS, {
  page: 0,
  size: 10,
  modelName: "Mariner",
  searchShip: "",
  searchName : ""
});


const load_data: FnLoad<IMarinerAndCert> = (
  page: number,
  size: number,
  search: any,
  callback
) => {
  console.log("page :>> ", page);
  console.log('search :>> ', search);
  refetch({
    page,
    size,
    modelName: "Mariner",
    ...search
  })
    ?.then((res) => {
      
      let mariners: IMarinerAndCert[] = [];
      let arr: Array<any> = res.data.allMariners;
      let total_count = res.data.totalCount;
      mariners = arr.map((item) => ({
        ...item.mariner,
        certificates: item.certificates,
        ship: item.ship?.name
      }));

      callback(mariners, total_count);
    })
    .catch((err) => console.log("err", err));
};

const onEdit = (item: IMarinerAndCert) => {
  console.log("item will be edited :>> ", item);
  router.get('mariner/edit', {id: item.pk})
};

let isDelete = ref<boolean>(false);
let deletePk = ref<string>("");
const onFinishDelete = (action: string) => {
  isDelete.value = false;

  if (action == "save") {
    mutateDelete({ pk: deletePk.value })
      .then((res) => {
        forceReload.value = !forceReload.value;
      })
      .catch((err) => console.error(err));
  }
};

const onDelete = (item: IMarinerAndCert) => {
  console.log("item will be deleted :>> ", item);
  isDelete.value = true;
  deletePk.value = item.pk;
};

const onDetail = (item: IMarinerAndCert) => {
  console.log('item :>> ', item);
  router.get('mariner/detail', {id: item.pk});
}
const onCreate = () => {
  router.get('mariner/edit', {id: 'new'});
};



</script>

<template>
  <ContentHeader :icon="'pe-7s-users'">Mariner</ContentHeader>

  <div class="px-4 py-2">
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="flex">
        <div class="text-2xl me-4">Mariner</div>
        <Button shape="circle" size="xs" class="my-auto" variant="neutral" @click="onCreate">
          <icon-add />
        </Button>
      </div>

      <Table  
        :load_data="load_data"
        @edit="onEdit"
        @delete="onDelete"
        @detail="onDetail"
        :forceReload="forceReload"
         :ships="ships"

      />
    </div>
  </div>

  <DeleteModal :open="isDelete" @close="onFinishDelete"
    >Are you sure you want to delete this item?</DeleteModal
  >
  
</template>
