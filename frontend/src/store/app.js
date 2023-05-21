// Utilities
import { defineStore } from 'pinia'
import { DateTime } from 'luxon';

export const useAppStore = defineStore('app', {
    state: () => ({

        selectedDate: DateTime.now(),

        shoppingList: [
            {
                name: "Apfel",
                amount: "4",
                unit: "Stk.",
                priceEstimate: 2.42,
                price: 2.42,
                cart: true,
                category: "Obst",
                product: "",
            },
            {
                name: "Birne",
                amount: "1",
                unit: "Stk.",
                cart: false,
                priceEstimate: 0.99,
                price: 0.99,
                category: "Obst",
                product: "",
            },
            {
                name: "Zucchini",
                amount: "2",
                unit: "Stk.",
                cart: false,
                priceEstimate: 1.08,
                price: 1.08,
                category: "Gemüse",
                product: "",
            },
        ],
        categories: [],
        products: [],
        units: ["Stk.", "g", "kg", "EL", "TL", "Msp"]
    }),

    getters: {
        itemsPerCategory: (state) => {
            const obj = {};
            state.categories.forEach(cat => {
                obj[cat] = state.shoppingList.filter(d => d.category === cat);
            });
            return obj;
        },
        itemsPerCategoryInCart: (state) => {
            const obj = {};
            state.categories.forEach(cat => {
                obj[cat] = state.shoppingList.filter(d => {
                    return d.category === cat && d.cart
                });
            });
            return obj;
        },
        itemsPerCategoryVisible: (state) => {
            const obj = {};
            state.categories.forEach(cat => {
                obj[cat] = state.shoppingList.filter(d => {
                    return d.category === cat && !d.cart
                });
            });
            return obj;
        },
        price: (state) => {
            return state.shoppingList.reduce((acc, d) => acc+(d.cart ? d.price : 0), 0)
        },
        priceEstimateTotal: (state) => {
            return state.shoppingList.reduce((acc, d) => acc+d.priceEstimate, 0)
        },
        selectedWeek: (state) => {
            return state.selectedDate.weekNumber
        },
        selectedMonth: (state) => {
            return state.selectedDate.month
        },
        selectedYear: (state) => {
            return state.selectedDate.year
        },
    },

    actions: {

        setShoppingListItems (items) {
            this.shoppingList = [];
            this.addItemsToShoppingList(items);
        },

        addItemToShoppingList(item) {
            if (item.unit === undefined) item.unit = "Stk."
            if (item.amount === undefined) item.amount = 1
            if (item.priceEstimate === undefined) item.priceEstimate = 0.99
            if (item.price === undefined) item.price = item.priceEstimate;
            if (item.product === undefined) item.product = "";
            if (item.category === undefined) item.category = "Sonstiges"
            if (item.currency === undefined) item.currency = "€"
            if (item.cart === undefined) item.cart = false
            this.shoppingList.push(item)
        },

        addItemsToShoppingList(items) {
            items.forEach(d => this.addItemToShoppingList(d))
        },

        removeItemFromShoppingList(id) {
            const idx = this.shoppingList.findIndex(d => d.id === id)
            if (idx >= 0) {
                this.shoppingList.splice(idx, 1);
            }
        },

        shoppingListIncludes(name) {
            return this.shoppingList.find(d => d.name === name) !== undefined
        },

        minusDate(move) {
            this.selectedDate = this.selectedDate.minus(move);
        },

        plusDate(move) {
            this.selectedDate = this.selectedDate.plus(move);
        },

        clearShoppingList() {
            this.shoppingList = [];
        }
    }
})
