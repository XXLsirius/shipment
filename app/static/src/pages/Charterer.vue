<script setup lang="ts">
import { ref } from "vue";

import DashboardLayout from "../components/DashboardLayout.vue";
import ContentHeader from "../components/ContentHeader.vue";

import Table from "../components/charterer/Table.vue";
import Modal from "../components/charterer/Modal.vue";

import DeleteModal from "../components/DeleteModal.vue";

import { FnDelete, FnLoad, FnLoadCallback, ICharterer } from "../types";
import { Button, IconAdd } from "daisyui-vue";
import {
  useApolloClient,
  useLazyQuery,
  useMutation,
  useQuery,
} from "@vue/apollo-composable";
import gql from "graphql-tag";
import { watch } from "vue";

defineOptions({ layout: DashboardLayout });
let isEditing = ref<boolean>(false);
let itemEditing = ref<ICharterer | null>();
let forceReload = ref<boolean>(false);
const QL_GET_CHARTERERS = gql`
  query (
    $page: Int!
    $size: Int!
    $modelName: String!
    $searchNation: String!
    $searchCompany: String!
  ) {
    allCharterers(
      pageSize: $size
      pageIndex: $page
      searchParams: [
        { key: "nation", value: $searchNation, op: "contains" }
        { key: "company", value: $searchCompany, op: "contains" }
      ]
    ) {
      pk
      nation
      company
      phone
      email
      note
    }
    totalCount(modelName: $modelName, searchParams: [])
  }
`;

const QL_UPATE_CHARTERERS = gql`
  mutation (
    $pk: String
    $company: String!
    $nation: String!
    $phone: String!
    $email: String!
    $note: String!
  ) {
    updateCharterer(
      data: {
        pk: $pk
        company: $company
        nation: $nation
        phone: $phone
        email: $email
        note: $note
      }
    ) {
      ok
    }
  }
`;

const QL_DELETE_CHARTERERS = gql`
  mutation ($pk: String!) {
    deleteCharterer(pk: $pk) {
      ok
    }
  }
`;

// watch(result, () => console.log(result));
const { mutate } = useMutation(QL_UPATE_CHARTERERS);

const { mutate: mutateDelete } = useMutation(QL_DELETE_CHARTERERS);

const { refetch } = useQuery(QL_GET_CHARTERERS, {
  page: 0,
  size: 10,
  modelName: "Charterer",
  searchCompany: "",
  searchNation: "",
});

const load_data: FnLoad<ICharterer> = (
  page: number,
  size: number,
  search: any,
  callback
) => {
  console.log("page :>> ", page);
  refetch({
    page,
    size,
    modelName: "Charterer",
    searchCompany: search.company,
    searchNation: search.nation,
  })
    ?.then((res) => {
      console.log("res :>> ", res);
      let charterers: ICharterer[] = [];
      let arr: Array<any> = res.data.allCharterers;
      let total_count = res.data.totalCount;
      charterers = arr.map((item) => ({
        pk: item.pk,
        note: item.note,
        company: item.company,
        email: item.email,
        nation: item.nation,
        phone: item.phone,
      }));

      callback(charterers, total_count);
    })
    .catch((err) => console.log("err", err));
};

const onEdit = (item: ICharterer) => {
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

const onDelete = (item: ICharterer) => {
  console.log("item will be deleted :>> ", item);
  isDelete.value = true;
  deletePk.value = item.pk;
};

const onFinishEditing = (action: string, item: ICharterer) => {
  isEditing.value = false;

  console.log("item :>> ", item);
  console.log("object :>> ", QL_UPATE_CHARTERERS);
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
  <ContentHeader :icon="'pe-7s-id'">Charterer</ContentHeader>

  <div class="px-4 py-2">
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="flex">
        <div class="text-2xl me-4">Charterer</div>
        <Button shape="circle" size="xs" class="my-auto" variant="neutral" @click="onCreate">
          <icon-add />
        </Button>
      </div>

      <Table
        :load_data="load_data"
        @edit="onEdit"
        @delete="onDelete"
        :forceReload="forceReload"
      />
    </div>
  </div>
  <Modal :open="isEditing" :data="itemEditing" @close="onFinishEditing" />
  <DeleteModal :open="isDelete" @close="onFinishDelete" >Are you sure you want to delete this item?</DeleteModal>
</template>
