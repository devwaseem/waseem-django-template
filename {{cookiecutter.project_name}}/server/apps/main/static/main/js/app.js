const $byId = (id) => document.getElementById(id);
const $byQuery = query => document.querySelector(query);
const csrfToken = document.currentScript.getAttribute('data-csrf-token');

document.addEventListener('htmx:historyRestore', (evt) => {
  document.querySelectorAll('[x-from-template]').forEach((e) => e.remove())
})

document.body.addEventListener('htmx:configRequest', (event) => {
  event.detail.headers['X-CSRFToken'] = csrfToken
})

document.addEventListener('htmx:afterSettle', (event) => {
  Alpine.initTree(event.target)
})

window.alpineInitialized = false
document.addEventListener('alpine:initialized', () => {
  window.alpineInitialized = true
})

function getDataFromDataset(componentId, dataset) {
  return JSON.parse($byId(componentId).getAttribute(`data-${dataset}`))
}

function setDataset(componentId, dataset, data) {
  $byId(componentId).setAttribute(`data-${dataset}`, data)
}

function loadAlpineComponents(callback) {
  if(window.alpineInitialized) {
    callback()
  } else {
    document.addEventListener('alpine:init', callback)
  }
}
