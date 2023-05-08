<template>
    <div class="d-flex">
        <v-autocomplete v-model="item.product"
            v-model:search="search"
            :loading="loading"
            :items="products"
            hide-no-data
            hide-details
            density="compact"
            :label="label"
            style="min-width: 150px;"/>
        <v-btn class="ml-2"
            icon="mdi-plus"
            variant="text"
            rounded="0"
            color="success"
            size="small"
            @click="dialog = true"/>

    <v-dialog v-model="dialog">
        <v-card title="Produkt hinzufügen">

            <v-card-text>
                <v-text-field label="Name"/>
            </v-card-text>

            <v-card-actions>
                <v-btn color="error" @click="dialog = false">close</v-btn>
                <v-btn color="success" @click="addBrandProduct">add</v-btn>
            </v-card-actions>

        </v-card>
    </v-dialog>

    </div>
</template>

<script setup>

    import { ref, watch } from 'vue';
    import useLoader from '@/use/loader';

    const loader = useLoader();
    const props = defineProps({
        item: {
            type: Object,
            required: true
        },
        label: {
            type: String,
            default: "Produkt"
        },
    })

    const loading = ref(false);
    const search = ref("");
    const products = ref([props.item.product]);

    const dialog = ref(false);

    function queryBrandProducts(name) {
        loading.value = true;
        loader.get("/brandproducts", { product: props.item.name, name: name })
            .then(list => {
                products.value = list;
                console.log(list)
                loading.value = false;
            })
    }
    // TODO
    function addBrandProduct() {

    }

    watch(search, function() {
        if (search.value) {
            queryBrandProducts(search.value);
        }
    })
</script>
