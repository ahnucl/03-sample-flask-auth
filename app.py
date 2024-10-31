from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_required, login_user, current_user, logout_user


app = Flask(__name__)
app.config["SECRET_KEY"] = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin123@host.docker.internal:3306/flask-crud"

login_manager = LoginManager()
login_manager.login_view = 'login' # type: ignore
login_manager.init_app(app)

db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"message": "Credenciais inválidas"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username and not password:
        return jsonify({"message": "Credenciais inválidas"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({"message": "Credenciais inválidas"}), 400

    login_user(user)
    print(current_user.is_authenticated)

    return jsonify({"message": "Autenticação realizada com sucesso"})


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Dados inválidos"}), 400

    user = User(username=username, password=password) # type: ignore
    db.session.add(user)
    db.session.commit()


    return jsonify({"message": "Usuário cadastrado com sucesso"}), 200


@app.route('/users/<int:user_id>', methods=['GET'])
@login_required
def read_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404


    return jsonify({"username": user.username})


@app.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    data = request.json
    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    user.password = data.get("password")
    db.session.commit()

    return jsonify({"message": f"Usuário {user_id} atualizado com sucesso"})


@app.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if user_id == current_user.id:
        return jsonify({"message": "Não é possível deletar o usuário logado"}), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"Usuário {user_id} deletado com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)
