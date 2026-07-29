/* offline-queue.js — offline order queue with Supabase sync for JG Mart catalog */
(function(){
'use strict';
const KEY='jgmart_pending_orders';
const MAX_ATTEMPTS=5;
const INITIAL_RETRY_MS=2000;
function getPending(){
  try{return JSON.parse(localStorage.getItem(KEY)||'[]');}catch(e){return[];}
}
function setPending(arr){localStorage.setItem(KEY,JSON.stringify(arr));}
function isSupabaseAvailable(){
  return typeof window!=='undefined' && typeof window.submitOrderToSupabase==='function';
}
function enqueue(order){
  const pending=getPending();
  order._queuedAt=Date.now();
  order._attempts=0;
  pending.push(order);
  setPending(pending);
  updateBadge();
  updateStatus('Queued offline');
}
function dequeue(){
  const pending=getPending();
  if(!pending.length)return null;
  return pending.shift();
}
function requeue(order){
  order._attempts=(order._attempts||0)+1;
  const pending=getPending();
  pending.unshift(order);
  setPending(pending);
}
function updateBadge(){
  const pending=getPending();
  let badge=document.getElementById('offlineBadge');
  if(!badge)return;
  if(!navigator.onLine && pending.length){
    badge.textContent='⏳ '+pending.length+' pending';
    badge.style.display='inline-flex';
    badge.style.background='#c9a227';
  }else if(pending.length){
    badge.textContent='🔄 Syncing...';
    badge.style.display='inline-flex';
    badge.style.background='#00442D';
  }else{
    badge.style.display='none';
  }
}
function updateStatus(message){
  const el=document.getElementById('connectionStatus');
  if(!el)return;
  el.textContent=message||'';
  if(!navigator.onLine){
    el.textContent='Offline';
    el.style.color='#c9a227';
  }else if(isSupabaseAvailable()){
    el.textContent='Online · Supabase';
    el.style.color='#00442D';
  }else{
    el.textContent='Online · Local';
    el.style.color='#6b7280';
  }
}
function toast(message){
  const existing=document.querySelector('.toast');
  if(existing)existing.remove();
  const t=document.createElement('div');
  t.className='toast';
  t.textContent=message;
  document.body.appendChild(t);
  requestAnimationFrame(()=>t.classList.add('show'));
  setTimeout(()=>{t.classList.remove('show');setTimeout(()=>t.remove(),300);},2500);
}
function delay(ms){return new Promise(r=>setTimeout(r,ms));}
async function syncWithSupabase(order){
  const delayMs=INITIAL_RETRY_MS * Math.pow(2, Math.min(order._attempts||0, MAX_ATTEMPTS-1));
  await delay(delayMs);
  try{
    const result=await window.submitOrderToSupabase(order);
    if(result && result.success){
      toast('✅ Order synced');
      return true;
    }
    return false;
  }catch(e){
    console.warn('Supabase sync failed:', e);
    return false;
  }
}
function syncWithLocalStorage(order){
  try{
    const orders=JSON.parse(localStorage.getItem('jgmart_ords')||'[]');
    orders.unshift(order);
    if(orders.length>50)orders.pop();
    localStorage.setItem('jgmart_ords',JSON.stringify(orders));
    toast('✅ Queued order saved locally');
    return true;
  }catch(e){
    console.warn('localStorage sync failed:', e);
    return false;
  }
}
async function processQueue(){
  if(!navigator.onLine)return;
  const pending=getPending();
  if(!pending.length){updateBadge();updateStatus();return;}
  updateBadge();
  const order=dequeue();
  if(!order)return;
  order._attempts=(order._attempts||0)+1;
  try{
    let saved=false;
    if(isSupabaseAvailable()){
      saved=await syncWithSupabase(order);
    }
    if(!saved){
      saved=syncWithLocalStorage(order);
    }
    if(!saved){
      requeue(order);
      toast('⚠️ Sync failed, will retry');
    }
  }catch(e){
    console.warn('Queue processing failed:', e);
    requeue(order);
  }
  updateBadge();
  updateStatus();
  if(getPending().length){
    setTimeout(processQueue,800);
  }
}
// Listen for online/offline
window.addEventListener('online',()=>{updateBadge();updateStatus();processQueue();});
window.addEventListener('offline',()=>{updateBadge();updateStatus();});
// Expose API
window.JG_OFFLINE_QUEUE={
  enqueue,
  getPending,
  processQueue,
  updateBadge,
  updateStatus,
  KEY,
  isSupabaseAvailable,
  syncWithLocalStorage
};
// Init
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',()=>{updateBadge();updateStatus();});
}else{updateBadge();updateStatus();}
})();
