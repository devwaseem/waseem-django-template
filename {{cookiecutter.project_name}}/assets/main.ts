import 'vite/modulepreload-polyfill';
import { $byId, openLinkInNewWindow } from './utils';

import './main.css';

document.addEventListener('toast', (event) => {
    // @ts-ignore
    const message = event?.detail?.message;
    // @ts-ignore
    const type = event?.detail?.type;
    if (message && type) {
        alert(message);
        // const toast = new Toast(message, type);
        // toast.showToast(5000);
    }
});

document.addEventListener('alert', (event: Event) => {
    // @ts-ignore
    const message = event?.detail?.message;
    if (message) {
        alert(message);
    }
});

window.$byId = $byId;
window.openLinkInNewWindow = openLinkInNewWindow;
