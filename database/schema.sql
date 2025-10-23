
CREATE SCHEMA IF NOT EXISTS `supplytrack` DEFAULT CHARACTER SET utf8 ;
USE `supplytrack` ;

-- Tabela: usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL UNIQUE,
  `cpf` varchar(14) not null unique,
  `senha` VARCHAR(255) NOT NULL, -- Aumentado para hash de senha
  `tipo_perfil` ENUM('ADMIN', 'GESTOR', 'MOTORISTA') NOT NULL,
  PRIMARY KEY (`id_usuario`)
);

-- Tabela: motorista
CREATE TABLE IF NOT EXISTS `motorista` (
  `id_motorista` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NOT NULL,
  `cnh` VARCHAR(45) NOT NULL UNIQUE,
  `status` ENUM('LIVRE', 'EM_ROTA', 'DESLIGADO') NOT NULL DEFAULT 'LIVRE',
  PRIMARY KEY (`id_motorista`),
  CONSTRAINT `fk_motorista_usuario`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `usuario` (`id_usuario`)
    ON DELETE CASCADE
);

-- Tabela: veiculo
CREATE TABLE IF NOT EXISTS `veiculo` (
  `id_veiculo` INT NOT NULL AUTO_INCREMENT,
  `placa` VARCHAR(45) NOT NULL UNIQUE,
  `capacidade` VARCHAR(45) NOT NULL,
  `status` ENUM('DISPONIVEL', 'EM_MANUTENCAO', 'EM_USO') NOT NULL DEFAULT 'DISPONIVEL',
  `id_motorista` INT NULL, -- Motorista principal (opcional)
  PRIMARY KEY (`id_veiculo`),
  CONSTRAINT `fk_veiculo_motorista`
    FOREIGN KEY (`id_motorista`)
    REFERENCES `motorista` (`id_motorista`)
    ON DELETE SET NULL
);

-- Tabela: armazem
CREATE TABLE IF NOT EXISTS `armazem` (
  `id_armazem` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `endereco` VARCHAR(45) NOT NULL,
  `numeroRua` INT NULL,
  PRIMARY KEY (`id_armazem`)
);

-- Tabela: rota
CREATE TABLE IF NOT EXISTS `rota` (
  `idRota` INT NOT NULL AUTO_INCREMENT,
  `DataSaida` DATE NOT NULL,
  `dataEntrega` DATE NULL,
  `distancia` VARCHAR(45) NULL,
  `status` ENUM('PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA') NOT NULL DEFAULT 'PENDENTE',
  `id_veiculo` INT NULL,
  `id_motorista` INT NULL,
  PRIMARY KEY (`idRota`),
  CONSTRAINT `fk_rota_veiculo`
    FOREIGN KEY (`id_veiculo`)
    REFERENCES `veiculo` (`id_veiculo`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_rota_motorista`
    FOREIGN KEY (`id_motorista`)
    REFERENCES `motorista` (`id_motorista`)
    ON DELETE SET NULL
);

-- Tabela: entrega (Representa uma parada na Rota)
CREATE TABLE IF NOT EXISTS `entrega` (
  `id_entrega` INT NOT NULL AUTO_INCREMENT,
  `idRota` INT NOT NULL,
  `dataPrevista` DATE NOT NULL,
  `dataRealizada` DATE NULL,
  `status` ENUM('PENDENTE', 'SAIU_PARA_ENTREGA', 'ENTREGUE', 'NAO_ENTREGUE') NOT NULL DEFAULT 'PENDENTE',
  `id_motorista` INT NULL,
  PRIMARY KEY (`id_entrega`),
  CONSTRAINT `fk_entrega_rota`
    FOREIGN KEY (`idRota`)
    REFERENCES `rota` (`idRota`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_entrega_motorista`
    FOREIGN KEY (`id_motorista`)
    REFERENCES `motorista` (`id_motorista`)
    ON DELETE SET NULL
);

-- Tabela: carga
CREATE TABLE IF NOT EXISTS `carga` (
  `id_carga` INT NOT NULL AUTO_INCREMENT,
  `volume` VARCHAR(45) NOT NULL,
  `peso` VARCHAR(45) NOT NULL,
  `status` ENUM('CADASTRADA', 'EM_ARMEZEM', 'EM_ROTA', 'ENTREGUE') NOT NULL DEFAULT 'CADASTRADA',
  `localizacaoAtual` VARCHAR(255) NULL,
  `id_armazem` INT NULL,
  `id_entrega` INT NULL,
  PRIMARY KEY (`id_carga`),
  CONSTRAINT `fk_carga_armazem`
    FOREIGN KEY (`id_armazem`)
    REFERENCES `armazem` (`id_armazem`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_carga_entrega`
    FOREIGN KEY (`id_entrega`)
    REFERENCES `entrega` (`id_entrega`)
    ON DELETE SET NULL
);

-- Tabela: historico (Movimentação de Carga)
CREATE TABLE IF NOT EXISTS `historico` (
  `id_historico` INT NOT NULL AUTO_INCREMENT,
  `id_carga` INT NOT NULL,
  `tempo` TIME NOT NULL,
  `localizacao` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_historico`),
  CONSTRAINT `fk_historico_carga`
    FOREIGN KEY (`id_carga`)
    REFERENCES `carga` (`id_carga`)
    ON DELETE CASCADE
);

-- Tabela: alerta
CREATE TABLE IF NOT EXISTS `alerta` (
  `id_alerta` INT NOT NULL AUTO_INCREMENT,
  `tipo` ENUM('ATRASO', 'PERIGO', 'ROTA_INVALIDA', 'OUTRO') NOT NULL,
  `horario` TIME NOT NULL,
  `status` ENUM('ABERTO', 'RESOLVIDO') NOT NULL DEFAULT 'ABERTO',
  `idRota` INT NULL,
  `id_veiculo` INT NULL,
  `id_motorista` INT NULL,
  `id_entrega` INT NULL,
  PRIMARY KEY (`id_alerta`),
  CONSTRAINT `fk_alerta_rota`
    FOREIGN KEY (`idRota`)
    REFERENCES `rota` (`idRota`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_alerta_veiculo`
    FOREIGN KEY (`id_veiculo`)
    REFERENCES `veiculo` (`id_veiculo`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_alerta_motorista`
    FOREIGN KEY (`id_motorista`)
    REFERENCES `motorista` (`id_motorista`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_alerta_entrega`
    FOREIGN KEY (`id_entrega`)
    REFERENCES `entrega` (`id_entrega`)
    ON DELETE SET NULL
);

-- Tabela: relatorio
CREATE TABLE IF NOT EXISTS `relatorio` (
  `id_relatorio` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(45) NOT NULL,
  `periodo` VARCHAR(45) NULL,
  `dadosGerados` TEXT NULL, -- Coluna TEXT para armazenar JSON/dados
  PRIMARY KEY (`id_relatorio`)
);