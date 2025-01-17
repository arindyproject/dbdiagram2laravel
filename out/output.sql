CREATE TABLE IF NOT EXISTS users (
  id bigint  UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255)  NULL DEFAULT 'bambang',
  alamat text  NULL,
  id_kelamin bigint  UNSIGNED NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS k_jenis (
  id bigint  UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255)  NOT NULL,
  id_author bigint  UNSIGNED NULL,
  created_at timestamp  NULL DEFAULT NULL,
  updated_at timestamp  NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS k_satuan (
  id bigint  UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255)  NOT NULL,
  id_author bigint  UNSIGNED NULL,
  created_at timestamp  NULL DEFAULT NULL,
  updated_at timestamp  NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS k_produk (
  id bigint  UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255)  NOT NULL,
  keterangan text  NULL,
  harga decimal(10,2)  NULL,
  diskon decimal(5,2)  NULL,
  ppn decimal(5,2)  NULL DEFAULT 11.0,
  id_jenis bigint  UNSIGNED NULL,
  id_satuan bigint  UNSIGNED NULL,
  id_author bigint  UNSIGNED NULL,
  created_at timestamp  NULL DEFAULT NULL,
  updated_at timestamp  NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS k_customer (
  id bigint  UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(255)  NOT NULL,
  alamat text  NULL,
  no_tlp varchar(255)  NULL,
  id_author bigint  UNSIGNED NULL,
  created_at timestamp  NULL DEFAULT NULL,
  updated_at timestamp  NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS k_kartu (
  id bigint  UNSIGNED NOT NULL AUTO_INCREMENT,
  kode_member varchar(255) UNIQUE NOT NULL,
  id_user bigint  UNSIGNED NOT NULL,
  created_at timestamp  NULL DEFAULT NULL,
  updated_at timestamp  NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS k_transaksi (
  id bigint  UNSIGNED NOT NULL AUTO_INCREMENT,
  id_customer bigint  UNSIGNED NULL,
  id_kasir bigint  UNSIGNED NULL,
  created_at timestamp  NULL DEFAULT NULL,
  updated_at timestamp  NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS k_transaksi_items (
  id bigint  UNSIGNED NOT NULL AUTO_INCREMENT,
  id_transaksi bigint  UNSIGNED NOT NULL,
  id_produk bigint  UNSIGNED NOT NULL,
  jumlah int  NOT NULL,
  harga decimal(10,2)  NOT NULL,
  created_at timestamp  NULL DEFAULT NULL,
  updated_at timestamp  NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

ALTER TABLE `k_jenis` ADD FOREIGN KEY (`id_author`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `k_satuan` ADD FOREIGN KEY (`id_author`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `k_produk` ADD FOREIGN KEY (`id_author`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `k_produk` ADD FOREIGN KEY (`id_jenis`) REFERENCES `k_jenis` (`id`) ON DELETE SET NULL;
ALTER TABLE `k_produk` ADD FOREIGN KEY (`id_satuan`) REFERENCES `k_satuan` (`id`) ON DELETE SET NULL;
ALTER TABLE `k_kartu` ADD FOREIGN KEY (`id_user`) REFERENCES `k_customer` (`id`) ON DELETE CASCADE;
ALTER TABLE `k_customer` ADD FOREIGN KEY (`id_author`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `k_transaksi` ADD FOREIGN KEY (`id_customer`) REFERENCES `k_customer` (`id`) ON DELETE SET NULL;
ALTER TABLE `k_transaksi` ADD FOREIGN KEY (`id_kasir`) REFERENCES `users` (`id`) ON DELETE SET NULL;
ALTER TABLE `k_transaksi_items` ADD FOREIGN KEY (`id_produk`) REFERENCES `k_produk` (`id`) ON DELETE CASCADE;
ALTER TABLE `k_transaksi_items` ADD FOREIGN KEY (`id_transaksi`) REFERENCES `k_transaksi` (`id`) ON DELETE CASCADE;