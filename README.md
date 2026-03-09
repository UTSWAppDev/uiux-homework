# UI/UX Principles in Healthcare Application Development

## Overview

This exercise demonstrates four principles of good UI/UX design using a Flask web
application that provides **cardiovascular disease (CVD) risk calculators**:

- **ASCVD Calculator** — Pooled Cohort Equations (ACC/AHA 2013), for patients aged 40–79
- **PREVENT Calculator** — AHA 2023 PREVENT Equations, for patients aged 30–79

The application is fully functional when you receive it, but it has **no visual styling**.
Your task is to progressively apply CSS to improve the user experience by following the
four steps below.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Installation

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the application:**

   ```bash
   flask --app app run --debug
   ```

3. **Open your browser** and navigate to `http://127.0.0.1:5000`

Take a moment to click through the application.  Notice that it is functional but
difficult to use — the forms are hard to read, navigation is not obvious, and the
results are not visually distinct.  Over the next four steps you will fix this.

> **All CSS changes are made in `static/css/style.css`.**
> Add each step's CSS to the file and refresh your browser to see the changes.

---

## Step 1 — User-Centered Design: Accessibility and High Contrast

### What Is User-Centered Design?

User-centered design (UCD) means building software around the real needs of the
people who use it.  For healthcare applications this is critical because:

- Users may be under stress and need information to be unambiguous
- Errors in data entry can have clinical consequences
- Many users rely on assistive technology (screen readers, keyboard navigation)
- Regulatory standards such as Section 508 and the ADA may apply

### Web Content Accessibility Guidelines (WCAG)

The WCAG 2.1 AA standard provides the minimum accessibility bar for most healthcare
software.  The most important rules for forms are:

| Rule | Requirement |
|------|-------------|
| **Contrast (1.4.3)** | Body text must have a contrast ratio of at least **4.5:1** against its background. |
| **Labels (1.3.1)** | Every form input must have an associated `<label>`. |
| **Focus Indicator (2.4.7)** | Keyboard-focused elements must have a visible outline. |
| **Font Size** | Body text should be at least **16px** (browser default is 16px, but many sites override it downward — don't). |

### What to Add

Copy the CSS below and paste it at the top of `static/css/style.css`, then refresh
your browser.

```css
/* ============================================================
   STEP 1 — USER-CENTERED DESIGN
   Goal: high contrast, readable forms, keyboard accessibility
   ============================================================ */

/* 1a. Box-sizing reset so padding doesn't break widths */
*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* 1b. Base body — dark text on white background (contrast ratio > 7:1) */
body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #1a1a1a;
    background-color: #ffffff;
}

/* 1c. Make labels clearly visible and associated with each input */
label,
legend {
    display: block;
    font-weight: bold;
    margin-bottom: 4px;
    color: #1a1a1a;
}

/* 1d. Large, high-contrast input fields */
input[type="number"],
input[type="text"],
select,
textarea {
    width: 100%;
    padding: 10px 12px;
    font-size: 16px;
    border: 2px solid #444444;
    border-radius: 4px;
    background-color: #ffffff;
    color: #1a1a1a;
}

/* 1e. Visible keyboard focus indicator (3:1 contrast against focus ring color) */
input:focus,
select:focus,
textarea:focus,
button:focus,
a:focus {
    outline: 3px solid #005fcc;
    outline-offset: 2px;
}

/* 1f. Group each label+input together with consistent spacing */
.form-group {
    margin-bottom: 24px;
}

/* 1g. Radio buttons inside fieldsets */
fieldset {
    border: 1px solid #888;
    padding: 12px 16px;
    border-radius: 4px;
}

.radio-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: normal;
    margin-top: 8px;
    cursor: pointer;
}

/* 1h. Required field asterisk is red */
.required-mark {
    color: #cc0000;
    margin-left: 2px;
}

/* 1i. Hint text under inputs */
.field-hint,
.optional-label {
    display: block;
    font-size: 14px;
    color: #444444;
    margin-top: 4px;
}

/* 1j. Error messages — high contrast red */
.error-message {
    background-color: #fce4e4;
    border: 2px solid #b30000;
    color: #6e0000;
    padding: 12px 16px;
    border-radius: 4px;
    margin-bottom: 20px;
}

/* 1k. Result box — dark border for clear visual separation */
.result-box {
    border: 2px solid #1a1a1a;
    padding: 24px;
    border-radius: 4px;
    background-color: #f5f5f5;
    margin-top: 24px;
}
```

### What You Should See

After saving and refreshing:

- The page text is dark on a white background — easy to read
- Every form input has a thick border that clearly separates it from the background
- Pressing **Tab** to move between form fields shows a bright blue outline around the
  focused element
- Required-field asterisks are red
- The error box (try submitting age 85) is clearly red and distinct

---

## Step 2 — Consistency: Navigation, Headers, Footers, and Buttons

### What Is Consistency?

Consistency means that similar elements look and behave the same way throughout the
application.  When users learn that a blue, bold link opens a calculator on one page,
they expect it to do the same on every page.  Inconsistency forces users to
re-learn the interface and increases errors.

Three design tools support consistency:

1. **CSS variables (custom properties)** — define your color palette once and reuse it
2. **A shared base template** — `templates/base.html` already provides a shared `<nav>`,
   `<header>`, and `<footer>` for every page
3. **Utility classes** — `btn`, `btn-primary`, `btn-secondary` are already in the HTML;
   you only need to style them once

### What to Add

Add the CSS below **after** the Step 1 CSS in `static/css/style.css`.

```css
/* ============================================================
   STEP 2 — CONSISTENCY
   Goal: shared color palette, navigation, header, footer,
         and consistent link/button styling
   ============================================================ */

/* 2a. Color palette — define once, use everywhere */
:root {
    --color-primary:      #003366;   /* UTSW dark blue */
    --color-primary-dark: #001f3f;
    --color-accent:       #0056b3;
    --color-white:        #ffffff;
    --color-light-bg:     #f0f4f8;
    --color-border:       #cccccc;
    --color-success-bg:   #d4edda;
    --color-success-text: #155724;
    --color-warning-bg:   #fff3cd;
    --color-warning-text: #856404;
    --color-danger-bg:    #f8d7da;
    --color-danger-text:  #721c24;
}

/* 2b. Consistent navigation bar */
nav {
    background-color: var(--color-primary);
    padding: 0 20px;
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 14px 0;
}

.nav-brand {
    color: var(--color-white);
    font-size: 1.2rem;
    font-weight: bold;
    text-decoration: none;
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 24px;
    margin: 0;
    padding: 0;
}

.nav-links a {
    color: var(--color-white);
    text-decoration: none;
    font-weight: 500;
}

/* 2c. Consistent header */
header {
    background-color: var(--color-primary);
    color: var(--color-white);
    padding: 40px 20px;
}

.header-container {
    max-width: 1200px;
    margin: 0 auto;
}

header h1 {
    font-size: 2rem;
    margin-bottom: 6px;
}

header p {
    font-size: 1rem;
    opacity: 0.9;
}

/* 2d. Consistent footer */
footer {
    background-color: var(--color-primary);
    color: var(--color-white);
    padding: 24px 20px;
    margin-top: 48px;
}

.footer-container {
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
}

footer p {
    margin: 4px 0;
    font-size: 0.9rem;
    opacity: 0.9;
}

/* 2e. Consistent link styling (outside the nav) */
a {
    color: var(--color-accent);
    text-decoration: underline;
}

/* 2f. Consistent button styling — same shape and padding everywhere */
.btn {
    display: inline-block;
    padding: 10px 24px;
    font-size: 16px;
    font-weight: bold;
    text-align: center;
    text-decoration: none;
    border: 2px solid transparent;
    border-radius: 4px;
    line-height: 1.4;
}

.btn-primary {
    background-color: var(--color-accent);
    color: var(--color-white);
    border-color: var(--color-accent);
}

.btn-secondary {
    background-color: transparent;
    color: var(--color-primary);
    border-color: var(--color-primary);
}
```

### What You Should See

After saving and refreshing, all three pages — Home, ASCVD, and PREVENT — share the
same dark-blue navigation bar, the same header treatment, and the same footer.
The "Calculate" and "Clear Form" buttons look the same on both calculator pages.

---

## Step 3 — Hierarchy: Typography, Layout, and Visual Emphasis

### What Is Visual Hierarchy?

Visual hierarchy guides the user's eye toward the most important content first.
It answers the question: *"What should I look at first?"*

The primary tools are:

- **Font size** — bigger text is seen first
- **Font weight** — bold text stands out
- **Color** — saturated or contrasting color draws attention
- **Whitespace** — spacing separates groups of content and creates breathing room
- **Layout** — cards, grids, and boxes group related content and separate sections

### What to Add

Add the CSS below **after** the Step 2 CSS.

```css
/* ============================================================
   STEP 3 — HIERARCHY
   Goal: clear typography scale, page layout, emphasis on
         important actions and risk results
   ============================================================ */

/* 3a. Main content area — centered, max-width container */
.main-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
}

/* 3b. Typography scale — each heading level clearly smaller than the last */
h1 { font-size: 2.25rem; font-weight: 700; }

h2 {
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--color-primary);
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid var(--color-accent);
}

h3 {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--color-primary);
    margin-bottom: 10px;
}

p { margin-bottom: 12px; }

ul, ol {
    margin-left: 24px;
    margin-bottom: 12px;
}

/* 3c. Section spacing */
section {
    margin-bottom: 48px;
}

/* 3d. Calculator cards on the home page — side-by-side grid */
.calculator-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    margin-top: 20px;
}

.calculator-card {
    background-color: var(--color-white);
    border: 1px solid var(--color-border);
    border-radius: 8px;
    padding: 28px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.calculator-card h3 {
    font-size: 1.3rem;
    border-bottom: 2px solid var(--color-accent);
    padding-bottom: 10px;
    margin-bottom: 14px;
}

/* 3e. Primary call-to-action button — larger than secondary to create emphasis */
.btn-primary {
    font-size: 1.05rem;
    padding: 12px 28px;
    margin-top: 16px;
}

/* 3f. Form actions row */
.form-actions {
    display: flex;
    gap: 16px;
    align-items: center;
    margin-top: 8px;
}

/* 3g. Result box — risk value is large and color-coded */
.result-risk-value {
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.result-category {
    font-size: 1.1rem;
    margin-bottom: 12px;
}

/* Color-code risk levels so the severity is immediately obvious */
.risk-high {
    color: var(--color-danger-text);
}

.risk-intermediate {
    color: var(--color-warning-text);
}

.risk-low {
    color: var(--color-success-text);
}

/* 3h. Disclaimer/reference sections — de-emphasize with smaller text and lighter bg */
.disclaimer-section,
.references-section {
    background-color: var(--color-light-bg);
    border-left: 4px solid var(--color-border);
    padding: 20px 24px;
    border-radius: 0 4px 4px 0;
}

.disclaimer-section h2,
.references-section h2 {
    font-size: 1.1rem;
    border-bottom: none;
    padding-bottom: 0;
}

.disclaimer-section p,
.references-section li {
    font-size: 0.9rem;
    color: #444444;
}
```

### What You Should See

After saving and refreshing:

- The Home page shows two calculator cards side by side
- Headings are clearly larger than body text, with a blue underline on `<h2>`
- The "Open … Calculator" buttons are larger and more prominent than the "Clear Form"
  button — guiding the user toward the primary action
- Risk results are color-coded: red for High, amber for Intermediate, green for Low
- The Disclaimer and References sections are visually subdued, signalling lower priority

---

## Step 4 — Communication: Hover Effects, Cursor Changes, and Transitions

### What Is Visual Communication?

Visual communication is the application's way of talking to the user without words.
Hover effects, cursor changes, and transitions give users real-time feedback about:

- **What is clickable** — the `pointer` cursor signals "you can click this"
- **What is focused** — outline styles tell keyboard users where they are
- **What is happening** — transitions make state changes feel smooth rather than jarring
- **What is disabled** — a `not-allowed` cursor communicates "this is not available"

These details take only a few lines of CSS but significantly improve usability.

### What to Add

Add the CSS below **after** the Step 3 CSS.

```css
/* ============================================================
   STEP 4 — COMMUNICATION WITH THE USER
   Goal: cursor changes, hover effects, smooth transitions
   ============================================================ */

/* 4a. Pointer cursor on everything clickable */
a,
button,
.btn,
input[type="submit"],
input[type="button"],
input[type="radio"],
input[type="checkbox"],
select,
label[for],
.radio-label {
    cursor: pointer;
}

/* 4b. Not-allowed cursor on disabled elements */
input:disabled,
select:disabled,
button:disabled,
.btn:disabled {
    cursor: not-allowed;
    opacity: 0.55;
}

/* 4c. Smooth transitions on elements that change appearance */
a,
.btn,
button,
.nav-links a,
.calculator-card,
.nav-brand,
input[type="number"],
input[type="text"],
select {
    transition: all 0.2s ease;
}

/* 4d. Nav links highlight on hover */
.nav-links a:hover,
.nav-brand:hover {
    background-color: rgba(255, 255, 255, 0.15);
    padding: 4px 8px;
    border-radius: 4px;
}

/* 4e. Primary button lifts slightly on hover */
.btn-primary:hover {
    background-color: var(--color-primary-dark);
    border-color: var(--color-primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* 4f. Secondary button fills on hover */
.btn-secondary:hover {
    background-color: var(--color-primary);
    color: var(--color-white);
}

/* 4g. Calculator cards raise on hover */
.calculator-card:hover {
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    transform: translateY(-3px);
}

/* 4h. Input glow on focus (reinforces Step 1 outline) */
input:focus,
select:focus {
    border-color: var(--color-accent);
    box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.25);
}

/* 4i. Active (clicked) state for buttons — sinks back to give press feedback */
.btn:active {
    transform: translateY(0);
    box-shadow: none;
}
```

### What You Should See

After saving and refreshing:

- Moving your mouse over a navigation link highlights it with a subtle white glow
- Hovering over the "Open … Calculator" buttons causes them to lift off the page
- Hovering over the calculator cards on the Home page also lifts them slightly
- Clicking a button causes it to press down (the `translateY(0)` in `:active`)
- Moving your mouse over a form field's label shows a pointer cursor — confirming it is
  interactive when you hover over its associated input via `label[for]`

---

## Summary

You have now applied four fundamental UI/UX principles to a healthcare web application:

| Step | Principle | Key Techniques |
|------|-----------|----------------|
| 1 | **User-Centered Design** | High contrast (dark text / white bg), visible focus rings, large inputs, accessible labels |
| 2 | **Consistency** | CSS variables, shared nav/header/footer, uniform button styles |
| 3 | **Hierarchy** | Typography scale, card layout, color-coded risk results, de-emphasized secondary content |
| 4 | **Communication** | Pointer cursor, hover lift/glow effects, smooth transitions, active press feedback |

These principles apply to virtually every healthcare application you will build or
evaluate during your career in health informatics.

---

## Reference

- Goff DC Jr, et al. 2013 ACC/AHA Guideline on the Assessment of Cardiovascular Risk.
  *J Am Coll Cardiol.* 2014;63(25 Pt B):2935–2959.
- Khan SS, et al. Development and Validation of the American Heart Association's PREVENT
  Equations. *Circulation.* 2024;149:430–449.
- [Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/TR/WCAG21/)
- [MDN Web Docs — CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
