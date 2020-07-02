# data_gestion_hobby_personne.py
# OM 2020.04.22 Permet de gérer (CRUD) les données de la table intermédiaire "hobby_personne"

from flask import flash
from APP_hackerspace.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_hackerspace.DATABASE.erreurs import *


class GestionGenresFilms():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions genres")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion genres films ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionGenresFilms {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionGenresFilms ")

    def genres_afficher_data (self):
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM hobby"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher
            strsql_genres_afficher = """SELECT id_genre, nom_hobby FROM hobby ORDER BY id_genre ASC"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_genres_afficher)
                # Récupère les données de la requête.
                data_genres = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_genres ", data_genres, " Type : ", type(data_genres))
                # Retourne les données du "SELECT"
                return data_genres
        except pymysql.Error as erreur:
            print(f"DGG gad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGG gad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG gad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGG gad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def hobby_personne_afficher_data (self, valeur_id_personne_selected_dict):
        print("valeur_id_personne_selected_dict...", valeur_id_personne_selected_dict)
        try:

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM hobby"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_film_selected = """SELECT id_personne, nom, prenom, date_naissance, GROUP_CONCAT(id_genre) as GenresFilms FROM hobby_personne AS T1
                                        INNER JOIN personne AS T2 ON T2.id_personne = T1.fk_film
                                        INNER JOIN hobby AS T3 ON T3.id_genre = T1.fk_genre
                                        WHERE id_personne = %(value_id_personne_selected)s"""

            strsql_hobby_personne_non_attribues = """SELECT id_genre, nom_hobby FROM hobby
                                                    WHERE id_genre not in(SELECT id_genre as idGenresFilms FROM hobby_personne AS T1
                                                    INNER JOIN personne AS T2 ON T2.id_personne = T1.fk_film
                                                    INNER JOIN hobby AS T3 ON T3.id_genre = T1.fk_genre
                                                    WHERE id_personne = %(value_id_personne_selected)s)"""

            strsql_hobby_personne_attribues = """SELECT id_personne, id_genre, nom_hobby FROM hobby_personne AS T1
                                            INNER JOIN personne AS T2 ON T2.id_personne = T1.fk_film
                                            INNER JOIN hobby AS T3 ON T3.id_genre = T1.fk_genre
                                            WHERE id_personne = %(value_id_personne_selected)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_hobby_personne_non_attribues, valeur_id_personne_selected_dict)
                # Récupère les données de la requête.
                data_hobby_personne_non_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("dfad data_hobby_personne_non_attribues ", data_hobby_personne_non_attribues, " Type : ",
                      type(data_hobby_personne_non_attribues))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_film_selected, valeur_id_personne_selected_dict)
                # Récupère les données de la requête.
                data_film_selected = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_film_selected  ", data_film_selected, " Type : ", type(data_film_selected))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_hobby_personne_attribues, valeur_id_personne_selected_dict)
                # Récupère les données de la requête.
                data_hobby_personne_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_hobby_personne_attribues ", data_hobby_personne_attribues, " Type : ",
                      type(data_hobby_personne_attribues))

                # Retourne les données du "SELECT"
                return data_film_selected, data_hobby_personne_non_attribues, data_hobby_personne_attribues
        except pymysql.Error as erreur:
            print(f"DGGF gfad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGGF gfad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG gad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGGF gfad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def hobby_personne_afficher_data_concat (self, id_personne_selected):
        print("id_personne_selected  ", id_personne_selected)
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM hobby"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_hobby_personne_afficher_data_concat = """SELECT id_personne, nom, prenom, date_naissance,
                                                            GROUP_CONCAT(nom_hobby) as GenresFilms FROM hobby_personne AS T1
                                                            RIGHT JOIN personne AS T2 ON T2.id_personne = T1.fk_film
                                                            LEFT JOIN hobby AS T3 ON T3.id_genre = T1.fk_genre
                                                            GROUP BY id_personne"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # le paramètre 0 permet d'afficher tous les films
                # Sinon le paramètre représente la valeur de l'id du film
                if id_personne_selected == 0:
                    mc_afficher.execute(strsql_hobby_personne_afficher_data_concat)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_personne_selected_dictionnaire = {"value_id_personne_selected": id_personne_selected}
                    strsql_hobby_personne_afficher_data_concat += """ HAVING id_personne= %(value_id_personne_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_hobby_personne_afficher_data_concat, valeur_id_personne_selected_dictionnaire)

                # Récupère les données de la requête.
                data_hobby_personne_afficher_concat = mc_afficher.fetchall()
                # Affichage dans la console
                print("dggf data_hobby_personne_afficher_concat ", data_hobby_personne_afficher_concat, " Type : ",
                      type(data_hobby_personne_afficher_concat))

                # Retourne les données du "SELECT"
                return data_hobby_personne_afficher_concat


        except pymysql.Error as erreur:
            print(f"DGGF gfadc pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise MaBdErreurPyMySl(
                f"DGG gad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGGF gfadc Exception {erreur.args}")
            raise MaBdErreurConnexion(
                f"DGG gfadc Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans le fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"DGGF gfadc pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def hobby_personne_add (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Insérer une (des) nouvelle(s) association(s) entre "id_personne" et "id_genre" dans la "t_genre_film"
            strsql_insert_genre_film = """INSERT INTO hobby_personne (id_genre_film, fk_genre, fk_film)
                                            VALUES (NULL, %(value_fk_genre)s, %(value_fk_film)s)"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_genre_film, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def hobby_personne_delete (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Effacer une (des) association(s) existantes entre "id_personne" et "id_genre" dans la "t_genre_film"
            strsql_delete_genre_film = """DELETE FROM hobby_personne WHERE fk_genre = %(value_fk_genre)s AND fk_film = %(value_fk_film)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_delete_genre_film, valeurs_insertion_dictionnaire)
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème hobby_personne_delete Gestions Genres films numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème hobby_personne_delete Gestions Genres films  numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème hobby_personne_delete Gestions Genres films  {erreur}")

    def edit_genre_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le genre sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_genre = "SELECT id_genre, nom_hobby FROM hobby WHERE id_genre = %(value_id_genre)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_genre, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_genre_data Data Gestions Genres numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions Genres numéro de l'erreur : {erreur}", "danger")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_genre_data d'un genre Data Gestions Genres {erreur}")

    def update_genre_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleGenreHTML" du form HTML "GenresEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleGenreHTML" value="{{ row.nom_hobby }}"/></td>
            str_sql_update_intitulegenre = "UPDATE hobby SET nom_hobby = %(value_name_genre)s WHERE id_genre = %(value_id_genre)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_genre_data Data Gestions Genres numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions Genres numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_genre_data d\'un genre Data Gestions Genres {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "warning")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_genre_data Data Gestions Genres numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_genre_data d'un genre DataGestionsGenres {erreur}")

    def delete_select_genre_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleGenreHTML" du form HTML "GenresEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleGenreHTML" value="{{ row.nom_hobby }}"/></td>

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le genre sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_genre = "SELECT id_genre, nom_hobby FROM hobby WHERE id_genre = %(value_id_genre)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode"mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_id_genre, valeur_delete_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème delete_select_genre_data Gestions Genres numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_genre_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_genre_data d\'un genre Data Gestions Genres {erreur}")

    def delete_genre_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "GenresEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleGenreHTML" value="{{ row.nom_hobby }}"/></td>
            str_sql_delete_intitulegenre = "DELETE FROM hobby WHERE id_genre = %(value_id_genre)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_intitulegenre, valeur_delete_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème delete_genre_data Data Gestions Genres numéro de l'erreur : {erreur}")
            flash(f"Flash. Problèmes Data Gestions Genres numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un genre qui est associé à un film dans la table intermédiaire "hobby_personne"
                # il y a une contrainte sur les FK de la table intermédiaire "hobby_personne"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce genre est associé à des films dans la hobby_personne !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !!! Ce genre est associé à des films dans la hobby_personne !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
