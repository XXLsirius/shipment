<script setup lang="ts">
import { ref } from "vue";

import DashboardLayout from "../components/DashboardLayout.vue";
import ContentHeader from "../components/ContentHeader.vue";

import Table from "../components/waterarea/Table.vue";
import Modal from "../components/waterarea/Modal.vue";

import DeleteModal from "../components/DeleteModal.vue";

import { FnLoad, IWaterarea } from "../types";
import { Button, IconAdd } from "daisyui-vue";
import { useMutation, useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";

defineOptions({ layout: DashboardLayout });
let isEditing = ref<boolean>(false);
let itemEditing = ref<IWaterarea | null>();
let forceReload = ref<boolean>(false);

const QL_GET_WATERAREAS = gql`
  query ($page: Int!, $size: Int!, $modelName: String!) {
    allWaterareas(pageSize: $size, pageIndex: $page, searchParams: []) {
      pk
      name
      note
    }
    totalCount(modelName: $modelName, searchParams: [])
  }
`;

const QL_UPATE_WATERAREAS = gql`
  mutation ($pk: String, $name: String!, $note: String!) {
    updateWaterarea(data: { pk: $pk, name: $name, note: $note }) {
      ok
    }
  }
`;

const QL_DELETE_WATERAREAS = gql`
  mutation ($pk: String!) {
    deleteWaterarea(pk: $pk) {
      ok
    }
  }
`;

// watch(result, () => console.log(result));
const { mutate } = useMutation(QL_UPATE_WATERAREAS);

const { mutate: mutateDelete } = useMutation(QL_DELETE_WATERAREAS);

const { refetch } = useQuery(QL_GET_WATERAREAS, {
  page: 0,
  size: 10,
  modelName: "Waterarea",
});

const load_data: FnLoad<IWaterarea> = (
  page: number,
  size: number,
  search: any,
  callback
) => {
  console.log("page :>> ", page);
  refetch({
    page,
    size,
    modelName: "Waterarea",
  })
    ?.then((res) => {
      console.log("res :>> ", res);
      let waterareas: IWaterarea[] = [];
      let arr: Array<any> = res.data.allWaterareas;
      let total_count = res.data.totalCount;
      waterareas = arr.map((item) => ({
        pk: item.pk,
        name: item.name,
        note: item.note,
      }));

      callback(waterareas, total_count);
    })
    .catch((err) => console.log("err", err));
};

const onEdit = (item: IWaterarea) => {
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

const onDelete = (item: IWaterarea) => {
  console.log("item will be deleted :>> ", item);
  isDelete.value = true;
  deletePk.value = item.pk;
};

const onFinishEditing = (action: string, item: IWaterarea) => {
  isEditing.value = false;

  console.log("item :>> ", item);
  console.log("object :>> ", QL_UPATE_WATERAREAS);
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
  <ContentHeader :icon="'pe-7s-target'">Waterarea</ContentHeader>

  <div class="px-4 py-2">
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="flex">
        <div class="text-2xl me-4">Waterarea</div>
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
  <DeleteModal :open="isDelete" @close="onFinishDelete"
    >Are you sure you want to delete this item?</DeleteModal
  >
</template>
