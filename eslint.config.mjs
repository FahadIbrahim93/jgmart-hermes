import js from '@eslint/js';
import globals from 'globals';

export default [
  js.configs.recommended,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.es2022,
        localStorage: 'readonly',
        caches: 'readonly',
        self: 'readonly',
        URL: 'readonly',
        Response: 'readonly',
        Request: 'readonly',
        CustomEvent: 'readonly',
        StorageEvent: 'readonly',
        navigator: 'readonly',
        JG_DATA_STORE: 'readonly',
        JG_ADMIN_BACKEND: 'readonly',
        escapeHtml: 'readonly',
        showToast: 'readonly',
        JG_DATA_STORE: 'readonly',
      },
      ecmaVersion: 2022,
      sourceType: 'module',
    },
    rules: {
      'no-undef': 'error',
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'no-console': 'off',
      'no-redeclare': 'error',
      'no-constant-condition': 'warn',
      'no-debugger': 'error',
      'no-empty': 'warn',
      'no-extra-semi': 'error',
      'no-irregular-whitespace': 'error',
      'no-unreachable': 'error',
      'prefer-const': 'warn',
      'eqeqeq': ['warn', 'smart'],
      'curly': ['warn', 'multi-line'],
    },
    ignores: [
      'node_modules/',
      'ARCHIVE/',
      '_archive/',
      'src/web/supabase/client.js',
    ],
  },
];