<template>
    <div>
        <h3>{{ title }}</h3>
        <div v-for="d in data" :key="d.title">
            <div class="text-caption">{{ d.title }}</div>
            <v-slider
                v-model="d.value"
                :min="d.min"
                :max="d.max"
                :ticks="ticks(d.goal)"
                :color="getColor(d)"
                show-ticks="always"
                height="10"
                tick-size="4"
                thumb-size="0"
                readonly
                />
        </div>
    </div>
</template>

<script>
export default {
    props: {
        data: {
            type: Array,
            required: true
        },
        title: {
            type: String,
            default: "Goals"
        },
    },
    setup() {

        function ticks(value) {
            const obj = {};
            obj[value] = value;
            return obj;
        }

        function getColor(d) {
            if (d.value >= d.goal) {
                return d.moreBetter || d.value === d.goal ?
                    "success" : 'error'
            }
            return !d.moreBetter ? "success" : "error"
        }

        return {
            ticks,
            getColor
        }
    }
}
</script>
