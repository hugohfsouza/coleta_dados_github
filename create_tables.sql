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


CREATE TABLE `pull_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `repo_id` int(11) NOT NULL,
  `number` int(11) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `user` varchar(200) DEFAULT NULL,
  `created_at` varchar(45) DEFAULT NULL,
  `updated_at` varchar(45) DEFAULT NULL,
  `closed_at` varchar(45) DEFAULT NULL,
  `merged_at` varchar(45) DEFAULT NULL,
  `hasTest` tinyint(4) DEFAULT NULL,
  `hasCode` tinyint(4) DEFAULT NULL,
  `qtdArqTest` int(11) DEFAULT NULL,
  `qtdArqCode` int(11) DEFAULT NULL,
  `qtdAdditions` int(11) DEFAULT NULL,
  `qtdDeletions` int(11) DEFAULT NULL,
  `analisado` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `un_1` (`repo_id`,`number`),
  KEY `ix_id` (`id`),
  KEY `ix_2` (`repo_id`),
  KEY `ix_3` (`user`),
  KEY `ix_4` (`repo_id`,`user`),
  KEY `ix_5` (`merged_at`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `pull_request_files` (
  `pr_id` int(11) NOT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `additions` int(11) DEFAULT NULL,
  `deletions` int(11) DEFAULT NULL,
  `sha` varchar(100) NOT NULL,
  `status` varchar(45) DEFAULT NULL,
  `changes` int(11) DEFAULT NULL,
  `patch` longtext,
  `contents_url` varchar(255) DEFAULT NULL,
  UNIQUE KEY `unique_todas` (`pr_id`,`filename`,`additions`,`deletions`,`sha`),
  KEY `ix_01` (`pr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
