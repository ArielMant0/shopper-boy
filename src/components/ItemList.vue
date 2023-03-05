<template>
    <div>
    <v-toolbar density="compact">
        <v-toolbar-title>
            Est. Price: <b>{{ priceEstimate.toFixed(2) }} €</b>
        </v-toolbar-title>
        <v-spacer/>
        <v-btn @click="showAll = !showAll"
            :icon="showAll ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
            variant="text"/>
        <v-btn @click="dialog = true"
            icon="mdi-playlist-plus"
            variant="text"/>
        <v-btn @click="addReceipt"
            icon="mdi-receipt-text-plus-outline"
            variant="text"/>
    </v-toolbar>
    <v-list min-width="500">
        <template v-for="(array, cat) in items" :key="cat">
            <v-list-subheader v-if="array.length > 0" inset>{{ cat }}</v-list-subheader>

            <v-list-item
                v-for="item in array"
                :key="item.name"
                :title="item.name"
                :class="'text-caption' + (item.cart ? ' item-in-cart' : '')"
                >

                <template v-slot:prepend>
                    <div class="amount">
                        <v-text-field v-model="item.amount"
                            class="mr-1"
                            type="number"
                            density="compact"
                            :hide-details="true"
                            variant="solo"/>
                        <v-select v-model="item.unit"
                            :items="units"
                            class="mr-2"
                            density="compact"
                            :hide-details="true"
                            variant="solo"/>
                    </div>
                </template>

                <template v-slot:append>
                    <span>
                        <v-icon size="x-small">mdi-approximately-equal</v-icon>
                        {{ item.priceEstimate }}
                        €
                    </span>
                    <v-btn @click="toggleCartStatus(item)"
                        :color="item.cart ? 'error' : 'success'"
                        :icon="item.cart ? 'mdi-cart-remove' : 'mdi-cart-check'"
                        variant="text"/>
                    <v-btn @click="removeItem(item.name)"
                        color="error"
                        icon="mdi-playlist-remove"
                        variant="text"/>
                </template>
            </v-list-item>
        </template>
    </v-list>

    <ItemSelector :open="dialog" @close="dialog = false"/>
    </div>
</template>

<script>
/**
 * {
 *   name: ".."
 *   priceEstimate: >0,
 *   amount: >0,
 *   cart: false,
 *   category: ".."
 * }
 */
import { ref, computed } from 'vue';
import ItemSelector from '@/components/ItemSelector.vue';
import { useAppStore } from '@/store/app';
import { storeToRefs } from 'pinia';

export default {
    components: { ItemSelector },
    setup() {
        const app = useAppStore();
        const { units, priceEstimate } = storeToRefs(app);

        const dialog = ref(false);
        const showAll = ref(true);

        const items = computed(() => {
            return showAll.value ?
                app.itemsPerCategory :
                app.itemsPerCategoryVisible
        })

        function toggleCartStatus(item) {
            item.cart = !item.cart;
        }
        function removeItem(name) {
            app.removeItemFromShoppingList(name);
        }
        // TODO
        function addReceipt() { }

        return {
            items,
            priceEstimate,
            dialog,
            showAll,
            units,
            toggleCartStatus,
            removeItem,
            addReceipt
        };
    },
}
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
.amount .v-field__input {
    --v-field-padding-start: 12px;
    font-size: 12px;
}

.amount .v-select__selection-text {
    padding-top: 4px;
}
</style>
