'use strict';

const QUESTIONS = [
  {
    id: 'q1',
    label: "What's your first name?",
    type: 'text',
    placeholder: 'Jane',
    required: true,
    autocomplete: 'given-name',
  },
  {
    id: 'q2',
    label: 'And your last name?',
    type: 'text',
    placeholder: 'Doe',
    required: true,
    autocomplete: 'family-name',
  },
  {
    id: 'q3',
    label: "What's the best number to reach you?",
    type: 'tel',
    placeholder: '+1 (555) 000-0000',
    required: false,
    autocomplete: 'tel',
  },
  {
    id: 'q4',
    label: "What's your business called?",
    type: 'text',
    placeholder: 'Acme Inc.',
    required: true,
  },
  {
    id: 'q5',
    label: "What's your role or job title?",
    type: 'text',
    placeholder: 'Head of Growth',
    required: true,
  },
  {
    id: 'q6',
    label: 'Which industry are you in?',
    type: 'select',
    required: true,
    options: [
      'Technology / SaaS',
      'E-commerce / Retail',
      'Healthcare',
      'Finance / FinTech',
      'Education',
      'Marketing / Agency',
      'Other',
    ],
  },
  {
    id: 'q7',
    label: 'How large is your team?',
    type: 'select',
    required: true,
    options: ['Just me', '2–10', '11–50', '51–200', '201–1000', '1000+'],
  },
  {
    id: 'q8',
    label: 'How did you hear about us?',
    type: 'text',
    placeholder: 'A friend, Google, social media…',
    required: false,
  },
  {
    id: 'q9',
    label: "What's your biggest challenge right now?",
    type: 'textarea',
    placeholder: 'Tell us freely — the more detail the better.',
    required: true,
  },
  {
    id: 'q10',
    label: 'What are your primary goals with us?',
    type: 'textarea',
    placeholder: 'More leads, less churn, faster growth…',
    required: true,
  },
  {
    id: 'q11',
    label: 'When are you looking to get started?',
    type: 'date',
    required: false,
  },
  {
    id: 'q12',
    label: "Anything else you'd like us to know?",
    type: 'textarea',
    placeholder: "Go ahead — don't hold back.",
    required: false,
  },
];

const TOTAL = QUESTIONS.length;
let current = 0;
const answers = {};

// ── DOM Generation ────────────────────────────────────────────

function buildInput(q) {
  if (q.type === 'select') {
    const opts = q.options
      .map(o => `<option value="${o}">${o}</option>`)
      .join('');
    return `<select id="${q.id}" class="step-input step-select">
      <option value="">Choose one…</option>
      ${opts}
    </select>`;
  }

  if (q.type === 'textarea') {
    return `<textarea id="${q.id}" class="step-input step-textarea"
      placeholder="${q.placeholder ?? ''}"
    ></textarea>`;
  }

  return `<input id="${q.id}" class="step-input"
    type="${q.type}"
    placeholder="${q.placeholder ?? ''}"
    autocomplete="${q.autocomplete ?? 'off'}"
  />`;
}

function buildHint(q) {
  if (q.type === 'textarea') {
    return 'Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> or click Next';
  }
  if (q.type === 'select') {
    return 'Choose an option, then click Next';
  }
  return 'Press <kbd>Enter</kbd> ↵ or click Next';
}

function buildSteps() {
  const container = document.getElementById('form-container');

  QUESTIONS.forEach((q, i) => {
    const step = document.createElement('div');
    step.className = 'step';
    step.dataset.step = i;

    const optionalBadge = !q.required
      ? '<span class="step-optional">Optional</span>'
      : '';

    step.innerHTML = `
      <span class="step-counter">${i + 1} / ${TOTAL}</span>
      <label class="step-question" for="${q.id}">${q.label}${optionalBadge}</label>
      ${buildInput(q)}
      <p class="step-hint">${buildHint(q)}</p>
      <button class="btn-next" type="button">Next &rarr;</button>
      <p class="step-error" role="alert" aria-live="polite"></p>
    `;

    container.appendChild(step);
  });

  // Thank-you screen
  const ty = document.createElement('div');
  ty.className = 'step step--thankyou';
  ty.dataset.step = TOTAL;
  ty.innerHTML = `
    <div class="thankyou-icon">✓</div>
    <h1 class="thankyou-title">You're all set!</h1>
    <p class="thankyou-sub">Thanks for taking the time. We'll be in touch within one business day.</p>
    <button class="btn-restart" type="button">Start over</button>
  `;
  container.appendChild(ty);
}

// ── Navigation ────────────────────────────────────────────────

function allSteps() {
  return document.querySelectorAll('.step');
}

function goToStep(nextIndex) {
  const steps = allSteps();
  const outgoing = steps[current];

  outgoing.classList.remove('is-active');
  outgoing.classList.add('is-exiting');
  outgoing.addEventListener(
    'transitionend',
    () => outgoing.classList.remove('is-exiting'),
    { once: true }
  );

  current = nextIndex;
  steps[current].classList.add('is-active');

  // Focus input after slide-in starts
  setTimeout(() => {
    const input = steps[current].querySelector('.step-input');
    if (input) input.focus();
  }, 80);

  updateProgress();
}

function updateProgress() {
  // +1 in numerator so step 1 shows a visible sliver; TOTAL+1 keeps 100% for thank-you screen
  const pct = ((current + 1) / (TOTAL + 1)) * 100;
  document.getElementById('progress-bar-fill').style.width = pct + '%';
}

// ── Validation ────────────────────────────────────────────────

function validate(stepIndex) {
  const q = QUESTIONS[stepIndex];
  if (!q) return true;

  const input = document.getElementById(q.id);
  const errorEl = input.closest('.step').querySelector('.step-error');
  const val = input.value.trim();

  if (q.required && !val) {
    showError(input, errorEl, 'This field is required — please fill it in.');
    return false;
  }

  if (q.type === 'tel' && val && !/^[\d\s+\-().]{7,}$/.test(val)) {
    showError(input, errorEl, 'Please enter a valid phone number.');
    return false;
  }

  errorEl.textContent = '';
  answers[q.id] = val;
  return true;
}

function showError(input, errorEl, message) {
  errorEl.textContent = message;
  input.classList.add('shake');
  input.addEventListener('animationend', () => input.classList.remove('shake'), { once: true });
  input.focus();
}

// ── Advance ───────────────────────────────────────────────────

function tryAdvance() {
  if (current >= TOTAL) return;
  if (!validate(current)) return;
  goToStep(current + 1);
}

// ── Reset ─────────────────────────────────────────────────────

function resetForm() {
  Object.keys(answers).forEach(k => delete answers[k]);

  document.querySelectorAll('.step-input').forEach(el => {
    if (el.tagName === 'SELECT') el.selectedIndex = 0;
    else el.value = '';
  });

  document.querySelectorAll('.step-error').forEach(el => {
    el.textContent = '';
  });

  goToStep(0);
}

// ── Event Listeners ───────────────────────────────────────────

document.addEventListener('keydown', e => {
  if (e.key !== 'Enter') return;

  const focused = document.activeElement;

  if (focused && focused.tagName === 'TEXTAREA') {
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault();
      tryAdvance();
    }
    // plain Enter in textarea → newline (default)
    return;
  }

  // Let the browser handle Enter natively for selects (open/confirm dropdown)
  if (focused && focused.tagName === 'SELECT') return;

  e.preventDefault();
  tryAdvance();
});

document.getElementById('form-container').addEventListener('click', e => {
  if (e.target.matches('.btn-next'))    tryAdvance();
  if (e.target.matches('.btn-restart')) resetForm();
});

// ── Init ──────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  buildSteps();

  const steps = allSteps();
  steps[0].classList.add('is-active');
  updateProgress();

  setTimeout(() => {
    const input = steps[0].querySelector('.step-input');
    if (input) input.focus();
  }, 80);
});
