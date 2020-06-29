/*
	Toutes les colonnes
*/
SELECT * FROM t_sexe_films AS T1
INNER JOIN t_films AS T2 ON T2.id_film = T1.fk_film
INNER JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe

/*
	Seulement certaines colonnes
*/
SELECT id_sexe, intitule_sexe , id_film, nom_film FROM t_sexe_films AS T1
INNER JOIN t_films AS T2 ON T2.id_film = T1.fk_film
INNER JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe

/* 	
	Permet d'afficher toutes les lignes de la table de droite (t_sexe) (qui est écrite en sql à droite de t_sexe_films)
	y compris les lignes qui ne sont pas attribuées à des films.
*/
SELECT id_sexe, intitule_sexe , id_film, nom_film FROM t_sexe_films AS T1
INNER JOIN t_films AS T2 ON T2.id_film = T1.fk_film
RIGHT JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe

/* 	
	Permet d'afficher toutes les lignes de la table de droite (t_sexe) (qui est écrite en sql à droite de t_sexe_films)
	y compris les lignes qui ne sont pas attribuées à des films.
*/
SELECT id_sexe, intitule_sexe , id_film, nom_film  FROM t_sexe_films AS T1
RIGHT JOIN t_films AS T2 ON T2.id_film = T1.fk_film
LEFT JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe


/*
	Affiche TOUS les films qui n'ont pas de sexe attribués
*/
SELECT id_sexe, intitule_sexe , id_film, nom_film  FROM t_sexe_films AS T1
RIGHT JOIN t_films AS T2 ON T2.id_film = T1.fk_film
LEFT JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe


/*
	Affiche SEULEMENT les films qui n'ont pas de sexe attribués
*/

SELECT id_sexe, intitule_sexe , id_film, nom_film  FROM t_sexe_films AS T1
RIGHT JOIN t_films AS T2 ON T2.id_film = T1.fk_film
LEFT JOIN t_sexe AS T3 ON T3.id_sexe = T1.fk_sexe
WHERE T1.fk_sexe IS NULL
