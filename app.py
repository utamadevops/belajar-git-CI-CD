from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "toko_val"),
        user=os.getenv("DB_USER","richval"),
        password=os.getenv("DB_PASSWORD", "12345")
    )

@app.route("/health", methods=["GET"])
def healt_check():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1"
        )
        cur.close()
        conn.close()
        return jsonify({"status": "OK"}), 200
    except Exception as e:
        return jsonify({"status": "DOWN", "detail": str(e)}), 500
@app.route("/nambah/<nama>/<harga>/<stok>/<kategori>", methods=["POST"])
def nambah(nama, harga, stok, kategori):
    harga = int(harga)
    stok = int(stok)
    if harga <= 0:
        return jsonify({"message:", f"{harga} tidak boleh kosong"}), 200
    if stok < 0:
        return jsonify({"message", f"{stok} gak boleh minus"}), 200
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO produk (nama, harga, stok, kategori) VALUES (%s, %s, %s, %s)",
        (nama, harga, stok, kategori)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"{nama}, {harga}, {stok}, {kategori}, berhasil ditambahkan."}), 201

@app.route("/lihat", methods=["GET"])
def lihat():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT nama, harga, stok, kategori FROM produk;"
    )
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({
        "message": "menampilkan daftar produk",
        "total": len(data),
        "data": data
    }), 200

@app.route("/buat/<nama_produk>/<harga_baru>", methods=["PUT"])
def buat(nama_produk, harga_baru):
    harga_baru = int(harga_baru)
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE produk SET harga=%s WHERE nama = %s",
        (harga_baru, nama_produk)
    )
    baru = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if baru > 0:
        return jsonify({"message": f"{nama_produk} berhasil diubah, harga sekarang{harga_baru}"}), 201
    return jsonify ({"message": "produk tidak ditemuka"}), 404

@app.route("/hapus/<nama_produk>", methods=["DELETE"])
def hapus(nama_produk,):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM produk WHERE nama = %s",
        (nama_produk,)
    )
    hapus_apa = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if hapus_apa > 0:
        return jsonify({"message": f"{nama_produk} berhasil dihapus"}), 200
    return jsonify({"message": "nama produk tidak ada"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 8000, debug=True)