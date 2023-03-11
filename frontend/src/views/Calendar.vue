<template>
    <div class="main">
        <div class="ma-2 pa-2 wrapper">
            <WeeklyPlan/>
        </div>
    </div>
</template>

<script>
import WeeklyPlan from '@/components/WeeklyPlan.vue';

export default {
    setup() {},
    components: { WeeklyPlan }
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
    max-width: 80%;
}
</style>
