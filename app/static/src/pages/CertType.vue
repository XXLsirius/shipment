<script setup lang="ts">
import { ref } from "vue";

import DashboardLayout from "../components/DashboardLayout.vue";
import ContentHeader from "../components/ContentHeader.vue";

import Table from "../components/certtype/Table.vue";
import Modal from "../components/certtype/Modal.vue";

import DeleteModal from "../components/DeleteModal.vue";

import { FnDelete, FnLoad, FnLoadCallback, ICertType } from "../types";
import { Button, IconAdd } from "daisyui-vue";
import {
  useMutation,
  useQuery,
} from "@vue/apollo-composable";
import gql from "graphql-tag";

defineOptions({ layout: DashboardLayout });
let openTab = ref(0);
let isEditing = ref<boolean>(false);
let itemEditing = ref<ICertType | null>();
let forceReload = ref<boolean>(false);
const QL_GET_CERTTYPE = gql`
  query (
    $page: Int!
    $size: Int!
    $modelName: String!
    $searchKind: String!
  ) {
    allCerttypes(
      pageSize: $size
      pageIndex: $page
      searchParams: [
        { key: "kind", value: $searchKind, op: "=" }
      ]
    ) {
      pk
      name
      agency
      note
    }
    totalCount(modelName: $modelName, searchParams: [
      { key: "kind", value: $searchKind, op: "=" }
    ])
  }
`;

const QL_UPATE_CERTTYPE = gql`
  mutation (
    $pk: String
    $name: String!
    $agency: String!
    $note: String!
    $kind: Int!
  ) {
    updateCerttype(
      data: {
        pk: $pk
        name: $name
        agency: $agency
        note: $note
        kind: $kind
      }
    ) {
      ok
    }
  }
`;

const QL_DELETE_CERTTYPE = gql`
  mutation ($pk: String!) {
    deleteCerttype(pk: $pk) {
      ok
    }
  }
`;

// watch(result, () => console.log(result));
const { mutate } = useMutation(QL_UPATE_CERTTYPE);

const { mutate: mutateDelete } = useMutation(QL_DELETE_CERTTYPE);

const { refetch } = useQuery(QL_GET_CERTTYPE, {
  page: 0,
  size: 0,
  modelName: "Certtype",
  searchKind: 0,
});

const load_data: FnLoad<ICertType> = (
  page: number,
  size: number,
  search: any,
  callback
) => {
  console.log("page :>> ", page);
  refetch({
    page,
    size,
    modelName: "Certtype",
    searchKind: openTab.value,
  })
    ?.then((res) => {
      console.log("res :>> ", res);
      let certtypes: ICertType[] = [];
      let arr: Array<any> = res.data.allCerttypes;
      let total_count = res.data.totalCount;
      certtypes = arr.map((item) => ({
        pk: item.pk,
        name: item.name,
        agency: item.agency,
        note: item.note,
        kind: item.kind,
      }));

      callback(certtypes, total_count);
    })
    .catch((err) => console.log("err", err));
};

const onEdit = (item: ICertType) => {
  console.log("item will be edited :>> ", item);
  isEditing.value = true;
  itemEditing.value = item;
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

const onDelete = (item: ICertType) => {
  console.log("item will be deleted :>> ", item);
  isDelete.value = true;
  deletePk.value = item.pk;
};

const onFinishEditing = (action: string, item: ICertType) => {
  isEditing.value = false;

  item.kind = openTab.value;

  console.log("item :>> ", item);
  console.log("object :>> ", QL_UPATE_CERTTYPE);
  if (action == "save") {
    console.log("item :>> ", item);
    mutate(item)
      .then((res) => {
        forceReload.value = !forceReload.value;
      })
      .catch((err) => console.error(err));
  }
};

const onCreate = () => {
  console.log("item will be created :>> ");
  isEditing.value = true;
  itemEditing.value = null;
};
</script>

<template>
  <ContentHeader :icon="'pe-7s-box1'">Types of Certificate</ContentHeader>

  <div class="px-4 py-2">
    <ul class="flex text-sm flex-wrap pt-3 pb-2 flex-row">
      <li class="mb-px mr-2 last:mr-0 text-center w-32 cursor-pointer">
        <a
          class="text-sm p-2 shadow-lg rounded block leading-normal hover:bg-blue-600 hover:text-white"
          @click="openTab = 0; forceReload = !forceReload"
          :class="{
            'text-blue-600 bg-white': openTab !== 0,
            'text-white bg-blue-600': openTab === 0,
          }"
        >
          Ship
        </a>
      </li>
      <li class="mb-px mr-2 last:mr-0 text-center w-32 cursor-pointer">
        <a
          class="text-sm p-2 shadow-lg rounded block leading-normal hover:bg-blue-600 hover:text-white"
          @click="openTab = 1; forceReload = !forceReload"
          :class="{
            'text-blue-600 bg-white': openTab !== 1,
            'text-white bg-blue-600': openTab === 1,
          }"
        >
          Personal
        </a>
      </li>
    </ul>
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <div :class="{ hidden: openTab !== 0, block: openTab === 0 }">
        <div class="flex">
          <div class="text-2xl me-4">Ship Certificates</div>
          <Button shape="circle" size="xs" class="my-auto" variant="neutral" @click="onCreate">
            <icon-add />
          </Button>
        </div>

        <Table
          :load_data="load_data"
          @edit="onEdit"
          @delete="onDelete"
          :forceReload="forceReload"
          :searchKind="0"
        />
      </div>
      <div :class="{ hidden: openTab !== 1, block: openTab === 1 }">
        <div class="flex">
          <div class="text-2xl me-4">Personal Certificates</div>
          <Button shape="circle" size="xs" class="my-auto" variant="neutral" @click="onCreate">
            <icon-add />
          </Button>
        </div>

        <Table
          :load_data="load_data"
          @edit="onEdit"
          @delete="onDelete"
          :forceReload="forceReload"
          :searchKind="1"
        />
      </div>
    </div>
  </div>
  
  <Modal :open="isEditing" :data="itemEditing" @close="onFinishEditing" />
  <DeleteModal :open="isDelete" @close="onFinishDelete"
    >Are you sure you want to delete this item?</DeleteModal
  >
</template>
