import os

# Bind to PORT env variable (Render provides this)
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Workers
workers = 2
threads = 2
worker_class = "sync"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Timeout
timeout = 120
