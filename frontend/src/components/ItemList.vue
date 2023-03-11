<template>
    <div>
    <v-toolbar density="compact">
        <v-toolbar-title class="text-overline">
            Est. Price: <b>{{ priceEstimate.toFixed(2) }} €</b>
        </v-toolbar-title>
        <v-spacer/>
        <v-btn @click="showAll = !showAll"
            :icon="showAll ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
            variant="plain"/>
        <v-btn @click="dialog = true"
            icon="mdi-playlist-plus"
            variant="plain"/>
        <v-btn @click="addReceipt"
            icon="mdi-receipt-text-plus-outline"
            variant="plain"/>
    </v-toolbar>
    <v-list min-width="50vw">
        <template v-for="(array, cat) in items" :key="cat">
            <div v-if="array.length > 0" class="ml-4 text-overline">{{ cat }}</div>

            <v-list-item
                v-for="item in array"
                :key="item.name"
                :class="item.cart ? ' item-in-cart' : ''">

                <v-list-item-title class="text-caption">{{ item.name }}</v-list-item-title>

                <template v-slot:prepend>
                    <div class="amount">
                        <!-- <v-text-field v-model="item.amount"
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
                            variant="solo"/> -->
                        <input type="number" min="0"
                            @change="item.amount = Number.parseFloat($event.target.value)"
                            class="pa-1 text-caption"
                            :value="item.amount"
                            style="max-width:45px;">
                        <select :value="item.unit"
                            @change="item.unit = $event.target.value"
                            class="mr-2 text-caption bg-surface"
                            style="cursor: pointer;">
                            <option v-for="unit in units" class="text-caption" :value="unit">
                                {{ unit }}
                            </option>
                        </select>
                    </div>
                </template>

                <template v-slot:append>
                    <span class="text-caption">
                        <v-icon size="x-small">mdi-approximately-equal</v-icon>
                        {{ item.priceEstimate }}
                        €
                    </span>
                    <v-btn @click="toggleCartStatus(item)"
                        class="pa-0" size="small"
                        :color="item.cart ? 'error' : 'success'"
                        :icon="item.cart ? 'mdi-cart-remove' : 'mdi-cart-check'"
                        variant="text"/>
                    <v-btn @click="removeItem(item.name)"
                        size="small"
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
