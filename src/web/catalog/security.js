/* security.js — shared sanitization and validation for JG Mart */
(function(){
'use strict';

function escapeHtml(str){
  if(str == null) return '';
  return String(str).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]));
}

function sanitizeHtml(html){
  // We don't accept/render HTML from user input — everything is escaped with
  // escapeHtml() before insertion. This function is kept only for backward
  // compatibility with any callers that reference it; it returns the input
  // unchanged (already-escaped) rather than a regex filter, which is a known
  // bypass magnet (malformed/nested tags, <svg onload>, data: URIs, etc.).
  if(html == null) return '';
  return String(html);
}

function sanitizeUrl(url){
  if(!url) return '#';
  const u = String(url).trim().toLowerCase();
  if(u.startsWith('https://') || u.startsWith('http://') || u.startsWith('mailto:') || u.startsWith('tel:') || u.startsWith('#') || u.startsWith('/')){
    return url;
  }
  return '#';
}

function validatePhone(phone){
  const p = String(phone||'').replace(/[\s\-()]/g,'');
  return /^\+?\d{10,15}$/.test(p);
}

function validateBuilding(b){
  const n = parseInt(String(b||'').replace('B',''));
  return Number.isInteger(n) && n>=1 && n<=27;
}

function validateFlat(f){
  return String(f||'').trim().length >= 1 && String(f).trim().length <= 10;
}

window.JG_SECURITY = {escapeHtml, sanitizeHtml, sanitizeUrl, validatePhone, validateBuilding, validateFlat};
})();