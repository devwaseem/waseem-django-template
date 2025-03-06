import { $byId } from '@shared/utils';
import AlpineInstance from 'alpinejs';

AlpineInstance.data('ModalContainer', () => ({
    closeModal(id: string) {
        $byId(id)?.remove();
    },
}));
