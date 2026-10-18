(() => {
  document.documentElement.classList.add('js');
  const toggle = document.querySelector('.menu-button');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    const setMenu = (open, restoreFocus = false) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      nav.classList.toggle('open', open);
      if (restoreFocus) toggle.focus();
    };
    setMenu(false);
    toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && nav.classList.contains('open')) setMenu(false, true);
    });
    document.addEventListener('click', event => {
      if (nav.classList.contains('open') && !event.target.closest('.site-header')) setMenu(false);
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    matchMedia('(min-width: 951px)').addEventListener('change', () => setMenu(false));
  }

  const filters = Array.from(document.querySelectorAll('[data-filter]'));
  const cards = Array.from(document.querySelectorAll('[data-category]'));
  if (filters.length) {
    const counter = document.querySelector('[data-results-count]');
    const selectedSector = () => {
      const value = new URL(location.href).searchParams.get('sector') || 'all';
      return filters.some(button => button.dataset.filter === value) ? value : 'all';
    };
    const showSector = value => {
      filters.forEach(button => {
        const active = button.dataset.filter === value;
        button.classList.toggle('active', active);
        button.setAttribute('aria-pressed', String(active));
      });
      cards.forEach(card => { card.hidden = value !== 'all' && card.dataset.category !== value; });
      const count = cards.filter(card => !card.hidden).length;
      if (counter) counter.textContent = `${count} ${count === 1 ? 'initiative' : 'initiatives'} shown`;
    };
    filters.forEach(button => button.addEventListener('click', () => {
      const value = button.dataset.filter;
      const url = new URL(location.href);
      if (value === 'all') url.searchParams.delete('sector');
      else url.searchParams.set('sector', value);
      if (url.href !== location.href) history.pushState({}, '', url);
      showSector(value);
    }));
    showSector(selectedSector());
    addEventListener('popstate', () => showSector(selectedSector()));
  }
})();
