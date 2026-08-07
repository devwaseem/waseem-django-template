type SearchSelectOption = {
  key: string;
  label: string;
};

type SearchSelectConfig = {
  inputId: string;
  selectedKey: string;
  query: string;
  options?: SearchSelectOption[];
  onChoose?: () => void;
};

export default (config: SearchSelectConfig) => ({
  open: false,
  selectedKey: config.selectedKey,
  query: config.query,
  committedQuery: config.query,
  highlightedIndex: 0,
  options: config.options ?? [],
  showAllOptions: false,
  isInvalid: false,
  dropUp: false,
  prioritizedOptions(): SearchSelectOption[] {
    if (!this.selectedKey) return this.options;
    const selectedOption = this.options.find((option) => option.key === this.selectedKey);
    if (!selectedOption) return this.options;
    return [selectedOption, ...this.options.filter((option) => option.key !== this.selectedKey)];
  },
  filteredOptions(): SearchSelectOption[] {
    const options = this.prioritizedOptions();
    if (this.showAllOptions) return options;
    const value = this.query.toLowerCase().trim();
    if (!value) return options;
    return options.filter((option) => option.label.toLowerCase().includes(value));
  },
  openMenu(): void {
    this.open = true;
    this.highlightedIndex = 0;
    queueMicrotask(() => this.updateDirection());
  },
  updateDirection(): void {
    const input = document.getElementById(config.inputId);
    if (!input) return;
    const rect = input.getBoundingClientRect();
    const spaceBelow = window.innerHeight - rect.bottom;
    const spaceAbove = rect.top;
    this.dropUp = spaceBelow < 260 && spaceAbove > spaceBelow;
  },
  focusInput(): void {
    this.showAllOptions = true;
    this.openMenu();
  },
  search(): void {
    this.showAllOptions = false;
    this.isInvalid = false;
    this.openMenu();
  },
  closeMenu(commitTypedMatch = false): void {
    if (commitTypedMatch && this.open) this.commitTypedMatch();
    this.open = false;
    this.showAllOptions = false;
  },
  highlightNext(): void {
    const options = this.filteredOptions();
    if (options.length === 0) return;
    this.open = true;
    this.highlightedIndex = (this.highlightedIndex + 1) % options.length;
  },
  highlightPrevious(): void {
    const options = this.filteredOptions();
    if (options.length === 0) return;
    this.open = true;
    this.highlightedIndex = (this.highlightedIndex - 1 + options.length) % options.length;
  },
  choose(option: SearchSelectOption): void {
    if (option.key === this.selectedKey) {
      this.query = option.label;
      this.committedQuery = option.label;
      this.open = false;
      this.showAllOptions = false;
      this.isInvalid = false;
      return;
    }
    this.selectedKey = option.key;
    this.query = option.label;
    this.committedQuery = option.label;
    this.isInvalid = false;
    this.closeMenu();
    queueMicrotask(() => config.onChoose?.());
  },
  commitTypedMatch(): void {
    const normalizedQuery = this.query.trim().toLowerCase();
    if (!normalizedQuery) {
      this.isInvalid = false;
      return;
    }
    if (this.selectedKey && normalizedQuery === this.committedQuery.trim().toLowerCase()) {
      this.isInvalid = false;
      return;
    }
    const option = this.options.find(
      (candidate) => candidate.label.trim().toLowerCase() === normalizedQuery,
    );
    if (option) {
      this.choose(option);
      return;
    }
    this.isInvalid = true;
  },
  chooseHighlighted(): void {
    const option = this.filteredOptions()[this.highlightedIndex];
    if (option) this.choose(option);
  },
});
