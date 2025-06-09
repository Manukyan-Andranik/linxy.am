import os
PORT=8080
bind = f"0.0.0.0:{PORT}"
workers = os.cpu_count() * 2 + 1
timeout = 120
loglevel = "info"
accesslog = "-"
errorlog = "-"