"use strict";
const locale = document.documentElement.lang || "es";
localStorage.setItem("portfolio_lang", locale);
const target = new URL("../../", window.location.href);
target.searchParams.set("lang", locale);
target.hash = window.location.hash;
window.location.replace(target);
