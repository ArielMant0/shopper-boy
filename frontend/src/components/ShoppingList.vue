<template>
    <div class="mt-4">
        <v-toolbar density="compact">
            <v-toolbar-title class="text-overline">
                Est. Price: <b>{{ priceEstimateTotal.toFixed(2) }} €</b>
            </v-toolbar-title>
            <v-spacer/>
            <v-btn @click="showAll = !showAll"
                :icon="showAll ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
                variant="text" rounded="0"/>
            <v-btn @click="itemDialog = true"
                icon="mdi-playlist-plus"
                variant="text" rounded="0"/>
            <v-btn @click="addReceipt"
                icon="mdi-receipt-text-plus-outline"
                variant="text" rounded="0"/>
        </v-toolbar>

        <ItemList :items="items" min-width="50vw" @remove="removeItem"/>

        <div class="mt-2 d-flex justify-end">
            <v-btn @click="receiptDialog = true">bon speichern</v-btn>
        </div>

        <ItemSelector :open="itemDialog" @close="itemDialog = false" @update="loadItems"/>
        <ReceiptDialog :open="receiptDialog" @close="receiptDialog = false"/>
    </div>
</template>

<script setup>
    /**
     * {
     *   name: ".."
     *   priceEstimate: >0,
     *   amount: >0,
     *   cart: false,
     *   category: ".."
     * }
     */
    import { ref, computed, onMounted } from 'vue';
    import ItemSelector from '@/components/ItemSelector.vue';
    import ItemList from './ItemList.vue';
    import ReceiptDialog from '@/components/ReceiptDialog.vue';
    import { useAppStore } from '@/store/app';
    import { storeToRefs } from 'pinia';
    import useLoader from '@/use/loader';

    const app = useAppStore();
    const { priceEstimateTotal } = storeToRefs(app);

    const loader = useLoader();

    const itemDialog = ref(false);
    const receiptDialog = ref(false);
    const showAll = ref(true);

    const items = computed(() => {
        return showAll.value ?
            app.itemsPerCategory :
            app.itemsPerCategoryVisible
    })

    function loadItems() {
        loader.get("/shopping")
            .then(data => app.setShoppingListItems(data))
    }
    function removeItem(item) {
        loader.post("/delete/shopping", null, { id: item.id })
            .then(response => {
                app.removeItemFromShoppingList(item.id)
            })
    }

    // TODO
    function addReceipt() {}

    onMounted(loadItems)

</script>

<style scoped>
.item-in-cart {
    color: #888;
}
</style>

<style>
.amount {
    display: flex;
}
.amount > * {
    max-width: 75px;
}
</style>
