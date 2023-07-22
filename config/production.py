from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STRIPE_PUBLIC_KEY = 'pk_test_51NVZh4H7qCwTnShMCUwM7uddUM1B6frEoZVOxqxSbYsrAP2kzcfCjtc5HuWIhfS1q5mJHMlikAsfPP6OEOQSKkbp00M2Hp2maQ'
STRIPE_SECRET_KEY = 'sk_test_51NVZh4H7qCwTnShMeTYhEsWGbYNwNAB0L4yJSSuqelqNHTbfNRZuVJ33wo2sGw6eNHLKRBvO2bDjUv2dmv8vqDI600eyPZVwqa'
STRIPE_WEBHOOK_SECRET_TEST = 'whsec_2ae30b3f22574281519a6ff5398e092b2485e97bdd212cef1b54cdd2342950ec' 

YOUR_DOMAIN = 'http://188.120.239.209'