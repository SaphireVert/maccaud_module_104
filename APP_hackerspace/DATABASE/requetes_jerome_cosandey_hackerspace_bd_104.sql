/*
	Toutes les colonnes
*/
SELECT * FROM t_personne_films AS T1
INNER JOINAS T2 ON T2.id_coordonnees = T1.fk_film
INNER JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne

/*
	Seulement certaines colonnes
*/
SELECT id_personne, intitule_personne , id_coordonnees, telephone FROM t_personne_films AS T1
INNER JOINAS T2 ON T2.id_coordonnees = T1.fk_film
INNER JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne

/* 	
	Permet d'afficher toutes les lignes de la table de droite (t_personne) (qui est écrite en sql à droite de t_personne_films)
	y compris les lignes qui ne sont pas attribuées à des films.
*/
SELECT id_personne, intitule_personne , id_coordonnees, telephone FROM t_personne_films AS T1
INNER JOINAS T2 ON T2.id_coordonnees = T1.fk_film
RIGHT JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne

/* 	
	Permet d'afficher toutes les lignes de la table de droite (t_personne) (qui est écrite en sql à droite de t_personne_films)
	y compris les lignes qui ne sont pas attribuées à des films.
*/
SELECT id_personne, intitule_personne , id_coordonnees, telephone  FROM t_personne_films AS T1
RIGHT JOINAS T2 ON T2.id_coordonnees = T1.fk_film
LEFT JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne


/*
	Affiche TOUS les films qui n'ont pas de personne attribués
*/
SELECT id_personne, intitule_personne , id_coordonnees, telephone  FROM t_personne_films AS T1
RIGHT JOINAS T2 ON T2.id_coordonnees = T1.fk_film
LEFT JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne


/*
	Affiche SEULEMENT les films qui n'ont pas de personne attribués
*/

SELECT id_personne, intitule_personne , id_coordonnees, telephone  FROM t_personne_films AS T1
RIGHT JOINAS T2 ON T2.id_coordonnees = T1.fk_film
LEFT JOIN t_personne AS T3 ON T3.id_personne = T1.fk_personne
WHERE T1.fk_personne IS NULL
