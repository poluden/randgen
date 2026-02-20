from __future__ import annotations

from flask import Flask, jsonify, render_template, request
from rng import generate

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/")
def index():
    return render_template("index.html", result=None)


@app.post("/generate")
def do_generate():
    # seed_hint — просто для демонстрації керованого впливу (не зберігаємо)
    seed_hint = request.form.get("seed_hint", "").strip()
    result = generate(seed_hint=seed_hint if seed_hint else None)
    return render_template("index.html", result=result, seed_hint=seed_hint)

@app.get("/api/generate")
def api_generate():
    seed_hint = request.args.get("seed_hint", "").strip() or None
    r = generate(seed_hint=seed_hint)
    return jsonify(
        ts_iso=r.ts_iso,
        ts_ms=r.ts_ms,
        nonce=r.nonce,
        rand_a=r.rand_a,
        calc_b=r.calc_b,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)