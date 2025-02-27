import { $byId } from 'frontend/shared/utils';
import AlpineInstance from 'alpinejs';

AlpineInstance.data('ModalContainer', () => ({
    closeModal(id: string) {
        $byId(id)?.remove();
    },
}));
