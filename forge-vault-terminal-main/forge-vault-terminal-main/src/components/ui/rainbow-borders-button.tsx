"use client";

import React from "react";

interface RainbowButtonProps {
  children?: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
  type?: "button" | "submit" | "reset";
}

const STYLE_ID = "rainbow-borders-button-styles";
const CSS = `
@keyframes rainbow-borders {
  0% { background-position: 0 0; }
  50% { background-position: 400% 0; }
  100% { background-position: 0 0; }
}
.rb-btn-wrap {
  position: relative;
  display: inline-block;
  padding: 3px;
  border-radius: 9999px;
  background: linear-gradient(90deg,
    #ff0000, #ff7f00, #ffff00, #00ff00,
    #0000ff, #4b0082, #9400d3, #ff0000);
  background-size: 400% 100%;
  animation: rainbow-borders 6s linear infinite;
  isolation: isolate;
}
.rb-btn-wrap::before {
  content: "";
  position: absolute;
  inset: -3px;
  border-radius: 9999px;
  background: inherit;
  background-size: inherit;
  animation: inherit;
  filter: blur(14px);
  opacity: 0.7;
  z-index: -1;
}
.rb-btn-wrap[data-disabled="true"] { opacity: 0.45; cursor: not-allowed; }
.rb-btn-wrap[data-disabled="true"]::before { opacity: 0.25; }
.rb-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #000;
  color: #fff;
  border: none;
  border-radius: 9999px;
  padding: 1rem 2.5rem;
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 600;
  letter-spacing: 0.25em;
  cursor: pointer;
  transition: background 200ms ease, transform 150ms ease;
  outline: none;
}
.rb-btn:hover:not(:disabled) { background: #0a0a0a; }
.rb-btn:active:not(:disabled) { transform: translateY(1px); }
.rb-btn:disabled { cursor: not-allowed; }
`;

function injectStyles() {
  if (typeof document === "undefined") return;
  if (document.getElementById(STYLE_ID)) return;
  const el = document.createElement("style");
  el.id = STYLE_ID;
  el.textContent = CSS;
  document.head.appendChild(el);
}

export function RainbowButton({
  children = "Button",
  onClick,
  disabled,
  className = "",
  type = "button",
}: RainbowButtonProps) {
  if (typeof document !== "undefined") injectStyles();
  return (
    <div className="rb-btn-wrap" data-disabled={disabled ? "true" : "false"}>
      <button type={type} className={`rb-btn ${className}`} onClick={onClick} disabled={disabled}>
        {children}
      </button>
    </div>
  );
}

export const Button = RainbowButton;
