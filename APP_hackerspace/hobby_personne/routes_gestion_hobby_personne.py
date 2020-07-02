# routes_gestion_hobby_personne.py
# OM 2020.04.16 Gestions des "routes" FLASK pour la table intermédiaire qui associe les films et les genres.

from flask import render_template, request, flash, session
from APP_hackerspace import obj_mon_application
from APP_hackerspace.hobby.data_gestion_hobby import Gestionhobby
from APP_hackerspace.hobby_personne.data_gestion_hobby_personne import GestionGenresFilms


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /hobby_personne_afficher_concat
# Récupère la liste de tous les films et de tous les genres associés aux films.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/hobby_personne_afficher_concat/<int:id_personne_sel>", methods=['GET', 'POST'])
def hobby_personne_afficher_concat (id_personne_sel):
    print("id_personne_sel ", id_personne_sel)
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_genres = GestionGenresFilms()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionGenres()
            # Fichier data_gestion_genres.py
            data_hobby_personne_afficher_concat = obj_actions_genres.hobby_personne_afficher_data_concat(id_personne_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data genres", data_hobby_personne_afficher_concat, "type ", type(data_hobby_personne_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_hobby_personne_afficher_concat:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données genres affichés dans GenresFilms!!", "success")
            else:
                flash(f"""Le film demandé n'existe pas. Ou la table "hobby_personne" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("hobby_personne/hobby_personne_afficher.html",
                           data=data_hobby_personne_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.21 Définition d'une "route" /gf_edit_genre_film_selected
# Récupère la liste de tous les genres du film sélectionné.
# Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_genre_film_selected", methods=['GET', 'POST'])
def gf_edit_genre_film_selected ():
    if request.method == "GET":
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_genres = GestionGenres()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionGenres()
            # Fichier data_gestion_genres.py
            # Pour savoir si la table "hobby" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(hobby_personne_modifier_tags_dropbox.html)
            data_genres_all = obj_actions_genres.genres_afficher_data('ASC', 0)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_genres = GestionGenresFilms()

            # OM 2020.04.21 Récupère la valeur de "id_personne" du formulaire html "hobby_personne_afficher.html"
            # l'utilisateur clique sur le lien "Modifier genres de ce film" et on récupère la valeur de "id_personne" grâce à la variable "id_personne_genres_edit_html"
            # <a href="{{ url_for('gf_edit_genre_film_selected', id_personne_genres_edit_html=row.id_personne) }}">Modifier les genres de ce film</a>
            id_personne_genres_edit = request.values['id_personne_genres_edit_html']

            # OM 2020.04.21 Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_personne_genres_edit'] = id_personne_genres_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_personne_selected_dictionnaire = {"value_id_personne_selected": id_personne_genres_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe GestionGenresFilms()
            # 1) Sélection du film choisi
            # 2) Sélection des genres "déjà" attribués pour le film.
            # 3) Sélection des genres "pas encore" attribués pour le film choisi.
            # Fichier data_gestion_hobby_personne.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "hobby_personne_afficher_data"
            data_genre_film_selected, data_hobby_personne_non_attribues, data_hobby_personne_attribues = \
                obj_actions_genres.hobby_personne_afficher_data(valeur_id_personne_selected_dictionnaire)

            lst_data_film_selected = [item['id_personne'] for item in data_genre_film_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_film_selected  ", lst_data_film_selected,
                  type(lst_data_film_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui ne sont pas encore sélectionnés.
            lst_data_hobby_personne_non_attribues = [item['id_genre'] for item in data_hobby_personne_non_attribues]
            session['session_lst_data_hobby_personne_non_attribues'] = lst_data_hobby_personne_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_hobby_personne_non_attribues  ", lst_data_hobby_personne_non_attribues,
                  type(lst_data_hobby_personne_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui sont déjà sélectionnés.
            lst_data_hobby_personne_old_attribues = [item['id_genre'] for item in data_hobby_personne_attribues]
            session['session_lst_data_hobby_personne_old_attribues'] = lst_data_hobby_personne_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_hobby_personne_old_attribues  ", lst_data_hobby_personne_old_attribues,
                  type(lst_data_hobby_personne_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_genre_film_selected", data_genre_film_selected, "type ", type(data_genre_film_selected))
            print(" data data_hobby_personne_non_attribues ", data_hobby_personne_non_attribues, "type ",
                  type(data_hobby_personne_non_attribues))
            print(" data_hobby_personne_attribues ", data_hobby_personne_attribues, "type ",
                  type(data_hobby_personne_attribues))

            # Extrait les valeurs contenues dans la table "hobby", colonne "nom_hobby"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_genre
            lst_data_hobby_personne_non_attribues = [item['nom_hobby'] for item in data_hobby_personne_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_genres gf_edit_genre_film_selected ", lst_data_hobby_personne_non_attribues,
                  type(lst_data_hobby_personne_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_film_selected == [None]:
                flash(f"""Le film demandé n'existe pas. Ou la table "hobby_personne" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données genres affichées dans GenresFilms!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("hobby_personne/hobby_personne_modifier_tags_dropbox.html",
                           data_genres=data_genres_all,
                           data_film_selected=data_genre_film_selected,
                           data_genres_attribues=data_hobby_personne_attribues,
                           data_genres_non_attribues=data_hobby_personne_non_attribues)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /gf_update_genre_film_selected
# Récupère la liste de tous les genres du film sélectionné.
# Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_genre_film_selected", methods=['GET', 'POST'])
def gf_update_genre_film_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_personne_selected = session['session_id_personne_genres_edit']
            print("session['session_id_personne_genres_edit'] ", session['session_id_personne_genres_edit'])

            # Récupère la liste des genres qui ne sont pas associés au film sélectionné.
            old_lst_data_hobby_personne_non_attribues = session['session_lst_data_hobby_personne_non_attribues']
            print("old_lst_data_hobby_personne_non_attribues ", old_lst_data_hobby_personne_non_attribues)

            # Récupère la liste des genres qui sont associés au film sélectionné.
            old_lst_data_hobby_personne_attribues = session['session_lst_data_hobby_personne_old_attribues']
            print("old_lst_data_hobby_personne_old_attribues ", old_lst_data_hobby_personne_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "hobby_personne_modifier_tags_dropbox.html"
            new_lst_str_hobby_personne = request.form.getlist('name_select_tags')
            print("new_lst_str_hobby_personne ", new_lst_str_hobby_personne)

            # OM 2020.04.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_inhobby_personne_old = list(map(int, new_lst_str_hobby_personne))
            print("new_lshobby_personne ", new_lst_inhobby_personne_old, "type new_lshobby_personne ",
                  type(new_lst_inhobby_personne_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2020.04.29 Une liste de "id_genre" qui doivent être effacés de la table intermédiaire "hobby_personne".
            lst_diff_genres_delete_b = list(
                set(old_lst_data_hobby_personne_attribues) - set(new_lst_inhobby_personne_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_genres_delete_b ", lst_diff_genres_delete_b)

            # OM 2020.04.29 Une liste de "id_genre" qui doivent être ajoutés à la BD
            lst_diff_genres_insert_a = list(
                set(new_lst_inhobby_personne_old) - set(old_lst_data_hobby_personne_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_genres_insert_a ", lst_diff_genres_insert_a)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_genres = GestionGenresFilms()

            # Pour le film sélectionné, parcourir la liste des genres à INSÉRER dans la "hobby_personne".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_genre_ins in lst_diff_genres_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                # et "id_genre_ins" (l'id du genre dans la liste) associé à une variable.
                valeurs_film_sel_genre_sel_dictionnaire = {"value_FK_personne": id_personne_selected,
                                                           "value_fk_genre": id_genre_ins}
                # Insérer une association entre un(des) genre(s) et le film sélectionner.
                obj_actions_genres.hobby_personne_add(valeurs_film_sel_genre_sel_dictionnaire)

            # Pour le film sélectionné, parcourir la liste des genres à EFFACER dans la "hobby_personne".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_genre_del in lst_diff_genres_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                valeurs_film_sel_genre_sel_dictionnaire = {"value_FK_personne": id_personne_selected,
                                                           "value_fk_genre": id_genre_del}
                # Effacer une association entre un(des) genre(s) et le film sélectionner.
                obj_actions_genres.hobby_personne_delete(valeurs_film_sel_genre_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe GestionGenres()
            # Fichier data_gestion_genres.py
            # Afficher seulement le film dont les genres sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_hobby_personne_afficher_concat = obj_actions_genres.hobby_personne_afficher_data_concat(id_personne_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data genres", data_hobby_personne_afficher_concat, "type ", type(data_hobby_personne_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_hobby_personne_afficher_concat == None:
                flash(f"""Le film demandé n'existe pas. Ou la table "hobby_personne" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données genres affichées dans GenresFilms!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "hobby_personne",
    # on affiche les films et le(urs) genre(s) associé(s).
    return render_template("hobby_personne/hobby_personne_afficher.html",
                           data=data_hobby_personne_afficher_concat)
