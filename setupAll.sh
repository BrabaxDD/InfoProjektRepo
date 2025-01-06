touch "$filename"
rm tmp/runningservers.txt
touch tmp/runningservers.txt
python manage.py runserver 0.0.0.0:8000  > "$filename"

