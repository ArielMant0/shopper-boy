<template>
    <div class="main">
        <div class="wrapper">
            <ShoppingList/>
        </div>
    </div>
</template>

<script setup>
    import ShoppingList from '@/components/ShoppingList.vue';
    import { useAppStore } from '@/store/app';
    import useLoader from '@/use/loader';
    import { onMounted } from 'vue';

    const app = useAppStore();
    const loader = useLoader()

    function init() {
        loader.get("/categories").then(cats => app.categories = cats);
        loader.get("/products_list").then(prods => app.products = prods);
        loader.get("/units").then(units => app.units = units);
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
