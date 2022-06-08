CREATE TABLE IF NOT EXISTS tbl_data (
    id_agendamento INTEGER(10) PRIMARY KEY NOT NULL,
    id_usuario INTEGER(10) NOT NULL, 
    dt_envio DATETIME NOT NULL,
    formato_comunicacao VARCHAR(255), 
    status_agendamento VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS tbl_clientes (
    id_usuario INTEGER(10) PRIMARY KEY NOT NULL,
    email VARCHAR(255),
    tel VARCHAR(255),
    user VARCHAR(255)
);
