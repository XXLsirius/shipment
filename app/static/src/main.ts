import { createApp, h } from "vue";
import Vue from "vue";
import "vite/modulepreload-polyfill";
import { createInertiaApp } from "@inertiajs/vue3";

import "./assets/main.css";
import "./assets/pe-icon-7-stroke/css/pe-icon-7-stroke.css";

import Dashboard from "./pages/Dashboard.vue";
import Shipping from "./pages/Shipping.vue";
import WaterArea from "./pages/WaterArea.vue";
import Charterer from "./pages/Charterer.vue";
import Certificate from "./pages/Certificate.vue";
import Ship from "./pages/Ship.vue";
import ShipEdit from "./pages/ShipEdit.vue";
import ShipDetail from "./pages/ShipDetail.vue";
import Mariner from "./pages/Mariner.vue";
import MarinerEdit from "./pages/MarinerEdit.vue";
import MarinerDetail from "./pages/MarinerDetail.vue";
import CertType from "./pages/CertType.vue";
import CertificateEdit from "./pages/CertificateEdit.vue";

import VueApollo from "vue-apollo"
import { provideApolloClient } from '@vue/apollo-composable'
import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'
import { ApolloLink } from "apollo-boost";
import { createUploadLink } from 'apollo-upload-client'
import { BatchHttpLink } from "@apollo/client/link/batch-http";


// const httpLink = createHttpLink({
//   uri: 'http://localhost:8000/graphql',
// })

const httpOptions = {
  uri:'http://localhost:8000/graphql',
}

// const httpLink = ApolloLink.split( operation=>operation.getContext().hasUpload,
//   createUploadLink(httpOptions),
//   new BatchHttpLink(httpOptions)
//  )

const cache = new InMemoryCache()

const apolloClient = new ApolloClient({
  link: createUploadLink(httpOptions),
  cache,
});

createInertiaApp({
  resolve: (name) => {
    let page: any;
    switch (name) {
      case "shipping":
        page = Shipping;
        break;
      case "waterArea":
        page = WaterArea;
        break;
      case "charterer":
        page = Charterer;
        break;
      case "certificate":
        page = Certificate;
        break;
      case "certificate/edit":
        page = CertificateEdit;
        break;
      case "ship":
        page = Ship;
        break;
      case "ship/edit":
        page = ShipEdit;
        break;
      case "ship/detail":
        page = ShipDetail;
        break;
      case "mariner":
        page = Mariner;
        break;
      case "mariner/edit":
        page = MarinerEdit;
        break;
      case "mariner/detail":
        page = MarinerDetail;
        break;
      case "certType":
        page = CertType;
        break;
      default:
        page = Dashboard;
        break;
    }

    return page;
  },
  setup({ el, App, props, plugin }) {
    provideApolloClient(apolloClient);
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el);
  },
});
