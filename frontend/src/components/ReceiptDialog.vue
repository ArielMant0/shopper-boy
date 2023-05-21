<template>
    <v-dialog
        v-model="dialog"
        @update:modelValue="checkDialog"
        transition="dialog-bottom-transition">
        <v-card title="Bon hinzufügen">
        <v-card-text>

        <ItemList :items="itemsPerCategoryInCart" :highlight-in-cart="false" :show-categories="false">

            <template #item-append="{ item }">
                <div class="d-flex align-center">
                    <BrandProductSelector :item="item"/>
                    <div class="ml-4">
                        <input type="number" min="0" step="0.01"
                            @change="item.price = Number.parseFloat($event.target.value)"
                            class="pa-1 text-caption"
                            :value="item.price"
                            style="width: 50px;">
                        <span class="text-caption">€</span>
                    </div>
                </div>
            </template>

        </ItemList>

        <div class="d-flex justify-end">
            <span class="mr-4 mt-4">Summe: {{ clamp(price) }} €</span>
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
    import BrandProductSelector from './BrandProductSelector.vue';
    import useLoader from '@/use/loader';

    const app = useAppStore();
    const { itemsPerCategoryInCart, price } = storeToRefs(app)
    const props = defineProps({
        open: {
            type: Boolean,
            default: false
        }
    });
    const emit = defineEmits(["close"])

    const loader = useLoader();

    const dialog = ref(props.open);

    function clamp(value) {
        return +value.toFixed(2)
    }
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
        const body = {
            items: app.shoppingList.filter(d => d.cart)
        }
        dialog.value = false;
        loader.post("receipt", body)
            .then(response => {
                if (response.error) {
                    console.error(response.error)
                } else {
                    console.log(response)
                    app.clearShoppingList();
                }
            })
    }

    watch(() => props.open, () => {
        if (props.open) {
            dialog.value = true;
        }
    })

</script>

<style scoped>
.amount {
    display: flex;
}
.amount > * {
    max-width: 75px;
}
</style>
