import 'htmx.org';
import 'htmx.org/dist/ext/loading-states.js';

//@ts-ignore
if (import.meta.env.MODE != 'production') {
    //@ts-ignore
    import('htmx.org/dist/ext/debug.js');
}

document.addEventListener('htmx:historyRestore', () => {
    removeOrphanElementsGeneratedByAlpineJs();
});

function removeOrphanElementsGeneratedByAlpineJs() {
    document.querySelectorAll('[x-from-template]').forEach((e) => e.remove());
}

// document.addEventListener('htmx:afterSettle', (event: Event) => {
// @ts-ignore
// debugger;
// Alpine.initTree(event.target);
// });

document.addEventListener('htmx:sendError', () => {
    const message =
        "We're sorry, it looks like there was a problem connecting to the network or server. Please check your internet connection and try again, or wait a few minutes and try again later.";
    alert(message);
    // const toast = new Toast(message, ToastType.ERROR);
    // toast.showToast(5000);
});

document.addEventListener('htmx:afterSettle', function (event) {
    //@ts-ignore
    const { isError, xhr } = event.detail.xhr;
    if (!isError) {
        return;
    }

    if (xhr.status == 429) {
        alert('Too Many Requests. Please wait and try again later.');
        return;
    }

    if (xhr.status > 400 && xhr.status < 599) {
        event.stopPropagation(); // Tell htmx not to process these requests
        let message = 'Something went wrong! Please try again!';
        alert(message);

        // const toast = new Toast(message, ToastType.ERROR);
        // toast.showToast(5000);
    }
});

document.body.addEventListener('htmx:beforeSwap', function (event) {
    // Allow 422 and 400 responses to swap
    // We treat these as form validation errors
    //@ts-ignore
    const xhr = event.detail.xhr;
    if (xhr.status === 422 || xhr.status === 400) {
        //@ts-ignore
        event.detail.shouldSwap = true;
        //@ts-ignore
        event.detail.isError = false;
        alert('Please check your inputs');
    }
});
