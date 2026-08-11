from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
  return (
      jsonify({
          "status": "success",
          "message": "Flask Application Deployed via ArgoCD Operator!",
      }),
      200,
  )


@app.route("/healthz", methods=["GET"])
def health():
  return jsonify({"status": "UP"}), 200


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)