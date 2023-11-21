<script setup lang="ts">
import { ref } from "vue";
import { useSidebar } from "../composables/useSidebar";
import { Link } from "@inertiajs/vue3";
import { STATIC_URL } from "../config";

const ImageLogo = STATIC_URL + "images/logo.svg";

const { isOpen } = useSidebar();
const activeClass = ref(
  "bg-gray-600 bg-opacity-25 text-gray-100 border-gray-100"
);
const inactiveClass = ref(
  "border-gray-900 text-gray-400 hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100"
);
</script>

<script lang="ts">
export default {
  methods: {
    isUrl(urls: string[] | string) {
      let currentUrl = this.$page.url.substr(1);
      if (typeof urls === "string") {
        return currentUrl.indexOf("/" + urls) !== -1;
      }
      return (
        Array.isArray(urls) &&
        urls.filter((url) => currentUrl.indexOf(url) !== -1).length
      );
    },
  },
  mounted: () => {
    console.log("side bar mounted again");
  },
};

const menus = [
  { title: "DASHBOARDS" },
  { title: "Dashboard", page: "dashboard", icon: "pe-7s-display2" },

  { title: "Water areas", page: "waterArea", icon: "pe-7s-target" },
  { title: "Charterers", page: "charterer", icon: "pe-7s-id" },
  { title: "Certificates", page: "certificate", icon: "pe-7s-credit" },
  { title: "SETTING" },
  { title: "Ship", page: "ship", icon: "pe-7s-helm" },
  { title: "Mariner", page: "mariner", icon: "pe-7s-users" },
  {
    title: "Type of Certificate",
    page: "certType",
    icon: "pe-7s-box1",
  },
];
</script>
<template>
  <div class="flex">
    <!-- Backdrop -->
    <div
      :class="isOpen ? 'block' : 'hidden'"
      class="fixed inset-0 z-20 transition-opacity bg-black opacity-50 lg:hidden"
      @click="isOpen = false"
    />
    <!-- End Backdrop -->

    <div
      :class="isOpen ? 'translate-x-0 ease-out' : '-translate-x-full ease-in'"
      class="fixed inset-y-0 left-0 z-30 w-64 overflow-y-auto transition duration-300 transform bg-gray-800 lg:translate-x-0 lg:static lg:inset-0"
    >
      <div class="flex items-center justify-center bg-gray-600">
        <div class="flex items-center p-1.5">
          <img class="w-12 h-12 p-1" :src="ImageLogo" />
          <span class="mx-2 text-xl font-semibold text-white"
            >Business Name</span
          >
        </div>
      </div>

      <nav>
        <!-- <img :src="Image" /> -->
        <div v-for="menu in menus">
          <Link
            v-if="menu.page"
            class="flex items-center px-6 py-3 duration-200 border-l-4"
            :class="[isUrl(menu.page) ? activeClass : inactiveClass]"
            :href="'/' + menu.page"
          >
            <span :class="menu.icon" class="text-xl"></span>
            <span class="mx-4">{{ menu.title }}</span>
          </Link>
          <div
            v-else
            class="flex items-center py-2 mt-2 duration-200 text-gray-400"
          >
            <span class="mx-4">{{ menu.title }}</span>
          </div>
        </div>
      </nav>
    </div>
  </div>
</template>
