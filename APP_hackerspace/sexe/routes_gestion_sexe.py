# routes_gestion_sexe.py
# OM 2020.04.06 Gestions des "routes" FLASK pour les sexe.

from flask import render_template, flash, redirect, url_for, request
from APP_hackerspace import obj_mon_application
from APP_hackerspace.sexe.data_gestion_sexe import Gestionsexe
from APP_hackerspace.DATABASE.erreurs import *
# OM 2020.04.10 Pour utiliser les expressions régulières REGEX
import re


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /sexe_afficher
# cela va permettre de programmer les actions avant d'interagir
# avec le navigateur par la méthode "render_template"
# Pour tester http://127.0.0.1:5005/sexe_afficher
# order_by : ASC : Ascendant, DESC : Descendant
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/sexe_afficher/<string:order_by>/<int:id_sexe_sel>", methods=['GET', 'POST'])
def sexe_afficher(order_by,id_sexe_sel):
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_sexe = Gestionsexe()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionsexe()
            # Fichier data_gestion_sexe.py
            # "order_by" permet de choisir l'ordre d'affichage des sexe.
            data_sexe = obj_actions_sexe.sexe_afficher_data(order_by,id_sexe_sel)
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data sexe", data_sexe, "type ", type(data_sexe))

            # Différencier les messages si la table est vide.
            if not data_sexe and id_sexe_sel == 0:
                flash("""La table "t_sexe" est vide. !!""", "warning")
            elif not data_sexe and id_sexe_sel > 0:
                # Si l'utilisateur change l'id_sexe dans l'URL et que le sexe n'existe pas,
                flash(f"Le sexe demandé n'existe pas !!", "warning")
            else:
                # Dans tous les autres cas, c'est que la table "t_sexe" est vide.
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données sexe affichés !!", "success")


        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("sexe/sexe_afficher.html", data=data_sexe)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /sexe_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "sexe_add.html"
# Pour la tester http://127.0.0.1:5005/sexe_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/sexe_add", methods=['GET', 'POST'])
def sexe_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_sexe = Gestionsexe()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "sexe_add.html"
            name_sexe = request.form['name_sexe_html']
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            name_sexe):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")
                # On doit afficher à nouveau le formulaire "sexe_add.html" à cause des erreurs de "claviotage"
                return render_template("sexe/sexe_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_intitule_sexe": name_sexe}
                obj_actions_sexe.add_sexe_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'sexe_afficher', car l'utilisateur
                # doit voir le nouveau sexe qu'il vient d'insérer. Et on l'affiche de manière
                # à voir le dernier élément inséré.
                return redirect(url_for('sexe_afficher', order_by = 'DESC', id_sexe_sel=0))

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
    return render_template("sexe/sexe_add.html")


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /sexe_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un sexe de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/sexe_edit', methods=['POST', 'GET'])
def sexe_edit ():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "sexe_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "id_sexe" du formulaire html "sexe_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_sexe"
            # grâce à la variable "id_sexe_edit_html"
            # <a href="{{ url_for('sexe_edit', id_sexe_edit_html=row.id_sexe) }}">Edit</a>
            id_sexe_edit = request.values['id_sexe_edit_html']

            # Pour afficher dans la console la valeur de "id_sexe_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_sexe_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_id_sexe": id_sexe_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_sexe = Gestionsexe()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_sexe = obj_actions_sexe.edit_sexe_data(valeur_select_dictionnaire)
            print("dataIdsexe ", data_id_sexe, "type ", type(data_id_sexe))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le sexe d'un film !!!", "success")

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

    return render_template("sexe/sexe_edit.html", data=data_id_sexe)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /sexe_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un sexe de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/sexe_update', methods=['POST', 'GET'])
def sexe_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "sexe_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du sexe alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "id_sexe" du formulaire html "sexe_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_sexe"
            # grâce à la variable "id_sexe_edit_html"
            # <a href="{{ url_for('sexe_edit', id_sexe_edit_html=row.id_sexe) }}">Edit</a>
            id_sexe_edit = request.values['id_sexe_edit_html']

            # Récupère le contenu du champ "intitule_sexe" dans le formulaire HTML "sexeEdit.html"
            name_sexe = request.values['name_edit_intitule_sexe_html']
            valeur_edit_list = [{'id_sexe': id_sexe_edit, 'intitule_sexe': name_sexe}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            name_sexe):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "intitule_sexe" dans le formulaire HTML "sexeEdit.html"
                # name_sexe = request.values['name_edit_intitule_sexe_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")

                # On doit afficher à nouveau le formulaire "sexe_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "sexe_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_sexe': 13, 'intitule_sexe': 'philosophique'}]
                valeur_edit_list = [{'id_sexe': id_sexe_edit, 'intitule_sexe': name_sexe}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "sexe_edit.html"
                print(valeur_edit_list, "type ..", type(valeur_edit_list))
                return render_template('sexe/sexe_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_id_sexe": id_sexe_edit, "value_name_sexe": name_sexe}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_sexe = Gestionsexe()

                # La commande MySql est envoyée à la BD
                data_id_sexe = obj_actions_sexe.update_sexe_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdsexe ", data_id_sexe, "type ", type(data_id_sexe))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Valeur sexe modifiée. ", "success")
                # On affiche les sexe avec celui qui vient d'être edité en tête de liste. (DESC)
                return redirect(url_for('sexe_afficher', order_by="ASC", id_sexe_sel=id_sexe_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème sexe ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_sexe_html" alors on renvoie le formulaire "EDIT"
    return render_template('sexe/sexe_edit.html', data=valeur_edit_list)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /sexe_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un sexe de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/sexe_select_delete', methods=['POST', 'GET'])
def sexe_select_delete ():
    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_sexe = Gestionsexe()
            # OM 2019.04.04 Récupère la valeur de "idsexeDeleteHTML" du formulaire html "sexeDelete.html"
            id_sexe_delete = request.args.get('id_sexe_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_sexe": id_sexe_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_sexe = obj_actions_sexe.delete_select_sexe_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur sexe_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur sexe_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('sexe/sexe_delete.html', data=data_id_sexe)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /sexeUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un sexe, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/sexe_delete', methods=['POST', 'GET'])
def sexe_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_sexe = Gestionsexe()
            # OM 2019.04.02 Récupère la valeur de "id_sexe" du formulaire html "sexeAfficher.html"
            id_sexe_delete = request.form['id_sexe_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_sexe": id_sexe_delete}

            data_sexe = obj_actions_sexe.delete_sexe_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des sexe des films
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les sexe
            return redirect(url_for('sexe_afficher',order_by="ASC",id_sexe_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "sexe" de films qui est associé dans "t_sexe_films".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des films !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce sexe est associé à des films dans la t_sexe_films !!! : {erreur}")
                # Afficher la liste des sexe des films
                return redirect(url_for('sexe_afficher', order_by="ASC", id_sexe_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur sexe_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur sexe_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('sexe/sexe_afficher.html', data=data_sexe)