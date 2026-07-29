/* offline-queue.js — offline order queue with auto-retry for JG Mart catalog */
(function(){
'use strict';
const KEY='jgmart_pending_orders';
function getPending(){
  try{return JSON.parse(localStorage.getItem(KEY)||'[]');}catch(e){return[];}
}
function setPending(arr){localStorage.setItem(KEY,JSON.stringify(arr));}
function enqueue(order){
  const pending=getPending();
  order._queuedAt=Date.now();
  order._attempts=0;
  pending.push(order);
  setPending(pending);
  updateBadge();
}
function dequeue(){
  const pending=getPending();
  if(!pending.length)return null;
  return pending.shift();
}
function updateBadge(){
  const pending=getPending();
  let badge=document.getElementById('offlineBadge');
  if(!badge)return;
  if(!navigator.onLine && pending.length){
    badge.textContent='⏳ '+pending.length+' pending';
    badge.style.display='inline-flex';
  }else if(pending.length){
    badge.textContent='🔄 Syncing...';
    badge.style.display='inline-flex';
  }else{
    badge.style.display='none';
  }
}
function processQueue(){
  if(!navigator.onLine)return;
  const pending=getPending();
  if(!pending.length){updateBadge();return;}
  updateBadge();
  const order=dequeue();
  if(!order)return;
  order._attempts=(order._attempts||0)+1;
  // Simulate send: in production this would POST to /api/orders
  // For catalog, we add to main orders list
  try{
    const orders=JSON.parse(localStorage.getItem('jgmart_ords')||'[]');
    orders.unshift(order);
    if(orders.length>50)orders.pop();
    localStorage.setItem('jgmart_ords',JSON.stringify(orders));
    setPending(getPending());
    toast('✅ Queued order synced');
  }catch(e){
    // Re-queue on failure
    order._attempts=(order._attempts||0)+1;
    const pending=getPending();
    pending.unshift(order);
    setPending(pending);
  }
  updateBadge();
  // Process next after short delay
  setTimeout(processQueue,800);
}
// Listen for online/offline
window.addEventListener('online',()=>{updateBadge();processQueue();});
window.addEventListener('offline',()=>{updateBadge();});
// Expose API
window.JG_OFFLINE_QUEUE={enqueue,getPending,processQueue,updateBadge,KEY};
// Init
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',()=>{updateBadge();});
}else{updateBadge();}
})();
