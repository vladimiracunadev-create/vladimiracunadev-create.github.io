// Formulario de solicitud de auditoria.
//
// El sitio es estatico en GitHub Pages: no hay backend al que enviar el POST y
// la CSP no permite hosts externos, asi que meter un servicio de formularios
// obligaria a abrir connect-src y a mandar los datos del cliente a un tercero.
// En vez de eso el formulario compone un mailto: con lo que la persona escribio
// y deja que su propio cliente de correo lo envie. Nada sale hacia terceros y
// no hace falta ninguna dependencia nueva.

(function () {
    "use strict";

    var form = document.getElementById("auditForm");
    if (!form) return;

    var DEST = "vladimir.acuna.dev@gmail.com";
    var btn = document.getElementById("auditSubmit");
    var okBox = document.getElementById("auditOk");
    var errBox = document.getElementById("auditError");

    // Etiquetas del correo en el idioma activo. Se leen del DOM para no
    // duplicar aqui las seis traducciones que ya viven en el HTML.
    function labelOf(id) {
        var el = form.querySelector('label[for="' + id + '"], #' + id);
        var lang = document.body.dataset.lang || "es";
        var host = form.querySelector('label[for="' + id + '"]');
        if (!host) return id;
        var span = host.querySelector("[data-" + lang + "]");
        return span ? span.textContent.trim() : (el ? id : id);
    }

    function legendOf(group) {
        var input = form.querySelector('[name="' + group + '"]');
        var fs = input ? input.closest("fieldset") : null;
        if (!fs) return group;
        var lang = document.body.dataset.lang || "es";
        var span = fs.querySelector("legend [data-" + lang + "]");
        return span ? span.textContent.trim() : group;
    }

    function radioValue(group) {
        var checked = form.querySelector('[name="' + group + '"]:checked');
        if (!checked) return "";
        var lang = document.body.dataset.lang || "es";
        var span = checked.parentElement.querySelector("span [data-" + lang + "]");
        return span ? span.textContent.trim() : checked.value;
    }

    function val(id) {
        var el = document.getElementById(id);
        return el ? el.value.trim() : "";
    }

    function show(box, on) {
        if (box) box.dataset.on = on ? "true" : "false";
    }

    function markInvalid(el, bad) {
        if (!el) return;
        el.setAttribute("aria-invalid", bad ? "true" : "false");
        var field = el.closest(".field");
        if (field) field.dataset.invalid = bad ? "true" : "false";
    }

    var REQUIRED_TEXT = ["f-name", "f-email", "f-tech", "f-problem"];
    var REQUIRED_RADIO = ["state", "kind", "conf"];

    form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        show(okBox, false);
        show(errBox, false);

        var bad = false;
        REQUIRED_TEXT.forEach(function (id) {
            var el = document.getElementById(id);
            var empty = !el || !el.value.trim();
            if (id === "f-email" && el && el.value.trim() && el.value.indexOf("@") < 0) {
                empty = true;
            }
            markInvalid(el, empty);
            if (empty) bad = true;
        });
        REQUIRED_RADIO.forEach(function (g) {
            var missing = !form.querySelector('[name="' + g + '"]:checked');
            var fs = form.querySelector('[name="' + g + '"]').closest("fieldset");
            if (fs) fs.dataset.invalid = missing ? "true" : "false";
            if (missing) bad = true;
        });

        if (bad) {
            show(errBox, true);
            // El .field marcado va antes que su input en el DOM y un div no
            // recibe foco: hay que apuntar al control, no al contenedor.
            var first = form.querySelector('[aria-invalid="true"]') ||
                form.querySelector('fieldset[data-invalid="true"] input');
            if (first && first.focus) first.focus();
            return;
        }

        // Estado de carga: componer y abrir el cliente de correo es inmediato,
        // pero el boton deja constancia visible de que la accion ocurrio.
        if (btn) btn.dataset.busy = "true";

        var lines = [
            labelOf("f-name") + ": " + val("f-name"),
            labelOf("f-email") + ": " + val("f-email"),
            labelOf("f-company") + ": " + (val("f-company") || "-"),
            labelOf("f-repo") + ": " + (val("f-repo") || "-"),
            labelOf("f-tech") + ": " + val("f-tech"),
            legendOf("state") + ": " + radioValue("state"),
            legendOf("kind") + ": " + radioValue("kind"),
            legendOf("conf") + ": " + radioValue("conf"),
            "",
            labelOf("f-problem") + ":",
            val("f-problem"),
            "",
            labelOf("f-message") + ":",
            val("f-message") || "-"
        ];

        var subject = "[Auditoria IA] " + val("f-name") + (val("f-company") ? " - " + val("f-company") : "");
        var href = "mailto:" + DEST +
            "?subject=" + encodeURIComponent(subject) +
            "&body=" + encodeURIComponent(lines.join("\n"));

        window.location.href = href;

        if (btn) btn.dataset.busy = "false";
        show(okBox, true);
        if (okBox && okBox.scrollIntoView) okBox.scrollIntoView({ block: "nearest" });
    });

    // Al corregir un campo, el estado de error deja de gritar.
    form.addEventListener("input", function (ev) {
        markInvalid(ev.target, false);
    });
    form.addEventListener("change", function (ev) {
        if (ev.target.type !== "radio") return;
        var fs = ev.target.closest("fieldset");
        if (fs) fs.dataset.invalid = "false";
    });
})();
