(function () {
  'use strict';

  // ── Header & Footer Injection ─────────────────────────────────────────────
  async function loadComponents() {
    const headerEl = document.getElementById('global-header');
    const footerEl = document.getElementById('global-footer');

    const [headerRes, footerRes] = await Promise.all([
      headerEl ? fetch('/header.html') : Promise.resolve(null),
      footerEl ? fetch('/footer.html') : Promise.resolve(null),
    ]);

    if (headerEl && headerRes && headerRes.ok) {
      headerEl.innerHTML = await headerRes.text();
      setActiveNav();
      initDropdown();
      initSearch();
    }

    injectSubpageNav();

    if (footerEl && footerRes && footerRes.ok) {
      footerEl.innerHTML = await footerRes.text();
    }
  }

  // ── Active Nav ────────────────────────────────────────────────────────────
  function setActiveNav() {
    const path = window.location.pathname;
    const header = document.getElementById('global-header');
    if (!header) return;

    if (path.startsWith('/elden-ring')) {
      const trigger = header.querySelector('.nav-dropdown-trigger');
      if (trigger) trigger.classList.add('active');
    }
  }

  // ── Elden Ring Subpage Nav Injection ──────────────────────────────────────
  const ER_NAV_LINKS = [
    { key: 'guides',    label: 'Guides',           href: '/elden-ring/guides/' },
    { key: 'checklist', label: 'Items Checklist',  href: '/elden-ring/items/' },
    { key: 'weapons',   label: 'Weapons Database', href: '/elden-ring/items/weapons/' },
    { key: 'ar-buffs',  label: 'AR Buff Calculator', href: '/elden-ring/ar-buffs/' },
  ];

  function injectSubpageNav() {
    document.querySelectorAll('.subpage-nav-container[data-er-nav]').forEach(nav => {
      const active = nav.dataset.erNav;
      const ul = document.createElement('ul');
      ul.className = 'subpage-nav-links';
      ER_NAV_LINKS.forEach(({ key, label, href }) => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = href;
        a.textContent = label;
        if (key === active) a.className = 'active';
        li.appendChild(a);
        ul.appendChild(li);
      });
      nav.innerHTML = '';
      nav.appendChild(ul);
    });
  }

  // ── Elden Ring Dropdown ───────────────────────────────────────────────────
  function initDropdown() {
    const wrap = document.querySelector('.nav-dropdown-wrap');
    if (!wrap) return;

    const trigger = wrap.querySelector('.nav-dropdown-trigger');
    if (!trigger) return;

    // First click opens the dropdown; second click follows the link.
    trigger.addEventListener('click', function (e) {
      if (!wrap.classList.contains('open')) {
        e.preventDefault();
        wrap.classList.add('open');
      }
      // Second click: let the browser navigate to /elden-ring/
    });

    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) wrap.classList.remove('open');
    });
  }

  // ── Search ────────────────────────────────────────────────────────────────
  let searchCache = null;

  async function getIndex() {
    if (searchCache) return searchCache;
    try {
      const res = await fetch('/search-index.json');
      if (res.ok) searchCache = await res.json();
    } catch (_) {
      searchCache = [];
    }
    return searchCache || [];
  }

  function initSearch() {
    const input = document.getElementById('wikiSearchInput');
    const dropdown = document.getElementById('searchResultsWindow');
    if (!input || !dropdown) return;

    input.addEventListener('input', async function () {
      const q = this.value.toLowerCase().trim();
      dropdown.innerHTML = '';
      if (!q) { dropdown.style.display = 'none'; return; }

      const index = await getIndex();
      const matches = index.filter(item =>
        item.title.toLowerCase().includes(q) ||
        (item.category || '').toLowerCase().includes(q) ||
        (item.description || '').toLowerCase().includes(q)
      );

      if (matches.length) {
        matches.slice(0, 12).forEach(m => {
          const a = document.createElement('a');
          a.href = m.url;
          a.className = 'search-result-item';
          a.innerHTML =
            `<span class="search-result-title">${m.title}</span>` +
            `<span class="search-result-category">${m.category}</span>`;
          dropdown.appendChild(a);
        });
      } else {
        dropdown.innerHTML =
          '<div style="padding:12px 16px;font-size:13px;color:#665E4A;font-family:\'Fira Code\',monospace;">No matching entries found.</div>';
      }
      dropdown.style.display = 'block';
    });

    document.addEventListener('click', function (e) {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = 'none';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', loadComponents);
})();
