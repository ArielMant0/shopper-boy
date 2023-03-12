<template>
    <div class="main">
        <div class="wrapper">
            <ItemList/>
        </div>
    </div>
</template>

<script setup>
    import ItemList from '@/components/ItemList.vue';
    import { useAppStore } from '@/store/app';
    import useLoader from '@/use/loader';
    import { onMounted } from 'vue';

    const app = useAppStore();
    const loader = useLoader()

    function init() {
        loader.get("categories").then(cats => app.categories = cats);
        loader.get("products").then(prods => app.products = prods);
    }
    onMounted(init)

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
