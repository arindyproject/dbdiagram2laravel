CREATE TABLE IF NOT EXISTS kelamin (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255) NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS users (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255) NULL,
  alamat text NULL,
  id_kelamin bigint UNSIGNED NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ktp (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  nik varchar(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS jenis (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255) NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS kelompok (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  id_user bigint UNSIGNED NULL,
  id_jenis bigint UNSIGNED NULL,
  PRIMARY KEY (id)
);

ALTER TABLE `ktp` ADD FOREIGN KEY (`id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
ALTER TABLE `users` ADD FOREIGN KEY (`id_kelamin`) REFERENCES `kelamin` (`id`) ON DELETE SET NULL;
ALTER TABLE `kelompok` ADD FOREIGN KEY (`id_user`) REFERENCES `users` (`id`) ON DELETE CASCADE;
ALTER TABLE `kelompok` ADD FOREIGN KEY (`id_jenis`) REFERENCES `jenis` (`id`);