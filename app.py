"""
DigiWorkers Platform - Complete Full Stack App
===============================================
Flask Backend + HTML Frontend + Razorpay Payment
All in ONE file!

SETUP:
  pip install flask flask-cors requests
  python app.py
  Open: http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3, json, datetime, os, secrets, requests

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(32)

DB_PATH = "digiworkers.db"

# ── Razorpay Keys (apni keys yahan daalein) ──────────────
RAZORPAY_KEY_ID     = "rzp_test_YourKeyHere"
RAZORPAY_KEY_SECRET = "YourSecretHere"
# ─────────────────────────────────────────────────────────

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DigiWorkers — India's Digital Services Platform</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Nunito:wght@300;400;500;600&display=swap" rel="stylesheet">
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:#06090f;--bg2:#0c1220;--bg3:#111b2e;
  --card:#131d30;--card2:#192338;
  --brand:#2563eb;--brand2:#3b82f6;--brand3:#1d4ed8;
  --gold:#f59e0b;--gold2:#fbbf24;
  --green:#10b981;--red:#ef4444;
  --text:#e2e8f0;--muted:#64748b;--soft:#94a3b8;
  --border:rgba(255,255,255,0.06);--border2:rgba(255,255,255,0.12);
  --radius:12px;--radius2:16px;--radius3:20px;
}
html{scroll-behavior:smooth;}
body{font-family:'Nunito',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden;}

/* scrollbar */
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--brand);border-radius:10px;}

/* ── NAV ── */
nav{position:fixed;top:0;left:0;right:0;z-index:1000;padding:0 2rem;height:64px;display:flex;align-items:center;justify-content:space-between;background:rgba(6,9,15,0.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);}
.logo{font-family:'Syne',sans-serif;font-weight:800;font-size:1.35rem;color:#fff;display:flex;align-items:center;gap:8px;cursor:pointer;}
.logo-dot{width:8px;height:8px;background:var(--gold);border-radius:50%;display:inline-block;}
.nav-links{display:flex;gap:0.25rem;align-items:center;}
.nav-link{padding:0.45rem 0.9rem;border-radius:8px;color:var(--soft);font-size:0.88rem;font-weight:500;cursor:pointer;transition:all 0.2s;border:none;background:none;}
.nav-link:hover,.nav-link.active{background:rgba(37,99,235,0.15);color:var(--brand2);}
.nav-cta{background:var(--brand);color:#fff;padding:0.45rem 1.1rem;border-radius:8px;font-size:0.88rem;font-weight:600;cursor:pointer;border:none;font-family:'Nunito',sans-serif;transition:all 0.2s;}
.nav-cta:hover{background:var(--brand3);transform:translateY(-1px);}

/* ── PAGES ── */
.page{display:none;padding-top:64px;min-height:100vh;animation:fadeIn 0.3s ease;}
.page.active{display:block;}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);}}

/* ── HERO ── */
.hero{padding:5rem 2rem 3rem;text-align:center;position:relative;}
.hero-glow{position:absolute;top:0;left:50%;transform:translateX(-50%);width:700px;height:350px;background:radial-gradient(ellipse,rgba(37,99,235,0.12) 0%,transparent 70%);pointer-events:none;}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.25);color:var(--gold);padding:0.4rem 1rem;border-radius:30px;font-size:0.8rem;font-weight:600;margin-bottom:1.5rem;}
.hero h1{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(2.2rem,5.5vw,3.6rem);line-height:1.08;color:#fff;margin-bottom:1.2rem;}
.hero h1 em{font-style:normal;background:linear-gradient(135deg,var(--brand2),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{color:var(--soft);font-size:1.05rem;max-width:540px;margin:0 auto 2.5rem;line-height:1.75;}
.hero-btns{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;}
.btn-primary{background:var(--brand);color:#fff;padding:0.8rem 2rem;border-radius:var(--radius);font-weight:600;cursor:pointer;border:none;font-family:'Nunito',sans-serif;font-size:0.95rem;transition:all 0.2s;}
.btn-primary:hover{background:var(--brand3);transform:translateY(-2px);box-shadow:0 8px 25px rgba(37,99,235,0.3);}
.btn-ghost{background:rgba(255,255,255,0.05);color:var(--text);padding:0.8rem 2rem;border-radius:var(--radius);font-weight:600;cursor:pointer;border:1px solid var(--border2);font-family:'Nunito',sans-serif;font-size:0.95rem;transition:all 0.2s;}
.btn-ghost:hover{background:rgba(255,255,255,0.08);}

/* ── STATS BAR ── */
.stats-bar{display:flex;justify-content:center;gap:0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);background:var(--bg2);}
.stat-item{flex:1;max-width:200px;text-align:center;padding:1.5rem 1rem;border-right:1px solid var(--border);}
.stat-item:last-child{border-right:none;}
.stat-num{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:#fff;}
.stat-num span{color:var(--gold);}
.stat-lbl{font-size:0.78rem;color:var(--muted);margin-top:0.2rem;font-weight:500;}

/* ── SECTION ── */
.section{padding:3rem 2rem;max-width:1200px;margin:0 auto;}
.sec-head{margin-bottom:2rem;}
.sec-title{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:700;color:#fff;margin-bottom:0.4rem;}
.sec-sub{color:var(--muted);font-size:0.9rem;}

/* ── CATEGORY TABS ── */
.cat-tabs{display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;}
.cat-tab{padding:0.45rem 1rem;border-radius:30px;font-size:0.82rem;font-weight:600;cursor:pointer;border:1px solid var(--border2);background:transparent;color:var(--soft);transition:all 0.2s;font-family:'Nunito',sans-serif;}
.cat-tab:hover{border-color:var(--brand2);color:var(--brand2);}
.cat-tab.active{background:var(--brand);border-color:var(--brand);color:#fff;}

/* ── SERVICE CARDS ── */
.services-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:1rem;}
.svc-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius2);padding:1.3rem;cursor:pointer;transition:all 0.22s;position:relative;overflow:hidden;}
.svc-card::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(37,99,235,0.04),transparent);opacity:0;transition:opacity 0.2s;}
.svc-card:hover{border-color:rgba(59,130,246,0.4);transform:translateY(-3px);box-shadow:0 12px 35px rgba(0,0,0,0.4);}
.svc-card:hover::before{opacity:1;}
.svc-icon{width:44px;height:44px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;margin-bottom:1rem;}
.svc-tag{position:absolute;top:12px;right:12px;font-size:0.65rem;font-weight:700;padding:3px 8px;border-radius:6px;letter-spacing:0.5px;}
.tag-hot{background:rgba(239,68,68,0.15);color:#f87171;}
.tag-new{background:rgba(16,185,129,0.15);color:#34d399;}
.tag-pop{background:rgba(245,158,11,0.15);color:var(--gold2);}
.svc-name{font-weight:600;font-size:0.92rem;color:#fff;margin-bottom:0.4rem;}
.svc-desc{font-size:0.78rem;color:var(--muted);margin-bottom:0.8rem;line-height:1.5;}
.svc-footer{display:flex;justify-content:space-between;align-items:center;}
.svc-price{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:var(--gold);}
.svc-time{font-size:0.72rem;color:var(--muted);}

/* ── ORDER MODAL ── */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:2000;display:none;align-items:center;justify-content:center;padding:1rem;}
.modal-overlay.open{display:flex;}
.modal{background:var(--bg3);border:1px solid var(--border2);border-radius:var(--radius3);width:100%;max-width:500px;max-height:90vh;overflow-y:auto;animation:slideUp 0.3s ease;}
@keyframes slideUp{from{opacity:0;transform:translateY(20px);}to{opacity:1;transform:translateY(0);}}
.modal-head{padding:1.5rem 1.5rem 0;display:flex;justify-content:space-between;align-items:flex-start;}
.modal-title{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#fff;}
.modal-close{background:rgba(255,255,255,0.08);border:none;color:var(--soft);width:32px;height:32px;border-radius:8px;cursor:pointer;font-size:1rem;display:flex;align-items:center;justify-content:center;}
.modal-body{padding:1.5rem;}
.svc-summary{background:var(--card);border-radius:var(--radius);padding:1rem;margin-bottom:1.2rem;display:flex;justify-content:space-between;align-items:center;}
.svc-sum-name{font-weight:600;font-size:0.9rem;color:#fff;}
.svc-sum-time{font-size:0.75rem;color:var(--muted);margin-top:2px;}
.svc-sum-price{font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;color:var(--gold);}

/* ── FORMS ── */
.form-group{margin-bottom:1rem;}
.form-label{display:block;font-size:0.82rem;font-weight:600;color:var(--soft);margin-bottom:0.4rem;letter-spacing:0.3px;}
.form-input{width:100%;background:var(--card);border:1px solid var(--border2);border-radius:var(--radius);padding:0.7rem 0.9rem;color:var(--text);font-family:'Nunito',sans-serif;font-size:0.9rem;transition:border-color 0.2s;}
.form-input:focus{outline:none;border-color:var(--brand2);}
.form-input::placeholder{color:var(--muted);}
select.form-input option{background:var(--bg3);}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;}
.form-textarea{resize:vertical;min-height:80px;}

/* priority selector */
.priority-btns{display:flex;gap:0.5rem;}
.pri-btn{flex:1;padding:0.55rem;border-radius:8px;border:1px solid var(--border2);background:transparent;color:var(--soft);font-size:0.8rem;font-weight:600;cursor:pointer;font-family:'Nunito',sans-serif;transition:all 0.2s;text-align:center;}
.pri-btn:hover{border-color:var(--brand2);}
.pri-btn.active{border-color:var(--brand);background:rgba(37,99,235,0.15);color:var(--brand2);}
.pri-btn.active.urgent{border-color:var(--gold);background:rgba(245,158,11,0.1);color:var(--gold);}
.pri-btn.active.express{border-color:var(--red);background:rgba(239,68,68,0.1);color:#f87171;}

.price-preview{background:linear-gradient(135deg,rgba(37,99,235,0.1),rgba(245,158,11,0.05));border:1px solid rgba(37,99,235,0.2);border-radius:var(--radius);padding:1rem;margin:1rem 0;display:flex;justify-content:space-between;align-items:center;}
.price-label{font-size:0.82rem;color:var(--soft);}
.price-final{font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:var(--gold);}
.btn-pay{width:100%;background:linear-gradient(135deg,var(--brand),var(--brand3));color:#fff;padding:0.85rem;border-radius:var(--radius);font-weight:700;cursor:pointer;border:none;font-family:'Nunito',sans-serif;font-size:1rem;transition:all 0.2s;margin-top:0.5rem;}
.btn-pay:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(37,99,235,0.35);}
.btn-pay:disabled{opacity:0.5;cursor:not-allowed;transform:none;}

/* ── WORKERS PAGE ── */
.workers-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;}
.worker-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius2);padding:1.3rem;transition:all 0.2s;}
.worker-card:hover{border-color:var(--border2);transform:translateY(-2px);}
.worker-top{display:flex;align-items:center;gap:12px;margin-bottom:1rem;}
.worker-av{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:800;font-size:0.9rem;flex-shrink:0;}
.worker-name{font-weight:600;font-size:0.95rem;color:#fff;}
.worker-skill{font-size:0.78rem;color:var(--muted);margin-top:2px;}
.worker-stats{display:flex;gap:0.5rem;margin-bottom:1rem;}
.w-stat{flex:1;background:var(--bg2);border-radius:8px;padding:0.6rem;text-align:center;}
.w-stat-val{font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#fff;}
.w-stat-lbl{font-size:0.68rem;color:var(--muted);margin-top:1px;}
.status-badge{display:inline-flex;align-items:center;gap:5px;font-size:0.75rem;font-weight:600;padding:4px 10px;border-radius:20px;}
.badge-avail{background:rgba(16,185,129,0.12);color:#34d399;}
.badge-busy{background:rgba(245,158,11,0.12);color:var(--gold2);}
.badge-offline{background:rgba(100,116,139,0.2);color:var(--muted);}

/* worker join form */
.join-card{background:var(--card);border:1px solid var(--border2);border-radius:var(--radius2);padding:1.5rem;max-width:600px;}

/* ── DASHBOARD ── */
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:2rem;}
.metric-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius2);padding:1.2rem;position:relative;overflow:hidden;}
.metric-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;}
.metric-card.blue::after{background:var(--brand);}
.metric-card.gold::after{background:var(--gold);}
.metric-card.green::after{background:var(--green);}
.metric-card.red::after{background:var(--red);}
.metric-lbl{font-size:0.75rem;color:var(--muted);font-weight:600;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:0.6rem;}
.metric-val{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:#fff;}
.metric-change{font-size:0.75rem;margin-top:0.3rem;}
.up{color:var(--green);}
.warn{color:var(--gold);}

/* orders table */
.table-wrap{background:var(--card);border:1px solid var(--border);border-radius:var(--radius2);overflow:hidden;}
.table-head{padding:1rem 1.2rem;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;}
.table-title{font-family:'Syne',sans-serif;font-weight:700;font-size:0.95rem;color:#fff;}
table{width:100%;border-collapse:collapse;}
th{padding:0.75rem 1rem;text-align:left;font-size:0.75rem;font-weight:700;color:var(--muted);letter-spacing:0.5px;text-transform:uppercase;border-bottom:1px solid var(--border);}
td{padding:0.8rem 1rem;font-size:0.85rem;color:var(--soft);border-bottom:1px solid var(--border);}
tr:last-child td{border-bottom:none;}
tr:hover td{background:rgba(255,255,255,0.02);}
.status-pill{display:inline-flex;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;}
.pill-done{background:rgba(16,185,129,0.12);color:#34d399;}
.pill-pending{background:rgba(245,158,11,0.12);color:var(--gold2);}
.pill-assigned{background:rgba(37,99,235,0.12);color:var(--brand2);}
.pill-cancelled{background:rgba(239,68,68,0.12);color:#f87171;}

/* top services */
.top-svc-list{display:flex;flex-direction:column;gap:0.6rem;}
.top-svc-item{display:flex;align-items:center;gap:12px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:0.8rem 1rem;}
.top-svc-rank{font-family:'Syne',sans-serif;font-size:0.85rem;font-weight:800;color:var(--muted);width:20px;}
.top-svc-name{flex:1;font-size:0.88rem;color:#fff;font-weight:500;}
.top-svc-rev{font-family:'Syne',sans-serif;font-size:0.9rem;font-weight:700;color:var(--gold);}
.top-svc-bar{height:4px;background:var(--bg);border-radius:2px;margin-top:4px;overflow:hidden;}
.top-svc-fill{height:100%;background:linear-gradient(90deg,var(--brand),var(--gold));border-radius:2px;}

/* ── PRICING ── */
.pricing-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.2rem;}
.plan-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius2);padding:1.8rem;transition:all 0.2s;position:relative;}
.plan-card.featured{border-color:rgba(37,99,235,0.5);background:linear-gradient(135deg,rgba(37,99,235,0.08),var(--card));}
.plan-badge{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--brand);color:#fff;font-size:0.72rem;font-weight:700;padding:4px 14px;border-radius:20px;white-space:nowrap;letter-spacing:0.5px;}
.plan-name{font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;color:#fff;margin-bottom:0.5rem;}
.plan-price{font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;color:var(--gold);margin:0.5rem 0;}
.plan-price small{font-size:0.9rem;color:var(--muted);font-family:'Nunito',sans-serif;font-weight:400;}
.plan-features{list-style:none;margin:1.2rem 0;}
.plan-features li{font-size:0.83rem;color:var(--soft);padding:0.4rem 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;}
.plan-features li::before{content:'';width:6px;height:6px;background:var(--green);border-radius:50%;flex-shrink:0;}

/* split display */
.split-display{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:2rem;}
.split-box{border-radius:var(--radius2);padding:1.5rem;text-align:center;}
.split-pct{font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;margin-bottom:0.4rem;}
.split-lbl{font-size:0.8rem;font-weight:600;}

/* ── TOAST ── */
.toast{position:fixed;bottom:2rem;right:2rem;z-index:9999;padding:1rem 1.5rem;border-radius:var(--radius);font-size:0.88rem;font-weight:600;transform:translateY(100px);opacity:0;transition:all 0.3s;max-width:320px;}
.toast.show{transform:translateY(0);opacity:1;}
.toast.success{background:#065f46;border:1px solid #10b981;color:#d1fae5;}
.toast.error{background:#7f1d1d;border:1px solid #ef4444;color:#fee2e2;}
.toast.info{background:#1e3a5f;border:1px solid var(--brand);color:#bfdbfe;}

/* ── FOOTER ── */
footer{border-top:1px solid var(--border);padding:2rem;text-align:center;color:var(--muted);font-size:0.82rem;}
footer span{color:var(--gold);}

/* ── LOADING ── */
.spinner{display:inline-block;width:18px;height:18px;border:2px solid rgba(255,255,255,0.3);border-top-color:#fff;border-radius:50%;animation:spin 0.7s linear infinite;}
@keyframes spin{to{transform:rotate(360deg);}}

/* responsive */
@media(max-width:640px){
  .nav-links{display:none;}
  .form-row{grid-template-columns:1fr;}
  .split-display{grid-template-columns:1fr;}
  .stats-bar{flex-wrap:wrap;}
}
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <div class="logo" onclick="showPage('home')">
    <span class="logo-dot"></span>DigiWorkers
  </div>
  <div class="nav-links">
    <button class="nav-link active" onclick="showPage('home')">Home</button>
    <button class="nav-link" onclick="showPage('services')">Services</button>
    <button class="nav-link" onclick="showPage('workers')">Workers</button>
    <button class="nav-link" onclick="showPage('pricing')">Pricing</button>
    <button class="nav-link" onclick="showPage('dashboard')">Dashboard</button>
  </div>
  <button class="nav-cta" onclick="showPage('services')">Order Now →</button>
</nav>

<!-- ═══════════ HOME ═══════════ -->
<div id="page-home" class="page active">
  <div class="hero">
    <div class="hero-glow"></div>
    <div class="hero-badge">🇮🇳 India's #1 Micro Digital Services Platform</div>
    <h1>100+ Digital Services<br><em>On Demand. Delivered Fast.</em></h1>
    <p class="hero-sub">Facebook ads, YouTube scripts, GST invoices, PPT, Excel fixes — sab kuch ek jagah. AI-powered workers se 2–3× fast delivery.</p>
    <div class="hero-btns">
      <button class="btn-primary" onclick="showPage('services')">Browse Services</button>
      <button class="btn-ghost" onclick="showPage('workers')">Become a Worker</button>
    </div>
  </div>

  <div class="stats-bar">
    <div class="stat-item"><div class="stat-num">100<span>+</span></div><div class="stat-lbl">Digital Services</div></div>
    <div class="stat-item"><div class="stat-num" id="stat-workers">0</div><div class="stat-lbl">Verified Workers</div></div>
    <div class="stat-item"><div class="stat-num" id="stat-orders">0</div><div class="stat-lbl">Orders Completed</div></div>
    <div class="stat-item"><div class="stat-num">2–3<span>×</span></div><div class="stat-lbl">AI Productivity</div></div>
    <div class="stat-item"><div class="stat-num">70<span>%</span></div><div class="stat-lbl">Worker Earnings</div></div>
  </div>

  <div class="section">
    <div class="sec-head">
      <div class="sec-title">Popular Services</div>
      <div class="sec-sub">Chote businesses, YouTubers, students — sab ke liye</div>
    </div>
    <div class="services-grid" id="home-services-grid"></div>
  </div>

  <!-- HOW IT WORKS -->
  <div style="background:var(--bg2);padding:3rem 2rem;border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
    <div style="max-width:900px;margin:0 auto;">
      <div class="sec-head" style="text-align:center;">
        <div class="sec-title">Kaise Kaam Karta Hai?</div>
        <div class="sec-sub">3 simple steps mein order complete</div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.5rem;margin-top:1rem;">
        <div style="text-align:center;padding:1.5rem;">
          <div style="width:56px;height:56px;background:rgba(37,99,235,0.15);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin:0 auto 1rem;">📋</div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;color:#fff;margin-bottom:0.4rem;">1. Service Chunein</div>
          <div style="font-size:0.82rem;color:var(--muted);line-height:1.6;">100+ services mein se apni zaroorat ka kaam select karein</div>
        </div>
        <div style="text-align:center;padding:1.5rem;">
          <div style="width:56px;height:56px;background:rgba(245,158,11,0.15);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin:0 auto 1rem;">💳</div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;color:#fff;margin-bottom:0.4rem;">2. Payment Karein</div>
          <div style="font-size:0.82rem;color:var(--muted);line-height:1.6;">Secure Razorpay se UPI, card, netbanking se pay karein</div>
        </div>
        <div style="text-align:center;padding:1.5rem;">
          <div style="width:56px;height:56px;background:rgba(16,185,129,0.15);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin:0 auto 1rem;">✅</div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;color:#fff;margin-bottom:0.4rem;">3. Kaam Ready</div>
          <div style="font-size:0.82rem;color:var(--muted);line-height:1.6;">AI-powered worker fast delivery time mein kaam deliver karega</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════ SERVICES ═══════════ -->
<div id="page-services" class="page">
  <div class="section">
    <div class="sec-head">
      <div class="sec-title">All Services</div>
      <div class="sec-sub">Category chunein aur order place karein</div>
    </div>
    <div class="cat-tabs" id="cat-tabs">
      <button class="cat-tab active" onclick="filterCat(this,'all')">🔥 All</button>
      <button class="cat-tab" onclick="filterCat(this,'social')">📱 Social Media</button>
      <button class="cat-tab" onclick="filterCat(this,'content')">🎬 Content</button>
      <button class="cat-tab" onclick="filterCat(this,'business')">💼 Business</button>
      <button class="cat-tab" onclick="filterCat(this,'tech')">🔧 Tech</button>
    </div>
    <div class="services-grid" id="all-services-grid"></div>
  </div>
</div>

<!-- ═══════════ WORKERS ═══════════ -->
<div id="page-workers" class="page">
  <div class="section">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:start;">
      <div>
        <div class="sec-head">
          <div class="sec-title">Active Workers</div>
          <div class="sec-sub">AI se productivity badhao, 70–80% kamaao</div>
        </div>
        <div class="workers-grid" id="workers-list" style="grid-template-columns:1fr;"></div>
      </div>
      <div>
        <div class="sec-head">
          <div class="sec-title">Worker ke roop mein Join karein</div>
          <div class="sec-sub">Apni skills se ghar baithe kamaao</div>
        </div>
        <div class="join-card">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Full Name</label>
              <input class="form-input" id="w-name" placeholder="Aapka naam" type="text">
            </div>
            <div class="form-group">
              <label class="form-label">WhatsApp Number</label>
              <input class="form-input" id="w-phone" placeholder="9876543210" type="text">
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Primary Skill</label>
            <select class="form-input" id="w-skill">
              <option value="Social Media & Copywriting">Social Media & Copywriting</option>
              <option value="Content & Video">Content & Video</option>
              <option value="Design & Thumbnail">Design & Thumbnail</option>
              <option value="Excel & Data">Excel & Data</option>
              <option value="Web & Tech Support">Web & Tech Support</option>
              <option value="Business Documents">Business Documents</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Experience (Brief)</label>
            <textarea class="form-input form-textarea" id="w-exp" placeholder="Apna experience likhein..."></textarea>
          </div>
          <button class="btn-primary" style="width:100%;" onclick="applyWorker()">Apply as Worker →</button>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════ PRICING ═══════════ -->
<div id="page-pricing" class="page">
  <div class="section">
    <div class="sec-head" style="text-align:center;">
      <div class="sec-title">Simple, Transparent Pricing</div>
      <div class="sec-sub">Clients ke liye — koi hidden charges nahi</div>
    </div>
    <div class="pricing-grid">
      <div class="plan-card">
        <div class="plan-name">Starter</div>
        <div class="plan-price">₹149 <small>/ service</small></div>
        <ul class="plan-features">
          <li>Basic digital tasks</li>
          <li>Normal delivery (2–6 hrs)</li>
          <li>WhatsApp support</li>
          <li>1 revision included</li>
        </ul>
        <button class="btn-ghost" style="width:100%;" onclick="showPage('services')">Browse Services</button>
      </div>
      <div class="plan-card featured">
        <div class="plan-badge">⭐ MOST POPULAR</div>
        <div class="plan-name">Professional</div>
        <div class="plan-price">₹299 <small>/ service</small></div>
        <ul class="plan-features">
          <li>All premium services</li>
          <li>Priority delivery</li>
          <li>24/7 WhatsApp support</li>
          <li>3 revisions included</li>
          <li>AI-enhanced output</li>
        </ul>
        <button class="btn-primary" style="width:100%;" onclick="showPage('services')">Order Now →</button>
      </div>
      <div class="plan-card">
        <div class="plan-name">Business Bundle</div>
        <div class="plan-price">₹1,999 <small>/ month</small></div>
        <ul class="plan-features">
          <li>10 services per month</li>
          <li>Dedicated worker assigned</li>
          <li>Express delivery</li>
          <li>Unlimited revisions</li>
          <li>GST invoice included</li>
          <li>Priority queue</li>
        </ul>
        <button class="btn-ghost" style="width:100%;" onclick="showToast('info','Team se contact karein: digiworkers@gmail.com')">Contact Us</button>
      </div>
    </div>

    <div style="margin-top:3rem;">
      <div class="sec-title" style="text-align:center;margin-bottom:0.5rem;">Worker Revenue Split</div>
      <div class="sec-sub" style="text-align:center;margin-bottom:1.5rem;">Fair & Transparent — AI productivity se 2–3x zyada kamaao</div>
      <div class="split-display">
        <div class="split-box" style="background:rgba(37,99,235,0.1);border:1px solid rgba(37,99,235,0.2);">
          <div class="split-pct" style="color:var(--brand2);">25%</div>
          <div class="split-lbl" style="color:var(--brand2);">Platform Commission</div>
          <div style="font-size:0.75rem;color:var(--muted);margin-top:0.5rem;">Infrastructure, support, marketing</div>
        </div>
        <div class="split-box" style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);">
          <div class="split-pct" style="color:var(--green);">75%</div>
          <div class="split-lbl" style="color:var(--green);">Worker Earnings</div>
          <div style="font-size:0.75rem;color:var(--muted);margin-top:0.5rem;">Direct payment every week</div>
        </div>
        <div class="split-box" style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.2);">
          <div class="split-pct" style="color:var(--gold);">2–3×</div>
          <div class="split-lbl" style="color:var(--gold);">AI Productivity</div>
          <div style="font-size:0.75rem;color:var(--muted);margin-top:0.5rem;">More tasks, more income</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════ DASHBOARD ═══════════ -->
<div id="page-dashboard" class="page">
  <div class="section">
    <div class="sec-head" style="display:flex;justify-content:space-between;align-items:center;">
      <div>
        <div class="sec-title">Admin Dashboard</div>
        <div class="sec-sub">Business performance — live data</div>
      </div>
      <button class="btn-ghost" style="font-size:0.82rem;padding:0.5rem 1rem;" onclick="loadDashboard()">↻ Refresh</button>
    </div>

    <div class="metrics-grid" id="metrics-grid">
      <div class="metric-card blue"><div class="metric-lbl">Total Revenue</div><div class="metric-val" id="m-revenue">—</div><div class="metric-change up" id="m-rev-sub"></div></div>
      <div class="metric-card gold"><div class="metric-lbl">Platform Earnings</div><div class="metric-val" id="m-platform">—</div><div class="metric-change up">Net profit</div></div>
      <div class="metric-card green"><div class="metric-lbl">Active Orders</div><div class="metric-val" id="m-active">—</div><div class="metric-change up" id="m-act-sub"></div></div>
      <div class="metric-card red"><div class="metric-lbl">Total Workers</div><div class="metric-val" id="m-workers">—</div><div class="metric-change warn" id="m-wkr-sub"></div></div>
    </div>

    <div style="display:grid;grid-template-columns:2fr 1fr;gap:1.5rem;align-items:start;">
      <div class="table-wrap">
        <div class="table-head">
          <div class="table-title">Recent Orders</div>
          <div style="display:flex;gap:0.5rem;">
            <select class="form-input" style="width:auto;font-size:0.8rem;padding:0.3rem 0.6rem;" id="order-filter" onchange="loadOrders()">
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="assigned">Assigned</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>
        <div style="overflow-x:auto;">
          <table>
            <thead><tr>
              <th>Order #</th><th>Client</th><th>Service</th><th>Amount</th><th>Worker</th><th>Status</th><th>Action</th>
            </tr></thead>
            <tbody id="orders-tbody"><tr><td colspan="7" style="text-align:center;color:var(--muted);padding:2rem;">Loading...</td></tr></tbody>
          </table>
        </div>
      </div>

      <div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.95rem;color:#fff;margin-bottom:1rem;">Top Services</div>
        <div class="top-svc-list" id="top-services"></div>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════ ORDER MODAL ═══════════ -->
<div class="modal-overlay" id="order-modal">
  <div class="modal">
    <div class="modal-head">
      <div>
        <div class="modal-title" id="modal-svc-name">Place Order</div>
        <div style="font-size:0.78rem;color:var(--muted);margin-top:3px;" id="modal-svc-time"></div>
      </div>
      <button class="modal-close" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-body">
      <div class="svc-summary">
        <div>
          <div class="svc-sum-name" id="sum-name">—</div>
          <div class="svc-sum-time" id="sum-time">—</div>
        </div>
        <div class="svc-sum-price" id="sum-base-price">—</div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Your Name</label>
          <input class="form-input" id="o-name" placeholder="Rahul Sharma" type="text">
        </div>
        <div class="form-group">
          <label class="form-label">WhatsApp Number</label>
          <input class="form-input" id="o-phone" placeholder="9876543210" type="text">
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Requirements</label>
        <textarea class="form-input form-textarea" id="o-req" placeholder="Aapki zaroorat detail mein likhein..."></textarea>
      </div>

      <div class="form-group">
        <label class="form-label">Priority</label>
        <div class="priority-btns">
          <button class="pri-btn active" onclick="setPriority(this,'normal')">Normal</button>
          <button class="pri-btn urgent" onclick="setPriority(this,'urgent')">Urgent +50%</button>
          <button class="pri-btn express" onclick="setPriority(this,'express')">Express +100%</button>
        </div>
      </div>

      <div class="price-preview">
        <div>
          <div class="price-label">Total Amount</div>
          <div style="font-size:0.75rem;color:var(--muted);margin-top:2px;">Razorpay secure payment</div>
        </div>
        <div class="price-final" id="final-price">₹0</div>
      </div>

      <button class="btn-pay" id="pay-btn" onclick="initiatePayment()">
        💳 Pay & Place Order
      </button>
    </div>
  </div>
</div>

<!-- TOAST -->
<div class="toast" id="toast"></div>

<footer>
  © 2026 DigiWorkers — India's Digital Micro-Services Platform &nbsp;|&nbsp;
  Made with <span>♥</span> in India &nbsp;|&nbsp;
  Powered by Razorpay
</footer>

<script>
const API = '';  // same origin
let currentService = null;
let currentPriority = 'normal';
let allServices = [];

// ── Page Navigation ──────────────────────────
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
  document.getElementById('page-' + id).classList.add('active');
  const links = document.querySelectorAll('.nav-link');
  links.forEach(l => { if(l.textContent.toLowerCase().includes(id.substring(0,4))) l.classList.add('active'); });
  window.scrollTo(0, 0);
  if(id === 'dashboard') { loadDashboard(); loadOrders(); }
  if(id === 'workers') loadWorkers();
  if(id === 'home') loadHomeServices();
  if(id === 'services') loadAllServices();
}

// ── Toast ────────────────────────────────────
function showToast(type, msg) {
  const t = document.getElementById('toast');
  t.className = 'toast ' + type;
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3500);
}

// ── Service Card HTML ────────────────────────
const icons = {social:'📢',content:'🎬',business:'💼',tech:'🔧'};
const tags  = {hot:'<span class="svc-tag tag-hot">HOT</span>',
               new:'<span class="svc-tag tag-new">NEW</span>',
               pop:'<span class="svc-tag tag-pop">POPULAR</span>'};
const tagMap = {1:'hot',2:'pop',3:'new',4:'pop',5:'hot',6:'pop',7:'hot',8:'new',9:'new',10:'pop'};

function svcCardHTML(s, onclick='') {
  const icon = icons[s.category] || '⚡';
  const tagKey = tagMap[s.id] || '';
  const tagHTML = tagKey ? tags[tagKey] : '';
  const bg = {social:'rgba(37,99,235,0.12)',content:'rgba(239,68,68,0.12)',business:'rgba(16,185,129,0.12)',tech:'rgba(155,89,182,0.12)'}[s.category]||'rgba(37,99,235,0.12)';
  const safeData = encodeURIComponent(JSON.stringify(s));
  const clickHandler = onclick || `openOrderById('${safeData}')`;
  return `<div class="svc-card" onclick="${clickHandler}">
    <div class="svc-icon" style="background:${bg}">${icon}</div>
    ${tagHTML}
    <div class="svc-name">${s.name}</div>
    <div class="svc-desc">${s.description||''}</div>
    <div class="svc-footer">
      <div class="svc-price">₹${s.price}</div>
      <div class="svc-time">⏱ ${s.delivery_hours}h delivery</div>
    </div>
  </div>`;
}

function openOrderById(encoded) {
  try {
    const svc = JSON.parse(decodeURIComponent(encoded));
    openOrder(svc);
  } catch(e) {
    console.error('Parse error:', e);
  }
}

// ── Load Home Services ───────────────────────
async function loadHomeServices() {
  const resp = await fetch(API+'/api/services');
  const svcs = await resp.json();
  allServices = svcs;
  const grid = document.getElementById('home-services-grid');
  grid.innerHTML = svcs.slice(0,6).map(s => svcCardHTML(s)).join('');
}

// ── Load All Services ────────────────────────
async function loadAllServices() {
  if(!allServices.length) {
    const resp = await fetch(API+'/api/services');
    allServices = await resp.json();
  }
  renderServicesGrid(allServices);
}

function renderServicesGrid(svcs) {
  document.getElementById('all-services-grid').innerHTML = svcs.map(s => svcCardHTML(s)).join('');
}

function filterCat(el, cat) {
  document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  const filtered = cat === 'all' ? allServices : allServices.filter(s => s.category === cat);
  renderServicesGrid(filtered);
}

// ── Order Modal ──────────────────────────────
function openOrder(svc) {
  if(typeof svc === 'string') svc = JSON.parse(svc);
  currentService = svc;
  currentPriority = 'normal';
  document.getElementById('modal-svc-name').textContent = svc.name;
  document.getElementById('modal-svc-time').textContent = `Delivery: ${svc.delivery_hours} hours`;
  document.getElementById('sum-name').textContent = svc.name;
  document.getElementById('sum-time').textContent = `${svc.delivery_hours} hrs delivery`;
  document.getElementById('sum-base-price').textContent = '₹' + svc.price;
  document.getElementById('o-name').value = '';
  document.getElementById('o-phone').value = '';
  document.getElementById('o-req').value = '';
  document.querySelectorAll('.pri-btn').forEach(b => b.classList.remove('active'));
  document.querySelector('.pri-btn').classList.add('active');
  updateFinalPrice();
  document.getElementById('order-modal').classList.add('open');
}

function closeModal() {
  document.getElementById('order-modal').classList.remove('open');
}

function setPriority(el, val) {
  currentPriority = val;
  document.querySelectorAll('.pri-btn').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  updateFinalPrice();
}

function updateFinalPrice() {
  if(!currentService) return;
  const mult = {normal:1, urgent:1.5, express:2}[currentPriority];
  const final = Math.round(currentService.price * mult);
  document.getElementById('final-price').textContent = '₹' + final;
}

// ── Razorpay Payment ─────────────────────────
async function initiatePayment() {
  const name = document.getElementById('o-name').value.trim();
  const phone = document.getElementById('o-phone').value.trim();
  const req = document.getElementById('o-req').value.trim();
  if(!name || !phone || !req) { showToast('error','Saare fields fill karein!'); return; }
  if(!/^[6-9]\\d{9}$/.test(phone)) { showToast('error','Valid 10-digit WhatsApp number daalein'); return; }

  const btn = document.getElementById('pay-btn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Processing...';

  try {
    const mult = {normal:1, urgent:1.5, express:2}[currentPriority];
    const amount = Math.round(currentService.price * mult);

    // Create Razorpay order
    const resp = await fetch(API+'/api/payment/create-order', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({amount, service_id: currentService.id})
    });
    const data = await resp.json();

    if(data.error) throw new Error(data.error);

    const options = {
      key: data.key_id,
      amount: data.amount,
      currency: 'INR',
      name: 'DigiWorkers',
      description: currentService.name,
      order_id: data.razorpay_order_id,
      handler: async function(response) {
        // Verify & place order
        const orderResp = await fetch(API+'/api/orders', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({
            client_name: name,
            client_phone: phone,
            service_id: currentService.id,
            requirements: req,
            priority: currentPriority,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_order_id: response.razorpay_order_id,
            razorpay_signature: response.razorpay_signature
          })
        });
        const orderData = await orderResp.json();
        closeModal();
        showToast('success','✅ Order placed! #'+orderData.order_number+' — Worker 30 min mein contact karega!');
      },
      prefill: { name, contact: phone },
      theme: { color: '#2563eb' },
      modal: { ondismiss: function(){ btn.disabled=false; btn.innerHTML='💳 Pay & Place Order'; } }
    };
    new Razorpay(options).open();
  } catch(e) {
    showToast('error', 'Payment error: ' + e.message);
    btn.disabled = false;
    btn.innerHTML = '💳 Pay & Place Order';
  }
}

// ── Workers ──────────────────────────────────
async function loadWorkers() {
  const resp = await fetch(API+'/api/workers');
  const workers = await resp.json();
  const colors = ['rgba(37,99,235,0.2)','rgba(16,185,129,0.2)','rgba(245,158,11,0.2)','rgba(239,68,68,0.2)','rgba(155,89,182,0.2)'];
  const tcolors= ['#60a5fa','#34d399','#fbbf24','#f87171','#c084fc'];
  document.getElementById('workers-list').innerHTML = workers.length ? workers.map((w,i)=>{
    const initials = w.name.split(' ').map(n=>n[0]).join('').substring(0,2).toUpperCase();
    const badge = w.status==='available'?'badge-avail':w.status==='busy'?'badge-busy':'badge-offline';
    const bLabel = {available:'✓ Available',busy:'⏳ On Task',offline:'○ Offline'}[w.status]||w.status;
    return `<div class="worker-card">
      <div class="worker-top">
        <div class="worker-av" style="background:${colors[i%5]};color:${tcolors[i%5]}">${initials}</div>
        <div>
          <div class="worker-name">${w.name}</div>
          <div class="worker-skill">${w.skills}</div>
        </div>
      </div>
      <div class="worker-stats">
        <div class="w-stat"><div class="w-stat-val">₹${(w.total_earned||0).toLocaleString()}</div><div class="w-stat-lbl">Earned</div></div>
        <div class="w-stat"><div class="w-stat-val">${w.rating||5.0}</div><div class="w-stat-lbl">Rating</div></div>
      </div>
      <span class="status-badge ${badge}">${bLabel}</span>
    </div>`;
  }).join('') : '<div style="color:var(--muted);padding:1rem;">Abhi koi worker nahi. Pehle apply karein!</div>';

  // update stat
  document.getElementById('stat-workers').textContent = workers.length || 0;
}

async function applyWorker() {
  const name = document.getElementById('w-name').value.trim();
  const phone = document.getElementById('w-phone').value.trim();
  const skills = document.getElementById('w-skill').value;
  if(!name||!phone) { showToast('error','Name aur phone required hai!'); return; }
  const resp = await fetch(API+'/api/workers/apply',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({name,phone,skills,experience:document.getElementById('w-exp').value})
  });
  const data = await resp.json();
  if(resp.ok){ showToast('success','Application submit! 24 hrs mein contact karenge.'); document.getElementById('w-name').value=''; document.getElementById('w-phone').value=''; loadWorkers(); }
  else showToast('error', data.error||'Error!');
}

// ── Dashboard ────────────────────────────────
async function loadDashboard() {
  const resp = await fetch(API+'/api/dashboard');
  const d = await resp.json();
  document.getElementById('m-revenue').textContent = '₹'+((d.total_revenue||0).toLocaleString());
  document.getElementById('m-platform').textContent = '₹'+((d.platform_earnings||0).toLocaleString());
  document.getElementById('m-active').textContent = d.active_orders||0;
  document.getElementById('m-act-sub').textContent = (d.completed_orders||0)+' completed total';
  document.getElementById('m-workers').textContent = d.total_workers||0;
  document.getElementById('m-wkr-sub').textContent = (d.available_workers||0)+' available now';

  const ts = document.getElementById('top-services');
  if(d.top_services && d.top_services.length) {
    const max = d.top_services[0].revenue||1;
    ts.innerHTML = d.top_services.map((s,i)=>`
      <div class="top-svc-item">
        <div class="top-svc-rank">#${i+1}</div>
        <div style="flex:1">
          <div class="top-svc-name">${s.name}</div>
          <div class="top-svc-bar"><div class="top-svc-fill" style="width:${Math.round((s.revenue/max)*100)}%"></div></div>
        </div>
        <div class="top-svc-rev">₹${(s.revenue||0).toLocaleString()}</div>
      </div>`).join('');
  } else {
    ts.innerHTML = '<div style="color:var(--muted);font-size:0.85rem;padding:1rem;">Abhi koi completed order nahi.</div>';
  }
}

async function loadOrders() {
  const status = document.getElementById('order-filter').value;
  const url = API+'/api/orders'+(status?'?status='+status:'');
  const resp = await fetch(url);
  const orders = await resp.json();
  const pillClass = {completed:'pill-done',pending:'pill-pending',assigned:'pill-assigned',cancelled:'pill-cancelled'};
  const tbody = document.getElementById('orders-tbody');
  tbody.innerHTML = orders.length ? orders.map(o=>`
    <tr>
      <td style="color:#fff;font-weight:600;">${o.order_number}</td>
      <td>${o.client_name}</td>
      <td>${o.service_name||'—'}</td>
      <td style="color:var(--gold);font-weight:600;">₹${o.amount}</td>
      <td>${o.worker_name||'<span style="color:var(--muted)">Assigning...</span>'}</td>
      <td><span class="status-pill ${pillClass[o.status]||''}">${o.status}</span></td>
      <td>${o.status==='assigned'?`<button onclick="completeOrder('${o.order_number}')" style="font-size:0.75rem;padding:3px 10px;border-radius:6px;background:rgba(16,185,129,0.15);color:#34d399;border:none;cursor:pointer;font-family:'Nunito',sans-serif;">✓ Complete</button>`:'—'}</td>
    </tr>`).join('')
  : '<tr><td colspan="7" style="text-align:center;color:var(--muted);padding:2rem;">Koi orders nahi milae.</td></tr>';

  document.getElementById('stat-orders').textContent = orders.filter(o=>o.status==='completed').length;
}

async function completeOrder(num) {
  const resp = await fetch(API+'/api/orders/'+num+'/complete',{method:'PATCH'});
  if(resp.ok){ showToast('success','Order completed!'); loadOrders(); loadDashboard(); }
  else showToast('error','Error completing order');
}

// close modal on overlay click
document.getElementById('order-modal').addEventListener('click', function(e){
  if(e.target===this) closeModal();
});

// ── Init ─────────────────────────────────────
loadHomeServices();
</script>
</body>
</html>"""


# ──────────────────────────────────────────────
# DB SETUP
# ──────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, category TEXT NOT NULL,
        price INTEGER NOT NULL, delivery_hours INTEGER NOT NULL,
        description TEXT, is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, phone TEXT UNIQUE NOT NULL,
        skills TEXT NOT NULL, experience TEXT,
        status TEXT DEFAULT 'available',
        total_earned INTEGER DEFAULT 0,
        rating REAL DEFAULT 5.0,
        joined_at TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        client_name TEXT NOT NULL, client_phone TEXT NOT NULL,
        service_id INTEGER NOT NULL, worker_id INTEGER,
        requirements TEXT, priority TEXT DEFAULT 'normal',
        amount INTEGER NOT NULL, platform_cut INTEGER NOT NULL,
        worker_earn INTEGER NOT NULL,
        razorpay_payment_id TEXT, razorpay_order_id TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT (datetime('now')),
        completed_at TEXT,
        FOREIGN KEY(service_id) REFERENCES services(id),
        FOREIGN KEY(worker_id) REFERENCES workers(id)
    );
    """)

    cur.execute("SELECT COUNT(*) as c FROM services")
    if cur.fetchone()["c"] == 0:
        svcs = [
            ("Facebook Ads Copy",    "social",   299,  2,  "Professional ad copy for Facebook/Instagram campaigns"),
            ("YouTube Script",       "content",  499,  4,  "Engaging YouTube video scripts with hook and CTA"),
            ("Thumbnail Editing",    "content",  249,  2,  "Eye-catching YouTube thumbnails"),
            ("GST Invoice",          "business", 149,  1,  "Professional GST-compliant invoices"),
            ("Excel Formula Fix",    "tech",     199,  3,  "Fix and optimize Excel formulas and macros"),
            ("PPT Ready",            "business", 399,  6,  "Professional PowerPoint presentations"),
            ("Website Error Fix",    "tech",     599,  24, "Debug and fix website bugs and errors"),
            ("Instagram Caption",    "social",   149,  1,  "Viral Instagram captions with hashtags"),
            ("Business Logo",        "business", 799,  12, "Professional logo design"),
            ("WhatsApp Marketing",   "social",   199,  2,  "Bulk WhatsApp marketing message copy"),
        ]
        cur.executemany(
            "INSERT INTO services (name,category,price,delivery_hours,description) VALUES (?,?,?,?,?)", svcs
        )
    conn.commit()
    conn.close()
    print("✅ Database ready!")

def row_to_dict(r): return dict(r) if r else None
def gen_order_num():
    return f"DW{datetime.datetime.now().strftime('%Y%m%d')}{secrets.randbelow(9000)+1000}"
def calc_split(price, priority):
    mult = {"normal":1.0,"urgent":1.5,"express":2.0}.get(priority,1.0)
    final = int(price * mult)
    cut = int(final * 0.25)
    return final, cut, final - cut


# ──────────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────────
@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/api/services", methods=["GET"])
def get_services():
    cat = request.args.get("category")
    conn = get_db()
    if cat and cat != "all":
        rows = conn.execute("SELECT * FROM services WHERE is_active=1 AND category=? ORDER BY price",(cat,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM services WHERE is_active=1 ORDER BY category,price").fetchall()
    conn.close()
    return jsonify([row_to_dict(r) for r in rows])

@app.route("/api/services", methods=["POST"])
def add_service():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO services (name,category,price,delivery_hours,description) VALUES (?,?,?,?,?)",
        (d["name"],d["category"],d["price"],d["delivery_hours"],d.get("description","")))
    conn.commit(); conn.close()
    return jsonify({"message":"Service added"}), 201

@app.route("/api/workers", methods=["GET"])
def get_workers():
    conn = get_db()
    rows = conn.execute("SELECT * FROM workers ORDER BY total_earned DESC").fetchall()
    conn.close()
    return jsonify([row_to_dict(r) for r in rows])

@app.route("/api/workers/apply", methods=["POST"])
def apply_worker():
    d = request.json
    conn = get_db()
    try:
        conn.execute("INSERT INTO workers (name,phone,skills,experience) VALUES (?,?,?,?)",
            (d["name"],d["phone"],d["skills"],d.get("experience","")))
        conn.commit()
        return jsonify({"message":"Application submitted!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error":"Phone number already registered"}), 409
    finally:
        conn.close()

@app.route("/api/workers/<int:wid>/status", methods=["PATCH"])
def update_worker(wid):
    status = request.json.get("status")
    conn = get_db()
    conn.execute("UPDATE workers SET status=? WHERE id=?", (status, wid))
    conn.commit(); conn.close()
    return jsonify({"message":"Updated"})

@app.route("/api/payment/create-order", methods=["POST"])
def create_payment():
    """Create Razorpay order."""
    d = request.json
    amount_paise = int(d["amount"]) * 100  # Razorpay uses paise

    # Call Razorpay API
    try:
        resp = requests.post(
            "https://api.razorpay.com/v1/orders",
            auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET),
            json={"amount": amount_paise, "currency": "INR", "receipt": gen_order_num()}
        )
        data = resp.json()
        if "id" not in data:
            return jsonify({"error": data.get("error",{}).get("description","Razorpay error")}), 400
        return jsonify({"razorpay_order_id": data["id"], "amount": amount_paise, "key_id": RAZORPAY_KEY_ID})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/orders", methods=["POST"])
def place_order():
    d = request.json
    conn = get_db()
    svc = conn.execute("SELECT * FROM services WHERE id=? AND is_active=1",(d["service_id"],)).fetchone()
    if not svc: return jsonify({"error":"Service not found"}), 404

    priority = d.get("priority","normal")
    final, cut, earn = calc_split(svc["price"], priority)
    num = gen_order_num()
    worker = conn.execute("SELECT * FROM workers WHERE status='available' ORDER BY RANDOM() LIMIT 1").fetchone()
    wid = worker["id"] if worker else None

    conn.execute("""INSERT INTO orders
        (order_number,client_name,client_phone,service_id,worker_id,requirements,
         priority,amount,platform_cut,worker_earn,razorpay_payment_id,razorpay_order_id,status)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (num,d["client_name"],d["client_phone"],d["service_id"],wid,d.get("requirements"),
         priority,final,cut,earn,d.get("razorpay_payment_id"),d.get("razorpay_order_id"),
         "assigned" if wid else "pending"))
    if wid:
        conn.execute("UPDATE workers SET status='busy' WHERE id=?", (wid,))
    conn.commit(); conn.close()
    return jsonify({"message":"Order placed!","order_number":num,"amount":final,
                    "worker_assigned":worker["name"] if worker else "Assigning soon"}), 201

@app.route("/api/orders", methods=["GET"])
def get_orders():
    status = request.args.get("status")
    conn = get_db()
    q = """SELECT o.*,s.name as service_name,w.name as worker_name
           FROM orders o JOIN services s ON o.service_id=s.id
           LEFT JOIN workers w ON o.worker_id=w.id """
    rows = conn.execute(q+("WHERE o.status=? ORDER BY o.created_at DESC",(status,)) if status
                        else (q+"ORDER BY o.created_at DESC",())).fetchall() if False else \
           conn.execute(q+("WHERE o.status=?" if status else "")+" ORDER BY o.created_at DESC",
                        (status,) if status else ()).fetchall()
    conn.close()
    return jsonify([row_to_dict(r) for r in rows])

@app.route("/api/orders/<order_num>/complete", methods=["PATCH"])
def complete_order(order_num):
    conn = get_db()
    order = conn.execute("SELECT * FROM orders WHERE order_number=?",(order_num,)).fetchone()
    if not order: return jsonify({"error":"Not found"}), 404
    now = datetime.datetime.now().isoformat()
    conn.execute("UPDATE orders SET status='completed',completed_at=? WHERE order_number=?",(now,order_num))
    if order["worker_id"]:
        conn.execute("UPDATE workers SET status='available',total_earned=total_earned+? WHERE id=?",
                     (order["worker_earn"],order["worker_id"]))
    conn.commit(); conn.close()
    return jsonify({"message":"Completed!"})

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    conn = get_db()
    def one(q,*a): return conn.execute(q,a).fetchone()
    rev   = one("SELECT COALESCE(SUM(amount),0) as v FROM orders WHERE status='completed'")["v"]
    pcut  = one("SELECT COALESCE(SUM(platform_cut),0) as v FROM orders WHERE status='completed'")["v"]
    act   = one("SELECT COUNT(*) as v FROM orders WHERE status IN ('pending','assigned')")["v"]
    comp  = one("SELECT COUNT(*) as v FROM orders WHERE status='completed'")["v"]
    tw    = one("SELECT COUNT(*) as v FROM workers")["v"]
    aw    = one("SELECT COUNT(*) as v FROM workers WHERE status='available'")["v"]
    ts    = conn.execute("""SELECT s.name,COUNT(o.id) as orders,COALESCE(SUM(o.amount),0) as revenue
                            FROM orders o JOIN services s ON o.service_id=s.id
                            WHERE o.status='completed' GROUP BY s.id ORDER BY orders DESC LIMIT 5""").fetchall()
    conn.close()
    return jsonify({"total_revenue":rev,"platform_earnings":pcut,"active_orders":act,
                    "completed_orders":comp,"total_workers":tw,"available_workers":aw,
                    "top_services":[row_to_dict(r) for r in ts]})

@app.route("/api/health")
def health():
    return jsonify({"status":"ok","platform":"DigiWorkers v2.0",
                    "timestamp":datetime.datetime.now().isoformat()})


if __name__ == "__main__":
    init_db()
    print("\n" + "="*55)
    print("  🚀  DigiWorkers Platform — Full Stack Running!")
    print("="*55)
    print("  🌐  Website   : http://localhost:5000")
    print("  📊  Dashboard : http://localhost:5000  → Dashboard tab")
    print("  🔑  Razorpay  : app.py mein apni keys daalo")
    print("="*55 + "\n")
    import os
port = int(os.environ.get("PORT", 5000))
app.run(debug=False, host="0.0.0.0", port=port)
# ```---**Step 5** — Folder aisa dikhna chahiye:```
# digiworkers/├── app.py          ✅
# ├── requirements.txt ✅
# └── Procfile        ✅  (koi extension nahi)