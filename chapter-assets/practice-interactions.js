/* ENV2301 practice supplement: self-assessment, no automated grading of written answers.
   All interactions are local to the student's browser; responses are not transmitted. */
(() => {
  'use strict';
  function install() {
    const exercises = [...document.querySelectorAll('.practice-exercise')];
    if (!exercises.length) return;

    for (const exercise of exercises) {
      const area = exercise.querySelector('.practice-response');
      const reveal = exercise.querySelector('.practice-reveal');
      const solution = exercise.querySelector('.practice-solution');
      const status = exercise.querySelector('.practice-status');
      if (!area || !reveal || !solution) continue;
      const mode = area.dataset.mode;
      solution.hidden = true;
      reveal.setAttribute('aria-expanded', 'false');

      function stepComplete(step) {
        const stepMode = step.dataset.mode;
        if (stepMode === 'text') {
          const entry = step.querySelector('textarea');
          return Boolean(entry && entry.value.trim().length >= 5);
        }
        if (stepMode === 'single' || stepMode === 'multi') {
          return Boolean(step.querySelector('input:checked'));
        }
        if (stepMode === 'matching') {
          const selects = [...step.querySelectorAll('select')];
          return selects.length > 0 && selects.every(select => select.value !== '');
        }
        if (stepMode === 'fill') {
          const inputs = [...step.querySelectorAll('input[type="text"]')];
          return inputs.length > 0 && inputs.every(input => input.value.trim() !== '');
        }
        return false;
      }
      function updateSequence() {
        if (mode !== 'sequence') return;
        const steps = [...area.querySelectorAll('.practice-step')];
        let priorReady = true;
        for (const step of steps) {
          step.hidden = !priorReady;
          if (priorReady) priorReady = stepComplete(step);
        }
      }
      function hasAttempt() {
        if (mode === 'sequence') {
          const steps = [...area.querySelectorAll('.practice-step')];
          return steps.length > 0 && steps.every(step => !step.hidden && stepComplete(step));
        }
        if (mode === 'text') {
          const entry = area.querySelector('textarea');
          return Boolean(entry && entry.value.trim().length >= 5);
        }
        if (mode === 'fill') {
          const inputs = [...area.querySelectorAll('input[type="text"]')];
          return inputs.length > 0 && inputs.every(input => input.value.trim().length > 0);
        }
        if (mode === 'single' || mode === 'multi') {
          return Boolean(area.querySelector('input:checked'));
        }
        if (mode === 'matching') {
          const selects = [...area.querySelectorAll('select')];
          return selects.length > 0 && selects.every(s => s.value !== '');
        }
        return false;
      }

      function compare() {
        if (mode === 'sequence') return null; // Written steps need human interpretation.
        if (mode === 'fill') {
          return [...area.querySelectorAll('input[type="text"]')].every(input => input.value.trim().toLowerCase() === input.dataset.answer.toLowerCase());
        }
        if (mode === 'single') {
          const checked = area.querySelector('input:checked');
          const expected = area.querySelector('fieldset')?.dataset.correct;
          return checked?.value === expected;
        }
        if (mode === 'multi') {
          const inputs = [...area.querySelectorAll('input[type="checkbox"]')];
          return inputs.every(input => input.checked === (input.dataset.answer === 'true'));
        }
        if (mode === 'matching') {
          return [...area.querySelectorAll('select')].every(select => select.value === select.dataset.answer);
        }
        return null; // Written answers cannot be judged reliably by a keyword match.
      }

      function closeExplanation() {
        solution.hidden = true;
        reveal.setAttribute('aria-expanded', 'false');
        reveal.textContent = 'Show explained answer';
        status.textContent = '';
      }
      function respondToChange() {
        updateSequence();
        closeExplanation();
        reveal.disabled = !hasAttempt();
      }
      area.addEventListener('input', respondToChange);
      area.addEventListener('change', respondToChange);
      updateSequence();
      reveal.disabled = !hasAttempt();

      reveal.addEventListener('click', () => {
        if (!hasAttempt()) return;
        if (!solution.hidden) {
          closeExplanation();
          return;
        }
        const match = compare();
        if (match === true) {
          status.textContent = 'Your choices match the suggested answer.';
          status.dataset.result = 'matches';
        } else if (match === false) {
          status.textContent = 'Some choices differ. Compare them with the reasoning below.';
          status.dataset.result = 'differs';
        } else {
          status.textContent = 'Compare your reasoning with the explanation below.';
          status.dataset.result = 'written';
        }
        solution.hidden = false;
        reveal.setAttribute('aria-expanded', 'true');
        reveal.textContent = 'Hide explanation';
      });
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', install);
  } else {
    install();
  }
})();
