from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# Session <- conexão ativa

"""
flask shell -> roda uma instância da aplicação
db.create_all()
db.session <- sessão atual
db.session.commit()
"""