/**
 * Mente Desperta — Book Series Landing Page
 * Vanilla ES6+ · No dependencies
 * -------------------------------------------
 * Features: smart nav, mobile menu, smooth scroll, cover language
 * toggle, 3D tilt, intersection-observer fade-ins, hero float
 * stagger, Netlify form, CTA language priority, a11y, performance.
 */
(() => {
  'use strict';

  /* -------------------------------------------------- *
   *  Utilities
   * -------------------------------------------------- */

  /** True when the user prefers reduced motion. */
  const prefersReducedMotion = () =>
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /** True on touch-primary devices. */
  const isTouchDevice = () => 'ontouchstart' in window;

  /** Debounce — returns a rAF-throttled wrapper. */
  const rafDebounce = (fn) => {
    let ticking = false;
    return (...args) => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        fn(...args);
        ticking = false;
      });
    };
  };

  /** Shorthand selectors. */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  /* -------------------------------------------------- *
   *  1 · Navigation Scroll Effect  (smart nav)
   * -------------------------------------------------- */
  const initSmartNav = () => {
    const nav = $('.site-nav');
    if (!nav) return;

    let lastScrollY = window.scrollY;
    const SCROLL_THRESHOLD = 50;

    const onScroll = rafDebounce(() => {
      const currentY = window.scrollY;

      // Toggle .scrolled when past threshold
      nav.classList.toggle('scrolled', currentY > SCROLL_THRESHOLD);

      // Hide on down, show on up (only after threshold)
      if (currentY > SCROLL_THRESHOLD) {
        nav.classList.toggle('nav-hidden', currentY > lastScrollY);
      } else {
        nav.classList.remove('nav-hidden');
      }

      lastScrollY = currentY;
    });

    window.addEventListener('scroll', onScroll, { passive: true });
  };

  /* -------------------------------------------------- *
   *  2 · Mobile Menu
   * -------------------------------------------------- */
  const initMobileMenu = () => {
    const toggle = $('.nav-toggle');
    const nav = $('.site-nav');
    if (!toggle || !nav) return;

    const focusableSelector =
      'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])';

    /** Open / close helpers. */
    const openMenu = () => {
      document.body.classList.add('menu-open');
      nav.classList.add('menu-open');
      toggle.setAttribute('aria-expanded', 'true');

      // Focus first link inside nav menu
      const firstLink = $('a[href]', nav);
      if (firstLink) firstLink.focus();
    };

    const closeMenu = () => {
      document.body.classList.remove('menu-open');
      nav.classList.remove('menu-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus(); // return focus to trigger
    };

    const isOpen = () => document.body.classList.contains('menu-open');

    // Toggle click
    toggle.addEventListener('click', () => (isOpen() ? closeMenu() : openMenu()));

    // Close on nav-link click
    $$('a[href]', nav).forEach((link) =>
      link.addEventListener('click', () => {
        if (isOpen()) closeMenu();
      })
    );

    // Escape key closes menu
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isOpen()) {
        e.preventDefault();
        closeMenu();
      }
    });

    // Focus trap when menu is open
    document.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab' || !isOpen()) return;

      const focusable = $$(focusableSelector, nav);
      if (!focusable.length) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });
  };

  /* -------------------------------------------------- *
   *  3 · Global Language Toggle
   * -------------------------------------------------- */
  const initLanguageToggle = () => {
    const globalToggles = $$('.global-lang-toggle button');
    if (!globalToggles.length) return;
    
    const setLanguage = (lang) => {
      // Toggle body class for CSS to handle visibility
      if (lang === 'en') {
        document.body.classList.add('lang-en');
      } else {
        document.body.classList.remove('lang-en');
      }
      
      // Update global toggle buttons
      globalToggles.forEach(btn => {
        const isSelected = btn.dataset.globalLang === lang;
        btn.classList.toggle('active', isSelected);
        btn.setAttribute('aria-pressed', isSelected.toString());
      });
      
      // Save preference
      localStorage.setItem('site_lang', lang);
    };

    // Initialize from local storage or default to 'pt'
    const savedLang = localStorage.getItem('site_lang') || 'pt';
    setLanguage(savedLang);

    // Add click listeners to toggle buttons
    globalToggles.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetLang = btn.dataset.globalLang;
        setLanguage(targetLang);
      });
    });
  };

  /* -------------------------------------------------- *
   *  4 · Smooth Scroll
   * -------------------------------------------------- */
  const initSmoothScroll = () => {
    const nav = $('.site-nav');
    const navHeight = nav ? nav.offsetHeight : 0;

    document.addEventListener('click', (e) => {
      if (e.defaultPrevented) return;
      const anchor = e.target.closest('a[href^="#"]');
      if (!anchor) return;

      const id = anchor.getAttribute('href');
      if (id === '#') return;

      const target = $(id);
      if (!target) return;

      e.preventDefault();

      const top = target.getBoundingClientRect().top + window.scrollY - navHeight;

      window.scrollTo({ top, behavior: 'smooth' });

      // Update hash without jump
      history.pushState(null, '', id);
    });
  };

  /* -------------------------------------------------- *
   *  4 · Book Cover Language Toggle
   * -------------------------------------------------- */
  const initCoverToggle = () => {
    const STORAGE_KEY = 'coverLang';
    const cards = $$('.book-card');
    if (!cards.length) return;

    /** Detect preferred language: stored → browser → default. */
    const detectLang = () => {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored === 'pt' || stored === 'en') return stored;
      return navigator.language.startsWith('pt') ? 'pt' : 'en';
    };

    const applyLang = (card, lang) => {
      // Cover images
      $$('.book-cover', card).forEach((img) => {
        img.classList.toggle('active', img.dataset.lang === lang);
      });

      // Excerpts
      $$('.book-excerpt', card).forEach((excerpt) => {
        excerpt.classList.toggle('active', excerpt.dataset.lang === lang);
      });

      // Toggle buttons
      $$('.cover-toggle button', card).forEach((btn) => {
        const isActive = btn.dataset.lang === lang;
        btn.classList.toggle('active', isActive);
        btn.setAttribute('aria-pressed', String(isActive));
      });
    };

    /** Apply language to ALL cards. */
    const applyAll = (lang) => {
      cards.forEach((card) => applyLang(card, lang));
      localStorage.setItem(STORAGE_KEY, lang);
    };

    // Initial application
    applyAll(detectLang());

    // Delegated click on toggle buttons
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.cover-toggle button[data-lang]');
      if (!btn) return;

      const lang = btn.dataset.lang;
      applyAll(lang);
    });
  };

  /* -------------------------------------------------- *
   *  5 · Book Cover 3D Tilt + Light Reflection
   * -------------------------------------------------- */
  const initTiltEffect = () => {
    // Skip on touch devices or when user prefers reduced motion
    if (isTouchDevice() || prefersReducedMotion()) return;

    const MAX_ROTATION = 8; // degrees

    const wrappers = $$('.book-cover-wrapper');
    if (!wrappers.length) return;

    wrappers.forEach((wrapper) => {
      const light = $('.cover-light-effect', wrapper);

      wrapper.addEventListener('mousemove', (e) => {
        const rect = wrapper.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        // Normalised –1 → 1
        const normalX = (e.clientX - centerX) / (rect.width / 2);
        const normalY = (e.clientY - centerY) / (rect.height / 2);

        // Invert Y so hovering top tilts towards viewer
        const rotateX = -normalY * MAX_ROTATION;
        const rotateY = normalX * MAX_ROTATION;

        requestAnimationFrame(() => {
          wrapper.style.transform =
            `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;

          // Light reflection follows mouse
          if (light) {
            const percentX = ((e.clientX - rect.left) / rect.width) * 100;
            const percentY = ((e.clientY - rect.top) / rect.height) * 100;
            light.style.background =
              `radial-gradient(circle at ${percentX}% ${percentY}%, rgba(255,255,255,0.18) 0%, transparent 60%)`;
            light.style.opacity = '1';
          }
        });
      });

      wrapper.addEventListener('mouseleave', () => {
        requestAnimationFrame(() => {
          wrapper.style.transform =
            'perspective(800px) rotateX(0deg) rotateY(0deg)';
          wrapper.style.transition = 'transform 0.45s ease';

          if (light) {
            light.style.opacity = '0';
          }
        });
      });

      // Remove transition on re-enter so movement is instant
      wrapper.addEventListener('mouseenter', () => {
        wrapper.style.transition = 'none';
      });
    });
  };

  /* -------------------------------------------------- *
   *  6 · Intersection Observer — Fade-In Animations
   * -------------------------------------------------- */
  const initFadeIns = () => {
    const targets = $$('.fade-in');
    if (!targets.length) return;

    // If reduced motion, make everything visible immediately
    if (prefersReducedMotion()) {
      targets.forEach((el) => el.classList.add('visible'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          const el = entry.target;

          // Stagger via data-delay attribute (value in multiples of 0.12s)
          const delay = el.dataset.delay;
          if (delay) {
            el.style.transitionDelay = `${parseFloat(delay) * 0.12}s`;
          }

          el.classList.add('visible');
          observer.unobserve(el); // animate only once
        });
      },
      { threshold: 0.15 }
    );

    targets.forEach((el) => observer.observe(el));
  };

  /* -------------------------------------------------- *
   *  7 · Hero Mini-Covers Float Stagger
   * -------------------------------------------------- */
  const initHeroCoversStagger = () => {
    const covers = $$('.hero-cover');
    covers.forEach((cover, i) => {
      cover.style.animationDelay = `${i * 0.8}s`;
    });
  };

  /* -------------------------------------------------- *
   *  8 · Email Form (Netlify Forms)
   * -------------------------------------------------- */
  const initNewsletterForm = () => {
    const form = $('form[data-netlify="true"]');
    if (!form) return;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const emailInput = $('input[type="email"]', form);
      const email = emailInput ? emailInput.value.trim() : '';

      if (!emailRegex.test(email)) {
        emailInput?.focus();
        emailInput?.setCustomValidity('Por favor, insira um email válido.');
        emailInput?.reportValidity();
        return;
      }

      // Submit via fetch to Netlify
      const formData = new FormData(form);

      fetch(form.action || '/', {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: formData,
      })
        .then((res) => {
          if (!res.ok) throw new Error(res.statusText);

          // Replace form with success message
          const wrapper = form.parentElement;
          const msg = document.createElement('div');
          msg.className = 'form-success';
          msg.setAttribute('role', 'status');
          msg.innerHTML =
            '<p>Obrigado! Você receberá novidades em primeira mão. 🙏</p>';
          wrapper.replaceChild(msg, form);
        })
        .catch(() => {
          // Graceful fallback — still show success for static deploys
          const wrapper = form.parentElement;
          const msg = document.createElement('div');
          msg.className = 'form-success';
          msg.setAttribute('role', 'status');
          msg.innerHTML =
            '<p>Obrigado! Você receberá novidades em primeira mão. 🙏</p>';
          wrapper.replaceChild(msg, form);
        });
    });
  };

  /* -------------------------------------------------- *
   *  9 · CTA Button Priority by Language
   * -------------------------------------------------- */
  const initLangClass = () => {
    const lang = navigator.language || '';
    const isPt = /^pt(-BR|-PT)?$/i.test(lang) || lang.startsWith('pt');

    document.body.classList.add(isPt ? 'lang-pt' : 'lang-en');
  };

  /* -------------------------------------------------- *
   * 10 · Lazy-Load ".loaded" Class for Cover Images
   * -------------------------------------------------- */
  const initImageLoadObserver = () => {
    const images = $$('img[loading="lazy"]');
    if (!images.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          const img = entry.target;

          // If already loaded (cached), add class immediately
          if (img.complete) {
            img.classList.add('loaded');
          } else {
            img.addEventListener('load', () => img.classList.add('loaded'), { once: true });
          }

          observer.unobserve(img);
        });
      },
      { rootMargin: '100px' } // start a little early
    );

    images.forEach((img) => observer.observe(img));
  };

  /* -------------------------------------------------- *
   * 11 · Expandable Blurbs
   * -------------------------------------------------- */
  const initBlurbToggle = () => {
    const blurbs = $$('.book-blurb');
    blurbs.forEach(blurb => {
      // Check if blurb actually overflows its container (clamped to 3 lines)
      const isOverflowing = blurb.scrollHeight > blurb.clientHeight;
      if (isOverflowing) {
        // O rotulo segue o idioma da pagina: a home em ingles exibia "Ler mais".
        const isEN = document.documentElement.lang.toLowerCase().startsWith('en');
        const MORE = isEN ? 'Read more' : 'Ler mais';
        const LESS = isEN ? 'Read less' : 'Ler menos';

        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'blurb-toggle';
        toggleBtn.textContent = MORE;
        toggleBtn.setAttribute('aria-expanded', 'false');
        
        blurb.insertAdjacentElement('afterend', toggleBtn);
        
        toggleBtn.addEventListener('click', () => {
          blurb.classList.toggle('expanded');
          const isExpanded = blurb.classList.contains('expanded');
          toggleBtn.textContent = isExpanded ? LESS : MORE;
          toggleBtn.setAttribute('aria-expanded', isExpanded.toString());
        });
      }
    });
  };

  /* -------------------------------------------------- *
   * 12 · Books Carousel
   * -------------------------------------------------- */
  const initCarousel = () => {
    const track = $('#books-track');
    const container = $('.books-carousel-container');
    if (!track || !container) return;

    const prevBtn = $('.carousel-nav-btn.prev');
    const nextBtn = $('.carousel-nav-btn.next');
    const dots = $$('.carousel-dot');
    const cards = $$('.book-card', track);

    if (!cards.length) return;

    // Scroll by 1 card width
    const scrollAmount = () => cards[0].offsetWidth + 32;

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        track.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        track.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
      });
    }

    // Dots logic
    const updateDots = () => {
      const trackCenter = track.scrollLeft + track.offsetWidth / 2;
      let closestIndex = 0;
      let minDistance = Infinity;

      cards.forEach((card, index) => {
        const cardCenter = card.offsetLeft + card.offsetWidth / 2;
        const distance = Math.abs(trackCenter - cardCenter);
        if (distance < minDistance) {
          minDistance = distance;
          closestIndex = index;
        }
      });

      dots.forEach((dot, index) => {
        const isActive = index === closestIndex;
        dot.classList.toggle('active', isActive);
        if (isActive) {
          dot.setAttribute('aria-current', 'true');
        } else {
          dot.removeAttribute('aria-current');
        }
      });
    };

    track.addEventListener('scroll', rafDebounce(updateDots), { passive: true });

    // Click on dots
    dots.forEach((dot) => {
      dot.addEventListener('click', () => {
        const targetId = dot.getAttribute('aria-controls');
        const targetCard = $(`#${targetId}`);
        if (targetCard) {
          const scrollPos = targetCard.offsetLeft - track.offsetWidth / 2 + targetCard.offsetWidth / 2;
          track.scrollTo({ left: scrollPos, behavior: 'smooth' });
        }
      });
    });

    /** True only when the track is a horizontal carousel (>= 900px).
     *  Below that the cards are stacked vertically and track.scrollTo()
     *  does nothing — the page must scroll straight to the card instead. */
    const isHorizontal = () => track.scrollWidth > track.clientWidth + 4;

    // Intercept decision helper tags and hero cover links.
    // .hero-cover-link entra no seletor porque tres miniaturas do topo
    // (Kshitigarbha, Ei Seu Buda e Karma) nao tinham .decision-tag-link:
    // o clique caia no scroll generico, que nao move a faixa do carrossel,
    // e o leitor aterrissava no primeiro card em vez do livro escolhido.
    const decisionTags = $$('.decision-tag, .decision-tag-link, .hero-cover-link');
    decisionTags.forEach((tag) => {
      tag.addEventListener('click', (e) => {
        const targetId = tag.getAttribute('href');
        if (!targetId || !targetId.startsWith('#livro-')) return;

        const targetCard = $(targetId);
        if (!targetCard) return;

        e.preventDefault();
        const navHeight = $('.site-nav') ? $('.site-nav').offsetHeight : 0;

        if (!isHorizontal()) {
          // Stacked layout (mobile / tablet): go straight to the card.
          const cardTop =
            targetCard.getBoundingClientRect().top + window.scrollY - navHeight - 16;
          window.scrollTo({ top: cardTop, behavior: 'smooth' });
          history.pushState(null, '', targetId);
          return;
        }

        // Carousel layout: scroll the page to the carousel, then the track to the card.
        const top = container.getBoundingClientRect().top + window.scrollY - navHeight - 20;
        window.scrollTo({ top, behavior: 'smooth' });

        setTimeout(() => {
          const scrollPos =
            targetCard.offsetLeft - track.offsetWidth / 2 + targetCard.offsetWidth / 2;
          track.scrollTo({ left: scrollPos, behavior: 'smooth' });
        }, 300);

        history.pushState(null, '', targetId);
      });
    });
  };


  /* -------------------------------------------------- *
   * 13 · Substack Feed (RSS to JSON)
   * -------------------------------------------------- */
  const initSubstackFeed = () => {
    const feedContainer = document.getElementById("substack-feed");
    if (!feedContainer) return;

    const isEN = document.documentElement.lang.toLowerCase().startsWith('en');
    const T = isEN
      ? { read: 'Read on Substack', empty: 'No articles at the moment.',
          locale: 'en-US' }
      : { read: 'Ler no Substack', empty: 'Nenhum artigo encontrado no momento.',
          locale: 'pt-BR' };

    // Titulos ja publicados em ingles no Substack; o que nao estiver aqui
    // aparece no idioma original, que e melhor do que traduzir na marra.
    const EN_TITLES = {
      "E se você não fosse você por uma hora?": "What if you weren't you for an hour?",
      "A jornada de escritor e o tribunal de uma pessoa só.": "The writer's journey and the one-person tribunal.",
      "A Segunda Flecha": "The Second Arrow"
    };

    const rssUrl = encodeURIComponent("https://mentedespertabooks.substack.com/feed");
    const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${rssUrl}`;

    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        if (data.status !== "ok") {
          // Keep static fallback visible — don't clear it
          return;
        }
        feedContainer.innerHTML = "";
        data.items.slice(0, 3).forEach(item => {
          const pubDate = new Date(item.pubDate).toLocaleDateString(
            T.locale, { month: "short", day: "numeric", year: "numeric" });
          const title = isEN ? (EN_TITLES[item.title] || item.title) : item.title;

          const card = document.createElement("a");
          card.className = "article-card";
          card.href = item.link;
          card.target = "_blank";
          card.rel = "noopener noreferrer";
          card.innerHTML = `
              <div class="article-date"></div>
              <h3 class="article-title"></h3>
              <span class="article-link"></span>
            `;
          // XSS Prevention: Use textContent instead of innerHTML for user data
          card.querySelector('.article-date').textContent = pubDate;
          card.querySelector('.article-title').textContent = title;
          card.querySelector('.article-link').textContent = T.read + ' \u2192';
          feedContainer.appendChild(card);
        });
      })
      .catch(error => {
        // On fetch failure, keep the static fallback HTML visible
        console.error("Error fetching Substack feed:", error);
      });
  };

  /* -------------------------------------------------- *
   * 14 · Outbound Click Tracking (Amazon links)
   * -------------------------------------------------- */
  const initOutboundTracking = () => {
    const lang = document.documentElement.lang || 'pt-BR';

    /**
     * Infer book slug from the nearest context:
     * 1. Closest element with data-book attribute
     * 2. Closest article[id^="livro-"] on the home page
     * 3. URL path segment for book pages (/livros/SLUG/ or /en/books/SLUG/)
     */
    const getBookSlug = (el) => {
      const dataBook = el.closest('[data-book]');
      if (dataBook) return dataBook.dataset.book;

      const article = el.closest('article[id]');
      if (article && article.id.startsWith('livro-')) {
        return article.id.replace('livro-', '');
      }

      const path = window.location.pathname;
      const ptMatch = path.match(/^\/livros\/([^/]+)\//);
      if (ptMatch) return ptMatch[1];
      const enMatch = path.match(/^\/en\/books\/([^/]+)\//);
      if (enMatch) return enMatch[1];

      return 'unknown';
    };

    /**
     * Infer button position from CSS classes or section context.
     */
    const getPosition = (el) => {
      if (el.closest('.bp-hero, .hero')) return 'hero';
      if (el.closest('.bp-final')) return 'cta-final';
      if (el.closest('.bp-authorbox')) return 'author-box';
      if (el.closest('.bp-related')) return 'related';
      if (el.closest('.book-ctas')) return 'book-card';
      if (el.closest('.site-footer')) return 'footer';
      return 'inline';
    };

    document.addEventListener('click', (e) => {
      const link = e.target.closest('a[href*="amazon.com"]');
      if (!link) return;

      const url = new URL(link.href);
      const destination = url.hostname.replace('www.', '');
      const book = getBookSlug(link);
      const position = getPosition(link);

      const eventData = {
        event: 'outbound_click',
        book: book,
        lang: lang,
        position: position,
        destination: destination,
        url: link.href
      };

      // Push to dataLayer (GA4) if available
      if (window.dataLayer) {
        window.dataLayer.push(eventData);
      }

      // Plausible custom event if available
      if (window.plausible) {
        window.plausible('Outbound Click', { props: eventData });
      }

      // Console log for debugging (remove in production if needed)
      console.debug('[tracking] outbound_click:', eventData);
    });
  };

  /* -------------------------------------------------- *
   * 15 · Newsletter Signup Tracking
   * -------------------------------------------------- */
  const initSignupTracking = () => {
    const form = document.getElementById('newsletter-form');
    if (!form) return;

    const lang = document.documentElement.lang || 'pt-BR';
    const source = window.location.pathname === '/' || window.location.pathname === '/en/'
      ? 'homepage' : 'book-page';

    form.addEventListener('submit', () => {
      const eventData = {
        event: 'newsletter_signup',
        lang: lang,
        source: source
      };

      if (window.dataLayer) {
        window.dataLayer.push(eventData);
      }
      if (window.plausible) {
        window.plausible('Newsletter Signup', { props: eventData });
      }
      console.debug('[tracking] newsletter_signup:', eventData);
    });
  };

  /* -------------------------------------------------- *
   * 16 · Bootstrap
   * -------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', () => {
    initSmartNav();
    initMobileMenu();
    initSmoothScroll();
    initLanguageToggle();
    initTiltEffect();
    initFadeIns();
    initHeroCoversStagger();
    initNewsletterForm();
    initImageLoadObserver();
    initBlurbToggle();
    initCarousel();
    initSubstackFeed();
    initOutboundTracking();
    initSignupTracking();
  });
})();

