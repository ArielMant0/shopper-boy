<template>
    <div style="font-size: small; width: 100%;">

        <v-container fluid class="simple-table">
            <v-row dense>
                <v-col cols="3" class="table-item">Month</v-col>
                <v-col cols="3" class="table-item text-success">
                    <v-icon>mdi-trending-up</v-icon>
                </v-col>
                <v-col cols="3" class="table-item text-error">
                    <v-icon>mdi-trending-down</v-icon>
                </v-col>
                <v-col cols="3" class="table-item">
                    <v-icon>mdi-sigma</v-icon>
                </v-col>
            </v-row>

            <v-row v-for="(d, i) in data" :key="i" dense>
                <v-col cols="3" class="table-item">{{ d.title }}</v-col>
                <v-col cols="3" class="table-item">{{ d.income.toFixed(2) }} €</v-col>
                <v-col cols="3" class="table-item">{{ d.expenses.toFixed(2) }} €</v-col>
                <v-col cols="3" class="table-item">
                    <div v-if="diff(d) < 0" class="text-error">
                        {{ diff(d).toFixed(2) }} €
                    </div>
                    <div v-else-if="diff(d) == 0">
                        {{ diff(d).toFixed(2) }} €
                    </div>
                    <div v-else class="text-success">
                        {{ diff(d).toFixed(2) }} €
                    </div>
                </v-col>
            </v-row>

        </v-container>

        <div class="d-flex justify-end mr-3 ml-3">
            <v-btn color="success" size="small" class="mb-2 mr-1" @click="addIncome">add income</v-btn>
            <v-btn color="error" size="small" class="mb-2 ml-1" @click="addExpense">add expense</v-btn>
        </div>

        <div style="max-height: 50%;" class="ma-3">
            <v-data-table v-if="details"
                v-model:items-per-page="itemsPerPage"
                :headers="headers"
                :items="details"
                density="compact"
                max-width="200"
                class="elevation-1">

                <template v-slot:item.value="{ item }">
                    {{ item.raw.value.toFixed(2) }} {{ item.raw.currency }}
                </template>

                <template v-slot:item.date_start="{ item }">
                    {{ item.raw.date_start.toLocaleString(DateTime.DATE_FULL) }}
                </template>

                <template v-slot:item.id="{ item }">
                    <div class="d-flex justify-end">
                        <v-icon v-if="item.raw.recurrence" size="small" class="clickable ml-1">mdi-pencil</v-icon>
                        <v-icon size="small" class="clickable ml-1" color="error" @click="setDelete(item.raw)">mdi-delete</v-icon>
                    </div>
                </template>

            </v-data-table>
        </div>

        <v-dialog v-model="dialog" width="auto" min-width="300">
            <v-card>
                <v-card-title>
                    <span class="text-h5">Add {{ dialogType === 0 ? 'Income' : 'Expense' }} Source</span>
                </v-card-title>
                <v-card-text>
                    <v-form v-model="form">
                        <v-text-field v-model="formName" class="mb-2"
                            label="name" :rules="[required]"
                            density="compact" hide-details/>
                        <v-text-field v-model="formValue" class="mb-2"
                            label="value" :rules="[required, v => v > 0 || 'value must be greater than 0']"
                            type="number" min="0.01" step="0.01"
                            density="compact" hide-details/>
                        <v-text-field v-model="formDateAsStr" class="mb-2"
                            label="start date" :rules="[required]"
                            type="date" @change="setFormDate"
                            density="compact" hide-details/>
                        <v-checkbox v-model="formHasEnd" class="mb-2"
                            label="has end date" density="compact" hide-details/>
                        <v-text-field v-if="formHasEnd" v-model="formDateEndAsStr" class="mb-2"
                            label="end date" type="date" @change="setFormDateEnd"
                            density="compact" hide-details/>
                        <v-checkbox v-model="formRecurring" class="mb-2"
                            label="recurring" density="compact" hide-details/>
                        <v-select v-if="formRecurring" v-model="formRecType" class="mb-2"
                            :items="formRecTypes"
                            density="compact" hide-details/>
                        <v-text-field v-if="formRecurring" v-model="formRecValue" class="mb-2"
                            type="number" min="1" step="1" label="every"
                            :rules="[v => !!(v && formRecurring) || 'value required']"
                            density="compact" hide-details/>
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="warning" @click="dialog = false">cancel</v-btn>
                    <v-btn color="success" @click="submitIncomeExpense">submit</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="delDialog" width="auto" min-width="300">
            <v-card>
                <v-card-title>
                    <span class="text-h5">Delete {{ delItem.name }}</span>
                </v-card-title>
                <v-card-text>
                    Are you sure you want to delete <b>{{ delItem.name }}</b>?
                    <div class="ml-4">
                        <div class="text-caption">Date: {{ delItem.date_start.toISODate() }}</div>
                        <div class="text-caption">Value: {{ delItem.value.toFixed(2) }}</div>
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="warning" @click="delDialog = false">cancel</v-btn>
                    <v-btn color="error" @click="deleteItem">delete</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script setup>
    import useLoader from '@/use/loader';
    import { ref, reactive } from 'vue'
    import { DateTime } from 'luxon';

    const props = defineProps({
        data: {
            type: Array,
            required: true
        },
        details: {
            type: Array,
            required: false
        },
        title: {
            type: String,
            default: "Monthly Expenses"
        },
    });

    const emit = defineEmits(["income-update", "expense-update", "update"]);

    const itemsPerPage = ref(10)

    const dialog = ref(false);
    const dialogType = ref(0);
    const form = ref(false);
    const formName = ref("Name");
    const formValue = ref(100);
    const formDate = ref(DateTime.now());
    const formDateAsStr = ref(formDate.value.toISODate())
    const formHasEnd = ref(false);
    const formDateEnd = ref(DateTime.now().plus({ weeks: 1 }));
    const formDateEndAsStr = ref(formDateEnd.value.toISODate());
    const formRecurring = ref(false)
    const formRecType = ref("week")
    const formRecTypes = ["week", "month", "year"]
    const formRecValue = ref(1)

    const delDialog = ref(false);
    let delItem = reactive({});

    const loader = useLoader();

    function diff(d) { return d.income - d.expenses }

    const headers = [
        {
            title: 'Datum',
            sortable: true,
            key: 'date_start',
            align: "start",
        },{
            title: 'Name',
            align: 'start',
            sortable: true,
            key: 'name',
            align: "end",
        },{
            title: 'Wert',
            sortable: true,
            key: 'value',
            align: "end",
        },{
            title: 'Aktionen',
            sortable: false,
            key: 'id',
            align: "end",
        },
    ]

    function addIncome() {
        dialogType.value = 0;
        dialog.value = true;
    }

    function addExpense() {
        dialogType.value = 1;
        dialog.value = true;
    }

    function submitIncomeExpense() {
        dialog.value = false;
        const which = dialogType.value === 0 ? "/income" : "/expense"
        const params = {
            name: formName.value,
            value: formValue.value,
            date_start: formDate.value.toISODate()
        };

        if (formHasEnd.value) {
            params.date_end = formDateEnd.value.toISODate();
        }
        if (formRecurring.value) {
            params.recurrence = formRecType.value;
            params.recurrence_value = formRecValue.value;
        }

        loader.post(which, null, params).then(() => {
            emit(dialogType.value === 0 ? "income-update" : "expense-update")
            formName.value = "Name";
            formValue.value = 0;
            formDate.value = DateTime.now();
            formDateAsStr.value = formDate.value.toISODate()
            formRecurring.value = false;
            formHasEnd.value = false;
            formDateEnd.value = formDate.value.plus({ weeks: 1 });
            formDateAsStr.value = formDateEnd.value.toISODate()
        })
    }

    function required (v) {
        return !!v || 'Field is required'
    }

    function setFormDate() {
        formDate.value = DateTime.fromISO(formDateAsStr.value);
    }
    function setFormDateEnd() {
        formDateEnd.value = DateTime.fromISO(formDateEndAsStr.value);
    }

    function setDelete(item) {
        delItem = item;
        delDialog.value = true;
    }
    function deleteItem() {
        if (delItem) {
            delDialog.value = false;
            loader.post("delete/expense", {}, { id: delItem.id })
                .then(() => {
                    delDialog.value = false
                    emit("update")
                })
        }
    }

</script>

<style scoped>
.table-item {
    text-align: right;
}
.simple-table .v-row  {
    border: 1px solid rgb(100, 100, 100);
}

.clickable {
    cursor: pointer;
}
</style>
