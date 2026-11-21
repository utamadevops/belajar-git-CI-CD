from flask import Flask, request,jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "richval"),
        database=os.getenv("DB_NAME", "latihan_final"),
        password=os.getenv("DB_PASSWORD", "richval1430")
    )

@app.route("/health", methods=["GET"])
def health():
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
        return jsonify({"error": str(e)}), 500
@app.route("/lihat", methods=["GET"])
def lihat():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT nama, harga, stok FROM produk"
    )
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({
        "message": "menampilkan produk",
        "total": len(data),
        "data": data
    }), 200
@app.route("/tambah_produk/<nama>/<harga>/<stok>", methods=["POST"])
def tambah(nama, harga, stok):
    harga=int(harga)
    stok=int(stok)
    if harga <= 0:
        return jsonify({"message": f"{harga} tidak boleh kosong"}), 200
    if stok <= 0:
        return jsonify({"message": f"{stok} tidak boleh kosong"})
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO produk (nama, harga, stok) VALUES (%s, %s, %s)",
        (nama,harga,stok)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"{nama}, {harga}, {stok} berhasil ditambahkan"})
@app.route("/update/<int:id>", methods={"PUT"})
def update_produk(id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE produk SET nama=%s, harga=%s, stok=%s WHERE id=%s RETURNING *",
        (data.get("nama"), data.get("harga"), data.get("stok"), id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"error": "produk tidak ditemukan"}), 404
    return jsonify(row)
@app.route("/delete/<int:id>", methods=["DELETE"])
def hapus_produk(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM produk WHERE id=%s RETURNING *", (id,)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"error": "produk tidak ditemukan"}), 404
    return jsonify({"message": "produk berhasil dihapus"}), 200
 
    
if __name__ == "__main__":
    app.run(host= "0.0.0.0", port= 9000, debug=True)
