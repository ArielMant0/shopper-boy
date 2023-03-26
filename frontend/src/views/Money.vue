<template>
    <div class="main">
        <div class="ma-2 pa-2 wrapper">
            <MonthlyExpenses :data="data.expenses" :details="data.details"/>
            <div class="mt-6">
                <GoalsTracker :data="goals"/>
            </div>
        </div>
    </div>
</template>

<script setup>
    import GoalsTracker from '@/components/GoalsTracker.vue';
    import MonthlyExpenses from '@/components/MonthlyExpenses.vue';
    import { reactive, onMounted, computed } from 'vue';
    import useLoader from '@/use/loader';
    import { DateTime } from 'luxon';

    const loader = useLoader();

    const selectedDate = DateTime.now()
    const selectedMonth = computed(() => selectedDate.month)

    const data = reactive({
        expenses: [],
        details: []
    })

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

    onMounted(function() {
        loader.get("/income").then(d => data.details = d)
        loader.get("/balance").then(d => data.expenses = d)
    })

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
    max-width: 80%;
}
</style>
