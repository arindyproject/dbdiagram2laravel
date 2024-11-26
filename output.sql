CREATE TABLE farmasi_pr_jenis (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  nama varchar NOT NULL,
  keterangan text NULL,
  id_author bigint UNSIGNED NULL DEFAULT NULL,
  id_editor bigint UNSIGNED NULL DEFAULT NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE farmasi_pr_satuan (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  nama varchar NOT NULL,
  keterangan text NULL,
  id_author bigint UNSIGNED NULL DEFAULT NULL,
  id_editor bigint UNSIGNED NULL DEFAULT NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE farmasi_pr_kategori (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  nama varchar NOT NULL,
  keterangan text NULL DEFAULT 'hallo',
  status boolean NULL DEFAULT True,
  harga decimal NULL DEFAULT 1000.0,
  id_author bigint UNSIGNED NULL DEFAULT 1,
  id_editor bigint UNSIGNED NULL DEFAULT 2,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE farmasi_pr_produk_kategori (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  id_produk bigint UNSIGNED NULL,
  id_kategori bigint UNSIGNED NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE farmasi_pr_produk (
  id bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  nama varchar NOT NULL,
  barcode varchar NULL,
  keterangan text NULL,
  harga decimal(15,2) NULL DEFAULT 0.0,
  diskon decimal(5,2) NULL DEFAULT 0.0,
  ppn decimal(4,2) NULL DEFAULT 11.0,
  jumlah_satuan_kecil integer NULL DEFAULT 1,
  status boolean NOT NULL DEFAULT True,
  id_jenis bigint UNSIGNED NULL DEFAULT NULL,
  id_satuan_kecil bigint UNSIGNED NULL DEFAULT NULL,
  id_satuan_beasr bigint UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (id)
);