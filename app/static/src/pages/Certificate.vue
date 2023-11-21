<script setup lang="ts">
import { ref } from "vue";

import DashboardLayout from "../components/DashboardLayout.vue";
import ContentHeader from "../components/ContentHeader.vue";

import Table from "../components/certificate/Table.vue";
import Modal from '../components/certificate/Modal.vue';
import {
  FnLoad,
  getUpdateQLParams,
  getQueryReturn,
  ICertificate,
} from "../types";

import { defaultCertificate, defaultCerttype } from "../config";
import { Button, IconAdd } from "daisyui-vue";
import { useMutation, useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { getUpdateQLData } from "../types";
import { router } from "@inertiajs/core";
import { computed } from "@vue/reactivity";
import { ICertAddInfo } from "../components/certificate/Modal.vue";
import { isTemplateNode } from "@vue/compiler-core";

export type ICertificateAndCert = ICertificate & {
  certificates: ICertificate;
  ship: string;
  mariner: string;
};

defineOptions({ layout: DashboardLayout });

let forceReload = ref<boolean>(false);
const isEditing = ref<boolean>(false);


const QL_GET_CERTIFICATES = gql`
  query ($page: Int!, $size: Int!, $kind: String!, $modelName: String!, $searchDepartment : String!, $searchShip : String!, $searchCerttype : String!, $searchMariner: String!) {
    allCertificate(pageSize: $size, pageIndex: $page, searchParams: [
      {
        key : "name",
        value: $searchDepartment,
        op: "contains"
      },
      {
        key : "shipPk",
        value: $searchShip,
        op: "equal"
      },
      {
        key : "certtypePk",
        value: $searchCerttype,
        op: "equal"
      },
      {
        key : "marinerName",
        value: $searchMariner,
        op: "equal"
      },
      {
        key : "kind",
        value: $kind,
        op: "="
      }
    ]) {
      certificate {
        ${getQueryReturn(defaultCertificate)}
      }
      certtype {
        ${getQueryReturn(defaultCerttype)}
      }
      ship
      mariner
    }
    totalCount(modelName: $modelName, searchParams: [])
  }
`;

const QL_UPATE_CERTIFICATES = gql`
  mutation (
    ${getUpdateQLParams(defaultCertificate)}
  ) {
    updateCertificate(
      data: {
        ${getUpdateQLData(defaultCertificate)}
      }
    ) {
      ok
    }
  }
`;

const QL_DELETE_CERTIFICATES = gql`
  mutation ($pk: String!) {
    deleteCertificate(pk: $pk) {
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
  console.log('resultShips.value :>> ', resultShips.value);
  return resultShips.value
    ? resultShips.value.allShips.map((ship: any) => ship.ship)
    : [];
});

const QL_GET_CERTTYPES = gql`
  query {
    allCerttypes(pageSize: 10000, pageIndex: 0, searchParams: []) {
      pk
      name
      kind
    }
  }
`;
const { result: resultCerttypes } = useQuery(QL_GET_CERTTYPES);

const certtypes = computed(() => {
  console.log('resultCerttypes :>> ', resultCerttypes.value);
  return resultCerttypes.value
    ? resultCerttypes.value.allCerttypes.map((_: any) => _)
    : [];
});

const { mutate: mutateDelete } = useMutation(QL_DELETE_CERTIFICATES);

const { refetch } = useQuery(QL_GET_CERTIFICATES, {
  page: 0,
  size: 10,
  modelName: "Certificate",
  searchShip: "",
  searchDepartment: "",
  searchCerttype : "",
  searchMariner : "",
});

const load_data: FnLoad<ICertificateAndCert> = (
  page: number,
  size: number,
  search: any,
  callback
) => {
  console.log("page :>> ", page);
  console.log("search :>> ", search);
  refetch({
    page,
    size,
    modelName: "Certificate",
    kind : kind.value,
    ...search,
  })
    ?.then((res) => {
      let certificates: ICertificateAndCert[] = [];
      let arr: Array<any> = res.data.allCertificate;
      let total_count = res.data.totalCount;
      certificates = arr.map((item) => ({
        ...item.certificate,
        certtype: item.certtype,
        certificates: item.certificates,
        ship: item.ship,
        mariner: item.mariner
      }));

      console.log('certificates :>> ', certificates);
      callback(certificates, total_count);
    })
    .catch((err) => console.log("err", err));
};

const onEdit = (item: ICertificateAndCert) => {
  console.log("item will be edited :>> ", item);
  router.get("certificate/edit", { id: item.pk });
};

const onDelete = (item: ICertificateAndCert) => {
  console.log("item will be deleted :>> ", item);

  mutateDelete({ pk: item.pk })
    .then((res) => {
      forceReload.value = !forceReload.value;
    })
    .catch((err) => console.error(err));
};

const onDetail = (item: ICertificateAndCert) => {
  
};
const onCreate = () => {
  isEditing.value = true;
  // router.get("certificate/edit", { id: "new" });
};

const onFinishEditing = (action: string, data: ICertAddInfo) => {
  isEditing.value = false;
  if (action == 'save') {
    router.get('certificate/edit', {id: 'new', ...data, kind: kind.value});
  }
}
const kind = ref(0);
</script>

<template>
  <ContentHeader :icon="'pe-7s-credit'">Certificates</ContentHeader>

  <div class="px-4 py-2">
    <ul class="flex text-sm flex-wrap pt-3 pb-2 flex-row">
      <li class="mb-px mr-2 last:mr-0 text-center w-32 cursor-pointer">
        <a
          class="text-sm p-2 shadow-lg rounded block leading-normal hover:bg-blue-600 hover:text-white"
          @click="kind = 0"
          :class="{
            'text-blue-600 bg-white': kind !== 0,
            'text-white bg-blue-600': kind === 0,
          }"
        >
          Ship
        </a>
      </li>
      <li class="mb-px mr-2 last:mr-0 text-center w-32 cursor-pointer">
        <a
          class="text-sm p-2 shadow-lg rounded block leading-normal hover:bg-blue-600 hover:text-white"
          @click="kind = 1"
          :class="{
            'text-blue-600 bg-white': kind !== 1,
            'text-white bg-blue-600': kind === 1,
          }"
        >
          Personal
        </a>
      </li>
    </ul>
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <div>
        <div class="flex">
          <div class="text-2xl me-4">
            {{ kind == 1 ? "Personal Certificates" : "Ship Certificates" }}
          </div>
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
          :kind="kind" :certtypes="certtypes"
        />
      </div>
    </div>
  </div>
  <Modal :open="isEditing" :kind="kind" @close="onFinishEditing" :ships="ships" :certtypes="certtypes" />
</template>
