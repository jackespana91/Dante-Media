(() => {
  const toggle = document.querySelector('.menu-button');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('open', !expanded);
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('open');
    }));
  }
  const filters = Array.from(document.querySelectorAll('[data-filter]'));
  const cards = Array.from(document.querySelectorAll('[data-category]'));
  if (filters.length) {
    filters.forEach(button => button.addEventListener('click', () => {
      const value = button.dataset.filter;
      filters.forEach(b => { b.classList.toggle('active', b === button); b.setAttribute('aria-pressed', String(b === button)); });
      cards.forEach(card => { card.hidden = value !== 'all' && card.dataset.category !== value; });
      const counter = document.querySelector('[data-results-count]');
      if (counter) counter.textContent = `${cards.filter(c=>!c.hidden).length} initiatives shown`;
    }));
  }
})();
