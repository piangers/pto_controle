BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE USER controle_pto WITH PASSWORD 'controle_pto';

CREATE SCHEMA controle;

CREATE TABLE controle.tipo_situacao(
	id SERIAL NOT NULL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL
);

INSERT INTO controle.tipo_situacao (nome) VALUES
('Não medido'),
('Reserva'),
('Não acessível'),
('Aguardando avaliação'),
('Aprovado'),
('Reprovado');

CREATE TABLE controle.ponto_controle_p(
	id serial NOT NULL,
    nome varchar(255) NOT NULL,
    mi varchar(255) NOT NULL,
    medidor varchar(255), 
    data_medicao timestamp with time zone,
	tipo_situacao_id INTEGER NOT NULL REFERENCES controle.tipo_situacao (id),
	geom geometry(POINT, 31982),
	CONSTRAINT ponto_controle_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
);

CREATE TABLE controle.trilha_l(
	id serial NOT NULL,
	geom geometry(LINESTRING, 31982),
	CONSTRAINT trilha_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
);

GRANT USAGE ON SCHEMA controle TO controle_pto;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA controle TO controle_pto;
GRANT ALL ON ALL SEQUENCES IN SCHEMA controle TO controle_pto;

COMMIT;