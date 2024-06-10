import { Alpine as AlpineType } from "alpinejs";

declare global {
    interface Window {
        Alpine: AlpineType;
        $byId: Function;
        openLinkInNewWindow: (string) => void;
    }
    const Alpine: AlpineType;
}
