<template>
    <v-dialog
        v-model="dialog"
        @update:modelValue="checkDialog"
        transition="dialog-bottom-transition">
    <v-card title="Add Receipt">
        <v-card-text>

        <ItemList :items="itemsPerCategoryInCart" :highlight-in-cart="false" :show-categories="false">

            <template #item-append="{ item }">
                <input type="number" min="0" step="0.01"
                    @change="item.price = Number.parseFloat($event.target.value)"
                    class="pa-1 text-caption"
                    :value="item.price"
                    style="max-width: 75px;">
                <span class="text-caption">€</span>
            </template>

        </ItemList>

        <div class="d-flex justify-end">
            <span>Summe: {{ price }} €</span>
        </div>

        </v-card-text>
          <v-card-actions>
            <v-btn color="error" @click="closeDialog">close</v-btn>
            <v-btn color="success" @click="addReceipt">add</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>

    import { ref,  watch } from 'vue';
    import { useAppStore } from '@/store/app';
    import { storeToRefs } from 'pinia';
    import ItemList from './ItemList.vue';

    const app = useAppStore();
    const { itemsPerCategoryInCart, price } = storeToRefs(app)
    const props = defineProps({
        open: {
            type: Boolean,
            default: false
        }
    });
    const emit = defineEmits(["close"])

    const dialog = ref(props.open);
    const finalPrice = ref(price.value);

    function closeDialog() {
        dialog.value = false;
        emit("close");
    }
    function checkDialog() {
        if (!dialog.value) {
            emit("close");
        }
    }
    function addReceipt() {

    }

    watch(() => props.open, () => {
        if (props.open) {
            dialog.value = true;
        }
    })
    watch(price, () => finalPrice.value = price.value);

</script>

<style scoped>
.amount {
    display: flex;
}
.amount > * {
    max-width: 75px;
}
</style>
