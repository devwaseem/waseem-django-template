import Alpine from 'alpinejs';
import { toast } from 'vanilla-sonner';
import 'vanilla-sonner/style.css';

import dropdown from '@shared/js/alpine/dropdown';
import modal from '@shared/js/alpine/modal';
import './toast';

function toastErrors() {
    const errorValues = document.scripts.namedItem('toast-errors');
    if (errorValues) {
        const errors = JSON.parse(errorValues.textContent);
        if (errors) {
            for (const error of errors) {
                toast.error(error);
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    toastErrors();
    document.querySelectorAll('[x-cloak]').forEach((el) => {
        el.removeAttribute('x-cloak');
    });
});

window.addEventListener('hyper:requestError', (event: Event) => {
    const custom = event as CustomEvent;
    const status = custom.detail.status;
    if (status === 404) {
        toast.error('Not Found');
        return;
    }

    if (status === 403) {
        toast.error("You don't have permission to run this action");
        return;
    }

    if (status === 400 || status >= 500) {
        toast.error(
            'Something went wrong, please try again. If the problem persists, contact support.',
        );
    }
});

// @ts-ignore
function toastError() {
    toast.error('Something went wrong');
}

// @ts-ignore
window.sendEvent = (name: string) => {
    const event = new CustomEvent(name);
    window.dispatchEvent(event);
};

declare global {
    interface Window {
        Alpine: typeof Alpine;
    }
}

window.Alpine = Alpine;

Alpine.data('dropdown', dropdown);
Alpine.data('modal', modal);
