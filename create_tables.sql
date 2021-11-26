CREATE TABLE `repositorios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `nameWithOwner` varchar(200) DEFAULT NULL,
  `createdAt` varchar(45) DEFAULT NULL,
  `databaseId` bigint(9) DEFAULT NULL,
  `languages` text,
  `temTeste` tinyint(4) DEFAULT NULL,
  `prs_recuperados` tinyint(4) DEFAULT NULL,
  `prs_analisados` tinyint(4) DEFAULT NULL,
  `qtdPrs` bigint(20) DEFAULT NULL,
  `linguagemReferencia` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unico_projeto` (`name`,`nameWithOwner`,`databaseId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
