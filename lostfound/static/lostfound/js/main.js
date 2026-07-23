document.addEventListener('DOMContentLoaded', () => {
  const revealElements = Array.from(document.querySelectorAll('.card, .hero, .stat-card, .item-card'));
  revealElements.forEach((element, index) => {
    element.classList.add('reveal');
    element.style.transitionDelay = `${Math.min(index * 35, 250)}ms`;
  });

  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    revealElements.forEach((element) => revealObserver.observe(element));
  } else {
    revealElements.forEach((element) => element.classList.add('is-visible'));
  }

  const searchInput = document.querySelector('#q');
  const categorySelect = document.querySelector('#category');
  const grid = document.querySelector('#item-grid');

  if (!searchInput || !categorySelect || !grid) {
    return;
  }

  const entries = Array.from(grid.querySelectorAll('.item-entry'));

  const applyClientFilter = () => {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const selectedCategory = categorySelect.value;

    let visibleCount = 0;

    entries.forEach((entry) => {
      const title = entry.dataset.title || '';
      const description = entry.dataset.description || '';
      const category = entry.dataset.category || '';

      const matchesSearch = !searchTerm || title.includes(searchTerm) || description.includes(searchTerm);
      const matchesCategory = !selectedCategory || category === selectedCategory;
      const visible = matchesSearch && matchesCategory;

      entry.classList.toggle('d-none', !visible);
      if (visible) {
        visibleCount += 1;
      }
    });

    let empty = document.querySelector('#client-empty-message');
    if (visibleCount === 0) {
      if (!empty) {
        empty = document.createElement('div');
        empty.id = 'client-empty-message';
        empty.className = 'col-12';
        empty.innerHTML = '<div class="alert alert-warning">No items match your current filters.</div>';
        grid.appendChild(empty);
      }
    } else if (empty) {
      empty.remove();
    }
  };

  searchInput.addEventListener('input', applyClientFilter);
  categorySelect.addEventListener('change', applyClientFilter);
});
