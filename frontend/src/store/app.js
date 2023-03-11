// Utilities
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
    state: () => ({
        shoppingList: [
            {
                name: "Apfel",
                amount: "4",
                unit: "Stk.",
                priceEstimate: 2.42,
                cart: true,
                category: "Obst"
            },
            {
                name: "Birne",
                amount: "1",
                unit: "Stk.",
                cart: false,
                priceEstimate: 0.99,
                category: "Obst"
            },
            {
                name: "Zucchini",
                amount: "2",
                unit: "Stk.",
                cart: false,
                priceEstimate: 1.08,
                category: "Gemüse"
            },
        ],
        categories: ["Obst", "Gemüse", "Milchprodukte", "Sonstiges"],
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
        itemsPerCategoryVisible: (state) => {
            const obj = {};
            state.categories.forEach(cat => {
                obj[cat] = state.shoppingList.filter(d => {
                    return d.category === cat && !d.cart
                });
            });
            return obj;
        },
        priceEstimate: (state) => {
            return state.shoppingList.reduce((acc, d) => acc+d.priceEstimate, 0)
        },
    },

    actions: {
        addItemToShoppingList(item) {
            if (item.unit === undefined) item.unit = "Stk."
            if (item.amount === undefined) item.amount = 1
            if (item.priceEstimate === undefined) item.priceEstimate = 0.99
            if (item.category === undefined) item.category = "Sonstiges"
            if (item.cart === undefined) item.cart = false
            this.shoppingList.push(item)
        },

        addItemsToShoppingList(items) {
            items.forEach(d => this.addItemToShoppingList(d))
        },

        removeItemFromShoppingList(name) {
            const idx = this.shoppingList.findIndex(d => d.name === name)
            if (idx >= 0) {
                this.shoppingList.splice(idx, 1);
            }
        },

        shoppingListIncludes(name) {
            return this.shoppingList.find(d => d.name === name) !== undefined
        }

    }
})
