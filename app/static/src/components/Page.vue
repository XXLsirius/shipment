<script setup>

import DashboardLayout from './DashboardLayout.vue';
import { Head } from "@inertiajs/vue3";

defineOptions({ layout: DashboardLayout });

</script>

<template>
    <Head title="Welcome" />
    <h1>Welcome</h1>
    <p>Hello , welcome to your first Inertia app!</p>
</template>
