<template>
  <v-main>
    <v-tabs stacked align-tabs="center" density="compact">
      <v-tab to="/">
          <v-icon>mdi-currency-eur</v-icon>
          Bilanz
        </v-tab>

        <v-tab to="/list">
          <v-icon>mdi-list-box-outline</v-icon>
          Einkaufsliste
        </v-tab>

        <v-tab to="/calendar">
          <v-icon>mdi-calendar-week</v-icon>
          Wochenplan
        </v-tab>
    </v-tabs>
    <router-view />
  </v-main>
</template>

<script setup>
  //
</script>
