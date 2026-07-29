/* order-state.js — shared order status constants and transition helper */
(function () {
  'use strict';

  const STATUSES = [
    'pending',
    'confirmed',
    'processing',
    'out_for_delivery',
    'delivered',
    'cancelled'
  ];

  const LABELS = {
    pending: 'Pending',
    confirmed: 'Confirmed',
    processing: 'Processing',
    out_for_delivery: 'Out for delivery',
    delivered: 'Delivered',
    cancelled: 'Cancelled'
  };

  const ALLOWED_NEXT = {
    pending: ['confirmed', 'cancelled'],
    confirmed: ['processing', 'cancelled'],
    processing: ['out_for_delivery', 'cancelled'],
    out_for_delivery: ['delivered', 'cancelled'],
    delivered: [],
    cancelled: []
  };

  function label(status) {
    return LABELS[status] || status || 'pending';
  }

  function canTransition(status, next) {
    if (!status || !next) return false;
    if (status === next) return true;
    return (ALLOWED_NEXT[status] || []).includes(next);
  }

  function transitions(status) {
    return ALLOWED_NEXT[status] || [];
  }

  function apply(order, next) {
    const current = order.status || 'pending';
    if (!canTransition(current, next)) return false;
    order.status = next;
    order.updatedAt = new Date().toISOString();
    return true;
  }

  window.JG_ORDER_STATE = {
    STATUSES,
    LABELS,
    ALLOWED_NEXT,
    label,
    canTransition,
    transitions,
    apply
  };
})();
