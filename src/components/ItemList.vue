<template>
    <div>
    <v-toolbar density="compact">
        <v-toolbar-title>Est. Price: {{ price }} €</v-toolbar-title>
        <v-spacer/>
        <v-btn @click="showAll = !showAll"
            :icon="showAll ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
            variant="text"/>
        <v-btn @click="addItem"
            icon="mdi-playlist-plus"
            variant="text"/>
        <v-btn @click="addReceipt"
            icon="mdi-receipt-text-plus-outline"
            variant="text"/>
    </v-toolbar>
    <v-list min-width="500">
        <template v-for="(items, cat) in itemsPerCat" :key="cat">
            <v-list-subheader v-if="items.length > 0" inset>{{ cat }}</v-list-subheader>

            <v-list-item
                v-for="item in items"
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
import { ref, reactive, computed } from 'vue';

export default {
    setup() {
        const showAll = ref(true);
        const items = reactive([
            {
                name: "Äpfel",
                amount: "4",
                unit: "Stk.",
                priceEstimate: 2.42,
                cart: true,
                category: "Obst"
            },{
                name: "Birnen",
                amount: "1",
                unit: "Stk.",
                cart: false,
                priceEstimate: 0.99,
                category: "Obst"
            },{
                name: "Zucchini",
                amount: "2",
                unit: "Stk.",
                cart: false,
                priceEstimate: 1.08,
                category: "Gemüse"
            },
        ])

        const units = ["Stk.", "g", "kg", "EL", "TL", "Msp"]
        const categories = ["Obst", "Gemüse", "Milchprodukte", "Sonstiges"]

        const itemsPerCat = computed(() => {
            const obj = {};
            categories.forEach(cat => {
                obj[cat] = filterByCategory(cat);
            })
            return obj;
        })

        const price = computed(() => {
            return items.reduce((acc,d) => acc + d.priceEstimate, 0);
        })

        function filterByCategory(category) {
            return items.filter(d => d.category === category &&
                (showAll.value || !d.cart))
        }

        function toggleCartStatus(item) {
            item.cart = !item.cart;
        }
        function removeItem(name) {
            items.splice(items.indexOf(d => d.name === name), 1)
        }

        function addItem() {
            items.push({
                name: "Käse",
                amount: "1",
                priceEstimate: 2.29,
                cart: false,
                category: "Milchprodukte"
            })
        }

        // TODO
        function addReceipt() {}

        return {
            itemsPerCat,
            price,
            showAll,
            units,
            toggleCartStatus,
            removeItem,
            addItem,
            addReceipt
        }
    }
}
</script>

<style scoped>
.item-in-cart {
    color: #666;
    font-size: smaller;
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
