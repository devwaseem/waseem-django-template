import AlpineInstance, { AlpineComponent } from 'alpinejs';

interface FormSetType {
    total_forms_input: Element | null;
    initial_forms_input: Element | null;
    template: HTMLTemplateElement | null;
    forms_container: Element | null;
    can_show_divider: boolean;
    total_forms: number;
    add_form: () => void;
    remove_form: () => void;
}

AlpineInstance.data(
    'Formset',
    (): AlpineComponent<FormSetType> => ({
        total_forms_input: null,
        initial_forms_input: null,
        template: null,
        forms_container: null,
        total_forms: 0,
        init() {
            this.total_forms_input = this.$root.querySelector(`input[name$='-TOTAL_FORMS']`);
            this.initial_forms_input = this.$root.querySelector('input[name$="-INITIAL_FORMS"]');
            this.template = this.$root.querySelector('template');
            this.forms_container = this.$root.querySelector('div[formset-container]');
            if (!this.template) {
                console.error('<template> not found');
                return;
            }
            if (!this.forms_container) {
                console.error("element with attribute 'formset-container' not found");
                return;
            }
            //@ts-ignore
            this.total_forms = this.total_forms_input.value || 0;
        },
        add_form() {
            const new_form = this.template!.content.cloneNode(true);
            //@ts-ignore
            const form_count = new_form.children.length || 0;
            //@ts-ignore
            for (let el of new_form.querySelectorAll('input, select, textarea')) {
                if (el.name.includes('__prefix__')) {
                    el.name = el.name.replace('__prefix__', this.forms_container!.children.length);
                }
                if (el.id.includes('__prefix__')) {
                    el.id = el.id.replace('__prefix__', this.forms_container!.children.length);
                }
            }
            //@ts-ignore
            const labels = new_form.querySelectorAll('label');
            for (let el of labels) {
                if (el.htmlFor.includes('__prefix__')) {
                    el.htmlFor = el.htmlFor.replace('__prefix__', this.forms_container!.children.length);
                }
            }

            this.forms_container!.append(new_form);

            //@ts-ignore
            this.total_forms_input.value = parseInt(this.total_forms_input.value) + 1;
            //@ts-ignore
            this.total_forms = this.total_forms_input.value;
            //@ts-ignore
            this.initial_forms_input.value = parseInt(initialFormsInput.value) + 1;
        },
        remove_form() {
            this.$el.closest('[formset-form]')?.remove();
            for (let i = 0; i < this.forms_container!.children.length; i++) {
                const form = this.forms_container!.children[i];
                //@ts-ignore
                for (let el of form.querySelectorAll('input, select, textarea')) {
                    el.name = el.name.replace(/\d+/, i);
                    el.id = el.id.replace(/\d+/, i);
                }
                //@ts-ignore
                for (let el of form.querySelectorAll('label')) {
                    el.htmlFor = el.htmlFor.replace(/\d+/, i);
                }
            }

            //@ts-ignore
            this.total_forms_input.value = Math.max(0, parseInt(this.total_forms_input.value) - 1);
            //@ts-ignore
            this.total_forms = this.total_forms_input.value;
            //@ts-ignore
            this.initial_forms_input.value = Math.max(0, parseInt(this.initial_forms_input.value) - 1);
        },
        get can_show_divider() {
            return this.total_forms > 1;
        },
    })
);
