import Alpine from 'alpinejs';
// @ts-expect-error Alpine plugin package has no local type declarations.
import focus from '@alpinejs/focus';
// @ts-expect-error Alpine plugin package has no local type declarations.
import persist from '@alpinejs/persist';

type PickerInput = HTMLInputElement & {
    showPicker?: () => void;
};

function openNativeDatePicker(target: EventTarget | null) {
    if (!(target instanceof HTMLInputElement)) {
        return;
    }

    if (target.type !== 'date') {
        return;
    }

    (target as PickerInput).showPicker?.();
}

document.addEventListener('click', (event) => {
    openNativeDatePicker(event.target);
});

document.addEventListener('keydown', (event) => {
    if (!['Enter', ' ', 'ArrowDown'].includes(event.key)) {
        return;
    }

    openNativeDatePicker(event.target);
});

Alpine.plugin(focus);
Alpine.plugin(persist);

Alpine.start();
