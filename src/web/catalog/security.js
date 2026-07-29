/* security.js — shared sanitization and validation for JG Mart */
(function(){
'use strict';
function escapeHtml(str){
  if(str == null) return '';
  return String(str).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]));
}
function sanitizeHtml(html){
  // Very basic sanitizer for admin/order display — strips <script> and event handlers
  if(html == null) return '';
  let s = String(html);
  s = s.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
  s = s.replace(/\son\w+\s*=\s*(".*?"|'.*?'|[^\s>]+)/gi, '');
  s = s.replace(/javascript:/gi, '');
  return s;
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
