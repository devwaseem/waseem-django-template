import { toast } from 'vanilla-sonner';

type ToastPayload = {
    type?: string;
    message?: string;
    title?: string;
    description?: string;
    duration?: number;
    action?: {
        label: string;
        onClick: () => void;
    };
} | string | null;

const showToast = (payload: ToastPayload) => {
    if (payload == null) {
        return;
    }

    if (typeof payload === 'string') {
        toast(payload);
        return;
    }

    const type = String(payload.type || '').toLowerCase();
    const message = payload.message || payload.title || 'Notification';
    const config: {
        duration?: number;
        action?: { label: string; onClick: () => void };
    } = {};

    if (typeof payload.duration === 'number') {
        config.duration = payload.duration;
    }

    if (
        payload.action &&
        typeof payload.action.label === 'string' &&
        typeof payload.action.onClick === 'function'
    ) {
        config.action = {
            label: payload.action.label,
            onClick: payload.action.onClick,
        };
    }

    if (type === 'success') {
        toast.success(message, config);
        return;
    }
    if (type === 'info') {
        toast.info(message, config);
        return;
    }
    if (type === 'warning') {
        toast.warning(message, config);
        return;
    }
    if (type === 'error') {
        toast.error(message, config);
        return;
    }

    if (
        typeof payload.description === 'string' &&
        payload.description.length > 0
    ) {
        toast.message(message, payload.description, config);
        return;
    }

    toast(message, config);
};

window.addEventListener('hyper:toast', (event: Event) => {
    const custom = event as CustomEvent<ToastPayload>;
    showToast(custom.detail);
});
