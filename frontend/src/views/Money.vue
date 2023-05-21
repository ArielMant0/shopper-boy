<template>
    <div class="main">
        <div class="ma-1 pa-1 wrapper" style="width: 100%">
            <MonthlyExpenses
                :data="data.balance"
                :details="details"
                @income-update="loadIncomes"
                @expense-update="loadExpenses"
                @update="loadAll"/>
        </div>
    </div>
</template>

<script setup>
    import MonthlyExpenses from '@/components/MonthlyExpenses.vue';
    import useLoader from '@/use/loader';
    import { computed, reactive, onMounted } from 'vue';
    import { useAppStore } from '@/store/app';
    import { DateTime } from 'luxon';

    const loader = useLoader();
    const app = useAppStore();

    const data = reactive({
        balance: [],
        incomes: [],
        expenses: []
    })
    const details = computed(() => {
        const all = data.incomes.concat(data.expenses)
        all.sort((a, b) => a.date_start - b.date_start)
        return all;
    })

    function addBalance(d) {
        data.balance.push(d);
        data.balance.sort((a, b) => a < b)
    }
    function loadIncomes(loadBalance=true) {
        if (loadBalance) {
            data.balance = [];
            const prev = app.selectedDate.startOf("month").minus({ month: 1}).toISODate();
            const curr = app.selectedDate.startOf("month").toISODate();
            loader.get("/balance", { date: prev }).then(d => addBalance(d))
            loader.get("/balance", { date: curr }).then(d => addBalance(d))
        }
        loader.get("/income").then(d => {
            data.incomes = d.map(dd => {
                dd.date_start = DateTime.fromRFC2822(dd.date_start)
                if (dd.date_end) {
                    dd.date_end = DateTime.fromRFC2822(dd.date_end)
                }
                return dd;
            })
        });
    }
    function loadExpenses(loadBalance=true) {
        if (loadBalance) {
            data.balance = [];
            const prev = app.selectedDate.startOf("month").minus({ month: 1}).toISODate();
            const curr = app.selectedDate.startOf("month").toISODate();
            loader.get("/balance", { date: prev }).then(d => addBalance(d))
            loader.get("/balance", { date: curr }).then(d => addBalance(d))
        }
        loader.get("/expense").then(d => {
            data.expenses = d.map(dd => {
                dd.value = -dd.value;
                dd.date_start = DateTime.fromRFC2822(dd.date_start)
                if (dd.date_end) {
                    dd.date_end = DateTime.fromRFC2822(dd.date_end)
                }
                return dd;
            })
        })
    }
    function loadAll() {
        data.balance = [];
        const prev = app.selectedDate.startOf("month").minus({ month: 1}).toISODate();
        const curr = app.selectedDate.startOf("month").toISODate();
        loader.get("/balance", { date: prev }).then(d => addBalance(d))
        loader.get("/balance", { date: curr }).then(d => addBalance(d))
        loadIncomes(false);
        loadExpenses(false);
    }

    onMounted(loadAll)

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
    max-width: 70%;
}
</style>
