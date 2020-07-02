# routes_gestion_genres.py
# OM 2020.04.06 Gestions des "routes" FLASK pour les genres.

from flask import render_template, flash, redirect, url_for, request, session
from APP_hackerspace import obj_mon_application
from APP_hackerspace.hobby.data_gestion_hobby import GestionGenres
from APP_hackerspace.DATABASE.erreurs import *
# OM 2020.04.10 Pour utiliser les expressions régulières REGEX
import re


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /genres_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:5005/genres_afficher
# order_by : ASC : Ascendant, DESC : Descendant
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/genres_afficher/<string:order_by>/<int:id_hobby_sel>", methods=['GET', 'POST'])
def hobby_afficher(order_by,id_hobby_sel):
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_genres = GestionGenres()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionGenres()
            # Fichier data_gestion_genres.py
            # "order_by" permet de choisir l'ordre d'affichage des genres.
            data_genres = obj_actions_genres.genres_afficher_data(order_by,id_hobby_sel)
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data genres", data_genres, "type ", type(data_genres))

            # Différencier les messages si la table est vide.
            if not data_genres and id_hobby_sel == 0:
                flash("""La table "hobby" est vide. !!""", "warning")
            elif not data_genres and id_hobby_sel > 0:
                # Si l'utilisateur change l'id_hobby dans l'URL et que le genre n'existe pas,
                flash(f"Le genre demandé n'existe pas !!", "warning")
            else:
                # Dans tous les autres cas, c'est que la table "hobby" est vide.
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données genres affichés !!", "success")


        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("hobby/hobby_afficher.html", data=data_genres)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /genres_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "genres_add.html"
# Pour la tester http://127.0.0.1:5005/genres_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/genres_add", methods=['GET', 'POST'])
def genres_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_genres = GestionGenres()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "genres_add.html"
            name_genre = request.form['name_hobby_html']
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            name_genre):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")
                # On doit afficher à nouveau le formulaire "genres_add.html" à cause des erreurs de "claviotage"
                return render_template("hobby/hobby_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_nom_hobby": name_genre}
                obj_actions_genres.add_genre_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'genres_afficher', car l'utilisateur
                # doit voir le nouveau genre qu'il vient d'insérer. Et on l'affiche de manière
                # à voir le dernier élément inséré.
                return redirect(url_for('hobby_afficher', order_by = 'DESC', id_hobby_sel=0))

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"RGG pei {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur:
            flash(f"Autre erreur {erreur}", "danger")
            raise MonErreur(f"Autre erreur")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except Exception as erreur:
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(
                f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']} et son status {msg_erreurs['ErreurConnexionBD']['status']}")
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("hobby/hobby_add.html")


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /genres_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un genre de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/genres_edit', methods=['POST', 'GET'])
def genres_edit ():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "genres_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "id_hobby" du formulaire html "genres_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_hobby"
            # grâce à la variable "id_hobby_edit_html"
            # <a href="{{ url_for('genres_edit', id_hobby_edit_html=row.id_hobby) }}">Edit</a>
            id_hobby_edit = request.values['id_hobby_edit_html']

            # Pour afficher dans la console la valeur de "id_hobby_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_hobby_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_id_hobby": id_hobby_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_genres = GestionGenres()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_hobby = obj_actions_genres.edit_genre_data(valeur_select_dictionnaire)
            print("dataIdGenre ", data_id_hobby, "type ", type(data_id_hobby))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le genre d'un film !!!", "success")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            # On indique un problème, mais on ne dit rien en ce qui concerne la résolution.
            print("Problème avec la BD ! : %s", erreur)
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']}"
                                      f"et son status {msg_erreurs['ErreurConnexionBD']['status']}")

    return render_template("hobby/hobby_edit.html", data=data_id_hobby)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /hobby_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un genre de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/hobby_update', methods=['POST', 'GET'])
def hobby_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "genres_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du genre alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "id_hobby" du formulaire html "genres_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_hobby"
            # grâce à la variable "id_hobby_edit_html"
            # <a href="{{ url_for('genres_edit', id_hobby_edit_html=row.id_hobby) }}">Edit</a>
            id_hobby_edit = request.values['id_hobby_edit_html']

            # Récupère le contenu du champ "nom_hobby" dans le formulaire HTML "GenresEdit.html"
            name_hobby = request.values['name_edit_nom_hobby_html']
            valeur_edit_list = [{'id_hobby': id_hobby_edit, 'nom_hobby': name_hobby}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            name_hobby):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "nom_hobby" dans le formulaire HTML "GenresEdit.html"
                # name_genre = request.values['name_edit_nom_hobby_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")

                # On doit afficher à nouveau le formulaire "genres_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "genres_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_hobby': 13, 'nom_hobby': 'philosophique'}]
                valeur_edit_list = [{'id_hobby': id_hobby_edit, 'nom_hobby': name_hobby}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "genres_edit.html"
                print(valeur_edit_list, "type ..", type(valeur_edit_list))
                return render_template('hobby/hobby_edit.html ', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_id_hobby": id_hobby_edit, "value_name_genre": name_hobby}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_genres = GestionGenres()

                # La commande MySql est envoyée à la BD
                data_id_hobby = obj_actions_genres.update_genre_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdGenre ", data_id_hobby, "type ", type(data_id_hobby))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Valeur genre modifiée. ", "success")
                # On affiche les genres avec celui qui vient d'être edité en tête de liste. (DESC)
                return redirect(url_for('hobby_afficher', order_by="ASC", id_hobby_sel=id_hobby_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème genres ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_nom_hobby_html" alors on renvoie le formulaire "EDIT"
    return render_template('hobby/hobby_edit.html ', data=valeur_edit_list)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /genres_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un genre de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/genres_select_delete', methods=['POST', 'GET'])
def genres_select_delete ():
    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_genres = GestionGenres()
            # OM 2019.04.04 Récupère la valeur de "idGenreDeleteHTML" du formulaire html "GenresDelete.html"
            id_hobby_delete = request.args.get('id_hobby_delete_html')
            # OM 2020.04.21 Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_hobby_delete'] = id_hobby_delete

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_hobby": id_hobby_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_hobby, films_associes_genre_delete  = obj_actions_genres.delete_select_genre_data(valeur_delete_dictionnaire)
            print("data_films_attribue_genre_delete ",films_associes_genre_delete," data_id_hobby ",data_id_hobby)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur genres_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur genres_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('hobby/hobby_delete.html',
                           data=data_id_hobby,
                           data_films_associes = films_associes_genre_delete)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /genresUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un genre, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/genres_delete', methods=['POST', 'GET'])
def genres_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_genres = GestionGenres()
            # OM 2019.04.02 Récupère la valeur de "id_hobby" par une variable de session de "genres_select_delete"
            id_hobby_delete = session['session_id_hobby_delete']
            print(" genres_delete id_hobby_delete ", id_hobby_delete)
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_hobby": id_hobby_delete}

            data_genres = obj_actions_genres.delete_genre_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des genres des films
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les genres
            return redirect(url_for('genres_afficher',order_by="ASC",id_hobby_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "genre" de films qui est associé dans "hobby_personne".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des films !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce genre est associé à des films dans la hobby_personne !!! : {erreur}")
                # Afficher la liste des genres des films
                return redirect(url_for('genres_afficher', order_by="ASC", id_hobby_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur genres_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur genres_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('hobby/hobby_afficher.html', data=data_genres)
