<script setup lang="ts">
import DashboardLayout from "../components/DashboardLayout.vue";
import ContentHeader from "../components/ContentHeader.vue";
import { STATIC_URL, defaultCertificate } from "../config";
import { Button, IconClose, IconAdd } from "daisyui-vue";
import { VNodeRef, computed, onMounted, ref } from "vue";
import gql from "graphql-tag";
import {
  ICertificate,
  getQueryReturn,
  getUpdateQLData,
  getUpdateQLParams,
} from "../types";
import { useMutation, useQuery } from "@vue/apollo-composable";
import { watch } from "vue";

const props = defineProps<{
  id: string;
  certtypePk: string;
  shipPk: string;
  kind: string;
  marinerPk: string;
}>();

defineOptions({ layout: DashboardLayout });

const QL_GET_TARGETNAME = gql`
  query ($marinerPk: String!, $shipPk: String!, $certtypePk: String!) {
    marinerById(pk: $marinerPk) {
      mariner {
        name
      }
    }
    shipById(pk: $shipPk) {
      ship {
        name
      }
    }
    certById(pk: $certtypePk) {
      name
    }
  }
`;
const { refetch: refetchTargetNames } = useQuery(QL_GET_TARGETNAME, {
  marinerPk: "",
  shipPk: "",
  certtypePk: "",
});

const QL_GET_CERTIFICATE = gql`
  query ($pk : String!) {
    certificateById(pk : $pk) {
      certificate {
        ${getQueryReturn(defaultCertificate)}
      }
      ship
      mariner
      certtype {
        name
      }
    }
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

const { refetch } = useQuery(QL_GET_CERTIFICATE, {
  pk: props.id,
});

let item = ref<ICertificate>(defaultCertificate);
let targetNames = ref({
  ship: "",
  mariner: "",
  certtype: "",
});

const departments = ["department 1", "department 2", "department 3"];

const { mutate: mutateUpdate } = useMutation(QL_UPATE_CERTIFICATES);

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
  console.log("resultCerttypes :>> ", resultCerttypes.value);
  return resultCerttypes.value
    ? resultCerttypes.value.allCerttypes.map((_: any) => _)
    : [];
});

onMounted(() => {
  console.log("props.id :>> ", props.id);
  if (props.id !== "new") {
    refetch({ pk: props.id })
      ?.then((res) => {
        console.log('res :>> ', res);
        item.value = Object.assign({}, res.data.certificateById.certificate);
        targetNames.value.certtype = res.data.certificateById.certtype.name;
        targetNames.value.ship = res.data.certificateById.ship;
        targetNames.value.mariner = res.data.certificateById.mariner;
        is_new.value = false;
        is_completed.value = true;
      })
      .catch((err) => console.error(err));
  } else {
    item.value.certtypePk = props.certtypePk;
    item.value.kind = parseInt(props.kind);
    item.value.marinerPk = props.marinerPk;
    item.value.shipPk = props.shipPk;
    is_new.value = true;
    refetchTargetNames({
      marinerPk: props.marinerPk,
      shipPk: props.shipPk,
      certtypePk: props.certtypePk,
    })
      ?.then((res) => {
        console.log("res :>> ", res);
        targetNames.value = {
          ship: res.data.shipById ? res.data.shipById.ship.name : "",
          mariner: res.data.marinerById
            ? res.data.marinerById.mariner.name
            : "",
          certtype: res.data.certById ? res.data.certById.name : "",
        };
      })
      .catch((err) => console.log(err));
  }
});

const is_completed = ref(false);
const is_edit_issue = ref(false);
const is_new = ref(true);

function handlePutIn() {
  is_edit_issue.value = true;
}

function handleCompleted() {
  console.log("item.value :>> ", item.value);
  console.log("getfasfdasf", getUpdateQLParams(defaultCertificate));
  console.log("object :>> ", defaultCertificate);
  mutateUpdate(item.value)
    .then(() => {
      console.log("successfully saved");
      is_new.value = false;
      is_completed.value = true;
    })
    .catch((err) => console.error(err));
}

function handleIssue() {
  is_completed.value = false;
  is_edit_issue.value = false;
}
</script>

<template>
  <ContentHeader :icon="'pe-7s-credit'">Certificates</ContentHeader>

  <div class="px-4 py-2">
    <div
      class="block w-full p-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
    >
      <span
        class="py-2 px-3 bg-amber-500 text-white rounded-s"
        style="min-width: 150px"
        >{{ targetNames.certtype }}</span
      >
      <span class="py-2 px-3 bg-stone-500 text-white rounded-e"
        >{{ item.kind == 1 ? targetNames.mariner : targetNames.ship }}
      </span>
      <button
        v-if="is_completed"
        id="btn_issue"
        class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-5 py-2 mx-4 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
        @click="handleIssue"
      >
        Issue
      </button>
    </div>
    <div>
      <div class="grid grid-cols-12 gap-4">
        <div v-if="!is_new" id="certificate-card-table" class="col-span-6">
          <table class="mt-4 min-w-full">
            <thead>
              <tr class="bg-sky-950 text-white">
                <th
                  class="w-full px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
                >
                  Item
                </th>
                <th
                  class="w-full px-4 py-2 text-xs font-medium leading-4 tracking-wider text-left uppercase border-b border-gray-200"
                >
                  Value
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="bg-white">
                <td class="px-4 py-2 border-b border-gray-200">Department</td>
                <td class="px-4 py-2 border-b border-gray-200">
                  {{ item.issueDepartment }}
                </td>
              </tr>
              <tr class="bg-gray-200">
                <td class="px-4 py-2 border-b border-gray-200">ID</td>
                <td class="px-4 py-2 border-b border-gray-200">
                  {{ item.issueId }}
                </td>
              </tr>
              <tr class="bg-white">
                <td class="px-4 py-2 border-b border-gray-200">Issue Date</td>
                <td class="px-4 py-2 border-b border-gray-200">
                  {{ item.issueDate }}
                </td>
              </tr>
              <tr class="bg-gray-200">
                <td class="px-4 py-2 border-b border-gray-200">
                  Expiration Date
                </td>
                <td class="px-4 py-2 border-b border-gray-200">
                  {{ item.issueExpireDate }}
                </td>
              </tr>
              <tr class="bg-white">
                <td class="px-4 py-2 border-b border-gray-200">Account</td>
                <td class="px-4 py-2 border-b border-gray-200">
                  {{ item.issueAccount }}
                  
                </td>
              </tr>
              <tr class="bg-gray-200">
                <td class="px-4 py-2 border-b border-gray-200">Price</td>
                <td class="px-4 py-2 border-b border-gray-200">
                  {{ item.issuePrice }}
                  
                </td>
              </tr>
              <tr class="bg-white">
                <td class="px-4 py-2 border-b border-gray-200">
                  Registration fee
                </td>
                <td class="px-4 py-2 border-b border-gray-200">
                  {{ item.issueRegfee }}
                  
                </td>
              </tr>
              <!-- <tr class="bg-gray-200">
                  <td class="px-4 py-2 border-b border-gray-200">Amount</td>
                  <td class="px-4 py-2 border-b border-gray-200">{certificate.issue_amount}</td>
                </tr> -->
            </tbody>
          </table>
        </div>
        <div
          v-if="!is_completed"
          class="col-span-6 bg-white border border-gray-200 rounded-lg shadow my-4"
        >
          <div class="text-2xl font-medium m-4">ISSUE</div>
          <div class="grid grid-cols-3 gap-2 m-4">
            <div class="col-span-1">
              <label
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Put in</label
              >
              <input
                type="date"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
                v-model="item.issuePutinDate"
              />
            </div>
            <div class="col-span-1">
              <label
                for="issue_department"
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Department</label
              >
              <select
                id="issue_department"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                v-model="item.issueDepartment"
                required
              >
                <option v-for="depart in departments">{{ depart }}</option>
              </select>
            </div>
            <div class="col-span-1">
              <label
                for="btn_put_in"
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >&nbsp;</label
              >
              <button
                v-if="is_edit_issue"
                class="py-2 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-black hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
                @click="handleCompleted"
              >
                Completed
              </button>
              <button
                v-else
                class="py-2 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-black hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
                @click="handlePutIn"
              >
                Put in
              </button>
            </div>
          </div>
          <hr v-if="is_edit_issue" class="border border-gray-400 my-4" />
          <div v-if="is_edit_issue" class="grid grid-cols-3 gap-2 m-4">
            <div class="col-span-1">
              <label
                for="issue_id"
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >ID</label
              >
              <input
                type="text"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                id="issue_id"
                v-model="item.issueId"
                required
              />
            </div>
            <div class="col-span-1">
              <label
                for="issue_date"
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Issue</label
              >
              <input
                type="date"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                id="issue_date"
                v-model="item.issueDate"
                required
              />
            </div>
            <div class="col-span-1">
              <label
                for="issue_expire_date"
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Expire</label
              >
              <input
                type="date"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                id="issue_expire_date"
                v-model="item.issueExpireDate"
              />
            </div>
            <div class="col-span-1">
              <label
                for="issue_account"
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Account</label
              >
              <input
                type="text"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                id="issue_account"
                v-model="item.issueAccount"
              />
            </div>
            <div class="col-span-1">
              <label
                for="issue_price"
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Price</label
              >
              <input
                type="number"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                id="issue_price"
                v-model="item.issuePrice"
              />
            </div>
            <div class="col-span-1">
              <label
                for="issue_regfee"
                class="block text-sm font-medium text-gray-900 dark:text-white"
                >Registration fee</label
              >
              <input
                type="number"
                class="mb-2 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                id="issue_regfee"
                v-model="item.issueRegfee"
              />
            </div>
            <!-- <div class="col-4">
              <label for="issue_amount" class="block text-sm font-medium text-gray-900 dark:text-white">Amount</label
                >
              <input type="number" class="input-control" id="issue_amount" bind:value="{certificate.issue_amount}" />
            </div> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
