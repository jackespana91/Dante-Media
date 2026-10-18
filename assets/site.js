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

  document.querySelectorAll('[data-venture-carousel]').forEach(carousel => {
    const rail = carousel.querySelector('.featured-grid');
    const controls = carousel.querySelector('.carousel-controls');
    const previous = carousel.querySelector('[data-carousel-prev]');
    const next = carousel.querySelector('[data-carousel-next]');
    const counter = carousel.querySelector('[data-carousel-count]');
    const mobile = matchMedia('(max-width: 670px)');
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
    const step = () => rail.children[0].getBoundingClientRect().width + 16;
    const update = () => {
      const index = Math.min(rail.children.length - 1, Math.round(rail.scrollLeft / step()));
      controls.hidden = !mobile.matches;
      rail.tabIndex = mobile.matches ? 0 : -1;
      previous.disabled = rail.scrollLeft < 2;
      next.disabled = rail.scrollLeft >= rail.scrollWidth - rail.clientWidth - 2;
      const label = `${index + 1} of ${rail.children.length}`;
      if (counter.textContent !== label) counter.textContent = label;
    };
    const move = direction => rail.scrollBy({left: direction * step(), behavior: reducedMotion.matches ? 'instant' : 'smooth'});
    previous.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    rail.addEventListener('scroll', update, {passive: true});
    rail.addEventListener('keydown', event => {
      if (event.target === rail && ['ArrowLeft', 'ArrowRight'].includes(event.key)) {
        event.preventDefault();
        move(event.key === 'ArrowRight' ? 1 : -1);
      }
    });
    mobile.addEventListener('change', update);
    addEventListener('resize', update, {passive: true});
    update();
  });

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
