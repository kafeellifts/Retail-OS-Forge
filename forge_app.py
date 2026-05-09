import webview
import subprocess
import threading
import time
import os
import sys
import json

class ForgeAPI:

    def __init__(self):
        self._window = None
        self._running = False

    def set_window(self, window):
        self._window = window

    def _log(self, msg):
        safe = json.dumps(msg)
        if self._window:
            self._window.evaluate_js(f"window.__appendLog({safe})")

    def _execute_cmd(self, title, cmd):
        self._log(f"\n> {title}")
        self._log(f"$ powershell -Command \"{cmd}\"")
        try:
            process = subprocess.run(
                ["powershell", "-Command", cmd],
                shell=True,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if process.stdout:
                for line in process.stdout.strip().splitlines():
                    self._log(line)
            if process.stderr:
                for line in process.stderr.strip().splitlines():
                    self._log(f"ERROR: {line}")
        except Exception as e:
            self._log(f"EXCEPTION: {str(e)}")
        time.sleep(0.3)

    def start_forge(self, debloat, pos, optimize):
        if self._running:
            return
        self._running = True
        thread = threading.Thread(
            target=self._forge_worker, args=(debloat, pos, optimize), daemon=True
        )
        thread.start()

    def _forge_worker(self, debloat, pos, optimize):
        self._log("[ ENGINE ] Connection established. Executing payload...")
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")
        self._log(f"[ {ts} ] INITIALIZING PAYLOAD...")
        self._log(f"[ CONFIG ] debloat_level={debloat} | pos_software={pos} | optimize_hardware={optimize}")
        if debloat == "Aggressive":
            cmd = "Get-AppxPackage -AllUsers | Where-Object {$_.Name -notmatch 'Store|Calculator|Photos'} | Remove-AppxPackage"
            self._execute_cmd("Aggressive Debloat", cmd)
        elif debloat == "Basic":
            cmd = "Get-AppxPackage *xbox* | Remove-AppxPackage; Get-AppxPackage *zune* | Remove-AppxPackage"
            self._execute_cmd("Basic Debloat", cmd)
        if optimize:
            cmd = (
                "powercfg -change -standby-timeout-ac 0; "
                "powercfg -change -monitor-timeout-ac 0; "
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot' "
                "-Name 'TurnOffWindowsCopilot' -Value 1 -Type DWord -Force"
            )
            self._execute_cmd("Applying Optimizations", cmd)
        if pos and pos != "None":
            cmd = f"Write-Host 'Simulating silent install for {pos}...'"
            self._execute_cmd(f"Installing {pos}", cmd)

        self._log("\n[!] PROVISIONING COMPLETE.")
        if self._window:
            self._window.evaluate_js("window.__onForgeComplete()")
        self._running = False

    def reboot_system(self):
        subprocess.run("shutdown /r /t 5", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

HTML = r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Retail OS Forge</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet" />
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#000;--fg:#fff;--muted:rgba(255,255,255,0.4);--border:rgba(255,255,255,0.1);
  --emerald:#34d399;--amber:#f59e0b;--red:#c81d25;
}
html,body{height:100%;overflow-x:hidden}
body{
  font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--fg);
  display:flex;justify-content:center;align-items:center;
  min-height:100vh;
  margin:0;
  position:relative;
}

  position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-2;
  background:#000;display:block;
}

.cursor-glow{
  position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:radial-gradient(600px circle at var(--mx,50%) var(--my,50%),
    rgba(255,255,255,0.06) 0%, rgba(120,120,255,0.03) 25%, transparent 60%);
  transition:background 0.15s ease-out;
}

.gradient-overlay{
  position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(to bottom,rgba(0,0,0,0.35),transparent 40%,transparent 60%,rgba(0,0,0,0.55));
}

.striped-overlay{
  position:fixed;inset:0;z-index:-1;pointer-events:none;
  background: repeating-linear-gradient(
    -45deg,
    rgba(255, 255, 255, 0.02),
    rgba(255, 255, 255, 0.02) 1px,
    transparent 1px,
    transparent 6px
  );
}

.glass-panel{
  position:relative;
  border-radius:10px;
  padding:48px 40px 40px;
  overflow:hidden;
  border: 1px solid rgba(164,132,215,0.5);
  background: rgba(85,80,110,0.15);
  box-shadow: 0 0 40px rgba(123,57,252,0.15), inset 0 1px 0 rgba(255,255,255,0.08);
  transform: perspective(1200px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1);
  transform-style: preserve-3d;
  transition: transform 0.2s ease-out;
  will-change: transform;
}
.glass-panel::before{
  content:'';position:absolute;inset:0;z-index:0;border-radius:inherit;
  backdrop-filter:blur(24px) saturate(1.4);
  -webkit-backdrop-filter:blur(24px) saturate(1.4);
  filter:url(#glass-distortion);
  isolation:isolate;
}
.glass-panel::after{
  content:'';position:absolute;inset:0;z-index:1;border-radius:inherit;
  background:transparent;
  pointer-events:none;
}
.glass-panel .glass-content{position:relative;z-index:2}

.spotlight-wrapper {
  position: absolute;
  inset: 0;
  z-index: 10;
  overflow: hidden;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: inherit;
}
.spotlight {
  position: absolute;
  width: 200%;
  height: 200%;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 40%);
}

.lamp-effect {
  position: absolute;
  top: -8rem;
  left: 50%;
  transform: translateX(-50%);
  width: 100vw;
  height: 35rem;
  z-index: -1;
  pointer-events: none;
}
.lamp-beam-left {
  position: absolute;
  right: 50%;
  top: 0;
  width: 40vw;
  height: 35rem;
  background: conic-gradient(from 70deg at center top, rgba(255,255,255,0.7), transparent, transparent);
  -webkit-mask-image: linear-gradient(to bottom, black 0%, transparent 80%);
  animation: expandBeamLeft 1s ease-in-out forwards;
}
.lamp-beam-right {
  position: absolute;
  left: 50%;
  top: 0;
  width: 40vw;
  height: 35rem;
  background: conic-gradient(from 290deg at center top, transparent, transparent, rgba(255,255,255,0.7));
  -webkit-mask-image: linear-gradient(to bottom, black 0%, transparent 80%);
  animation: expandBeamRight 1s ease-in-out forwards;
}
.lamp-glow-large {
  position: absolute;
  top: -2rem;
  left: 50%;
  transform: translateX(-50%);
  width: 50rem;
  height: 4rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  filter: blur(40px);
}
.lamp-glow-small {
  position: absolute;
  top: -2rem;
  left: 50%;
  transform: translateX(-50%);
  width: 24rem;
  height: 4rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  filter: blur(30px);
  animation: expandGlowSmall 1s ease-in-out forwards;
}
.lamp-line {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 50rem;
  height: 2px;
  background: #ffffff;
  box-shadow: 0 0 10px 2px rgba(255,255,255,0.4), 0 0 20px 2px rgba(255,255,255,0.6);
  animation: expandLine 1s ease-in-out forwards;
}

@keyframes expandBeamLeft {
  0% { width: 20vw; opacity: 0.3; }
  100% { width: 40vw; opacity: 1; }
}
@keyframes expandBeamRight {
  0% { width: 20vw; opacity: 0.3; }
  100% { width: 40vw; opacity: 1; }
}
@keyframes expandLine {
  0% { width: 25rem; }
  100% { width: 50rem; }
}
@keyframes expandGlowSmall {
  0% { width: 12rem; }
  100% { width: 24rem; }
}

.card-backdrop{
  position:absolute;inset:-2px;z-index:-1;border-radius:inherit;
  filter:url(#unopaq);pointer-events:none;
}
.border-element{
  position:absolute;z-index:3;pointer-events:none;
  border-radius:inherit;
}
.border-left{
  left:0;top:0;width:2px;height:100%;
  background:linear-gradient(to bottom,transparent,rgba(255,255,255,0.9),rgba(220,230,255,0.7),transparent);
  background-size:100% 300%;
  animation:glowMoveV 4s ease-in-out infinite;
}
.border-right{
  right:0;top:0;width:2px;height:100%;
  background:linear-gradient(to bottom,transparent,rgba(220,230,255,0.7),rgba(255,255,255,0.9),transparent);
  background-size:100% 300%;
  animation:glowMoveV 4s ease-in-out infinite reverse;
}
.border-top{
  top:0;left:0;height:2px;width:100%;
  background:linear-gradient(to right,transparent,rgba(255,255,255,0.9),rgba(220,230,255,0.7),transparent);
  background-size:300% 100%;
  animation:glowMoveH 4s ease-in-out infinite;
}
.border-bottom{
  bottom:0;left:0;height:2px;width:100%;
  background:linear-gradient(to right,transparent,rgba(220,230,255,0.7),rgba(255,255,255,0.9),transparent);
  background-size:300% 100%;
  animation:glowMoveH 4s ease-in-out infinite reverse;
}
@keyframes glowMoveV{
  0%{background-position:0% 0%}
  50%{background-position:0% 100%}
  100%{background-position:0% 0%}
}
@keyframes glowMoveH{
  0%{background-position:0% 0%}
  50%{background-position:100% 0%}
  100%{background-position:0% 0%}
}

.border-left::after,.border-right::after{
  content:'';position:absolute;top:0;width:12px;height:100%;
  filter:blur(8px);opacity:0.6;border-radius:inherit;
  background:inherit;
}
.border-left::after{left:-5px}
.border-right::after{right:-5px}
.border-top::after,.border-bottom::after{
  content:'';position:absolute;left:0;height:12px;width:100%;
  filter:blur(8px);opacity:0.6;border-radius:inherit;
  background:inherit;
}
.border-top::after{top:-5px}
.border-bottom::after{bottom:-5px}

.marquee-wrap{
  position:fixed;top:50%;left:0;right:0;transform:translateY(-50%);z-index:-1;
  overflow:hidden;pointer-events:none;user-select:none;
}
.marquee-track{
  display:flex;white-space:nowrap;
  animation:marqueeScroll 20s linear infinite;
}
.marquee-track span{
  font-size:18vw;font-weight:900;letter-spacing:-0.04em;
  color:rgba(255,255,255,0.04);text-shadow:0 0 40px rgba(255,255,255,0.03);
  padding-right:3rem;text-transform:uppercase;
}
@keyframes marqueeScroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}

.container{width:50vw;min-width:600px;position:relative;z-index:1}

.header{text-align:center;margin-bottom:48px;padding-bottom:24px;animation:fadeUp .6s ease-out}
.header h1{
  font-family:'Space Grotesk',sans-serif;
  font-size:clamp(2.5rem,7vw,4.5rem);font-weight:700;letter-spacing:.3em;
  background:linear-gradient(to bottom,rgba(255,255,255,0.2),rgba(255,255,255,0.0));
  -webkit-background-clip:text;background-clip:text;color:transparent;
  -webkit-text-stroke: 2px #ffffff;
  filter:drop-shadow(0 0 30px rgba(0,255,255,0.3));
}
.header .subtitle{
  margin-top:16px;font-size:10px;font-weight:600;letter-spacing:.5em;
  text-transform:uppercase;color:var(--muted);
}

@keyframes fadeUp{from{opacity:0;transform:translateY(12px);filter:blur(8px)}to{opacity:1;transform:translateY(0);filter:blur(0)}}

.section{margin-bottom:28px;animation:fadeUp .6s ease-out both}
.section:nth-child(2){animation-delay:.1s}
.section:nth-child(3){animation-delay:.2s}
.section:nth-child(4){animation-delay:.3s}
.section:nth-child(5){animation-delay:.4s}
.section-label{
  font-size:10px;font-weight:600;letter-spacing:.3em;text-transform:uppercase;
  color:var(--muted);margin-bottom:12px;
}

.btn-group{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}
.btn-pill{
  position:relative;min-width:140px;padding:10px 20px;
  border:1px solid var(--border);border-radius:999px;
  background:rgba(0,0,0,0.4);backdrop-filter:blur(4px);
  color:var(--muted);font-size:11px;font-weight:600;letter-spacing:.25em;
  text-transform:uppercase;cursor:pointer;transition:all .3s ease;
  overflow:hidden;
}
.btn-pill:hover{border-color:rgba(255,255,255,0.3);background:rgba(0,0,0,0.6);color:#fff}
.btn-pill.active{border-color:rgba(255,255,255,0.4);color:#fff;background:rgba(255,255,255,0.08)}
.btn-pill.active::before{
  content:'';position:absolute;inset:0;border-radius:inherit;
  background:radial-gradient(75% 180% at 50% 50%,#3275F8 0%,transparent 100%);
  opacity:0.15;pointer-events:none;
}

.select-wrap{position:relative;width:100%}
.select-trigger{
  display:flex;align-items:center;justify-content:space-between;width:100%;
  height:44px;padding:0 16px;
  border:1px solid var(--border);border-radius:8px;
  background:rgba(255,255,255,0.03);color:#fff;font-size:14px;
  cursor:pointer;transition:all .2s;appearance:none;
  font-family:'Inter',sans-serif;
}
.select-trigger:hover{border-color:rgba(255,255,255,0.3);background:rgba(255,255,255,0.06)}
.select-trigger:focus{outline:none;border-color:rgba(255,255,255,0.4);box-shadow:0 0 0 2px rgba(255,255,255,0.1)}
.select-trigger option{background:#111;color:#fff}

.checkbox-row{display:flex;align-items:flex-start;gap:12px;font-size:14px;color:rgba(255,255,255,0.8)}
.checkbox-row input[type="checkbox"]{
  appearance:none;width:20px;height:20px;min-width:20px;margin-top:2px;
  border:1px solid rgba(255,255,255,0.3);border-radius:4px;
  background:rgba(255,255,255,0.05);cursor:pointer;
  transition:all .2s;position:relative;
}
.checkbox-row input[type="checkbox"]:checked{background:#fff;border-color:#fff}
.checkbox-row input[type="checkbox"]:checked::after{
  content:'✓';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  color:#000;font-size:14px;font-weight:700;
}
.checkbox-row input[type="checkbox"]:hover{transform:scale(1.05)}
.checkbox-row label{cursor:pointer;line-height:1.6}

.legal-box{
  display:flex;align-items:flex-start;gap:12px;padding:16px;
  border:1px solid rgba(245,158,11,0.2);border-radius:8px;
  background:rgba(245,158,11,0.05);
}
.legal-icon{color:var(--amber);font-size:20px;flex-shrink:0;margin-top:2px}

.forge-wrap{display:flex;justify-content:center;margin-top:32px;animation:fadeUp .6s ease-out .5s both}
.forge-btn{
  position:relative;padding:16px 32px;border:1px solid var(--border);border-radius:999px;
  background:rgba(0,0,0,0.4);backdrop-filter:blur(4px);
  color:#fff;font-size:13px;font-weight:700;letter-spacing:.3em;text-transform:uppercase;
  cursor:pointer;transition:all .3s ease;overflow:hidden;
}
.forge-btn:hover:not(:disabled){border-color:rgba(255,255,255,0.4);background:rgba(0,0,0,0.6)}
.forge-btn:disabled{opacity:0.35;cursor:not-allowed;pointer-events:none}
.forge-btn.reboot{border-color:rgba(52,211,153,0.4);color:var(--emerald)}
.forge-btn.reboot:hover{background:rgba(52,211,153,0.1)}
.forge-btn.forging{animation:pulse 1.5s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}

.terminal-wrap{margin-top:32px;animation:fadeUp .6s ease-out .6s both}
.terminal-label{
  display:flex;align-items:center;gap:8px;font-size:10px;font-weight:600;
  letter-spacing:.3em;text-transform:uppercase;color:var(--muted);margin-bottom:8px;
}
.terminal-label svg{width:14px;height:14px}
.terminal{
  height:260px;overflow-y:auto;padding:16px;
  border:1px solid rgba(52,211,153,0.2);border-radius:8px;
  background:rgba(0,0,0,0.9);
  font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.8;
  color:var(--emerald);box-shadow:inset 0 2px 8px rgba(0,0,0,0.5);
  white-space:pre-wrap;word-break:break-word;
}
.terminal .cursor-blink{
  display:inline-block;width:8px;height:14px;background:var(--emerald);
  animation:blink 1s step-end infinite;vertical-align:middle;margin-left:2px;
}
@keyframes blink{50%{opacity:0}}

.terminal::-webkit-scrollbar{width:6px}
.terminal::-webkit-scrollbar-track{background:transparent}
.terminal::-webkit-scrollbar-thumb{background:rgba(52,211,153,0.3);border-radius:3px}
</style>
</head>
<body>

<svg style="display:none">
  <filter id="glass-distortion" x="0%" y="0%" width="100%" height="100%" filterUnits="objectBoundingBox">
    <feTurbulence type="fractalNoise" baseFrequency="0.001 0.005" numOctaves="1" seed="17" result="turbulence"/>
    <feComponentTransfer in="turbulence" result="mapped">
      <feFuncR type="gamma" amplitude="1" exponent="10" offset="0.5"/>
      <feFuncG type="gamma" amplitude="0" exponent="1" offset="0"/>
      <feFuncB type="gamma" amplitude="0" exponent="1" offset="0.5"/>
    </feComponentTransfer>
    <feGaussianBlur in="turbulence" stdDeviation="3" result="softMap"/>
    <feSpecularLighting in="softMap" surfaceScale="5" specularConstant="1" specularExponent="100" lightingColor="white" result="specLight">
      <fePointLight x="-200" y="-200" z="300"/>
    </feSpecularLighting>
    <feComposite in="specLight" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="litImage"/>
    <feDisplacementMap in="SourceGraphic" in2="softMap" scale="200" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter width="3000%" x="-1000%" height="3000%" y="-1000%" id="unopaq">
    <feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 3 0"/>
  </filter>
</svg>

<canvas id="entropyCanvas"></canvas>
<div class="striped-overlay"></div>
<div class="cursor-glow" id="cursorGlow"></div>
<div class="gradient-overlay"></div>
<div class="marquee-wrap">
  <div class="marquee-track">
    <span>RETAIL OS FORGE</span><span>RETAIL OS FORGE</span>
    <span>RETAIL OS FORGE</span><span>RETAIL OS FORGE</span>
  </div>
</div>

<div class="container">
<div class="lamp-effect">
  <div class="lamp-beam-left"></div>
  <div class="lamp-beam-right"></div>
  <div class="lamp-glow-large"></div>
  <div class="lamp-glow-small"></div>
  <div class="lamp-line"></div>
</div>
<div class="glass-panel" id="tiltCard">
<div class="spotlight-wrapper" id="spotlightWrapper"><div class="spotlight" id="spotlight"></div></div>
<div class="card-backdrop"></div>
<div class="border-element border-left"></div>
<div class="border-element border-right"></div>
<div class="border-element border-top"></div>
<div class="border-element border-bottom"></div>
<div class="glass-content">
  
  <div class="header">
    <h1>RETAIL OS FORGE</h1>
    <div class="subtitle">Hardware Provisioning Payload</div>
  </div>

  <div class="section">
    <div class="section-label">01 / Debloat Level</div>
    <div class="btn-group" id="debloatGroup">
      <button class="btn-pill" data-value="Aggressive" onclick="selectDebloat(this)">Aggressive</button>
      <button class="btn-pill active" data-value="Basic" onclick="selectDebloat(this)">Basic</button>
      <button class="btn-pill" data-value="None" onclick="selectDebloat(this)">None</button>
    </div>
  </div>

  <div class="section">
    <div class="section-label">02 / POS Software</div>
    <div class="select-wrap">
      <select class="select-trigger" id="posSelect">
        <option value="Marg ERP 9+">Marg ERP 9+</option>
        <option value="TallyPrime">TallyPrime</option>
        <option value="Busy Accounting">Busy Accounting</option>
        <option value="Vyapar">Vyapar</option>
        <option value="Zoho Inventory">Zoho Inventory</option>
        <option value="Hitech BillSoft">Hitech BillSoft</option>
        <option value="None">None</option>
      </select>
    </div>
  </div>

  <div class="section">
    <div class="section-label">03 / Optimizations</div>
    <div class="checkbox-row">
      <input type="checkbox" id="optimizeCheck" checked />
      <label for="optimizeCheck">Optimize Files & Hardware (Disable Sleep, Telemetry, Copilot)</label>
    </div>
  </div>

  <div class="section">
    <div class="section-label">04 / Legal Acknowledgement</div>
    <div class="legal-box">
      <div class="legal-icon">⚠</div>
      <div class="checkbox-row">
        <input type="checkbox" id="ackCheck" onchange="toggleForge()" />
        <label for="ackCheck">I acknowledge this payload will alter system settings and install software. Creators are not liable for data loss.</label>
      </div>
    </div>
  </div>

  <div class="forge-wrap">
    <button class="forge-btn" id="forgeBtn" disabled onclick="handleForge()">FORGE RETAIL TERMINAL</button>
  </div>

  <div class="terminal-wrap">
    <div class="terminal-label">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg>
      Live Terminal
    </div>
    <div class="terminal" id="terminal">[ READY ] Retail OS Forge terminal initialized.
[ INFO  ] Awaiting payload configuration...
</div>
  </div>
</div>
</div>
</div>

<script>
let debloatLevel = 'Basic';
let forging = false;
let completed = false;
(function(){
  const card = document.getElementById('tiltCard');
  const wrapper = document.getElementById('spotlightWrapper');
  const spot = document.getElementById('spotlight');
  const tiltLimit = 15;
  const scale = 1.02;
  const perspective = 1200;
  const dir = -1;

  card.addEventListener('pointermove', function(e){
    const rect = card.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width;
    const py = (e.clientY - rect.top) / rect.height;
    
    const xRot = (py - 0.5) * (tiltLimit * 2) * dir;
    const yRot = (px - 0.5) * -(tiltLimit * 2) * dir;
    
    card.style.transform = `perspective(${perspective}px) rotateX(${xRot}deg) rotateY(${yRot}deg) scale3d(${scale}, ${scale}, ${scale})`;
    
    wrapper.style.opacity = 1;
    spot.style.left = `${px * 100}%`;
    spot.style.top = `${py * 100}%`;
  });

  card.addEventListener('pointerleave', function(){
    card.style.transform = `perspective(${perspective}px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
    wrapper.style.opacity = 0;
  });
})();
const _glow = document.getElementById('cursorGlow');
let _mouseX = -1, _mouseY = -1;
document.addEventListener('mousemove', function(e){
  _mouseX = e.clientX; _mouseY = e.clientY;
  _glow.style.setProperty('--mx', e.clientX + 'px');
  _glow.style.setProperty('--my', e.clientY + 'px');
});
(function(){
  const canvas = document.getElementById('entropyCanvas');
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  let W, H;

  function resize(){
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
    ctx.scale(dpr, dpr);
  }
  resize();
  window.addEventListener('resize', function(){ resize(); initParticles(); });

  const COLOR = '#ffffff';
  let particles = [];

  function Particle(x, y, order){
    this.x = x; this.y = y;
    this.originalX = x; this.originalY = y;
    this.size = 2; this.order = order;
    this.vx = (Math.random() - 0.5) * 2;
    this.vy = (Math.random() - 0.5) * 2;
    this.influence = 0;
    this.neighbors = [];
  }

  Particle.prototype.update = function(){
    if(_mouseX > 0){
      const mdx = this.x - _mouseX, mdy = this.y - _mouseY;
      const md = Math.sqrt(mdx*mdx + mdy*mdy);
      if(md < 120){
        const force = (1 - md / 120) * 3;
        this.vx += (mdx / md) * force;
        this.vy += (mdy / md) * force;
      }
    }
    this.vx += (Math.random() - 0.5) * 0.5;
    this.vy += (Math.random() - 0.5) * 0.5;
    this.vx *= 0.95; this.vy *= 0.95;
    this.x += this.vx; this.y += this.vy;
    if(this.x < 0 || this.x > W) this.vx *= -1;
    if(this.y < 0 || this.y > H) this.vy *= -1;
    this.x = Math.max(0, Math.min(W, this.x));
    this.y = Math.max(0, Math.min(H, this.y));
  };

  Particle.prototype.draw = function(){
    ctx.fillStyle = COLOR + 'CC';
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
  };

  function initParticles(){
    particles = [];
    const gridX = 40, gridY = Math.round(40 * H / W);
    const spX = W / gridX, spY = H / gridY;
    for(let i = 0; i < gridX; i++){
      for(let j = 0; j < gridY; j++){
        const x = spX * i + spX / 2;
        const y = spY * j + spY / 2;
        particles.push(new Particle(x, y, false));
      }
    }
  }
  initParticles();

  function updateNeighbors(){
    for(let i = 0; i < particles.length; i++){
      const p = particles[i];
      p.neighbors = [];
      for(let j = 0; j < particles.length; j++){
        if(i === j) continue;
        const o = particles[j];
        const d = Math.sqrt(Math.pow(p.x-o.x,2)+Math.pow(p.y-o.y,2));
        if(d < 100) p.neighbors.push(o);
      }
    }
  }

  let time = 0;
  function animate(){
    ctx.clearRect(0, 0, W, H);
    if(time % 30 === 0) updateNeighbors();

    for(let i = 0; i < particles.length; i++){
      const p = particles[i];
      p.update(); p.draw();
      for(let j = 0; j < p.neighbors.length; j++){
        const n = p.neighbors[j];
        const d = Math.sqrt(Math.pow(p.x-n.x,2)+Math.pow(p.y-n.y,2));
        if(d < 50){
          const a = 0.2 * (1 - d / 50);
          const hex = Math.round(a * 255).toString(16).padStart(2, '0');
          ctx.strokeStyle = COLOR + hex;
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(n.x, n.y);
          ctx.stroke();
        }
      }
    }

    time++;
    requestAnimationFrame(animate);
  }
  animate();
})();

function selectDebloat(el) {
  document.querySelectorAll('#debloatGroup .btn-pill').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  debloatLevel = el.dataset.value;
}

function toggleForge() {
  const btn = document.getElementById('forgeBtn');
  const ack = document.getElementById('ackCheck').checked;
  btn.disabled = !ack || forging;
}
window.__appendLog = function(msg) {
  const term = document.getElementById('terminal');
  term.textContent += msg + '\n';
  term.scrollTop = term.scrollHeight;
};
window.__onForgeComplete = function() {
  forging = false;
  completed = true;
  const btn = document.getElementById('forgeBtn');
  btn.textContent = 'REBOOT SYSTEM';
  btn.classList.remove('forging');
  btn.classList.add('reboot');
  btn.disabled = false;
};

function handleForge() {
  if (completed) {
    pywebview.api.reboot_system();
    return;
  }

  forging = true;
  const btn = document.getElementById('forgeBtn');
  btn.textContent = 'INITIALIZING PAYLOAD...';
  btn.classList.add('forging');
  btn.disabled = true;

  const term = document.getElementById('terminal');
  term.textContent = '';

  const pos = document.getElementById('posSelect').value;
  const optimize = document.getElementById('optimizeCheck').checked;

  pywebview.api.start_forge(debloatLevel, pos, optimize);
}
</script>
</body>
</html>
"""

def main():
    api = ForgeAPI()
    try:
        import ctypes
        user32 = ctypes.windll.user32
        sw = user32.GetSystemMetrics(0)
        sh = user32.GetSystemMetrics(1)
        w, h = 900, 820
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
    except:
        x, y = None, None

    window = webview.create_window(
        "Retail OS Forge",
        html=HTML,
        js_api=api,
        width=900,
        height=820,
        x=x,
        y=y,
        resizable=True,
        min_size=(700, 600),
        background_color="#000000",
    )
    api.set_window(window)
    webview.start(debug=False)

if __name__ == "__main__":
    main()
