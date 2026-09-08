# QA Agent

`scripts/qa_agent.py` is the project’s executable end-to-end QA agent. It
translates the highest-risk flows in `TEST_CASES.md` into repeatable Playwright
browser checks.

It verifies:

- initial rendering, progress, labels, and optional indicators;
- required-field and telephone validation;
- keyboard behavior for inputs and textareas;
- select-field validation and navigation;
- the complete submission journey, progress state, and restart reset; and
- the mobile full-width primary-action layout.

Run it from the repository root:

```bash
python3 scripts/qa_agent.py
```

The agent starts and stops its own server on an available loopback port, so it
does not require `python3 -m http.server 8080` to be running. It runs headless
by default; add `--headed` to watch the browser.

To test an already deployed instance instead, point it at that instance:

```bash
QA_BASE_URL=https://your-form.example python3 scripts/qa_agent.py
```

Each test method records the corresponding IDs from `docs/TEST_CASES.md` in
its docstring, which keeps the test-plan and executable suite traceable.
