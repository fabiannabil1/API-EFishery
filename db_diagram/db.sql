-- Tabel pengguna
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Tabel barang lelang
CREATE TABLE barang (ca
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    nama TEXT NOT NULL,
    deskripsi TEXT NOT NULL,
    harga_awal INTEGER NOT NULL,
    status TEXT DEFAULT 'dibuka'
);

-- Tabel penawaran
CREATE TABLE penawaran (
    id SERIAL PRIMARY KEY,
    barang_id INTEGER NOT NULL REFERENCES barang(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    jumlah INTEGER NOT NULL,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
