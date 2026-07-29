/* data-store.js — normalized localStorage data access for JG Mart catalog */
(function() {
  'use strict';

  const PRODUCTS_KEY = 'jgmart_prods';
  const ORDERS_KEY = 'jgmart_ords';
  const CART_KEY = 'jgmart_c';
  const ADDR_KEY = 'jgmart_addr';
  const FEES_KEY = 'jgmart_fees';
  const LANG_KEY = 'jgmart_lang';
  const LAST_ORD_KEY = 'jgmart_lastOrd';

  function safeGet(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      console.warn('data-store: failed to read', key, e);
      return fallback;
    }
  }

  function safeSet(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) {
      console.warn('data-store: failed to write', key, e);
      return false;
    }
  }

  const DataStore = {
    products: {
      get() { return safeGet(PRODUCTS_KEY, []); },
      set(products) { return safeSet(PRODUCTS_KEY, products); }
    },

    orders: {
      get() { return safeGet(ORDERS_KEY, []); },
      set(orders) { return safeSet(ORDERS_KEY, orders); },
      add(order) {
        const orders = DataStore.orders.get();
        orders.unshift(order);
        if (orders.length > 50) orders.pop();
        return DataStore.orders.set(orders);
      }
    },

    cart: {
      get() { return safeGet(CART_KEY, []); },
      set(cart) { return safeSet(CART_KEY, cart); }
    },

    address: {
      get() { return safeGet(ADDR_KEY, {}); },
      set(address) { return safeSet(ADDR_KEY, address); }
    },

    fees: {
      get() { return safeGet(FEES_KEY, null); },
      set(fees) { return safeSet(FEES_KEY, fees); }
    },

    lang: {
      get() { return safeGet(LANG_KEY, 'en'); },
      set(lang) { return safeSet(LANG_KEY, lang); }
    },

    lastOrder: {
      get() { return safeGet(LAST_ORD_KEY, null); },
      set(order) { return safeSet(LAST_ORD_KEY, order); }
    },

    clearAll() {
      return safeSet(PRODUCTS_KEY, []) &&
             safeSet(ORDERS_KEY, []) &&
             safeSet(CART_KEY, []) &&
             safeSet(ADDR_KEY, {}) &&
             safeSet(FEES_KEY, null) &&
             safeSet(LANG_KEY, 'en') &&
             safeSet(LAST_ORD_KEY, null);
    }
  };

  window.JG_DATA_STORE = DataStore;
})();
