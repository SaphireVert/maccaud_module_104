# data_gestion_personne_films.py
# OM 2020.04.22 Permet de gérer (CRUD) les données de la table intermédiaire "t_personne_films"

from flask import flash
from APP_hackerspace.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_hackerspace.DATABASE.erreurs import *


class GestionpersonneFilms():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions personne")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion personne films ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionpersonneFilms {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionpersonneFilms ")

    def personne_afficher_data (self):
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_personne"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher
            strsql_personne_afficher = """SELECT id_personne, intitule_personne FROM t_personne ORDER BY id_personne ASC"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_personne_afficher)
                # Récupère les données de la requête.
                data_personne = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_personne ", data_personne, " Type : ", type(data_personne))
                # Retourne les données du "SELECT"
                return data_personne
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

    def personne_coordonnees_afficher_data (self, valeur_id_film_selected_dict):
        print("valeur_id_film_selected_dict...", valeur_id_film_selected_dict)
        try:

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_personne"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_film_selected = """SELECT id_film, nom_film, duree_film, description_film, cover_link_film, date_sortie_film, GROUP_CONCAT(id_personne) as personneFilms FROM t_personne_films AS T1
                                        INNER JOIN t_films AS T2 ON T2.id_film = T1.fk_film
                                        INNER JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne
                                        WHERE id_film = %(value_id_film_selected)s"""

            strsql_personne_films_non_attribues = """SELECT id_personne, intitule_personne FROM t_personne
                                                    WHERE id_personne not in(SELECT id_personne as idpersonneFilms FROM t_personne_films AS T1
                                                    INNER JOIN t_films AS T2 ON T2.id_film = T1.fk_film
                                                    INNER JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne
                                                    WHERE id_film = %(value_id_film_selected)s)"""

            strsql_personne_films_attribues = """SELECT id_film, id_personne, intitule_personne FROM t_personne_films AS T1
                                            INNER JOIN t_films AS T2 ON T2.id_film = T1.fk_film
                                            INNER JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne
                                            WHERE id_film = %(value_id_film_selected)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_personne_films_non_attribues, valeur_id_film_selected_dict)
                # Récupère les données de la requête.
                data_personne_films_non_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("dfad data_personne_films_non_attribues ", data_personne_films_non_attribues, " Type : ",
                      type(data_personne_films_non_attribues))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_film_selected, valeur_id_film_selected_dict)
                # Récupère les données de la requête.
                data_film_selected = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_film_selected  ", data_film_selected, " Type : ", type(data_film_selected))

                # Envoi de la commande MySql
                mc_afficher.execute(strsql_personne_films_attribues, valeur_id_film_selected_dict)
                # Récupère les données de la requête.
                data_personne_films_attribues = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_personne_films_attribues ", data_personne_films_attribues, " Type : ",
                      type(data_personne_films_attribues))

                # Retourne les données du "SELECT"
                return data_film_selected, data_personne_films_non_attribues, data_personne_films_attribues
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

    def personne_coordonnees_afficher_data_concat (self, id_film_selected):
        print("id_film_selected  ", id_film_selected)
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_personne"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher

            strsql_personne_coordonnees_afficher_data_concat = """SELECT id_film, nom_film, duree_film, description_film, cover_link_film, date_sortie_film,
                                                            GROUP_CONCAT(intitule_personne) as personneFilms FROM t_personne_films AS T1
                                                            RIGHT JOIN t_films AS T2 ON T2.id_film = T1.fk_film
                                                            LEFT JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne
                                                            GROUP BY id_film"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # le paramètre 0 permet d'afficher tous les films
                # Sinon le paramètre représente la valeur de l'id du film
                if id_film_selected == 0:
                    mc_afficher.execute(strsql_personne_coordonnees_afficher_data_concat)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_film_selected_dictionnaire = {"value_id_film_selected": id_film_selected}
                    strsql_personne_coordonnees_afficher_data_concat += """ HAVING id_film= %(value_id_film_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_personne_coordonnees_afficher_data_concat, valeur_id_film_selected_dictionnaire)

                # Récupère les données de la requête.
                data_personne_coordonnees_afficher_concat = mc_afficher.fetchall()
                # Affichage dans la console
                print("dggf data_personne_coordonnees_afficher_concat ", data_personne_coordonnees_afficher_concat, " Type : ",
                      type(data_personne_coordonnees_afficher_concat))

                # Retourne les données du "SELECT"
                return data_personne_coordonnees_afficher_concat


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

    def personne_films_add (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Insérer une (des) nouvelle(s) association(s) entre "id_film" et "id_personne" dans la "t_personne_film"
            strsql_insert_personne_film = """INSERT INTO t_personne_films (id_personne_film, fk_personne, fk_film)
                                            VALUES (NULL, %(value_fk_personne)s, %(value_fk_film)s)"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_personne_film, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def personne_films_delete (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Effacer une (des) association(s) existantes entre "id_film" et "id_personne" dans la "t_personne_film"
            strsql_delete_personne_film = """DELETE FROM t_personne_films WHERE fk_personne = %(value_fk_personne)s AND fk_film = %(value_fk_film)s"""

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_delete_personne_film, valeurs_insertion_dictionnaire)
        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème personne_films_delete Gestions personne films numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème personne_films_delete Gestions personne films  numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème personne_films_delete Gestions personne films  {erreur}")

    def edit_personne_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le personne sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_personne = "SELECT id_personne, intitule_personne FROM t_personne WHERE id_personne = %(value_id_personne)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_personne, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_personne_data Data Gestions personne numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions personne numéro de l'erreur : {erreur}", "danger")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_personne_data d'un personne Data Gestions personne {erreur}")

    def update_personne_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulepersonneHTML" du form HTML "personneEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulepersonneHTML" value="{{ row.intitule_personne }}"/></td>
            str_sql_update_intitulepersonne = "UPDATE t_personne SET intitule_personne = %(value_name_personne)s WHERE id_personne = %(value_id_personne)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_intitulepersonne, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_personne_data Data Gestions personne numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions personne numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_personne_data d\'un personne Data Gestions personne {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "warning")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_personne_data Data Gestions personne numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_personne_data d'un personne DataGestionspersonne {erreur}")

    def delete_select_personne_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulepersonneHTML" du form HTML "personneEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulepersonneHTML" value="{{ row.intitule_personne }}"/></td>

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le personne sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_personne = "SELECT id_personne, intitule_personne FROM t_personne WHERE id_personne = %(value_id_personne)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode"mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_id_personne, valeur_delete_dictionnaire)
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
            print(f"Problème delete_select_personne_data Gestions personne numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_personne_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_personne_data d\'un personne Data Gestions personne {erreur}")

    def delete_personne_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "personneEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulepersonneHTML" value="{{ row.intitule_personne }}"/></td>
            str_sql_delete_intitulepersonne = "DELETE FROM t_personne WHERE id_personne = %(value_id_personne)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_intitulepersonne, valeur_delete_dictionnaire)
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
            print(f"Problème delete_personne_data Data Gestions personne numéro de l'erreur : {erreur}")
            flash(f"Flash. Problèmes Data Gestions personne numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un personne qui est associé à un film dans la table intermédiaire "t_personne_films"
                # il y a une contrainte sur les FK de la table intermédiaire "t_personne_films"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce personne est associé à des films dans la t_personne_films !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !!! Ce personne est associé à des films dans la t_personne_films !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
