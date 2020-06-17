# routes_gestion_sexe_films.py
# OM 2020.04.16 Gestions des "routes" FLASK pour la table intermédiaire qui associe les films et les sexe.

from flask import render_template, request, flash, session
from APP_FILMS import obj_mon_application
from APP_FILMS.sexe.data_gestion_sexe import Gestionsexe
from APP_FILMS.sexe_FILMS.data_gestion_sexe_films import GestionsexeFilms


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /sexe_films_afficher_concat
# Récupère la liste de tous les films et de tous les sexe associés aux films.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/sexe_films_afficher_concat/<int:id_film_sel>", methods=['GET', 'POST'])
def sexe_films_afficher_concat (id_film_sel):
    print("id_film_sel ", id_film_sel)
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_sexe = GestionsexeFilms()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionsexe()
            # Fichier data_gestion_sexe.py
            data_sexe_films_afficher_concat = obj_actions_sexe.sexe_films_afficher_data_concat(id_film_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data sexe", data_sexe_films_afficher_concat, "type ", type(data_sexe_films_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_sexe_films_afficher_concat:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données sexe affichés dans sexeFilms!!", "success")
            else:
                flash(f"""Le film demandé n'existe pas. Ou la table "t_sexe_films" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("sexe_films/sexe_films_afficher.html",
                           data=data_sexe_films_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.21 Définition d'une "route" /gf_edit_sexe_film_selected
# Récupère la liste de tous les sexe du film sélectionné.
# Nécessaire pour afficher tous les "TAGS" des sexe, ainsi l'utilisateur voit les sexe à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_sexe_film_selected", methods=['GET', 'POST'])
def gf_edit_sexe_film_selected ():
    if request.method == "GET":
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_sexe = Gestionsexe()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionsexe()
            # Fichier data_gestion_sexe.py
            # Pour savoir si la table "t_sexe" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(sexe_films_modifier_tags_dropbox.html)
            data_sexe_all = obj_actions_sexe.sexe_afficher_data('ASC', 0)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_sexe = GestionsexeFilms()

            # OM 2020.04.21 Récupère la valeur de "id_film" du formulaire html "sexe_films_afficher.html"
            # l'utilisateur clique sur le lien "Modifier sexe de ce film" et on récupère la valeur de "id_film" grâce à la variable "id_film_sexe_edit_html"
            # <a href="{{ url_for('gf_edit_sexe_film_selected', id_film_sexe_edit_html=row.id_film) }}">Modifier les sexe de ce film</a>
            id_film_sexe_edit = request.values['id_film_sexe_edit_html']

            # OM 2020.04.21 Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_film_sexe_edit'] = id_film_sexe_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_film_selected_dictionnaire = {"value_id_film_selected": id_film_sexe_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe GestionsexeFilms()
            # 1) Sélection du film choisi
            # 2) Sélection des sexe "déjà" attribués pour le film.
            # 3) Sélection des sexe "pas encore" attribués pour le film choisi.
            # Fichier data_gestion_sexe_films.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "sexe_films_afficher_data"
            data_sexe_film_selected, data_sexe_films_non_attribues, data_sexe_films_attribues = \
                obj_actions_sexe.sexe_films_afficher_data(valeur_id_film_selected_dictionnaire)

            lst_data_film_selected = [item['id_film'] for item in data_sexe_film_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_film_selected  ", lst_data_film_selected,
                  type(lst_data_film_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les sexe qui ne sont pas encore sélectionnés.
            lst_data_sexe_films_non_attribues = [item['id_sexe'] for item in data_sexe_films_non_attribues]
            session['session_lst_data_sexe_films_non_attribues'] = lst_data_sexe_films_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_sexe_films_non_attribues  ", lst_data_sexe_films_non_attribues,
                  type(lst_data_sexe_films_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les sexe qui sont déjà sélectionnés.
            lst_data_sexe_films_old_attribues = [item['id_sexe'] for item in data_sexe_films_attribues]
            session['session_lst_data_sexe_films_old_attribues'] = lst_data_sexe_films_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_sexe_films_old_attribues  ", lst_data_sexe_films_old_attribues,
                  type(lst_data_sexe_films_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_sexe_film_selected", data_sexe_film_selected, "type ", type(data_sexe_film_selected))
            print(" data data_sexe_films_non_attribues ", data_sexe_films_non_attribues, "type ",
                  type(data_sexe_films_non_attribues))
            print(" data_sexe_films_attribues ", data_sexe_films_attribues, "type ",
                  type(data_sexe_films_attribues))

            # Extrait les valeurs contenues dans la table "t_sexe", colonne "intitule_sexe"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_sexe
            lst_data_sexe_films_non_attribues = [item['intitule_sexe'] for item in data_sexe_films_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_sexe gf_edit_sexe_film_selected ", lst_data_sexe_films_non_attribues,
                  type(lst_data_sexe_films_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_film_selected == [None]:
                flash(f"""Le film demandé n'existe pas. Ou la table "t_sexe_films" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données sexe affichées dans sexeFilms!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("sexe_films/sexe_films_modifier_tags_dropbox.html",
                           data_sexe=data_sexe_all,
                           data_film_selected=data_sexe_film_selected,
                           data_sexe_attribues=data_sexe_films_attribues,
                           data_sexe_non_attribues=data_sexe_films_non_attribues)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /gf_update_sexe_film_selected
# Récupère la liste de tous les sexe du film sélectionné.
# Nécessaire pour afficher tous les "TAGS" des sexe, ainsi l'utilisateur voit les sexe à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_sexe_film_selected", methods=['GET', 'POST'])
def gf_update_sexe_film_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_film_selected = session['session_id_film_sexe_edit']
            print("session['session_id_film_sexe_edit'] ", session['session_id_film_sexe_edit'])

            # Récupère la liste des sexe qui ne sont pas associés au film sélectionné.
            old_lst_data_sexe_films_non_attribues = session['session_lst_data_sexe_films_non_attribues']
            print("old_lst_data_sexe_films_non_attribues ", old_lst_data_sexe_films_non_attribues)

            # Récupère la liste des sexe qui sont associés au film sélectionné.
            old_lst_data_sexe_films_attribues = session['session_lst_data_sexe_films_old_attribues']
            print("old_lst_data_sexe_films_old_attribues ", old_lst_data_sexe_films_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme sexe dans le composant "tags-selector-tagselect"
            # dans le fichier "sexe_films_modifier_tags_dropbox.html"
            new_lst_str_sexe_films = request.form.getlist('name_select_tags')
            print("new_lst_str_sexe_films ", new_lst_str_sexe_films)

            # OM 2020.04.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_sexe_films_old = list(map(int, new_lst_str_sexe_films))
            print("new_lst_sexe_films ", new_lst_int_sexe_films_old, "type new_lst_sexe_films ",
                  type(new_lst_int_sexe_films_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2020.04.29 Une liste de "id_sexe" qui doivent être effacés de la table intermédiaire "t_sexe_films".
            lst_diff_sexe_delete_b = list(
                set(old_lst_data_sexe_films_attribues) - set(new_lst_int_sexe_films_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_sexe_delete_b ", lst_diff_sexe_delete_b)

            # OM 2020.04.29 Une liste de "id_sexe" qui doivent être ajoutés à la BD
            lst_diff_sexe_insert_a = list(
                set(new_lst_int_sexe_films_old) - set(old_lst_data_sexe_films_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_sexe_insert_a ", lst_diff_sexe_insert_a)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_sexe = GestionsexeFilms()

            # Pour le film sélectionné, parcourir la liste des sexe à INSÉRER dans la "t_sexe_films".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_sexe_ins in lst_diff_sexe_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                # et "id_sexe_ins" (l'id du sexe dans la liste) associé à une variable.
                valeurs_film_sel_sexe_sel_dictionnaire = {"value_fk_film": id_film_selected,
                                                           "value_fk_sexe": id_sexe_ins}
                # Insérer une association entre un(des) sexe(s) et le film sélectionner.
                obj_actions_sexe.sexe_films_add(valeurs_film_sel_sexe_sel_dictionnaire)

            # Pour le film sélectionné, parcourir la liste des sexe à EFFACER dans la "t_sexe_films".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_sexe_del in lst_diff_sexe_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                # et "id_sexe_del" (l'id du sexe dans la liste) associé à une variable.
                valeurs_film_sel_sexe_sel_dictionnaire = {"value_fk_film": id_film_selected,
                                                           "value_fk_sexe": id_sexe_del}
                # Effacer une association entre un(des) sexe(s) et le film sélectionner.
                obj_actions_sexe.sexe_films_delete(valeurs_film_sel_sexe_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe Gestionsexe()
            # Fichier data_gestion_sexe.py
            # Afficher seulement le film dont les sexe sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_sexe_films_afficher_concat = obj_actions_sexe.sexe_films_afficher_data_concat(id_film_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data sexe", data_sexe_films_afficher_concat, "type ", type(data_sexe_films_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_sexe_films_afficher_concat == None:
                flash(f"""Le film demandé n'existe pas. Ou la table "t_sexe_films" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données sexe affichées dans sexeFilms!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "t_sexe_films",
    # on affiche les films et le(urs) sexe(s) associé(s).
    return render_template("sexe_films/sexe_films_afficher.html",
                           data=data_sexe_films_afficher_concat)
