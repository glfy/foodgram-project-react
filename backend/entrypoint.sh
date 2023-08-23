# #!/bin/bash
# set -e

# python manage.py migrate --noinput
python manage.py load_ingredients
# python manage.py collectstatic --noinput
# cp -r  /app/static/. /static

# exec "$@"
