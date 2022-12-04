from config.settings.components.common import STATICFILES_FINDERS

# Django compressor Settings
COMPRESS_ENABLED = True
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
COMPRESS_OFFLINE = False
STATICFILES_FINDERS += [
    "compressor.finders.CompressorFinder",
]
