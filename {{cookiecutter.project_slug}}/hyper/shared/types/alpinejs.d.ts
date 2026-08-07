declare module "alpinejs" {
  type AlpineComponent = Record<string, unknown>;

  interface Alpine {
    data(name: string, callback: () => AlpineComponent): void;
    start(): void;
  }

  const Alpine: Alpine;
  export default Alpine;
}
