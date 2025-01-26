from flask import Flask, render_template, request, abort

from googleapiclient.discovery import build
from google.oauth2 import service_account

from apscheduler.schedulers.background import BackgroundScheduler

import random

app = Flask(__name__)

# In-memory cache
content_cache = {}
# To make sure the scheduler is only running one instance
appHasRunBefore = False


def refresh_content_cache(encoding='utf-8'):
  # Set up credentials
  SERVICE_ACCOUNT_FILE = 'credentials.json'
  SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
  credentials = service_account.Credentials.from_service_account_file(
      SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  FILE_ID = '1-mkNdY_PYf-FxQlV1Be0dvCvjHEdkBmn'

  # Build the Drive service
  service = build('drive', 'v3', credentials=credentials)

  request = service.files().get_media(fileId=FILE_ID)
  content_bytes = request.execute()

  try:
    content_str = content_bytes.decode(encoding)
  except UnicodeDecodeError:
    print(f"Error: Could not decode content using encoding {encoding}")
    return

  # Update the in-memory cache
  parse_markdown(content_str)


def parse_markdown(content_str: str):
  # Reset the cache
  content_cache['content'] = content_str
  content_cache['goals'] = []
  content_cache['week'] = []
  content_cache['meditations'] = []

  lines = [lin.strip() for lin in content_str.split('\n') if lin.strip()]

  current_key = None

  for line in lines:
    if line.startswith('#'):
      current_key = line.lstrip('#').strip().lower()
      content_cache[current_key] = []
    elif line.startswith('-') and current_key:
      content_cache[current_key].append(line.lstrip('-').strip())


@app.route('/')
def index():
  token = request.args.get('token')
  if token != 'testtoken':
    abort(403)

  num_pairs = len(content_cache.get('meditations', [])) // 2
  pair_index = random.randint(0, num_pairs - 1) if num_pairs > 0 else 0
  meditation = {}
  if num_pairs > 0:
    meditation['title'] = content_cache['meditations'][2 * pair_index]
    meditation['body'] = content_cache['meditations'][2 * pair_index + 1]

  # Render the index.html template
  return render_template('index.html',
                         goals=content_cache['goals'],
                         week=content_cache['week'],
                         meditation=meditation)


# Launch the scheduler
with app.app_context():
  if not appHasRunBefore:
    appHasRunBefore = True
    refresh_content_cache()
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(refresh_content_cache, 'interval', minutes=5)
    scheduler.start()


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8087, debug=True)
