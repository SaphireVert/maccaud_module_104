# Un objet "obj_mon_application" pour utiliser la classe Flask
# Pour les personnes qui veulent savoir ce que signifie __name__ une démonstration se trouve ici :
# https://www.studytonight.com/python/_name_-as-main-method-in-python
# __name__ garantit que la méthode run() est appelée uniquement lorsque main.py est exécuté en tant que programme principal.
# La méthode run() ne sera pas appelée si vous importez main.py dans un autre module Python.
from flask import Flask
from APP_FILMS.DATABASE import connect_db_context_manager


# Objet qui fait "exister" notre application
obj_mon_application = Flask(__name__, template_folder="templates")
# Flask va pouvoir crypter les cookies
obj_mon_application.secret_key = '_vogonAmiral_)?^'

# Doit se trouver ici... soit après l'instanciation de la classe "Flask"
# OM 2020.03.25 Tout commence ici par "indiquer" les routes de l'application.
from APP_FILMS import routes
from APP_FILMS.FILMS import routes_gestion_films
from APP_FILMS.GENRES import routes_gestion_genres
from APP_FILMS.GENRES_FILMS import routes_gestion_genres_films
