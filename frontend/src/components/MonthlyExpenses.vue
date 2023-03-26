<template>
    <div>
        <v-container>
            <v-row>
                <v-col cols="4" class="table-header" v-for="c in cols" :key="c">{{ c }}</v-col>
            </v-row>

            <v-row>
                <v-col cols="4">Income:</v-col>
                <v-col cols="4" class="table-item" v-for="(d, i) in data" :key="i">
                    {{ d.income.toFixed(2) }}
                </v-col>
            </v-row>

            <v-row>
                <v-col cols="4">Expenses:</v-col>
                <v-col cols="4" class="table-item" v-for="(d, i) in data" :key="i">
                    {{ d.expenses.toFixed(2) }}
                </v-col>
            </v-row>

            <v-row>
                <v-col cols="4">Difference:</v-col>
                <v-col cols="4" class="table-item" v-for="(d, i) in data" :key="i">
                    <div v-if="diff(d) < 0" class="text-error">
                        {{ diff(d).toFixed(2) }}
                    </div>
                    <div v-else-if="diff(d) == 0">
                        {{ diff(d).toFixed(2) }}
                    </div>
                    <div v-else class="text-success">
                        {{ diff(d).toFixed(2) }}
                    </div>
                </v-col>
            </v-row>

        </v-container>

        <div>
            <v-btn color="success" size="small" class="mb-2 mr-1" @click="addIncome">add income</v-btn>
            <v-btn color="error" size="small" class="mb-2 ml-1" @click="addExpense">add expense</v-btn>
        </div>

        <v-expansion-panels density="compact">
            <v-expansion-panel title="Details">
                <v-expansion-panel-text>
                <v-data-table v-if="details"
                    v-model:items-per-page="itemsPerPage"
                    :headers="headers"
                    :items="details"
                    density="compact"
                    max-width="200"
                    class="elevation-1">

                    <template v-slot:item.value="{ item }">
                        {{ item.value.value }} {{ item.value.currency }}
                    </template>
                </v-data-table>
            </v-expansion-panel-text>
            </v-expansion-panel>
        </v-expansion-panels>

    </div>
</template>

<script setup>
    import { ref, computed } from 'vue'

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

    const itemsPerPage = ref(10)
    const cols = computed(() => {
        return [""].concat(props.data.map(d => d.title))
    })

    function diff(d) { return d.income - d.expenses }

    const headers = [
        {
            title: 'Name',
            align: 'start',
            sortable: false,
            key: 'name',
        },{
            title: 'Value',
            sortable: true,
            key: 'value',
        },
    ]

    function addIncome() {

    }

    function addExpense() {

    }

</script>

<style scoped>
.table-header {
    text-align: center;
}
.table-item {
    text-align: right;
}
</style>
