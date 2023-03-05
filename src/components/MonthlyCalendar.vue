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
                    <p v-if="inDay(day)" class="in-month today">{{ day.day }}</p>
                    <p v-else-if="inMonth(day)" class="in-month">{{ day.day }}</p>
                    <p v-else class="not-in-month">{{ day.day }}</p>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import { DateTime, Info } from 'luxon';
import { ref, computed } from 'vue';

export default {
    setup() {

        const weekdays = Info.weekdays("short");

        const today = DateTime.now();
        const data = ref(DateTime.now())

        const mStart = computed(() => {
            return data.value
                .startOf("month")
                .startOf("week")
        });
        const mEnd = computed(() => {
            return data.value
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
            return dt.month === data.value.month;
        }
        function inWeek(dt) {
            return dt.year === today.year && dt.weekNumber === today.weekNumber;
        }
        function inDay(dt) {
            return inWeek(dt) && dt.day === today.day;
        }

        function prevMonth() {
            data.value = data.value.plus({ month: -1 })
        }
        function nextMonth() {
            data.value = data.value.plus({ month: 1 })
        }

        return {
            data,
            mStart, mEnd,
            weeks,
            weekdays,
            inMonth,
            inWeek,
            inDay,
            prevMonth,
            nextMonth
        }
    }
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
