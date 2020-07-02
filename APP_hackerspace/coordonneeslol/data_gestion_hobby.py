# data_gestion_coordonnees.py
# OM 2020.04.09 Permet de gérer (CRUD) les données de la table "coordonnees"
from flask import flash
from APP_hackerspace.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_hackerspace.DATABASE.erreurs import *


class GestionGenres():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions coordonnees")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash(f"Dans Gestion...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionGenres {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur GestionGenres ")

    def coordonnees_afficher_data (self, valeur_order_by, id_coordonnees_sel):
        try:
            print("valeur_order_by ", valeur_order_by, type(valeur_order_by))

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Afficher soit la liste desdans l'ordre inverse ou simplement le genre sélectionné
                # par l'action edit
                if valeur_order_by == "ASC" and id_coordonnees_sel == 0:
                    strsql_coordonnees_afficher = """SELECT id_coordonnees, mail  ORDER BY id_coordonnees ASC"""
                    mc_afficher.execute(strsql_coordonnees_afficher)
                elif valeur_order_by == "ASC":
                    # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * "
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_coordonnees_selected_dictionnaire = {"value_id_coordonnees_selected": id_coordonnees_sel}
                    strsql_coordonnees_afficher = """SELECT id_coordonnees, mail   WHERE id_coordonnees = %(value_id_coordonnees_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_coordonnees_afficher, valeur_id_coordonnees_selected_dictionnaire)
                else:
                    strsql_coordonnees_afficher = """SELECT id_coordonnees, mail  ORDER BY id_coordonnees DESC"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_coordonnees_afficher)
                # Récupère les données de la requête.
                data_coordonnees = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_coordonnees ", data_coordonnees, " Type : ", type(data_coordonnees))
                # Retourne les données du "SELECT"
                return data_coordonnees
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

    def add_coordonnees_data (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            strsql_insert_coordonnees = """INSERT INTO(id_coordonnees,mail) VALUES (NULL,%(value_mail)s)"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_coordonnees, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def edit_coordonnees_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le genre sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_coordonnees = "SELECT id_coordonnees, mail  WHERE id_coordonnees = %(value_id_coordonnees)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_coordonnees, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_coordonnees_data Data Gestionsnuméro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestionsnuméro de l'erreur : {erreur}", "danger")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_coordonnees_data d'un genre Data Gestions{erreur}")

    def update_coordonnees_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleGenreHTML" du form HTML "coordonneesEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleGenreHTML" value="{{ row.mail }}"/></td>
            str_sql_update_intitulegenre = "UPDATESET mail = %(value_name_coordonnees)s WHERE id_coordonnees = %(value_id_coordonnees)s"

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
            print(f"Problème update_coordonnees_data Data Gestionsnuméro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestionsnuméro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_coordonnees_data d\'un genre Data Gestions{}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"'Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_coordonnees_data Data Gestionsnuméro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_coordonnees_data d'un genre DataGestionscoordonnees {erreur}")

    def delete_select_coordonnees_data (self, valeur_delete_dictionnaire):
        try:
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntituleGenreHTML" du form HTML "coordonneesEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleGenreHTML" value="{{ row.mail }}"/></td>

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le genre sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_coordonnees = "SELECT id_coordonnees, mail  WHERE id_coordonnees = %(value_id_coordonnees)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_id_coordonnees, valeur_delete_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)


            # Affiche tous les films qui ont le genre que l'utilisateur veut effacer
            str_sql_coordonnees_films_delete = """SELECT id_coordonnees_film, nom_film, id_coordonnees, mail _films
                                            INNER JOIN personne ON coordonnees_films.fk_personne = personne.id_film
                                            INNER JOINON coordonnees_films.fk_coordonnees = coordonnees.id_coordonnees
                                            WHERE fk_coordonnees = %(value_id_coordonnees)s"""
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_coordonnees_films_delete, valeur_delete_dictionnaire)
                    data_films_attribue_coordonnees_delete = mc_cur.fetchall()
                    print("data_films_attribue_coordonnees_delete...", data_films_attribue_coordonnees_delete)

                    return data_one, data_films_attribue_coordonnees_delete

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème delete_select_coordonnees_data Gestionsnuméro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_coordonnees_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_coordonnees_data d\'un genre Data Gestions{erreur}")

    def delete_coordonnees_data (self, valeur_delete_dictionnaire):
        try:
            print(" delete_coordonnees_data", valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "coordonneesEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntituleGenreHTML" value="{{ row.mail }}"/></td>
            str_sql_delete_films_coordonnees = """DELETE _films WHERE fk_coordonnees = %(value_id_coordonnees)s"""

            str_sql_delete_intitulegenre = "DELETE  WHERE id_coordonnees = %(value_id_coordonnees)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_films_coordonnees, valeur_delete_dictionnaire)
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
            print(f"Problème delete_coordonnees_data Data Gestionsnuméro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestionsnuméro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un genre qui est associé à un film dans la table intermédiaire "coordonnees_films"
                # il y a une contrainte sur les FK de la table intermédiaire "coordonnees_films"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                # flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce genre est associé à des films dans la coordonnees_films !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(
                    f"IMPOSSIBLE d'effacer !!! Ce genre est associé à des films dans la coordonnees_films !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
