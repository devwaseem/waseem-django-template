import { $byId } from '@assets/utils';
import AlpineInstance from 'alpinejs';

AlpineInstance.data('ModalContainer', () => ({
    closeModal(id: string) {
        $byId(id)?.remove();
    },
}));
