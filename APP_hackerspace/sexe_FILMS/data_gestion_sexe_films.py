# data_gestion_sexe_films.py
# OM 2020.04.22 Permet de gérer (CRUD) les données de la table intermédiaire "t_sexe_films"

from flask import flash
from APP_hackerspace.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_hackerspace.DATABASE.erreurs import *


class GestionsexeFilms():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions sexe")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion sexe films ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionsexeFilms {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionsexeFilms ")

    def sexe_afficher_data (self):
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_sexe"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher
            strsql_sexe_afficher = """SELECT id_sexe, intitule_sexe FROM t_sexe ORDER BY id_sexe ASC"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_sexe_afficher)
                # Récupère les données de la requête.
                data_sexe = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_sexe ", data_sexe, " Type : ", type(data_sexe))
                # Retourne les données du "SELECT"
                return data_sexe
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

    def sexe_films_afficher_data (self, valeur_id_film_selected_dict):
        print("valeur_id_film_selected_dict...", valeur_id_film_selected_dict)
        try:

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_sexe"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_film_selected = """SELECT id_film, nom_film, duree_film, description_film, cover_link_film, date_sortie_film, GROUP_CONCAT(id_sexe) as sexeFilms FROM t_sexe_films AS T1
                                        INNER JOIN t_films AS T2 ON T2.id_film = T1.fk_film
                                        INNER JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe
                                        WHERE id_film = %(value_id_film_selected)s"""

            strsql_sexe_films_non_attribues = """SELECT id_sexe, intitule_sexe FROM t_sexe
                                                    WHERE id_sexe not in(SELECT id_sexe as idsexeFilms FROM t_sexe_films AS T1
                                                    INNER JOIN t_films AS T2 ON T2.id_film = T1.fk_film
                                                    INNER JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe
                                                    WHERE id_film = %(value_id_film_selected)s)"""

            strsql_sexe_films_attribues = """SELECT id_film, id_sexe, intitule_sexe FROM t_sexe_films AS T1
                                            INNER JOIN t_films AS T2 ON T2.id_film = T1.fk_film
                                            INNER JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe
                                            WHERE id_film = %(value_id_film_selected)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_sexe_films_non_attribues, valeur_id_film_selected_dict)
                # Récupère les données de la requête.
                data_sexe_films_non_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("dfad data_sexe_films_non_attribues ", data_sexe_films_non_attribues, " Type : ",
                      type(data_sexe_films_non_attribues))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_film_selected, valeur_id_film_selected_dict)
                # Récupère les données de la requête.
                data_film_selected = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_film_selected  ", data_film_selected, " Type : ", type(data_film_selected))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_sexe_films_attribues, valeur_id_film_selected_dict)
                # Récupère les données de la requête.
                data_sexe_films_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_sexe_films_attribues ", data_sexe_films_attribues, " Type : ",
                      type(data_sexe_films_attribues))

                # Retourne les données du "SELECT"
                return data_film_selected, data_sexe_films_non_attribues, data_sexe_films_attribues
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

    def sexe_films_afficher_data_concat (self, id_film_selected):
        print("id_film_selected  ", id_film_selected)
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_sexe"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_sexe_films_afficher_data_concat = """SELECT id_film, nom_film, duree_film, description_film, cover_link_film, date_sortie_film,
                                                            GROUP_CONCAT(intitule_sexe) as sexeFilms FROM t_sexe_films AS T1
                                                            RIGHT JOIN t_films AS T2 ON T2.id_film = T1.fk_film
                                                            LEFT JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe
                                                            GROUP BY id_film"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # le paramètre 0 permet d'afficher tous les films
                # Sinon le paramètre représente la valeur de l'id du film
                if id_film_selected == 0:
                    mc_afficher.execute(strsql_sexe_films_afficher_data_concat)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_film_selected_dictionnaire = {"value_id_film_selected": id_film_selected}
                    strsql_sexe_films_afficher_data_concat += """ HAVING id_film= %(value_id_film_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_sexe_films_afficher_data_concat, valeur_id_film_selected_dictionnaire)

                # Récupère les données de la requête.
                data_sexe_films_afficher_concat = mc_afficher.fetchall()
                # Affichage dans la console
                print("dggf data_sexe_films_afficher_concat ", data_sexe_films_afficher_concat, " Type : ",
                      type(data_sexe_films_afficher_concat))

                # Retourne les données du "SELECT"
                return data_sexe_films_afficher_concat


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

    def sexe_films_add (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Insérer une (des) nouvelle(s) association(s) entre "id_film" et "id_sexe" dans la "t_sexe_film"
            strsql_insert_sexe_film = """INSERT INTO t_sexe_films (id_sexe_film, fk_sexe, fk_film)
                                            VALUES (NULL, %(value_fk_sexe)s, %(value_fk_film)s)"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_sexe_film, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def sexe_films_delete (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Effacer une (des) association(s) existantes entre "id_film" et "id_sexe" dans la "t_sexe_film"
            strsql_delete_sexe_film = """DELETE FROM t_sexe_films WHERE fk_sexe = %(value_fk_sexe)s AND fk_film = %(value_fk_film)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_delete_sexe_film, valeurs_insertion_dictionnaire)
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème sexe_films_delete Gestions sexe films numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème sexe_films_delete Gestions sexe films  numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème sexe_films_delete Gestions sexe films  {erreur}")

    def edit_sexe_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le sexe sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_sexe = "SELECT id_sexe, intitule_sexe FROM t_sexe WHERE id_sexe = %(value_id_sexe)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_sexe, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_sexe_data Data Gestions sexe numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions sexe numéro de l'erreur : {erreur}", "danger")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_sexe_data d'un sexe Data Gestions sexe {erreur}")

    def update_sexe_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulesexeHTML" du form HTML "sexeEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulesexeHTML" value="{{ row.intitule_sexe }}"/></td>
            str_sql_update_intitulesexe = "UPDATE t_sexe SET intitule_sexe = %(value_name_sexe)s WHERE id_sexe = %(value_id_sexe)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_intitulesexe, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_sexe_data Data Gestions sexe numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions sexe numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_sexe_data d\'un sexe Data Gestions sexe {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "warning")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_sexe_data Data Gestions sexe numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_sexe_data d'un sexe DataGestionssexe {erreur}")

    def delete_select_sexe_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulesexeHTML" du form HTML "sexeEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulesexeHTML" value="{{ row.intitule_sexe }}"/></td>

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le sexe sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_sexe = "SELECT id_sexe, intitule_sexe FROM t_sexe WHERE id_sexe = %(value_id_sexe)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode"mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_id_sexe, valeur_delete_dictionnaire)
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
            print(f"Problème delete_select_sexe_data Gestions sexe numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_sexe_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_sexe_data d\'un sexe Data Gestions sexe {erreur}")

    def delete_sexe_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "sexeEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulesexeHTML" value="{{ row.intitule_sexe }}"/></td>
            str_sql_delete_intitulesexe = "DELETE FROM t_sexe WHERE id_sexe = %(value_id_sexe)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_intitulesexe, valeur_delete_dictionnaire)
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
            print(f"Problème delete_sexe_data Data Gestions sexe numéro de l'erreur : {erreur}")
            flash(f"Flash. Problèmes Data Gestions sexe numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un sexe qui est associé à un film dans la table intermédiaire "t_sexe_films"
                # il y a une contrainte sur les FK de la table intermédiaire "t_sexe_films"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce sexe est associé à des films dans la t_sexe_films !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !!! Ce sexe est associé à des films dans la t_sexe_films !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
