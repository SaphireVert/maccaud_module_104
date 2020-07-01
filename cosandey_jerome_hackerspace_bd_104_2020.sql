-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Mer 01 Juillet 2020 à 17:41
-- Version du serveur :  5.7.11
-- Version de PHP :  5.6.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `cosandey_jerome_hackerspace_bd_104_2020`
--

-- --------------------------------------------------------

--
-- Structure de la table `coordonnees`
--

CREATE TABLE `coordonnees` (
  `id_coordonnees` int(11) NOT NULL,
  `telephone` int(11) NOT NULL,
  `mail` text NOT NULL,
  `adresse` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `coordonnees`
--

INSERT INTO `coordonnees` (`id_coordonnees`, `telephone`, `mail`, `adresse`) VALUES
(1, 787775795, 'bd@mail.com', 'Rue des poijihus');

-- --------------------------------------------------------

--
-- Structure de la table `date_inscription`
--

CREATE TABLE `date_inscription` (
  `id_date_inscription` int(11) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `facture`
--

CREATE TABLE `facture` (
  `id_facture` int(11) NOT NULL,
  `nom` int(100) NOT NULL,
  `description` int(11) NOT NULL,
  `montant` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `personne`
--

CREATE TABLE `personne` (
  `id_personne` int(11) NOT NULL,
  `nom` text NOT NULL,
  `prenom` text NOT NULL,
  `date_naissance` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `personne`
--

INSERT INTO `personne` (`id_personne`, `nom`, `prenom`, `date_naissance`) VALUES
(9, 'oulala', 'oulala', '2020-06-16'),
(10, 'yeah', 'yeah', '2020-06-16'),
(11, 'jhndfihf', 'jhndfihf', '2020-06-16'),
(12, 'sgggs', 'sgggs', '2020-06-16'),
(13, 'sfifhb', 'sfifhb', '2020-06-16'),
(14, 'bdcajskbykf', 'bdcajskbykf', '2020-06-16'),
(15, 'gégé', 'gégé', '2020-06-16'),
(16, 'jéjé', 'cos', '2020-06-16'),
(17, 'abcde', 'fghi', '2020-06-16'),
(18, 'sf', 'ad', '2020-06-30'),
(19, 'da', 'gswe', '2020-06-16'),
(20, 'yeeeeeees', 'noooooooooooo', '2020-12-17'),
(21, 'yeeeeeees', 'nooooooooooooaf', '2020-12-17'),
(22, 'fwsgf', 'wf', '2020-12-17'),
(23, 'ged', 'ged', '2020-12-17'),
(24, 'gesdhg', 'sssssss', '2020-12-17'),
(26, 'asd', 'asd', '2020-12-17'),
(27, 'af', 'fsa', '2020-12-17');

-- --------------------------------------------------------

--
-- Structure de la table `personne_coordonnees`
--

CREATE TABLE `personne_coordonnees` (
  `id_personne_coordonnees` int(11) NOT NULL,
  `FK_Personne` int(11) NOT NULL,
  `FK_Coordonnees` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `personne_date_inscription`
--

CREATE TABLE `personne_date_inscription` (
  `id_date_inscription` int(11) NOT NULL,
  `FK_Personne` int(11) NOT NULL,
  `FK_Date_inscription` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `personne_facture`
--

CREATE TABLE `personne_facture` (
  `id_personne_facture` int(11) NOT NULL,
  `FK_Personne` int(11) NOT NULL,
  `FK_Facture` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `personne_sexe`
--

CREATE TABLE `personne_sexe` (
  `id_personne_sexe` int(11) NOT NULL,
  `FK_Personne` int(11) NOT NULL,
  `FK_Sexe` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `personne_status`
--

CREATE TABLE `personne_status` (
  `id_personne_status` int(11) NOT NULL,
  `FK_Personne` int(11) NOT NULL,
  `FK_Status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `sexe`
--

CREATE TABLE `sexe` (
  `id_sexe` int(11) NOT NULL,
  `sexe` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `sexe`
--

INSERT INTO `sexe` (`id_sexe`, `sexe`) VALUES
(1, 'ihgf'),
(2, 'serdftvbhnj'),
(3, 'jdwis'),
(4, 'qdfwedgffs');

-- --------------------------------------------------------

--
-- Structure de la table `status`
--

CREATE TABLE `status` (
  `id_status` int(11) NOT NULL,
  `status` int(50) NOT NULL,
  `carte_acces` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `coordonnees`
--
ALTER TABLE `coordonnees`
  ADD PRIMARY KEY (`id_coordonnees`);

--
-- Index pour la table `date_inscription`
--
ALTER TABLE `date_inscription`
  ADD PRIMARY KEY (`id_date_inscription`);

--
-- Index pour la table `facture`
--
ALTER TABLE `facture`
  ADD PRIMARY KEY (`id_facture`);

--
-- Index pour la table `personne`
--
ALTER TABLE `personne`
  ADD PRIMARY KEY (`id_personne`);

--
-- Index pour la table `personne_coordonnees`
--
ALTER TABLE `personne_coordonnees`
  ADD PRIMARY KEY (`id_personne_coordonnees`);

--
-- Index pour la table `personne_date_inscription`
--
ALTER TABLE `personne_date_inscription`
  ADD PRIMARY KEY (`id_date_inscription`);

--
-- Index pour la table `personne_facture`
--
ALTER TABLE `personne_facture`
  ADD PRIMARY KEY (`id_personne_facture`);

--
-- Index pour la table `personne_sexe`
--
ALTER TABLE `personne_sexe`
  ADD PRIMARY KEY (`id_personne_sexe`),
  ADD UNIQUE KEY `FK_Sexe` (`FK_Sexe`),
  ADD KEY `FK_Personne` (`FK_Personne`);

--
-- Index pour la table `personne_status`
--
ALTER TABLE `personne_status`
  ADD PRIMARY KEY (`id_personne_status`);

--
-- Index pour la table `sexe`
--
ALTER TABLE `sexe`
  ADD PRIMARY KEY (`id_sexe`);

--
-- Index pour la table `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`id_status`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `coordonnees`
--
ALTER TABLE `coordonnees`
  MODIFY `id_coordonnees` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `date_inscription`
--
ALTER TABLE `date_inscription`
  MODIFY `id_date_inscription` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `facture`
--
ALTER TABLE `facture`
  MODIFY `id_facture` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `personne`
--
ALTER TABLE `personne`
  MODIFY `id_personne` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;
--
-- AUTO_INCREMENT pour la table `personne_coordonnees`
--
ALTER TABLE `personne_coordonnees`
  MODIFY `id_personne_coordonnees` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `personne_date_inscription`
--
ALTER TABLE `personne_date_inscription`
  MODIFY `id_date_inscription` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `personne_facture`
--
ALTER TABLE `personne_facture`
  MODIFY `id_personne_facture` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `personne_sexe`
--
ALTER TABLE `personne_sexe`
  MODIFY `id_personne_sexe` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `personne_status`
--
ALTER TABLE `personne_status`
  MODIFY `id_personne_status` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `sexe`
--
ALTER TABLE `sexe`
  MODIFY `id_sexe` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT pour la table `status`
--
ALTER TABLE `status`
  MODIFY `id_status` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
