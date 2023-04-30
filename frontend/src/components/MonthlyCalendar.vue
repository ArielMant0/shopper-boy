<template>
    <div>
        <v-container>
            <v-row dense>
                <v-col cols="2" style="text-align: left;">
                    <v-icon @click="prevMonth">mdi-menu-left-outline</v-icon>
                </v-col>
                <v-col cols="8" style="text-align: center;">
                    {{ data.monthLong }} {{ data.year }}
                </v-col>
                <v-col cols="2" style="text-align: right;">
                    <v-icon @click="nextMonth">mdi-menu-right-outline</v-icon>
                </v-col>
            </v-row>

            <v-row class="mb-2" dense>
                <v-divider :thickness="3"/>
            </v-row>

            <v-row dense>
                <v-col :offset="idx === 0 ? 1 : 0" v-for="(day, idx) in weekdays"
                    style="text-align: center;">
                    {{ day }}
                </v-col>
            </v-row>

            <v-row class="mb-2" dense>
                <v-divider :thickness="3"/>
            </v-row>

            <v-row v-for="[num, week] in weeks" dense
                :class="week.some(inWeek) ? ['in-week', 'week-row'] : ['week-row']">
                <v-col>{{ num }}</v-col>

                <v-col v-for="day in week">
                    <div :class="dayClasses(day)">
                        <slot name="day">{{ day.day }}</slot>
                    </div>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script setup>
    import { useAppStore } from '@/store/app';
    import { DateTime, Info } from 'luxon';
    import { computed } from 'vue';

    const app = useAppStore();
    const weekdays = Info.weekdays("short");

    const props = defineProps({
        data: {
            type: DateTime,
            required: true
        }
    })

    const today = DateTime.now();

    const mStart = computed(() => {
        return props.data
            .startOf("month")
            .startOf("week")
    });
    const mEnd = computed(() => {
        return props.data
            .endOf("month")
            .plus({ week: 1 })
    });

    const weeks = computed(() => {
        const obj = new Map();
        let curr = mStart.value;
        while (curr < mEnd.value) {
            // for each week
            const array = [];
            const wn = curr.weekNumber;
            for (let j = 0; j < weekdays.length; ++j) {
                array.push(curr)
                curr = curr.plus({ day: 1 })
            }
            obj.set(wn, array);
        }
        return obj;
    });

    function inMonth(dt) {
        return dt.month === props.data.month;
    }
    function inWeek(dt) {
        return dt.year === today.year && dt.weekNumber === today.weekNumber;
    }
    function inDay(dt) {
        return inWeek(dt) && dt.day === today.day;
    }
    function dayClasses(dt) {
        return inDay(dt) ? ["today", "in-month"] :
            (inMonth(dt) ? ["in-month"] : ["not-in-month"])
    }

    function prevMonth() {
        app.minusDate({ month: 1 })
    }
    function nextMonth() {
        app.plusDate({ month: 1 })
    }
</script>

<style>
.not-in-month {
    color: #888;
    text-align: center;
}
.in-month {
    color: white;
    text-align: center;
}
.in-week { background-color: #333; }
.today { color: rgb(121, 194, 33); }

.week-row {
    border-radius: 3px;
}

.v-row--dense > .v-col {
    padding: 6px;
}
</style>
