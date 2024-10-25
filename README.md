# sample-flask-auth

Repositório criado para APi de autenticação em flask

# Criando registro com SQLAlchemy

`flask shell` para carregar o app dentro do console python

``` python
user = User(username="admin", password="123456") # Cria model
db.session.add(user) # Persiste no BD
db.session.commit() # Commita a transação
```