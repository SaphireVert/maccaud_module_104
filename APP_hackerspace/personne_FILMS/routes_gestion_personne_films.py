# routes_gestion_personne_films.py
# OM 2020.04.16 Gestions des "routes" FLASK pour la table intermédiaire qui associe les films et les personne.

from flask import render_template, request, flash, session
from APP_hackerspace import obj_mon_application
from APP_hackerspace.personne.data_gestion_personne import Gestionpersonne
from APP_hackerspace.personne_FILMS.data_gestion_personne_films import GestionpersonneFilms


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /personne_films_afficher_concat
# Récupère la liste de tous les films et de tous les personne associés aux films.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/personne_films_afficher_concat/<int:id_film_sel>", methods=['GET', 'POST'])
def personne_films_afficher_concat (id_film_sel):
    print("id_film_sel ", id_film_sel)
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personne = GestionpersonneFilms()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionpersonne()
            # Fichier data_gestion_personne.py
            data_personne_films_afficher_concat = obj_actions_personne.nom_films_afficher_data_concat(id_film_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data personne", data_personne_films_afficher_concat, "type ", type(data_personne_films_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_personne_films_afficher_concat:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données personne affichés dans personneFilms!!", "success")
            else:
                flash(f"""Le film demandé n'existe pas. Ou la table "t_personne_films" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("personne_films/personne_films_afficher.html",
                           data=data_personne_films_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.21 Définition d'une "route" /gf_edit_personne_film_selected
# Récupère la liste de tous les personne du film sélectionné.
# Nécessaire pour afficher tous les "TAGS" des personne, ainsi l'utilisateur voit les personne à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_personne_film_selected", methods=['GET', 'POST'])
def gf_edit_personne_film_selected ():
    if request.method == "GET":
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personne = Gestionpersonne()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionpersonne()
            # Fichier data_gestion_personne.py
            # Pour savoir si la table "t_personne" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(personne_films_modifier_tags_dropbox.html)
            data_personne_all = obj_actions_personne.personne_afficher_data('ASC', 0)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_personne = GestionpersonneFilms()

            # OM 2020.04.21 Récupère la valeur de "id_film" du formulaire html "personne_films_afficher.html"
            # l'utilisateur clique sur le lien "Modifier personne de ce film" et on récupère la valeur de "id_film" grâce à la variable "id_film_personne_edit_html"
            # <a href="{{ url_for('gf_edit_personne_film_selected', id_film_personne_edit_html=row.id_film) }}">Modifier les personne de ce film</a>
            id_film_personne_edit = request.values['id_film_personne_edit_html']

            # OM 2020.04.21 Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_film_personne_edit'] = id_film_personne_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_film_selected_dictionnaire = {"value_id_film_selected": id_film_personne_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe GestionpersonneFilms()
            # 1) Sélection du film choisi
            # 2) Sélection des personne "déjà" attribués pour le film.
            # 3) Sélection des personne "pas encore" attribués pour le film choisi.
            # Fichier data_gestion_personne_films.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "personne_films_afficher_data"
            data_personne_film_selected, data_personne_films_non_attribues, data_personne_films_attribues = \
                obj_actions_personne.nom_films_afficher_data(valeur_id_film_selected_dictionnaire)

            lst_data_film_selected = [item['id_film'] for item in data_personne_film_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_film_selected  ", lst_data_film_selected,
                  type(lst_data_film_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les personne qui ne sont pas encore sélectionnés.
            lst_data_personne_films_non_attribues = [item['id_personne'] for item in data_personne_films_non_attribues]
            session['session_lst_data_personne_films_non_attribues'] = lst_data_personne_films_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_personne_films_non_attribues  ", lst_data_personne_films_non_attribues,
                  type(lst_data_personne_films_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les personne qui sont déjà sélectionnés.
            lst_data_personne_films_old_attribues = [item['id_personne'] for item in data_personne_films_attribues]
            session['session_lst_data_personne_films_old_attribues'] = lst_data_personne_films_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_personne_films_old_attribues  ", lst_data_personne_films_old_attribues,
                  type(lst_data_personne_films_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_personne_film_selected", data_personne_film_selected, "type ", type(data_personne_film_selected))
            print(" data data_personne_films_non_attribues ", data_personne_films_non_attribues, "type ",
                  type(data_personne_films_non_attribues))
            print(" data_personne_films_attribues ", data_personne_films_attribues, "type ",
                  type(data_personne_films_attribues))

            # Extrait les valeurs contenues dans la table "t_personne", colonne "intitule_personne"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_personne
            lst_data_personne_films_non_attribues = [item['intitule_personne'] for item in data_personne_films_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_personne gf_edit_personne_film_selected ", lst_data_personne_films_non_attribues,
                  type(lst_data_personne_films_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_film_selected == [None]:
                flash(f"""Le film demandé n'existe pas. Ou la table "t_personne_films" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données personne affichées dans personneFilms!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au serveur.
    return render_template("personne_films/personne_films_modifier_tags_dropbox.html",
                           data_personne=data_personne_all,
                           data_film_selected=data_personne_film_selected,
                           data_personne_attribues=data_personne_films_attribues,
                           data_personne_non_attribues=data_personne_films_non_attribues)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /gf_update_personne_film_selected
# Récupère la liste de tous les personne du film sélectionné.
# Nécessaire pour afficher tous les "TAGS" des personne, ainsi l'utilisateur voit les personne à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_personne_film_selected", methods=['GET', 'POST'])
def gf_update_personne_film_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_film_selected = session['session_id_film_personne_edit']
            print("session['session_id_film_personne_edit'] ", session['session_id_film_personne_edit'])

            # Récupère la liste des personne qui ne sont pas associés au film sélectionné.
            old_lst_data_personne_films_non_attribues = session['session_lst_data_personne_films_non_attribues']
            print("old_lst_data_personne_films_non_attribues ", old_lst_data_personne_films_non_attribues)

            # Récupère la liste des personne qui sont associés au film sélectionné.
            old_lst_data_personne_films_attribues = session['session_lst_data_personne_films_old_attribues']
            print("old_lst_data_personne_films_old_attribues ", old_lst_data_personne_films_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme personne dans le composant "tags-selector-tagselect"
            # dans le fichier "personne_films_modifier_tags_dropbox.html"
            new_lst_str_personne_films = request.form.getlist('name_select_tags')
            print("new_lst_str_personne_films ", new_lst_str_personne_films)

            # OM 2020.04.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_personne_films_old = list(map(int, new_lst_str_personne_films))
            print("new_lst_personne_films ", new_lst_int_personne_films_old, "type new_lst_personne_films ",
                  type(new_lst_int_personne_films_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2020.04.29 Une liste de "id_personne" qui doivent être effacés de la table intermédiaire "t_personne_films".
            lst_diff_personne_delete_b = list(
                set(old_lst_data_personne_films_attribues) - set(new_lst_int_personne_films_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_personne_delete_b ", lst_diff_personne_delete_b)

            # OM 2020.04.29 Une liste de "id_personne" qui doivent être ajoutés à la BD
            lst_diff_personne_insert_a = list(
                set(new_lst_int_personne_films_old) - set(old_lst_data_personne_films_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_personne_insert_a ", lst_diff_personne_insert_a)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personne = GestionpersonneFilms()

            # Pour le film sélectionné, parcourir la liste des personne à INSÉRER dans la "t_personne_films".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_personne_ins in lst_diff_personne_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                # et "id_personne_ins" (l'id du personne dans la liste) associé à une variable.
                valeurs_film_sel_personne_sel_dictionnaire = {"value_fk_film": id_film_selected,
                                                           "value_fk_personne": id_personne_ins}
                # Insérer une association entre un(des) personne(s) et le film sélectionner.
                obj_actions_personne.nom_films_add(valeurs_film_sel_personne_sel_dictionnaire)

            # Pour le film sélectionné, parcourir la liste des personne à EFFACER dans la "t_personne_films".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_personne_del in lst_diff_personne_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                # et "id_personne_del" (l'id du personne dans la liste) associé à une variable.
                valeurs_film_sel_personne_sel_dictionnaire = {"value_fk_film": id_film_selected,
                                                           "value_fk_personne": id_personne_del}
                # Effacer une association entre un(des) personne(s) et le film sélectionner.
                obj_actions_personne.nom_films_delete(valeurs_film_sel_personne_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe Gestionpersonne()
            # Fichier data_gestion_personne.py
            # Afficher seulement le film dont les personne sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_personne_films_afficher_concat = obj_actions_personne.nom_films_afficher_data_concat(id_film_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data personne", data_personne_films_afficher_concat, "type ", type(data_personne_films_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_personne_films_afficher_concat == None:
                flash(f"""Le film demandé n'existe pas. Ou la table "t_personne_films" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données personne affichées dans personneFilms!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "t_personne_films",
    # on affiche les films et le(urs) personne(s) associé(s).
    return render_template("personne_films/personne_films_afficher.html",
                           data=data_personne_films_afficher_concat)
