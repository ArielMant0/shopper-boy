<template>
    <div class="main">
        <div class="wrapper">
            <ItemList/>
        </div>
    </div>
</template>

<script>
import ItemList from '@/components/ItemList.vue';

export default {
    components: { ItemList },
    setup() {
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
