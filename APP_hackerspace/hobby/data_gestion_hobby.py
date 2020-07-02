# data_gestion_hobby.py
# OM 2020.04.09 Permet de gérer (CRUD) les données de la table "hobby"
from flask import flash
from APP_hackerspace.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_hackerspace.DATABASE.erreurs import *


class Gestionhobby():
    def __init__ (self):
        try:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print("dans le try de gestions hobby")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash(f"Dans Gestion hobby ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur Gestionhobby {erreur.args[0]}")
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")
        print("Classe constructeur Gestionhobby ")

    def hobby_afficher_data (self, valeur_order_by, id_hobby_sel):
        try:
            print("valeur_order_by ", valeur_order_by, type(valeur_order_by))

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Afficher soit la liste des hobby dans l'ordre inverse ou simplement le hobby sélectionné
                # par l'action edit
                if valeur_order_by == "ASC" and id_hobby_sel == 0:
                    strsql_hobby_afficher = """SELECT id_hobby, nom_hobby FROM hobby ORDER BY id_hobby ASC"""
                    mc_afficher.execute(strsql_hobby_afficher)
                elif valeur_order_by == "ASC":
                    # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM hobby"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du hobby sélectionné avec un nom de variable
                    valeur_id_hobby_selected_dictionnaire = {"value_id_hobby_selected": id_hobby_sel}
                    strsql_hobby_afficher = """SELECT id_hobby, nom_hobby FROM hobby  WHERE id_hobby = %(value_id_hobby_selected)s"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_hobby_afficher, valeur_id_hobby_selected_dictionnaire)
                else:
                    strsql_hobby_afficher = """SELECT id_hobby, nom_hobby FROM hobby ORDER BY id_hobby DESC"""
                    # Envoi de la commande MySql
                    mc_afficher.execute(strsql_hobby_afficher)
                # Récupère les données de la requête.
                data_hobby = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_hobby ", data_hobby, " Type : ", type(data_hobby))
                # Retourne les données du "SELECT"
                return data_hobby
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

    def add_hobby_data (self, valeurs_insertion_dictionnaire):
        try:
            print(valeurs_insertion_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            strsql_insert_hobby = """INSERT INTO hobby (id_hobby,nom_hobby) VALUES (NULL,%(value_nom_hobby)s)"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(strsql_insert_hobby, valeurs_insertion_dictionnaire)


        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

    def edit_hobby_data (self, valeur_id_dictionnaire):
        try:
            print(valeur_id_dictionnaire)
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le hobby sélectionné dans le tableau dans le formulaire HTML
            str_sql_id_hobby = "SELECT id_hobby, nom_hobby FROM hobby WHERE id_hobby = %(value_id_hobby)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_id_hobby, valeur_id_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)
                    return data_one

        except Exception as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème edit_hobby_data Data Gestions hobby numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions hobby numéro de l'erreur : {erreur}", "danger")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(
                "Raise exception... Problème edit_hobby_data d'un hobby Data Gestions hobby {erreur}")

    def update_hobby_data (self, valeur_update_dictionnaire):
        try:
            print(valeur_update_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulehobbyHTML" du form HTML "hobbyEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulehobbyHTML" value="{{ row.nom_hobby }}"/></td>
            str_sql_update_intitulehobby = "UPDATE hobby SET nom_hobby = %(value_name_hobby)s WHERE id_hobby = %(value_id_hobby)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_update_intitulehobby, valeur_update_dictionnaire)

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
            print(f"Problème update_hobby_data Data Gestions hobby numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions hobby numéro de l'erreur : {erreur}", "danger")
            # raise Exception('Raise exception... Problème update_hobby_data d\'un hobby Data Gestions hobby {}'.format(str(erreur)))
            if erreur.args[0] == 1062:
                flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                flash(f"'Doublon !!! Introduire une valeur différente", "warning")
                # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_hobby_data Data Gestions hobby numéro de l'erreur : {erreur}")

                raise Exception("Raise exception... Problème update_hobby_data d'un hobby DataGestionshobby {erreur}")

    def delete_select_hobby_data (self, valeur_delete_dictionnaire):
        try:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulehobbyHTML" du form HTML "hobbyEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulehobbyHTML" value="{{ row.nom_hobby }}"/></td>

            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # Commande MySql pour afficher le hobby sélectionné dans le tableau dans le formulaire HTML
            str_sql_select_id_hobby = "SELECT id_hobby, nom_hobby FROM hobby WHERE id_hobby = %(value_id_hobby)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_select_id_hobby, valeur_delete_dictionnaire)
                    data_one = mc_cur.fetchall()
                    print("valeur_id_dictionnaire...", data_one)



            # Affiche tous les films qui ont le hobby que l'utilisateur veut effacer
            str_sql_hobby_films_delete = """SELECT id_hobby_personne, nom, prenom, id_hobby, nom_hobby FROM hobby_personne
                                            INNER JOIN personne ON hobby_personne.fk_personne = personne.id_personne
                                            INNER JOIN hobby ON hobby_personne.fk_hobby = hobby.id_hobby
                                            WHERE fk_hobby = %(value_id_hobby)s"""
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_hobby_films_delete, valeur_delete_dictionnaire)
                    data_films_attribue_hobby_delete = mc_cur.fetchall()
                    print("data_films_attribue_hobby_delete...", data_films_attribue_hobby_delete)

                    return data_one, data_films_attribue_hobby_delete

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Problème delete_select_hobby_data Gestions hobby numéro de l'erreur : {erreur}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Flash. Problème delete_select_hobby_data numéro de l'erreur : {erreur}", "danger")
            raise Exception(
                "Raise exception... Problème delete_select_hobby_data d\'un hobby Data Gestions hobby {erreur}")

    def delete_hobby_data (self, valeur_delete_dictionnaire):
        try:
            print(" delete_hobby_data", valeur_delete_dictionnaire)
            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "hobbyEdit.html"
            # le "%s" permet d'éviter des injections SQL "simples"
            # <td><input type = "text" name = "nameEditIntitulehobbyHTML" value="{{ row.nom_hobby }}"/></td>
            str_sql_delete_films_hobby = """DELETE FROM hobby_personne WHERE fk_hobby = %(value_id_hobby)s"""

            str_sql_delete_intitulehobby = "DELETE FROM hobby WHERE id_hobby = %(value_id_hobby)s"

            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
            # sera interprété, ainsi on fera automatiquement un commit
            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                with mconn_bd as mc_cur:
                    mc_cur.execute(str_sql_delete_films_hobby, valeur_delete_dictionnaire)
                    mc_cur.execute(str_sql_delete_intitulehobby, valeur_delete_dictionnaire)
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
            print(f"Problème delete_hobby_data Data Gestions hobby numéro de l'erreur : {erreur}")
            # flash(f"Flash. Problèmes Data Gestions hobby numéro de l'erreur : {erreur}", "danger")
            if erreur.args[0] == 1451:
                # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                # en MySql le moteur INNODB empêche d'effacer un hobby qui est associé à un film dans la table intermédiaire "hobby_personne"
                # il y a une contrainte sur les FK de la table intermédiaire "hobby_personne"
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                # flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce hobby est associé à des films dans la hobby_personne !!! : {erreur}", "danger")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(
                    f"IMPOSSIBLE d'effacer !!! Ce hobby est associé à des films dans la hobby_personne !!! : {erreur}")
            raise MaBdErreurDelete(f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
