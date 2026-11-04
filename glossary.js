<script>
(() => {
  const glossary = {
    "accessible population": "The part of the intended population from which units could realistically be selected under the actual field constraints.",
    "confidence interval": "A range expressing uncertainty in an estimate under a specified sampling and statistical procedure.",
    "detection probability": "The chance that an animal or species is recorded during a specified survey when it is present or using the relevant area, under the survey model.",
    "ecological variability": "Real differences among the organisms, places, times or conditions in the system being studied.",
    "environmental variability": "Real variation in environmental conditions among places or times.",
    "nonresponse": "Failure to obtain a usable response from a person or unit selected or invited by a study.",
    "population": "The full set of units, places, times or conditions about which a specific estimate or claim is made.",
    "probability sampling": "Selection using a specified random procedure in which each eligible unit has a known, nonzero chance of selection.",
    "pseudoreplication": "Treating observations within a shared higher-level unit as though they were independent replicates of a treatment or comparison at that level.",
    "random sampling": "Selecting eligible units by a specified random procedure rather than choosing those that seem typical or convenient.",
    "replicate": "A separate unit providing another example of the focal treatment, comparison or predictor at the level where it varies.",
    "replication": "Including separate units that provide additional examples of the comparison or process the study is intended to investigate.",
    "sample": "The set of units selected for observation by a sampling procedure.",
    "sample size": "The number of contributing sampling units at the level relevant to a particular estimate or comparison.",
    "sampling frame": "The operational list, map or selection rule used to identify which eligible units can be selected.",
    "sampling unit": "A unit selected by the sampling design to be observed or measured.",
    "sampling variability": "Differences among estimates that would result from selecting different samples from the same population using the same procedure.",
    "selection bias": "A systematic difference introduced when the units included in a study are selected in a way related to the quantity being estimated.",
    "standard deviation": "A measure of the spread of observed values around their mean.",
    "standard error": "An estimate of how strongly an estimator, such as a sample mean, would vary across repeated samples under the relevant assumptions.",
    "stratified sampling": "Dividing a target population into defined groups or ranges, then selecting units separately within them.",
    "subsample": "An observation collected within a larger selected unit to describe that unit more fully.",
    "systematic sampling": "Selecting units at regular spatial or temporal intervals, sometimes with a random starting position.",
    "target population": "The full set of people, places, organisms, times or conditions to which a study intends to generalise.",
    "targeted sampling": "Deliberately selecting units because they represent specific conditions, contrasts or features relevant to the question."
};
  let popover = null;
  let active = null;
  let hideTimer = null;

  function ensurePopover() {
    if (!popover) {
      popover = document.createElement('div');
      popover.className = 'glossary-popover';
      popover.setAttribute('role', 'dialog');
      popover.setAttribute('aria-label', 'Glossary definition');
      popover.hidden = true;
      popover.addEventListener('mouseenter', cancelHide);
      popover.addEventListener('mouseleave', scheduleHide);
      document.body.appendChild(popover);
    }
    return popover;
  }
  function cancelHide() { if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; } }
  function scheduleHide() { cancelHide(); hideTimer = setTimeout(hide, 220); }
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
    cancelHide();
    const key = (el.dataset.term || '').toLowerCase();
    const definition = glossary[key];
    if (!definition) return;
    const p = ensurePopover();
    p.replaceChildren();
    const def = document.createElement('div');
    def.textContent = definition;
    p.appendChild(def);
    const link = document.createElement('a');
    link.className = 'glossary-more';
    link.href = el.getAttribute('href') || `glossary.html#glossary-${key.replace(/[^a-z0-9]+/g, '-')}`;
    link.textContent = 'Full glossary entry';
    p.appendChild(link);
    active = el;
    position(el);
  }
  function hide() {
    cancelHide();
    if (popover) popover.hidden = true;
    active = null;
  }
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a.glossary[data-term]').forEach(el => {
      const key = (el.dataset.term || '').toLowerCase();
      if (!glossary[key]) return;
      el.removeAttribute('title');
      el.setAttribute('aria-label', `${el.textContent}: ${glossary[key]}. Activate to open definition.`);
      el.addEventListener('mouseenter', () => show(el));
      el.addEventListener('mouseleave', scheduleHide);
      el.addEventListener('focus', () => show(el));
      el.addEventListener('blur', scheduleHide);
      el.addEventListener('click', ev => {
        ev.preventDefault();
        ev.stopPropagation();
        show(el);
      });
    });
    document.addEventListener('click', ev => {
      if (popover && popover.contains(ev.target)) return;
      if (active && active.contains(ev.target)) return;
      hide();
    });
    document.addEventListener('keydown', ev => { if (ev.key === 'Escape') hide(); });
    window.addEventListener('scroll', () => { if (active) position(active); }, true);
    window.addEventListener('resize', () => { if (active) position(active); });
  });
})();
</script>
