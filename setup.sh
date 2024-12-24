conda deactivate
source venv/bin/activate
filename=logs/$(date +%Y%m%d%H%M%S).log
touch "$filename"
python manage.py runserver 0.0.0.0:8000  > "$filename"

