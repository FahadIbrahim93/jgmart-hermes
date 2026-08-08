/* global JG_LOG:off */
/* logger.js — minimal production logger
 * In production builds, set JG_MART_ENV='production' to suppress
 * debug/info logs. Always keep warn/error visible.
 */
(function () {
  'use strict';
  const env = (typeof window !== 'undefined' && window.JG_MART_ENV) || 'production';
  const noop = function () {};
  const prefix = '[JG Mart]';
  if (env === 'production') {
    window.JG_LOG = {
      debug: noop,
      info: noop,
      log: noop,
      warn: function () {
        if (typeof console !== 'undefined' && console.warn) {
          console.warn.apply(console, [prefix].concat([].slice.call(arguments)));
        }
      },
      error: function () {
        if (typeof console !== 'undefined' && console.error) {
          console.error.apply(console, [prefix].concat([].slice.call(arguments)));
        }
      }
    };
  } else {
    window.JG_LOG = {
      debug: function () {
        if (typeof console !== 'undefined' && console.debug) {
          console.debug.apply(console, [prefix + ' [DEBUG]'].concat([].slice.call(arguments)));
        }
      },
      info: function () {
        if (typeof console !== 'undefined' && console.info) {
          console.info.apply(console, [prefix + ' [INFO]'].concat([].slice.call(arguments)));
        }
      },
      log: function () {
        if (typeof console !== 'undefined' && console.log) {
          console.log.apply(console, [prefix].concat([].slice.call(arguments)));
        }
      },
      warn: function () {
        if (typeof console !== 'undefined' && console.warn) {
          console.warn.apply(console, [prefix].concat([].slice.call(arguments)));
        }
      },
      error: function () {
        if (typeof console !== 'undefined' && console.error) {
          console.error.apply(console, [prefix].concat([].slice.call(arguments)));
        }
      }
    };
  }
}());
