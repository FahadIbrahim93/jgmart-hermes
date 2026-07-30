/**
 * JG Mart — Supabase Client
 *
 * This is a lightweight Supabase client for browser usage.
 * In production, replace with: import { createClient } from '@supabase/supabase-js'
 *
 * For now, this uses fetch() directly to avoid npm dependencies.
 */

import { SUPABASE_URL, SUPABASE_ANON_KEY } from './config.js';

class SupabaseClient {
  constructor(url, key) {
    this.url = url.replace(/\/$/, '');
    this.key = key;
    this.headers = {
      'Content-Type': 'application/json',
      'apikey': this.key,
      'Authorization': `Bearer ${this.key}`
    };
  }

  async _request(method, path, body = null, extraHeaders = {}) {
    const options = {
      method,
      headers: { ...this.headers, ...extraHeaders }
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${this.url}/rest/v1${path}`, options);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: response.statusText }));
      throw new Error(error.message || `HTTP ${response.status}`);
    }

    if (response.status === 204) return null;

    const data = await response.json();
    return data;
  }

  async rpc(fn, params = {}) {
    try {
      const data = await this._request('POST', `/rpc/${fn}`, params);
      return { data, error: null };
    } catch (error) {
      return { data: null, error };
    }
  }

  // Auth
  async signUp(email, password, metadata = {}) {
    const response = await fetch(`${this.url}/auth/v1/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': this.key
      },
      body: JSON.stringify({
        email,
        password,
        data: metadata
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.msg || data.error_description || 'Signup failed');
    }

    return data;
  }

  async signIn(email, password) {
    const response = await fetch(`${this.url}/auth/v1/token?grant_type=password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': this.key
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.msg || data.error_description || 'Login failed');
    }

    // Store session
    localStorage.setItem('jgmart_session', JSON.stringify(data));

    // Update headers with access token
    this.headers['Authorization'] = `Bearer ${data.access_token}`;

    return data;
  }

  async signOut() {
    const session = localStorage.getItem('jgmart_session');
    if (!session) return;

    const { access_token } = JSON.parse(session);

    await fetch(`${this.url}/auth/v1/logout`, {
      method: 'POST',
      headers: {
        'apikey': this.key,
        'Authorization': `Bearer ${access_token}`
      }
    });

    localStorage.removeItem('jgmart_session');
    this.headers['Authorization'] = `Bearer ${this.key}`;
  }

  async getSession() {
    const sessionStr = localStorage.getItem('jgmart_session');
    if (!sessionStr) return null;

    try {
      const session = JSON.parse(sessionStr);

      // Check if token is expired
      if (session.expires_at && Date.now() / 1000 > session.expires_at) {
        await this.signOut();
        return null;
      }

      // Refresh headers
      this.headers['Authorization'] = `Bearer ${session.access_token}`;

      return session;
    } catch {
      return null;
    }
  }

  async getUser() {
    const session = await this.getSession();
    if (!session) return null;

    const response = await fetch(`${this.url}/auth/v1/user`, {
      headers: {
        'apikey': this.key,
        'Authorization': `Bearer ${session.access_token}`
      }
    });

    if (!response.ok) return null;

    return response.json();
  }

  // Database helpers
  async from(table) {
    return new QueryBuilder(this, table);
  }

  // Storage
  async upload(bucket, path, file) {
    const session = await this.getSession();
    if (!session) throw new Error('Not authenticated');

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.url}/storage/v1/object/${bucket}/${path}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${session.access_token}`,
        'apikey': this.key
      },
      body: file
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Upload failed');
    }

    return response.json();
  }

  getPublicUrl(bucket, path) {
    return `${this.url}/storage/v1/object/public/${bucket}/${path}`;
  }
}

class QueryBuilder {
  constructor(client, table) {
    this.client = client;
    this.table = table;
    this._query = `/${table}`;
    this._method = 'GET';
    this._body = null;
    this._select = null;
    this._single = false;
    this._preferRepresentation = false;
  }

  select(columns = '*') {
    this._query += `${this._query.includes('?') ? '&' : '?'}select=${encodeURIComponent(columns)}`;
    return this;
  }

  insert(data) {
    this._method = 'POST';
    this._query = `/${this.table}`;
    this._body = data;
    this._preferRepresentation = true;
    return this;
  }

  update(data) {
    this._method = 'PATCH';
    this._query = `/${this.table}`;
    this._body = data;
    return this;
  }

  delete() {
    this._method = 'DELETE';
    this._query = `/${this.table}`;
    return this;
  }

  eq(column, value) {
    const sep = this._query.includes('?') ? '&' : '?';
    this._query += `${sep}${column}=eq.${encodeURIComponent(value)}`;
    return this;
  }

  neq(column, value) {
    this._query += `&${column}=neq.${encodeURIComponent(value)}`;
    return this;
  }

  gt(column, value) {
    this._query += `&${column}=gt.${encodeURIComponent(value)}`;
    return this;
  }

  lt(column, value) {
    this._query += `&${column}=lt.${encodeURIComponent(value)}`;
    return this;
  }

  gte(column, value) {
    this._query += `&${column}=gte.${encodeURIComponent(value)}`;
    return this;
  }

  lte(column, value) {
    this._query += `&${column}=lte.${encodeURIComponent(value)}`;
    return this;
  }

  like(column, pattern) {
    this._query += `&${column}=like.${encodeURIComponent(pattern)}`;
    return this;
  }

  ilike(column, pattern) {
    this._query += `&${column}=ilike.${encodeURIComponent(pattern)}`;
    return this;
  }

  is(column, value) {
    this._query += `&${column}=is.${encodeURIComponent(value)}`;
    return this;
  }

  in(column, values) {
    const vals = Array.isArray(values) ? values.join(',') : values;
    this._query += `&${column}=in.(${encodeURIComponent(vals)})`;
    return this;
  }

  order(column, options = {}) {
    const asc = options.ascending !== false ? 'asc' : 'desc';
    const nulls = options.nullsFirst ? ',nullslast' : ',nullsfirst';
    this._query += `&order=${column}.${asc}${nulls}`;
    return this;
  }

  limit(count) {
    this._query += `&limit=${count}`;
    return this;
  }

  offset(count) {
    this._query += `&offset=${count}`;
    return this;
  }

  single() {
    this._single = true;
    if (this._method === 'GET') {
      this._query += '&limit=1';
    }
    return this;
  }

  async execute() {
    try {
      const extraHeaders = {};
      if (this._preferRepresentation) {
        extraHeaders['Prefer'] = 'return=representation';
      }
      let path = this._query;
      if (this._select && this._method !== 'GET') {
        path += `${path.includes('?') ? '&' : '?'}select=${encodeURIComponent(this._select)}`;
      }
      const result = await this.client._request(
        this._method,
        path,
        this._body,
        extraHeaders
      );
      let data = result;
      if (this._single && Array.isArray(data)) {
        data = data[0] ?? null;
      }
      return { data, error: null };
    } catch (error) {
      return { data: null, error };
    }
  }

  then(onFulfilled, onRejected) {
    return this.execute().then(onFulfilled, onRejected);
  }
}

// Export singleton
export const supabase = new SupabaseClient(SUPABASE_URL, SUPABASE_ANON_KEY);
export default supabase;

// Restore session token on load
if (typeof window !== 'undefined') {
  supabase.getSession().catch(() => {});
}
