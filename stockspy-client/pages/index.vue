<template>
  <!-- Table -->
  <v-simple-table>
    <template v-slot:default v-if="products">
      <thead>
        <tr>
          <th class="text-left">Stock</th>
          <th class="text-left">Vendor</th>
          <th class="text-left">URL</th>
          <th class="text-left">Last checked</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products.products" :key="product.url">
          <!-- Stock -->
          <td v-if="product.stock > 0">
            <v-chip class="ma-2" color="green" text-color="white"
              ><v-avatar left>
                <v-icon>mdi-checkbox-marked-circle</v-icon></v-avatar
              >Available</v-chip
            >
          </td>
          <td v-else>
            <v-chip class="ma-2" color="red" text-color="white"
              ><v-avatar left> <v-icon>mdi-cancel</v-icon></v-avatar
              >Unavailable
            </v-chip>
          </td>
          <!-- Vendor -->
          <td>
            {{ product.vendor }}
          </td>
          <!-- URL -->
          <td>
            <a :href="product.url">{{ product.url }}</a>
          </td>
          <!-- Timestamp -->
          <td>
            {{ product.timestamp }}
          </td>
        </tr>
      </tbody>
    </template>
    <p v-else>Loading stock...</p>
  </v-simple-table>
</template>

<script>
export default {
  props: {
    source: String
  },

  data() {
    return {
      drawer: null,
      products: null
    }
  },
  mounted() {
    let socket = new WebSocket('ws://127.0.0.1:8080')

    socket.onmessage = function(event) {
      this.products = JSON.parse(event.data)
    }.bind(this)
  }
}
</script>
