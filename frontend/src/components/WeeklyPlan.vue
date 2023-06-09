<template>
    <div style="min-width: 250px;">
    <v-list rounded class="week">

        <v-list-item style="text-align: center;" density="compact">
            <v-btn @click="prevDay"
                icon="mdi-menu-up"
                variant="text"
                density="compact"/>
        </v-list-item>
        <v-divider></v-divider>

        <v-list-item v-for="item in data.days"
            :key="item.day.toISODate()"
            :title="item.recipe_name"
            :variant="isToday(item.day)?'tonal':'plain'">

            <template v-slot:prepend>
                {{ item.day.toFormat("dd") }}.
                <v-divider vertical thickness="2" class="bo-100 ml-3 mt-1 mb-1"></v-divider>
                <v-avatar>{{ item.day.weekdayShort }}</v-avatar>
            </template>

            <template v-slot:append>
                <v-btn icon size="x-small" variant="plain">
                    <v-icon @click="openDialog(item)">mdi-pencil</v-icon>
                </v-btn>
            </template>

        </v-list-item>

        <v-divider></v-divider>
        <v-list-item style="text-align: center;" density="compact">
            <v-btn @click="nextDay"
                icon="mdi-menu-down"
                variant="text"
                density="compact"/>
        </v-list-item>

    </v-list>

    <v-dialog v-model="dialog">
        <v-card>
            <v-card-title>Change Recipe for X</v-card-title>
            <v-card-text>
                <v-text-field v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    density="compact"
                    class="mb-4"
                    clearable
                    single-line
                    hide-details/>

                <v-item-group
                    v-model="recipeId"
                    selected-class="bg-primary"
                    class="recipe-group">
                    <v-item v-for="r in recipes" v-slot="{ toggle, selectedClass }" :value="r.id">
                        <v-card
                            density="compact"
                            @click="toggle" rounded
                            :class="['ma-1', selectedClass]"
                            width="150">
                            <div class="text-caption pl-2 pr-2 pt-2">{{ r.name }}</div>
                            <v-img src="https://cdn.vuetifyjs.com/images/parallax/material.jpg" cover/>
                        </v-card>
                    </v-item>
                </v-item-group>

            </v-card-text>
            <v-card-actions>
                <v-btn color="error" @click="dialog = false">close</v-btn>
                <v-btn color="success" @click="saveChanges">save</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

    </div>
</template>

<script setup>
    import { ref, reactive, computed, onMounted } from 'vue';
    import { DateTime } from 'luxon';
    import useLoader from '@/use/loader'

    const loader = useLoader();

    const data = reactive({
        selected: DateTime.now(),
        days: []
    });

    fillData()

    function fillData() {
        const array = [];
        for (let i = -1; i < 6; ++i) {
            array.push({
                day: data.selected.plus({ day: i }),
                recipe_id: null,
                recipe_name: null,
                img: "https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            });
        }
        data.days = array;
    }

    const allRecipes = ref([]);

    const recipes = computed(() => {
        if (search.value.length === 0) {
            return allRecipes.value
        }
        return allRecipes.value
            .filter(r => r.name.toLowerCase().includes(search.value.toLowerCase()))
    })

    const dialog = ref(false);
    const sourceDay = ref(null);
    const recipeId = ref("")
    const search = ref("");

    function isDay(day, target) {
        return day.day === target.day &&
            day.month === target.month &&
            day.year === target.year
    }
    function isToday(day) {
        return isDay(day, DateTime.now());
    }

    function openDialog(item) {
        sourceDay.value = item.day;
        if (item.recipe_id) {
            recipeId.value = item.recipe_id;
        }
        dialog.value = true;
    }
    function saveChanges() {
        dialog.value = false;
        const day = data.days.find(d => isDay(d.day, sourceDay.value));
        if (day) {
            day.recipe_id = recipeId.value;
            day.recipe_name = allRecipes.value.find(r => r.id === recipeId.value).name;
            loader.post("daily-plan", null, {
                date: day.day.toISODate(),
                id: recipeId.value
            })
            recipeId.value = null;
        }
    }

    async function loadDay(day) {
        loader.get(`weekly-plan`, { date: day.toISODate() })
            .then(plan => {
                data.selected = day;
                fillData();
                mergePlan(plan);
            })
    }

    async function prevDay() {
        loadDay(data.selected.plus({ day: -1 }))
    }

    async function nextDay() {
        loadDay(data.selected.plus({ day: 1 }))
    }

    function mergePlan(plan) {
        plan.forEach(d => {
            const day = DateTime.fromRFC2822(d.date);
            const item = data.days.find(dd => isDay(dd.day, day))
            if (item) {
                item.recipe_id = d.recipe_id;
                item.recipe_name = d.recipe_name;
                item.name = d.name;
            }
        })
    }

    async function init() {
        loader.get("recipes").then(rs => allRecipes.value = rs)
        loader.get("weekly-plan").then(plan => mergePlan(plan))
    }

    onMounted(init);

</script>

<style>
.week .v-divider {
    opacity: 1;
}
.recipe-group {
    display:flex;
    flex-wrap: wrap;
    max-height:55vh;
    overflow-y:auto;
}
.selected-recipe {
    border: 3px solid red;
}
</style>
