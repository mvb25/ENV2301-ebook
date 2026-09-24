<script>
(() => {
  const glossary = {
    "population": "The full set of units, places, times or conditions that an estimate is intended to represent.",
    "sample": "In the statistical sense used in this book, the set of sampling units selected for a study. In running prose we often use the concrete units (for example, 'the plots we measured') to avoid confusion with the everyday meaning of sample.",
    "sampling unit": "A unit selected by the sampling design to be observed or measured. A sampling unit is not necessarily the same as an individual measurement or a physical specimen.",
    "sample size": "The number of sampling units contributing to an estimate at the level relevant to the question.",
    "ecological variability": "Real variation among organisms, places, times, environmental conditions or ecological states in the system being studied. This book uses ecological variability as a broad term that includes what is often called environmental variability.",
    "environmental variability": "Real variation in environmental conditions across places or times, such as variation in temperature, soil moisture or inundation. The term is often used more broadly; in this book, ecological variability is the broader house term.",
    "sampling variability": "Variation among estimates that would result if different sets of sampling units were selected from the same population using the same sampling procedure.",
    "standard deviation": "A measure of how spread out observed values are around their mean; in this chapter it is used as information about variability among units in the wider population.",
    "standard error": "An estimate of how much an estimated quantity, such as a mean, would vary across repeated samples of the same size under the sampling assumptions.",
    "confidence interval": "A range around an estimate that expresses sampling uncertainty. A 95% confidence-interval procedure is designed so that, over many repeated samples under its assumptions, about 95% of the intervals contain the population quantity being estimated.",
    "replicate": "A separate sampling or experimental unit that provides a distinct example of the focal comparison or treatment.",
    "subsample": "An observation taken within a larger sampling unit to characterise that unit more fully."
  };

  let popover = null;
  let active = null;

  function ensurePopover() {
    if (!popover) {
      popover = document.createElement('div');
      popover.className = 'glossary-popover';
      popover.setAttribute('role', 'tooltip');
      popover.hidden = true;
      document.body.appendChild(popover);
    }
    return popover;
  }

  function position(el) {
    const p = ensurePopover();
    const r = el.getBoundingClientRect();
    p.hidden = false;
    const pr = p.getBoundingClientRect();
    let left = r.left + r.width / 2 - pr.width / 2;
    left = Math.max(12, Math.min(left, window.innerWidth - pr.width - 12));
    let top = r.bottom + 8;
    if (top + pr.height > window.innerHeight - 12) top = r.top - pr.height - 8;
    p.style.left = `${left}px`;
    p.style.top = `${Math.max(12, top)}px`;
  }

  function show(el) {
    const key = (el.dataset.term || '').toLowerCase();
    const definition = glossary[key];
    if (!definition) return;
    const p = ensurePopover();
    p.textContent = definition;
    active = el;
    position(el);
  }

  function hide() {
    if (popover) popover.hidden = true;
    active = null;
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.glossary[data-term]').forEach(el => {
      const key = (el.dataset.term || '').toLowerCase();
      if (!glossary[key]) return;
      el.removeAttribute('title');
      el.setAttribute('tabindex', '0');
      el.setAttribute('aria-label', `${el.textContent}: ${glossary[key]}`);
      el.addEventListener('mouseenter', () => show(el));
      el.addEventListener('mouseleave', hide);
      el.addEventListener('focus', () => show(el));
      el.addEventListener('blur', hide);
      el.addEventListener('click', ev => {
        ev.stopPropagation();
        if (active === el && popover && !popover.hidden) hide(); else show(el);
      });
    });
    document.addEventListener('click', hide);
    window.addEventListener('scroll', () => { if (active) position(active); }, true);
    window.addEventListener('resize', () => { if (active) position(active); });
  });
})();
</script>
