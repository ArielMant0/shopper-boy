<template>
    <v-dialog v-model="dialog" transition="dialog-bottom-transition">
    <v-card title="Add Items To Shopping List">
        <v-card-text>
        <v-autocomplete v-model="searchProduct"
            v-model:search="search"
            :loading="loading"
            :items="searchResults"
            hide-no-data
            hide-details
            density="compact"
            label="Produkt finden ..."
            class="mb-4"/>
        <v-item-group
            v-model="selectedItems"
            multiple
            selected-class="bg-success"
            style="max-height: 55vh; overflow-y: auto;">
            <template v-for="(items, cat) in itemsPerCat">
                <div class="text-caption">{{ cat }}</div>
                <div>
                    <v-item>
                        <v-btn
                            size="small" color="grey-lighten-1" stacked
                            class="mr-1 mb-1"
                            @click="openNewItemDialog(cat)">
                            <v-icon>mdi-plus</v-icon>
                            <span>new</span>
                        </v-btn>
                    </v-item>
                    <v-item v-for="(item, index) in items" :key="index"
                        :value="item.name"
                        v-slot="{ selectedClass, toggle }">
                        <v-btn
                            size="small" color="grey-lighten-1" stacked
                            :class="['mr-1', 'mb-1', selectedClass]"
                            @click="toggle">
                            <v-icon>mdi-food</v-icon>
                            <span>{{ item.name }}</span>
                        </v-btn>
                    </v-item>
                </div>
            </template>
        </v-item-group>

        <v-dialog v-model="newItemDialog" width="auto">
            <v-card>
            <v-card-title>Add New Item</v-card-title>
            <v-card-text>
                <v-text-field v-model="newItem.name"
                    class="mb-4" hide-details
                    label="Name" autofocus
                    density="compact"/>
                <v-text-field readonly
                    class="mb-2" hide-details
                    density="compact"
                    :model-value="newItem.category"/>
            </v-card-text>
            <v-card-actions>
                <v-btn color="error" @click="newItemDialog = false">
                    close
                </v-btn>
                <v-btn color="success" @click="addNewItem">
                    add
                </v-btn>
            </v-card-actions>
            </v-card>
        </v-dialog>

        </v-card-text>
          <v-card-actions>
            <v-btn color="error" @click="closeDialog">close</v-btn>
            <v-btn color="success" @click="addItems">add</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
    import { ref, computed, reactive, watch } from 'vue';
    import { useAppStore } from '@/store/app';
    import useLoader from '@/use/loader';

    const props = defineProps({
        modelValue: {
            type: Boolean,
            required: true
        }
    });
    const emit = defineEmits(["update:modelValue", "add-to-list", "add-new-item"])

    const dialog = computed({
        get() {
            return props.modelValue
        },
        set(value) {
            emit("update:modelValue", value)
        }
    });
    const newItemDialog = ref(false);
    const selectedItems = ref([]);
    const newItem = reactive({
        name: "",
        category: ""
    })

    const search = ref("")
    const searchProduct = ref("")
    const loading = ref(false)
    const searchResults = ref([]);

    const app = useAppStore();
    const loader = useLoader();

    const itemsPerCat = computed(() => {
        const obj = {};
        app.categories.forEach(cat => {
            obj[cat] = filter(cat);
        });
        return obj;
    });
    function filter(category) {
        return app.products.filter(d => {
            return d.category === category &&
                !app.shoppingListIncludes(d.name)
        });
    }

    function addNewItem() {
        if (newItem.name && newItem.category) {
            emit("add-new-item", newItem)
            newItemDialog.value = false;
            newItem.name = "";
            newItem.category = "";
        }
    }
    function openNewItemDialog(category) {
        newItemDialog.value = true;
        newItem.name = "";
        newItem.category = category;
    }

    function closeDialog() {
        dialog.value = false;
    }
    function addItems() {
        dialog.value = false;
        const items = app.products.filter(d => selectedItems.value.includes(d.name));
        emit("add-to-list", items.map(d => app.fillItem(d)))
    }

    function loadProduct(name) {
        // TODO
    }
    function queryProducts(name) {
        loader.get("/products", { name: name })
            .then(results => searchResults.value = results.map(d => d.name))
    }

    watch(search, function() {
        if (search.value) {
            queryProducts(search.value);
        }
    })

    watch(searchProduct, loadProduct)

</script>
