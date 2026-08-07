import Alpine from "alpinejs";

import dropdown from "@shared/js/alpine/dropdown";
import modal from "@shared/js/alpine/modal";
import "@shared/js/main.body";

Alpine.data("dropdown", dropdown);
Alpine.data("modal", modal);
Alpine.start();
