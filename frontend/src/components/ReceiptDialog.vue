<template>
    <v-dialog v-model="dialog" transition="dialog-bottom-transition">
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

        <div class="mt-4 mb-2 text-caption">
            <v-text-field v-model="storeChain"
                class="mb-2" label="Laden"
                density="compact" hide-details/>
            <v-text-field v-model="storeAddress"
                class="mb-2" label="Adresse"
                density="compact" hide-details/>
            <div class="d-flex mb-2">
                <v-text-field v-model="date"
                    class="mb-2 mr-2" label="Datum"
                    type="date" density="compact" hide-details/>
                <v-text-field v-model="time"
                    class="mb-2" label="Uhrzeit"
                    type="time" density="compact" hide-details/>
            </div>
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

    import { ref, computed } from 'vue';
    import { useAppStore } from '@/store/app';
    import { storeToRefs } from 'pinia';
    import ItemList from './ItemList.vue';
    import BrandProductSelector from './BrandProductSelector.vue';
    import useLoader from '@/use/loader';
    import { DateTime } from 'luxon';

    const app = useAppStore();
    const { itemsPerCategoryInCart, price } = storeToRefs(app)

    const props = defineProps({
        modelValue: {
            type: Boolean,
            required: true
        }
    });
    const emit = defineEmits(["update:modelValue", "update"])

    const loader = useLoader();

    const dialog = computed({
        get() {
            return props.modelValue
        },
        set(value) {
            emit("update:modelValue", value)
        }
    });
    const storeChain = ref("EDEKA");
    const storeAddress = ref("Hauptstr. 5, 70563 Stuttgart");
    const date = ref(DateTime.now().toFormat("yyyy-MM-dd"))
    const time = ref("18:00")

    function clamp(value) {
        return +value.toFixed(2)
    }
    function closeDialog() {
        dialog.value = false;
    }
    function addReceipt() {
        const body = {
            items: app.shoppingList.filter(d => d.cart),
            storeChain: storeChain.value,
            storeAddress: storeAddress.value,
            date: date.value,
            time: time.value
        }
        dialog.value = false;
        loader.post("/receipt", body)
            .then(response => {
                if (response.error) {
                    console.error(response.error)
                } else {
                    emit("update")
                }
            })
    }
</script>

<style scoped>
.amount {
    display: flex;
}
.amount > * {
    max-width: 75px;
}
</style>
