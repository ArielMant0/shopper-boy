<template>
    <div>
    <v-list rounded class="week">
        <v-list-item v-for="item in data"
            :title="item.recipe"
            :variant="isToday(item.day)?'tonal':'plain'">

            <template v-slot:prepend>
                {{ item.day.toFormat("dd") }}.
                <v-divider vertical thickness="2" class="bo-100 ml-3 mt-1 mb-1"></v-divider>
                <v-avatar>{{ weekday(item.day, "short") }}</v-avatar>
            </template>

            <template v-slot:append>
                <v-btn icon size="x-small" variant="plain">
                    <v-icon @click="openDialog(item)">mdi-pencil</v-icon>
                </v-btn>
            </template>

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
                    v-model="recipe"
                    selected-class="bg-primary"
                    class="recipe-group">
                    <v-item v-for="r in recipes" v-slot="{ toggle, selectedClass }" :value="r">
                        <v-card
                            density="compact"
                            @click="toggle" rounded
                            :class="['ma-1', selectedClass]"
                            width="150">
                            <div class="text-caption pl-2 pr-2 pt-2">{{ r }}</div>
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

<script>
import { ref, reactive, computed } from 'vue';
import { DateTime } from 'luxon';

export default {

    setup() {

        const today = DateTime.now();
        const data = reactive([]);
        for (let i = -1; i < 6; ++i) {
            data.push({
                day: today.plus({ day: i }),
                recipe: i >= 0 && i < 2 ? "Chilli con Quinoa" : null,
                img: "https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            })
        }

        const allRecipes = [
            "Chilli con Quinoa",
            "Pesto-Nudeln",
            "Pizza",
            "Asia-Nudeln",
            "Salat",
            "Nudeln in Tomatensugo mit Erbsen",
            "Kartoffel-Rosenkohl-Auflauf",
            "Veganer Kartoffelsalat",
            "Gnocchi mit Gemüse",
            "Schnupfnudeln mit Gemüse",
        ];
        const recipes = computed(() => {
            if (search.value.length === 0) {
                return allRecipes
            }
            return allRecipes.filter(r => r.toLowerCase().includes(search.value.toLowerCase()))
        })

        const dialog = ref(false);
        const sourceDay = ref(null);
        const recipe = ref("")
        const search = ref("");

        function weekday(day, short=false) {
            return short ? day.weekdayShort : day.weekdayLong;
        }
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
            if (item.recipe) {
                recipe.value = item.recipe;
            }
            dialog.value = true;
        }
        function saveChanges() {
            dialog.value = false;
            const day = data.find(d => isDay(d.day, sourceDay.value));
            if (day) {
                day.recipe = recipe.value;
                recipe.value = "";
            }
        }

        return {
            data,
            dialog,
            search,
            recipe,
            recipes,
            weekday,
            isToday,
            openDialog,
            saveChanges
        }
    }
}
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
