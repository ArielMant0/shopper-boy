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
                    <div v-else class="text-success">
                        {{ diff(d).toFixed(2) }}
                    </div>
                </v-col>
            </v-row>

        </v-container>
    </div>
</template>

<script>
import { computed } from 'vue'

export default {
    props: {
        data: {
            type: Array,
            required: true
        },
        title: {
            type: String,
            default: "Monthly Expenses"
        },
    },
    setup(props) {

        const cols = computed(() => {
            return [""].concat(props.data.map(d => d.title))
        })

        function diff(d) {
            return d.income - d.expenses
        }

        return {
            cols,
            diff
        }
    }
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
