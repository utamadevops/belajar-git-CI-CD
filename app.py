from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "richval"),
        database=os.getenv("DB_NAME", "rental_kamera"),
        password=os.getenv("DB_PASSWORD", "richval1430")
    )

@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM cameras LIMIT 1;"
        )
        cur.close()
        conn.close()
        return jsonify({
            "status": "up",
            "service": "rental_kamera"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error"
        }), 503
@app.route("/lihat", methods={"GET"})
def lihat():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT brand, model, price_per_day FROM cameras"
    )
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({
        "message": "menampilkan isi table cameras",
        "total data": len(data),
        "data": data
        }), 200
@app.route("/tambah_kamera", methods={"POST"})
def tambah_kamera():
    data = request.get_json()
    if not data or not all(k in data for k in ("brand", "model", "price_per_day")):
        return jsonify({"error": "data brand, model, dan price_per_day wajib diisi"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cameras (brand, model, price_per_day, is_available) VALUES (%s, %s, %s, %s) RETURNING id;",
        (data["brand"], data["model"], data["price_per_day"], data.get("is_available", True))
    )
    kamera_baru = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({
        "message": "berhasil menambahkan kamera baru",
        "id": kamera_baru
    }), 201
@app.route("/pilih/<int:id>", methods=["GET"])
def pilih(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, brand, model, price_per_day, is_available, created_at FROM cameras WHERE id = %s;",
        (id,)
    )
    kamera = cur.fetchone()
    cur.close()
    conn.close()
    if not kamera:
        return jsonify({"error": f"kamera dengan id {id} tidak ada di database"}), 404
    return jsonify({
        "message": "menampilkan kamera",
        "kamera": kamera
    }), 200
@app.route("/update/<int:id>", methods={"PUT"})
def update_cameras(id):
    data = request.get_json()
    brand_baru = data.get("brand")
    model_baru = data.get("model")
    price_baru = data.get("price_per_day")
    available_baru = data.get("is_available")
    if not data:
        return jsonify({"error": "body json tidak boleh kosong"}), 404
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cameras SET brand = %s, model = %s, price_per_day = %s, is_available = %s WHERE id = %s;",
        (brand_baru, model_baru, price_baru, available_baru, id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"kamera dengan id {id}, berhasil diperbarui"}), 200
@app.route("/hapus/<int:id>", methods={"DELETE"})
def hapus_camera(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM cameras WHERE id = %s RETURNING id;",
        (id,)
    )
    camera_terhapus = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if camera_terhapus == 0:
        return jsonify({"message": "camera dengan id {id} tidak ada di database"})
    return jsonify({
        "message": "camera dengan id {id} berhasil dihapus"
    }), 200
if __name__ == "__main__":
    app.run(host= "0.0.0.0", port= 8000, debug=True)