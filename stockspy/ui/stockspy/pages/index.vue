<template>
  <v-simple-table dark>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Stock</th>
          <th class="text-left">URL</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products.products" :key="product.url">
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
          <td>
            <a :href="product.url">{{ product.url }}</a>
          </td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
import axios from 'axios'

export default {
  async asyncData() {
    const { data } = await axios.get('http://127.0.0.1:5000')
    return { products: data }
  }
}
</script>
