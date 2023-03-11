<template>
    <v-dialog
        v-model="dialog"
        @update:modelValue="checkDialog"
        transition="dialog-bottom-transition">
    <v-card title="Add Items To Shopping List">
        <v-card-text>
        <v-item-group
            v-model="selectedItems"
            mandatory multiple
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
                            <v-icon>{{ item.icon }}</v-icon>
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
                <v-text-field v-model="newItem.name" autofocus/>
                <v-text-field readonly>{{ newItem.category }}</v-text-field>
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

<script>
import { ref, computed, reactive, watch } from 'vue';
import { useAppStore } from '@/store/app';

export default {
    props: {
        open: {
            type: Boolean,
            default: false
        }
    },
    setup(props, { emit }) {
        const dialog = ref(false);
        const newItemDialog = ref(false);
        const selectedItems = ref([]);
        const newItem = reactive({
            name: "",
            category: ""
        })

        const app = useAppStore();

        const items = reactive([
            {
                name: "Apfel",
                icon: "mdi-food-apple-outline",
                category: "Obst"
            },{
                name: "Birne",
                icon: "mdi-food",
                category: "Obst"
            },{
                name: "Mandarine",
                icon: "mdi-food",
                category: "Obst"
            },{
                name: "Melone",
                icon: "mdi-food",
                category: "Obst"
            },{
                name: "Kirsche",
                icon: "mdi-food",
                category: "Obst"
            },{
                name: "Orange",
                icon: "mdi-food",
                category: "Obst"
            },{
                name: "Heidelbeere",
                icon: "mdi-food",
                category: "Obst"
            },{
                name: "Paprika",
                icon: "mdi-food",
                category: "Gemüse"
            },
        ]);

        const itemsPerCat = computed(() => {
            const obj = {};
            app.categories.forEach(cat => {
                obj[cat] = filter(cat);
            });
            return obj;
        });
        function filter(category) {
            return items.filter(d => {
                return d.category === category &&
                    !app.shoppingListIncludes(d.name)
            });
        }

        function addNewItem() {
            if (newItem.name && newItem.category) {
                items.push({
                    name: newItem.name,
                    category: newItem.category,
                    icon: "mdi-food"
                })
                newItemDialog.value = false;
                newItem.name = "";
                newItem.category = "";
            }
        }
        function openNewItemDialog(category) {
            newItem.category = category;
            newItemDialog.value = true;
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
        function addItems() {
            app.addItemsToShoppingList(items.filter(d => selectedItems.value.includes(d.name)))
            dialog.value = false;
            emit("close");
        }

        watch(() => props.open, () => {
            if (props.open) {
                dialog.value = true;
            }
        })

        return {
            selectedItems,
            dialog,
            newItemDialog,
            newItem,
            itemsPerCat,
            addNewItem,
            openNewItemDialog,
            addItems,
            closeDialog,
            checkDialog
        }
    },
    emits: ["close"],
}
</script>