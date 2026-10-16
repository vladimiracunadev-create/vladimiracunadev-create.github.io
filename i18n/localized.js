"use strict";
document.getElementById("locale-select").addEventListener("change", function () {
  window.location.href = "../" + encodeURIComponent(this.value) + "/";
});
