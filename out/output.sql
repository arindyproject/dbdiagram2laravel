CREATE TABLE IF NOT EXISTS users (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255) NULL,
  alamat text NULL,
  id_kelamin bigint UNSIGNED NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS jenis (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  id_author bigint UNSIGNED NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS satuan (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  id_author bigint UNSIGNED NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS produk (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  keterangan text NULL,
  harga decimal(10,2) NULL,
  diskon decimal(5,2) NULL,
  ppn decimal(5,2) NULL DEFAULT 11.0,
  id_jenis bigint UNSIGNED NULL,
  id_satuan bigint UNSIGNED NULL,
  id_author bigint UNSIGNED NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS customer (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  alamat text NULL,
  no_tlp varchar(255) NULL,
  id_author bigint UNSIGNED NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS kartu (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  kode_member varchar(255) NOT NULL,
  id_user bigint UNSIGNED NOT NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS transaksi (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  id_customer bigint UNSIGNED NULL,
  id_kasir bigint UNSIGNED NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS transaksi_items (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  id_transaksi bigint UNSIGNED NOT NULL,
  id_produk bigint UNSIGNED NOT NULL,
  jumlah int NOT NULL,
  harga decimal(10,2) NOT NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

ALTER TABLE `jenis` ADD FOREIGN KEY (`id_author`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `satuan` ADD FOREIGN KEY (`id_author`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `produk` ADD FOREIGN KEY (`id_author`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `produk` ADD FOREIGN KEY (`id_jenis`) REFERENCES `jenis` (`id`) ON DELETE SET NULL;
ALTER TABLE `produk` ADD FOREIGN KEY (`id_satuan`) REFERENCES `satuan` (`id`) ON DELETE SET NULL;
ALTER TABLE `kartu` ADD FOREIGN KEY (`id_user`) REFERENCES `customer` (`id`) ON DELETE CASCADE;
ALTER TABLE `customer` ADD FOREIGN KEY (`id_author`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `transaksi` ADD FOREIGN KEY (`id_customer`) REFERENCES `customer` (`id`) ON DELETE SET NULL;
ALTER TABLE `transaksi` ADD FOREIGN KEY (`id_kasir`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `transaksi_items` ADD FOREIGN KEY (`id_produk`) REFERENCES `produk` (`id`) ON DELETE CASCADE;
ALTER TABLE `transaksi_items` ADD FOREIGN KEY (`id_transaksi`) REFERENCES `transaksi` (`id`) ON DELETE CASCADE;