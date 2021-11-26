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
  `qtdArquivosStringTeste` bigint(9) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unico_projeto` (`name`,`nameWithOwner`,`databaseId`)
) ENGINE=InnoDB AUTO_INCREMENT=2433 DEFAULT CHARSET=latin1;


CREATE TABLE `startstop` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(100) DEFAULT NULL,
  `continuar` tinyint(4) DEFAULT '1',
  `continuarSearch` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `ix_name` (`token`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
