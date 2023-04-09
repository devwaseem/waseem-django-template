// import 'vite/modulepreload-polyfill'

import focus from "@alpinejs/focus";
import mask from "@alpinejs/mask";
import collapse from "@alpinejs/collapse";

import Alpine from "alpinejs";
import Cookies from "js-cookie";
import { $byId } from "./utils";

import "htmx.org";
import "htmx.org/dist/ext/debug.js";
import "htmx.org/dist/ext/alpine-morph.js";
import "htmx.org/dist/ext/morphdom-swap";
import "htmx.org/dist/ext/loading-states.js";

if (import.meta.env.MODE != "production") {
    //@ts-ignore
    await import("htmx.org/dist/ext/debug.js");
}

// @ts-expect-error
const { htmx } = window;

// HTMX Configuration (https://htmx.org/docs/#config)
htmx.defineExtension("get-csrf", {
    onEvent(name: string, evt: any) {
        if (name === "htmx:configRequest") {
            evt.detail.headers["X-CSRFToken"] = Cookies.get("csrftoken");
        }
    },
});

document.addEventListener("htmx:historyRestore", () => {
    removeOrphanElementsGeneratedByAlpineJs();
});

function removeOrphanElementsGeneratedByAlpineJs() {
    document.querySelectorAll("[x-from-template]").forEach((e) => e.remove());
}

document.addEventListener("htmx:afterSettle", (event: Event) => {
    // @ts-ignore
    Alpine.initTree(event.target);
});

document.addEventListener("alert", (event: Event) => {
  // @ts-ignore
  const message = event?.detail?.message;
  if(message) {
    alert(message)
  }

})

window.Alpine = Alpine;
window.$byId = $byId;

Alpine.plugin(focus);
Alpine.plugin(collapse);
Alpine.plugin(mask);
Alpine.start();
