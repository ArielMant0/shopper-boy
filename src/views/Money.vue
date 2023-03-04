<template>
    <div class="main">
        <div class="ma-2 pa-2 wrapper">
            <MonthlyExpenses :data="expenses"/>
            <div class="mt-6">
                <GoalsTracker :data="goals"/>
            </div>
        </div>
    </div>
</template>

<script>
import GoalsTracker from '@/components/GoalsTracker.vue';
import MonthlyExpenses from '@/components/MonthlyExpenses.vue';
import { reactive } from 'vue';

export default {
    components: { MonthlyExpenses, GoalsTracker },
    setup() {
        const expenses = reactive([
            {
                income: 5000.03,
                expenses: 10243.28,
                title: "April"
            },
            {
                income: 5000.03,
                expenses: 1243.28,
                title: "May"
            },
        ]);

        const goals = reactive([
            {
                title: "reduce number of shopping trips",
                min: 0,
                max: 10,
                goal: 4,
                moreBetter: false,
                value: 2
            },{
                title: "buy less junk food",
                min: 0,
                max: 10,
                goal: 2,
                moreBetter: false,
                value: 7
            },{
                title: "eat more vegan meals",
                min: 0,
                max: 10,
                goal: 6,
                moreBetter: true,
                value: 8
            }
        ]);

        return {
            expenses,
            goals,
        };
    },
}
</script>

<style scoped>
.main {
    display: flex;
    justify-content: stretch;
    flex-direction: column;
    align-items: center;
}
.wrapper {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    max-width: 500px;
}
</style>
