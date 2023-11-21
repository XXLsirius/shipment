<script setup lang="ts">
import { ref } from "vue";

import DashboardLayout from "../components/DashboardLayout.vue";
import ContentHeader from "../components/ContentHeader.vue";

import Table from "../components/ship/Table.vue";

import DeleteModal from "../components/DeleteModal.vue";

import {
  FnLoad,
  IShip,
  getUpdateQLParams,
  getQueryReturn,
  ICertificate,
} from "../types";
import { defaultCertificate, defaultShip } from "../config";
import { Button, IconAdd } from "daisyui-vue";
import { useMutation, useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { watch } from "vue";
import { getUpdateQLData } from "../types";
import { router } from "@inertiajs/core";
import { Certificate } from "crypto";
import { it } from "node:test";

export type IShipAndCert = IShip & {
  certificates: ICertificate[];
};

defineOptions({ layout: DashboardLayout });

let forceReload = ref<boolean>(false);

const QL_GET_SHIPS = gql`
  query ($page: Int!, $size: Int!, $modelName: String!) {
    allShips(pageSize: $size, pageIndex: $page, searchParams: []) {
      ship {
        ${getQueryReturn(defaultShip)}
      }
      certificates {
        ${getQueryReturn(defaultCertificate)}
      }
    }
    totalCount(modelName: $modelName, searchParams: [])
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

// watch(result, () => console.log(result));
const { mutate } = useMutation(QL_UPATE_SHIPS);

const { mutate: mutateDelete } = useMutation(QL_DELETE_SHIPS);

const { refetch } = useQuery(QL_GET_SHIPS, {
  page: 0,
  size: 10,
  modelName: "Ship",
});

const load_data: FnLoad<IShipAndCert> = (
  page: number,
  size: number,
  search: any,
  callback
) => {
  console.log("page :>> ", page);
  refetch({
    page,
    size,
    modelName: "Ship",
  })
    ?.then((res) => {
      let ships: IShipAndCert[] = [];
      let arr: Array<any> = res.data.allShips;
      let total_count = res.data.totalCount;
      ships = arr.map((item) => ({
        ...item.ship,
        certificates: item.certificates,
      }));

      callback(ships, total_count);
    })
    .catch((err) => console.log("err", err));
};

const onEdit = (item: IShipAndCert) => {
  console.log("item will be edited :>> ", item);
  router.get("ship/edit", { id: item.pk });
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

const onDelete = (item: IShipAndCert) => {
  console.log("item will be deleted :>> ", item);
  isDelete.value = true;
  deletePk.value = item.pk;
};

const onDetail = (item: IShipAndCert) => {
  console.log("item :>> ", item);
  router.get("ship/detail", { id: item.pk });
};
const onCreate = () => {
  router.get("ship/edit", { id: "new" });
};
</script>

<template>
  <ContentHeader :icon="'pe-7s-helm'">Ship</ContentHeader>

  <div class="px-4 py-2">
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="flex">
        <div class="text-2xl me-4">Ship</div>
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
      />
    </div>
  </div>

  <DeleteModal :open="isDelete" @close="onFinishDelete"
    >Are you sure you want to delete this item?</DeleteModal
  >
</template>
