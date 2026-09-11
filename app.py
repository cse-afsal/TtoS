from flask import Flask, request, send_file, render_template_string, jsonify
from flask_cors import CORS
from gtts import gTTS
import io

app = Flask(__name__)
CORS(app)

LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-CN": "Chinese (Simplified)",
    "ar": "Arabic",
    "hi": "Hindi",
    "nl": "Dutch",
    "sv": "Swedish",
    "pl": "Polish",
    "tr": "Turkish",
}

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TtoS &mdash; Text to Speech</title>
  <meta name="description" content="Convert text to natural-sounding MP3 audio instantly. Supports 16 languages and multiple regional accents." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --white:     #ffffff;
      --bg:        #f9f9fb;
      --surface:   #f4f4f6;
      --border:    #e4e4e7;
      --border-2:  #d4d4d8;
      --ink:       #09090b;
      --sub:       #3f3f46;
      --muted:     #71717a;
      --ghost:     #a1a1aa;
      --accent:    #4f46e5;
      --accent-h:  #4338ca;
      --accent-lt: #eef2ff;
      --accent-bd: #c7d2fe;
      --red:       #dc2626;
      --red-lt:    #fef2f2;
      --red-bd:    #fecaca;
      --green:     #16a34a;
      --green-lt:  #f0fdf4;
      --green-bd:  #bbf7d0;
      --r-sm:  6px;
      --r-md: 10px;
      --r-lg: 14px;
    }

    html { scroll-behavior: smooth; }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--ink);
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    /* ── NAV ───────────────────────────────────────── */
    .nav {
      position: sticky; top: 0; z-index: 50;
      background: rgba(255,255,255,.9);
      backdrop-filter: blur(14px) saturate(180%);
      border-bottom: 1px solid var(--border);
    }
    .nav-inner {
      max-width: 1100px; margin: 0 auto;
      padding: 0 24px; height: 56px;
      display: flex; align-items: center; justify-content: space-between;
    }
    .brand {
      display: flex; align-items: center; gap: 9px;
      font-size: .95rem; font-weight: 700;
      color: var(--ink); text-decoration: none;
      letter-spacing: -.015em;
    }
    .brand-mark {
      width: 29px; height: 29px;
      background: var(--accent);
      border-radius: 7px;
      display: grid; place-items: center;
    }
    .brand-mark svg { width: 15px; height: 15px; fill: white; }
    .nav-badge {
      font-size: .71rem; font-weight: 600;
      color: var(--accent);
      background: var(--accent-lt);
      border: 1px solid var(--accent-bd);
      border-radius: 50px;
      padding: 3px 10px;
      letter-spacing: .02em;
    }

    /* ── HERO ──────────────────────────────────────── */
    .hero {
      max-width: 1100px; margin: 0 auto;
      padding: 72px 24px 52px;
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: 56px;
      align-items: center;
    }
    @media (max-width: 800px) {
      .hero { grid-template-columns: 1fr; gap: 36px; padding: 44px 20px 28px; }
      .hero-preview { display: none; }
    }

    .eyebrow {
      display: inline-flex; align-items: center; gap: 7px;
      font-size: .73rem; font-weight: 600; color: var(--accent);
      background: var(--accent-lt); border: 1px solid var(--accent-bd);
      border-radius: 50px; padding: 4px 12px;
      margin-bottom: 18px;
      letter-spacing: .04em; text-transform: uppercase;
    }
    .eyebrow-dot {
      width: 5px; height: 5px;
      background: var(--accent); border-radius: 50%;
      animation: blink 2.4s ease-in-out infinite;
    }
    @keyframes blink {
      0%, 100% { opacity: 1; }
      50%       { opacity: .3; }
    }

    h1 {
      font-size: clamp(2rem, 4vw, 2.9rem);
      font-weight: 800;
      line-height: 1.13;
      letter-spacing: -.03em;
      color: var(--ink);
      margin-bottom: 16px;
    }
    h1 .accent { color: var(--accent); }

    .hero-desc {
      font-size: .97rem;
      line-height: 1.72;
      color: var(--muted);
      margin-bottom: 28px;
      max-width: 400px;
    }

    .hero-meta {
      display: flex; flex-wrap: wrap; gap: 18px;
    }
    .meta-item {
      display: flex; align-items: center; gap: 6px;
      font-size: .8rem; font-weight: 500; color: var(--sub);
    }
    .meta-item svg { width: 13px; height: 13px; fill: var(--accent); flex-shrink: 0; }

    /* Hero preview card */
    .hero-preview {
      background: var(--white);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      padding: 22px;
      box-shadow: 0 2px 8px rgba(0,0,0,.05), 0 1px 2px rgba(0,0,0,.06);
    }
    .prev-label {
      font-size: .7rem; font-weight: 700;
      letter-spacing: .07em; text-transform: uppercase;
      color: var(--ghost); margin-bottom: 14px;
    }
    .prev-bars {
      display: flex; align-items: center; gap: 3px;
      height: 48px; margin-bottom: 16px;
    }
    .prev-bar {
      flex: 1; border-radius: 2px;
      background: var(--accent); opacity: .12;
      animation: pvwave 1.8s ease-in-out infinite;
    }
    .prev-bar.hi { opacity: .85; }
    @keyframes pvwave {
      0%,100% { transform: scaleY(.22); }
      50%      { transform: scaleY(1); }
    }
    .prev-meta {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 12px;
    }
    .prev-filename { font-size: .77rem; color: var(--muted); font-weight: 500; }
    .prev-pill {
      font-size: .69rem; font-weight: 600;
      background: var(--green-lt); color: var(--green);
      border: 1px solid var(--green-bd);
      border-radius: 50px; padding: 2px 9px;
    }
    .prev-tags {
      display: flex; flex-wrap: wrap; gap: 5px;
    }
    .prev-tag {
      font-size: .71rem; font-weight: 500;
      background: var(--surface); border: 1px solid var(--border);
      border-radius: var(--r-sm); padding: 3px 8px; color: var(--sub);
    }

    /* ── LAYOUT ────────────────────────────────────── */
    .page-body {
      max-width: 1100px; margin: 0 auto;
      padding: 0 24px 80px;
      display: grid;
      grid-template-columns: 1fr 320px;
      gap: 20px;
      align-items: start;
    }
    @media (max-width: 860px) {
      .page-body { grid-template-columns: 1fr; }
    }

    /* ── CARD ──────────────────────────────────────── */
    .card {
      background: var(--white);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      box-shadow: 0 1px 3px rgba(0,0,0,.04);
      overflow: hidden;
    }
    .card-head {
      padding: 18px 22px;
      border-bottom: 1px solid var(--border);
      display: flex; align-items: center; gap: 9px;
    }
    .card-dot {
      width: 7px; height: 7px;
      background: var(--accent); border-radius: 50%;
    }
    .card-heading {
      font-size: .88rem; font-weight: 600; color: var(--ink);
    }
    .card-body { padding: 22px; }

    /* ── FIELDS ────────────────────────────────────── */
    .field { margin-bottom: 18px; }

    .field-top {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 7px;
    }
    .flabel {
      font-size: .76rem; font-weight: 600;
      color: var(--sub); letter-spacing: .01em;
    }
    .char-pill {
      font-size: .7rem; font-weight: 600;
      color: var(--muted);
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 50px; padding: 2px 9px;
      font-variant-numeric: tabular-nums;
    }
    .char-pill.warn {
      background: var(--red-lt); border-color: var(--red-bd); color: var(--red);
    }

    textarea#text-input {
      width: 100%;
      min-height: 188px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--r-md);
      color: var(--ink);
      font-family: inherit;
      font-size: .91rem; line-height: 1.72;
      padding: 13px 15px;
      resize: vertical;
      outline: none;
      transition: border-color .14s, box-shadow .14s, background .14s;
    }
    textarea#text-input::placeholder { color: var(--ghost); }
    textarea#text-input:focus {
      background: var(--white);
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(79,70,229,.1);
    }

    /* ── SELECTS ───────────────────────────────────── */
    .field-pair {
      display: grid; grid-template-columns: 1fr 1fr;
      gap: 14px; margin-bottom: 18px;
    }
    @media (max-width: 460px) { .field-pair { grid-template-columns: 1fr; } }

    .field-pair .inner label {
      display: block;
      font-size: .76rem; font-weight: 600;
      color: var(--sub); margin-bottom: 7px;
    }
    select {
      width: 100%;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--r-md);
      color: var(--ink);
      font-family: inherit;
      font-size: .88rem; font-weight: 500;
      padding: 10px 34px 10px 13px;
      outline: none; cursor: pointer;
      appearance: none;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%2371717a' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 11px center;
      transition: border-color .14s, box-shadow .14s;
    }
    select:focus {
      background-color: var(--white);
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(79,70,229,.1);
    }
    select option { background: white; }

    /* ── SLOW MODE ─────────────────────────────────── */
    .option-row {
      display: flex; align-items: center; justify-content: space-between;
      padding: 12px 15px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--r-md);
      margin-bottom: 22px;
      cursor: pointer;
      transition: background .12s, border-color .12s;
      user-select: none;
    }
    .option-row:hover {
      background: var(--surface);
      border-color: var(--border-2);
    }
    .opt-text {}
    .opt-title { font-size: .86rem; font-weight: 600; color: var(--ink); }
    .opt-sub   { font-size: .74rem; color: var(--muted); margin-top: 1px; }

    .sw { position: relative; width: 38px; height: 21px; flex-shrink: 0; }
    .sw input { position: absolute; opacity: 0; }
    .sw-track {
      position: absolute; inset: 0;
      background: var(--border-2); border-radius: 21px;
      transition: background .18s;
    }
    .sw-thumb {
      position: absolute;
      width: 15px; height: 15px;
      background: white; border-radius: 50%;
      top: 3px; left: 3px;
      transition: transform .18s;
      box-shadow: 0 1px 2px rgba(0,0,0,.18);
    }
    .sw input:checked ~ .sw-track { background: var(--accent); }
    .sw input:checked ~ .sw-thumb { transform: translateX(17px); }

    /* ── BUTTON ────────────────────────────────────── */
    .btn {
      width: 100%;
      display: flex; align-items: center; justify-content: center; gap: 8px;
      padding: 12px 20px;
      background: var(--accent);
      color: white;
      font-family: inherit;
      font-size: .89rem; font-weight: 600;
      border: none; border-radius: var(--r-md);
      cursor: pointer; letter-spacing: -.01em;
      transition: background .14s, transform .1s, box-shadow .14s;
      box-shadow: 0 1px 3px rgba(79,70,229,.28), 0 4px 10px rgba(79,70,229,.18);
    }
    .btn:hover:not(:disabled) {
      background: var(--accent-h);
      transform: translateY(-1px);
      box-shadow: 0 2px 6px rgba(79,70,229,.3), 0 8px 18px rgba(79,70,229,.2);
    }
    .btn:active:not(:disabled) { transform: translateY(0); }
    .btn:disabled { opacity: .5; cursor: not-allowed; }
    .btn svg { width: 15px; height: 15px; fill: white; flex-shrink: 0; }

    .spinner {
      width: 16px; height: 16px;
      border: 2px solid rgba(255,255,255,.3);
      border-top-color: white;
      border-radius: 50%;
      animation: spin .6s linear infinite;
      display: none; flex-shrink: 0;
    }
    .btn.loading .spinner { display: block; }
    .btn.loading .btn-lbl  { display: none; }
    .btn.loading .btn-ico  { display: none; }
    @keyframes spin { to { transform: rotate(360deg); } }

    .hint {
      text-align: center; margin-top: 9px;
      font-size: .71rem; color: var(--ghost);
    }
    .hint kbd {
      display: inline-block;
      background: var(--surface);
      border: 1px solid var(--border-2);
      border-bottom-width: 2px;
      border-radius: 4px;
      padding: 1px 5px;
      font-family: inherit; font-size: .69rem;
      color: var(--sub); font-weight: 500;
    }

    /* ── PROCESSING ────────────────────────────────── */
    .proc {
      display: none; align-items: center; gap: 11px;
      margin-top: 14px;
      padding: 12px 15px;
      background: var(--accent-lt);
      border: 1px solid var(--accent-bd);
      border-radius: var(--r-md);
    }
    .proc.show { display: flex; }
    .proc-waves {
      display: flex; align-items: center; gap: 2.5px; flex-shrink: 0;
    }
    .pw {
      width: 3px; height: 14px;
      background: var(--accent); border-radius: 2px;
      animation: pwanim 1s ease-in-out infinite;
    }
    @keyframes pwanim {
      0%,100% { transform: scaleY(.3); }
      50%      { transform: scaleY(1); }
    }
    .proc-text { font-size: .81rem; font-weight: 500; color: var(--accent); }

    /* ── STATUS ────────────────────────────────────── */
    #msg {
      margin-top: 13px; padding: 11px 14px;
      border-radius: var(--r-md);
      font-size: .82rem; font-weight: 500;
      display: none; align-items: center; gap: 9px; line-height: 1.4;
    }
    #msg svg { width: 15px; height: 15px; fill: currentColor; flex-shrink: 0; }
    #msg.ok  { display: flex; background: var(--green-lt); border: 1px solid var(--green-bd); color: var(--green); }
    #msg.err { display: flex; background: var(--red-lt);   border: 1px solid var(--red-bd);   color: var(--red); }

    /* ── SIDEBAR ───────────────────────────────────── */
    .sidebar { display: flex; flex-direction: column; gap: 14px; }

    .scard {
      background: var(--white);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      padding: 18px 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,.04);
    }
    .scard-title {
      font-size: .71rem; font-weight: 700;
      letter-spacing: .07em; text-transform: uppercase;
      color: var(--ghost); margin-bottom: 14px;
    }

    /* Stats list */
    .stat-list { display: flex; flex-direction: column; }
    .stat-row {
      display: flex; align-items: center; justify-content: space-between;
      padding: 9px 0;
      border-bottom: 1px solid var(--border);
    }
    .stat-row:last-child { border: none; }
    .stat-name {
      display: flex; align-items: center; gap: 6px;
      font-size: .82rem; color: var(--sub);
    }
    .stat-name svg { width: 13px; height: 13px; fill: var(--ghost); }
    .stat-val { font-size: .82rem; font-weight: 700; color: var(--ink); }

    /* Steps */
    .steps { display: flex; flex-direction: column; gap: 13px; }
    .stp { display: flex; gap: 11px; align-items: flex-start; }
    .stp-num {
      width: 22px; height: 22px; flex-shrink: 0;
      background: var(--accent-lt); border: 1px solid var(--accent-bd);
      border-radius: 50%;
      display: grid; place-items: center;
      font-size: .69rem; font-weight: 700; color: var(--accent);
    }
    .stp-title { font-size: .83rem; font-weight: 600; color: var(--ink); margin-bottom: 2px; }
    .stp-desc  { font-size: .75rem; color: var(--muted); line-height: 1.5; }

    /* ── FOOTER ────────────────────────────────────── */
    .footer { border-top: 1px solid var(--border); }
    .footer-in {
      max-width: 1100px; margin: 0 auto; padding: 20px 24px;
      display: flex; align-items: center; justify-content: space-between;
      flex-wrap: wrap; gap: 10px;
    }
    .foot-brand {
      display: flex; align-items: center; gap: 8px;
      font-size: .8rem; font-weight: 600; color: var(--sub);
      text-decoration: none;
    }
    .foot-mark {
      width: 22px; height: 22px; background: var(--accent);
      border-radius: 5px; display: grid; place-items: center;
    }
    .foot-mark svg { width: 11px; height: 11px; fill: white; }
    .foot-copy { font-size: .77rem; color: var(--ghost); }
  </style>
</head>
<body>

<!-- Nav -->
<header class="nav">
  <div class="nav-inner">
    <a class="brand" href="#">
      <div class="brand-mark">
        <svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3m7 9c0 3.53-2.61 6.44-6 6.93V21h-2v-3.07c-3.39-.49-6-3.4-6-6.93h2a5 5 0 0 0 10 0h2z"/></svg>
      </div>
      TtoS
    </a>
    <div class="nav-badge">Free &amp; instant</div>
  </div>
</header>

<!-- Hero -->
<section class="hero">
  <div>
    <div class="eyebrow">
      <span class="eyebrow-dot"></span>
      Powered by Google TTS
    </div>
    <h1>Convert text into<br/><span class="accent">natural speech</span></h1>
    <p class="hero-desc">
      Paste any text, pick a language and accent, and download a clean MP3 file in seconds. No sign-up required.
    </p>
    <div class="hero-meta">
      <span class="meta-item">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
        16 languages
      </span>
      <span class="meta-item">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
        5 regional accents
      </span>
      <span class="meta-item">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
        Instant MP3 download
      </span>
    </div>
  </div>

  <!-- Decorative waveform preview -->
  <div class="hero-preview">
    <div class="prev-label">Audio output</div>
    <div class="prev-bars">
      <div class="prev-bar"    style="animation-delay:.00s"></div>
      <div class="prev-bar hi" style="animation-delay:.10s"></div>
      <div class="prev-bar hi" style="animation-delay:.20s"></div>
      <div class="prev-bar hi" style="animation-delay:.05s"></div>
      <div class="prev-bar hi" style="animation-delay:.35s"></div>
      <div class="prev-bar"    style="animation-delay:.15s"></div>
      <div class="prev-bar hi" style="animation-delay:.25s"></div>
      <div class="prev-bar hi" style="animation-delay:.45s"></div>
      <div class="prev-bar hi" style="animation-delay:.15s"></div>
      <div class="prev-bar"    style="animation-delay:.30s"></div>
      <div class="prev-bar hi" style="animation-delay:.20s"></div>
      <div class="prev-bar hi" style="animation-delay:.40s"></div>
      <div class="prev-bar hi" style="animation-delay:.10s"></div>
      <div class="prev-bar"    style="animation-delay:.05s"></div>
      <div class="prev-bar hi" style="animation-delay:.30s"></div>
      <div class="prev-bar hi" style="animation-delay:.50s"></div>
      <div class="prev-bar hi" style="animation-delay:.20s"></div>
      <div class="prev-bar"    style="animation-delay:.15s"></div>
    </div>
    <div class="prev-meta">
      <span class="prev-filename">ttos_speech.mp3</span>
      <span class="prev-pill">Ready</span>
    </div>
    <div class="prev-tags">
      <span class="prev-tag">English</span>
      <span class="prev-tag">Spanish</span>
      <span class="prev-tag">French</span>
      <span class="prev-tag">Hindi</span>
      <span class="prev-tag">Japanese</span>
      <span class="prev-tag">+11 more</span>
    </div>
  </div>
</section>

<!-- Page body -->
<div class="page-body">

  <!-- Form card -->
  <div class="card">
    <div class="card-head">
      <div class="card-dot"></div>
      <div class="card-heading">Speech Generator</div>
    </div>
    <div class="card-body">

      <!-- Textarea -->
      <div class="field">
        <div class="field-top">
          <label class="flabel" for="text-input">Text to convert</label>
          <span class="char-pill" id="char-count">0 / 5000</span>
        </div>
        <textarea id="text-input"
          placeholder="Enter or paste your text here..."
          maxlength="5000"
          spellcheck="true"></textarea>
      </div>

      <!-- Language + Accent -->
      <div class="field-pair">
        <div class="inner">
          <label for="lang-select">Language</label>
          <select id="lang-select">
            {% for code, name in languages.items() %}
            <option value="{{ code }}" {% if code == 'en' %}selected{% endif %}>{{ name }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="inner">
          <label for="tld-select">Accent</label>
          <select id="tld-select">
            <option value="com">United States</option>
            <option value="co.uk">United Kingdom</option>
            <option value="com.au">Australia</option>
            <option value="co.in">India</option>
            <option value="ca">Canada</option>
          </select>
        </div>
      </div>

      <!-- Slow mode -->
      <div class="option-row" onclick="document.getElementById('slow-toggle').click()">
        <div class="opt-text">
          <div class="opt-title">Slow speech</div>
          <div class="opt-sub">Reduces speed for clearer pronunciation</div>
        </div>
        <label class="sw" onclick="event.stopPropagation()">
          <input type="checkbox" id="slow-toggle" />
          <div class="sw-track"></div>
          <div class="sw-thumb"></div>
        </label>
      </div>

      <!-- Generate -->
      <button class="btn" id="generate-btn" onclick="generateSpeech()">
        <div class="spinner"></div>
        <svg class="btn-ico" viewBox="0 0 24 24"><path d="M12 15.5a3.5 3.5 0 0 1-3.5-3.5V6a3.5 3.5 0 0 1 7 0v6a3.5 3.5 0 0 1-3.5 3.5zm7-3.5c0 3.38-2.44 6.17-5.67 6.73L13 21h-2l-.33-2.27C7.44 18.17 5 15.38 5 12H7a5 5 0 0 0 10 0h2z"/></svg>
        <span class="btn-lbl">Generate &amp; Download MP3</span>
      </button>

      <p class="hint">Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to generate</p>

      <!-- Processing -->
      <div class="proc" id="proc">
        <div class="proc-waves">
          <div class="pw" style="animation-delay:0s"></div>
          <div class="pw" style="animation-delay:.15s"></div>
          <div class="pw" style="animation-delay:.30s"></div>
          <div class="pw" style="animation-delay:.15s"></div>
          <div class="pw" style="animation-delay:0s"></div>
        </div>
        <span class="proc-text">Generating audio&hellip;</span>
      </div>

      <!-- Status -->
      <div id="msg"></div>

    </div>
  </div>

  <!-- Sidebar -->
  <aside class="sidebar">

    <div class="scard">
      <div class="scard-title">Details</div>
      <div class="stat-list">
        <div class="stat-row">
          <span class="stat-name">
            <svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm6.93 6h-2.95c-.32-1.25-.78-2.45-1.38-3.56 1.84.63 3.37 1.9 4.33 3.56zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14C4.1 13.36 4 12.69 4 12s.1-1.36.26-2h3.38c-.08.66-.14 1.32-.14 2s.06 1.34.14 2H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56-1.84-.63-3.37-1.9-4.33-3.56zm2.95-8H5.08c.96-1.66 2.49-2.93 4.33-3.56C8.81 5.55 8.35 6.75 8.03 8zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96zM14.34 14H9.66c-.09-.66-.16-1.32-.16-2s.07-1.35.16-2h4.68c.09.65.16 1.32.16 2s-.07 1.34-.16 2zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95c-.96 1.66-2.49 2.93-4.33 3.56zM16.36 14c.08-.66.14-1.32.14-2s-.06-1.34-.14-2h3.38c.16.64.26 1.31.26 2s-.1 1.36-.26 2h-3.38z"/></svg>
            Languages
          </span>
          <span class="stat-val">16</span>
        </div>
        <div class="stat-row">
          <span class="stat-name">
            <svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3m7 9c0 3.53-2.61 6.44-6 6.93V21h-2v-3.07c-3.39-.49-6-3.4-6-6.93h2a5 5 0 0 0 10 0h2z"/></svg>
            Accents
          </span>
          <span class="stat-val">5</span>
        </div>
        <div class="stat-row">
          <span class="stat-name">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/></svg>
            Generation speed
          </span>
          <span class="stat-val">&lt; 5s</span>
        </div>
        <div class="stat-row">
          <span class="stat-name">
            <svg viewBox="0 0 24 24"><path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/></svg>
            Price
          </span>
          <span class="stat-val">Free</span>
        </div>
        <div class="stat-row">
          <span class="stat-name">
            <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
            Output format
          </span>
          <span class="stat-val">MP3</span>
        </div>
      </div>
    </div>

    <div class="scard">
      <div class="scard-title">How it works</div>
      <div class="steps">
        <div class="stp">
          <div class="stp-num">1</div>
          <div>
            <div class="stp-title">Enter your text</div>
            <div class="stp-desc">Paste up to 5,000 characters into the editor.</div>
          </div>
        </div>
        <div class="stp">
          <div class="stp-num">2</div>
          <div>
            <div class="stp-title">Configure voice</div>
            <div class="stp-desc">Choose language, regional accent, and speed.</div>
          </div>
        </div>
        <div class="stp">
          <div class="stp-num">3</div>
          <div>
            <div class="stp-title">Download MP3</div>
            <div class="stp-desc">Click Generate — your file downloads instantly.</div>
          </div>
        </div>
      </div>
    </div>

  </aside>
</div>

<!-- Footer -->
<footer class="footer">
  <div class="footer-in">
    <a class="foot-brand" href="#">
      <div class="foot-mark">
        <svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3m7 9c0 3.53-2.61 6.44-6 6.93V21h-2v-3.07c-3.39-.49-6-3.4-6-6.93h2a5 5 0 0 0 10 0h2z"/></svg>
      </div>
      TtoS
    </a>
    <p class="foot-copy">Built with Google Text-to-Speech &amp; Flask &nbsp;&middot;&nbsp; &copy; 2025</p>
  </div>
</footer>

<script>
  const ta  = document.getElementById('text-input');
  const pill = document.getElementById('char-count');

  ta.addEventListener('input', () => {
    const n = ta.value.length;
    pill.textContent = n + ' / 5000';
    pill.classList.toggle('warn', n > 4500);
  });

  async function generateSpeech() {
    const text = ta.value.trim();
    if (!text) { showMsg('err', 'Please enter some text first.'); return; }

    const lang = document.getElementById('lang-select').value;
    const tld  = document.getElementById('tld-select').value;
    const slow = document.getElementById('slow-toggle').checked;
    const btn  = document.getElementById('generate-btn');
    const proc = document.getElementById('proc');

    btn.disabled = true;
    btn.classList.add('loading');
    proc.classList.add('show');
    clearMsg();

    try {
      const res = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, lang, tld, slow })
      });

      if (!res.ok) { const e = await res.json(); throw new Error(e.error || 'Server error'); }

      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href = url; a.download = 'ttos_speech.mp3';
      document.body.appendChild(a); a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      showMsg('ok', 'Your MP3 file is downloading.');
    } catch (e) {
      showMsg('err', e.message);
    } finally {
      btn.disabled = false;
      btn.classList.remove('loading');
      proc.classList.remove('show');
    }
  }

  const ICON_OK  = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>';
  const ICON_ERR = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>';

  function showMsg(type, text) {
    const el = document.getElementById('msg');
    el.innerHTML = (type === 'ok' ? ICON_OK : ICON_ERR) + text;
    el.className = type;
  }
  function clearMsg() {
    const el = document.getElementById('msg');
    el.innerHTML = ''; el.className = '';
  }

  ta.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') generateSpeech();
  });
</script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML_PAGE, languages=LANGUAGES)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("text", "").strip()
    lang = data.get("lang", "en")
    tld  = data.get("tld", "com")
    slow = bool(data.get("slow", False))

    if not text:
        return jsonify({"error": "Text cannot be empty."}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text exceeds 5000 character limit."}), 400
    if lang not in LANGUAGES:
        return jsonify({"error": "Unsupported language."}), 400

    try:
        tts = gTTS(text=text, lang=lang, tld=tld, slow=slow)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return send_file(
            audio_buffer,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="ttos_speech.mp3"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
