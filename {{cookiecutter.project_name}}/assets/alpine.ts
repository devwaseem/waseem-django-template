import Alpine from 'alpinejs';

import collapse from '@alpinejs/collapse';
import focus from '@alpinejs/focus';
import mask from '@alpinejs/mask';

import Tooltip from '@ryangjchandler/alpine-tooltip';
import 'tippy.js/dist/tippy.css'; // Need this for alpine Tooltip

window.Alpine = Alpine;

Alpine.plugin(focus);
Alpine.plugin(collapse);
Alpine.plugin(mask);
Alpine.plugin(Tooltip);
Alpine.start();
