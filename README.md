# Python Development Tasks

Six standalone projects, organised by level and task. Install optional web-app dependencies with `pip install -r requirements.txt` from this directory.

## Run

- Level 1 tasks: `python number_guessing_game.py` or `python word_counter.py path/to/file.txt`
- Level 2 scraper: `python data_scraper.py https://example.com --selector h1 --output results.csv`
- Level 2 API client: `python api_integration.py bitcoin eur`
- Level 3 Django app: `cd level_3/task_1_django_task_manager && python manage.py migrate && python manage.py runserver`
- Level 3 encryption: `python file_cipher.py encrypt input.txt encrypted.bin` (the generated key is written beside the output). Use `decrypt` with `--key keyfile.key`.

The Django project uses the console email backend for password-reset emails during development. Create an administrator with `python manage.py createsuperuser`.
