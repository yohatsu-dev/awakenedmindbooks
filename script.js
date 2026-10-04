/* Awakened Mind 2026 - minimal UI script */
(function(){
  "use strict";
  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function(){
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.addEventListener('click', function(e){
      if (e.target.tagName === 'A') { menu.classList.remove('open'); toggle.setAttribute('aria-expanded','false'); }
    });
  }

  // Track outbound Amazon clicks in GA4 (event: amazon_click)
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href*="amazon."]');
    if (!a || typeof gtag !== 'function') return;
    var book = a.getAttribute('data-book') || '';
    var store = /amazon\.com\.br/.test(a.href) ? 'BR' : 'US';
    gtag('event', 'amazon_click', {
      book: book,
      store: store,
      link_url: a.href,
      page_path: location.pathname
    });
  });
})();

/* Mobile buy bar on book pages: shown while no buy-button block is on screen. */
(function(){
  var bar=document.querySelector('[data-buybar]');
  if(!bar||!('IntersectionObserver' in window))return;
  var ctas=document.querySelectorAll('.bp-ctas');
  if(!ctas.length)return;
  bar.hidden=false;document.body.classList.add('has-buybar');
  var seen=new Set();
  var io=new IntersectionObserver(function(es){
    es.forEach(function(x){if(x.isIntersecting)seen.add(x.target);else seen.delete(x.target)});
    bar.classList.toggle('on',seen.size===0);
  });
  ctas.forEach(function(c){io.observe(c)});
})();
