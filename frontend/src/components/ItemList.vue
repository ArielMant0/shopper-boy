<template>
    <v-list :min-width="minWidth">
        <template v-for="(array, cat) in items" :key="cat">
            <div v-if="showCategories && array.length > 0" class="ml-4 text-overline">{{ cat }}</div>

            <v-list-item
                v-for="item in array"
                :key="item.name"
                :class="highlightInCart && item.cart ? ' item-in-cart' : ''">

                <slot name="item-content" :item="item">
                    <v-list-item-title class="text-caption">{{ item.name }}</v-list-item-title>
                </slot>

                <template v-slot:prepend>
                    <slot name="item-prepend" :item="item">
                        <div class="amount">
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
                    </slot>
                </template>

                <template v-slot:append>
                    <slot name="item-append" :item="item">
                        <span class="text-caption">
                            <v-icon size="x-small">mdi-approximately-equal</v-icon>
                            {{ item.priceEstimate }}
                            €
                        </span>
                        <v-btn @click="toggleCartStatus(item)"
                            class="pa-0" size="small"
                            :color="item.cart ? 'success' : 'default'"
                            :icon="item.cart ? 'mdi-cart-check' : 'mdi-cart-plus'"
                            variant="plain" rounded="0"/>
                        <v-btn @click="removeItem(item)"
                            size="small"
                            color="error"
                            icon="mdi-playlist-remove"
                            variant="plain" rounded="0"/>
                    </slot>
                </template>
            </v-list-item>
        </template>
    </v-list>
</template>

<script setup>

    import { useAppStore } from '@/store/app';
    import { storeToRefs } from 'pinia';

    const app = useAppStore();
    const { units } = storeToRefs(app);

    const emit = defineEmits(["remove"])

    const props = defineProps({
        items: {
            type: Object,
            required: true
        },
        minWidth: {
            type: String,
            default: "100px"
        },
        highlightInCart: {
            type: Boolean,
            default: true
        },
        showCategories: {
            type: Boolean,
            default: true
        },
    });

    function toggleCartStatus(item) {
        item.cart = !item.cart;
    }
    function removeItem(item) {
        emit("remove", item)
    }

</script>

<style scoped>
.item-in-cart {
    color: #888;
}
.amount {
    display: flex;
}
.amount > * {
    max-width: 75px;
}
</style>
