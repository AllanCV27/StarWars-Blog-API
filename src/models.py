from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#class User(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    #password = db.Column(db.String(80), unique=False, nullable=False)
    #is_active = db.Column(db.Boolean(), unique=False, nullable=False)


class Personajes(db.Model):
    __tablename__ = 'Personajes'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    imagen = db.Column(db.String(250))
    altura = db.Column(db.String(250))
    masa = db.Column(db.String(250))
    color_cabello = db.Column(db.String(250))
    piel = db.Column(db.String(250))
    ojos = db.Column(db.String(250))
    fecha_nacimiento = db.Column(db.String(250))
    genero = db.Column(db.String(250))
    creacion = db.Column(db.String(250))
    editado = db.Column(db.String(250))
    mundo_origen = db.Column(db.String(250))
    

    def serialize(self):
        return{
            "id":self.id,
            "imagen":self.imagen,
            "altura":self.altura,
            "masa":self.masa,
            "color_cabello":self.color_cabello,
            "piel":self.piel,
            "ojos":self.ojos,
            "fecha_nacimiento":self.fecha_nacimiento,
            "genero":self.genero,
            "creacion":self.creacion,
            "editado":self.editado,
            "name":self.name,
            "mundo_origen":self.mundo_origen,
        }

        def serialize2(self):
            return{
                "id":self.id,
                "name":self.name,
            }

class Planetas(db.Model):
    __tablename__ = 'Planetas'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    imagen = db.Column(db.String(250))
    clima = db.Column(db.String(250))
    diametro = db.Column(db.String(250))
    gravedad = db.Column(db.String(250))
    periodo_orbital = db.Column(db.String(250))
    poblacion = db.Column(db.String(250))
    residentes = db.Column(db.String(250))
    periodo_rotacion = db.Column(db.String(250))
    superficie_acuatica = db.Column(db.String(250))
    terreno = db.Column(db.String(250))

    def serialize(self):
        return{
            "id":self.id,
            "imagen":self.imagen,
            "clima":self.clima,
            "diametro":self.diametro,
            "gravedad":self.gravedad,
            "name":self.name,
            "periodo_orbital":self.periodo_orbital,
            "poblacion":self.poblacion,
            "residentes":self.residentes,
            "periodo_rotacion":self.periodo_rotacion,
            "superficie_acuatica":self.superficie_acuatica,
            "terreno":self.terreno,
        }
    
    def serialize2(self):
        return{
            "id":self.id,
            "name":self.name,
        }

class User(db.Model):
    __tablename__ = 'User'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

   

    def serialize(self):
        return{
            "id":self.id,
            "user":self.user,
            "email":self.email
        }

class Favoritos(db.Model):
    __tablename__ = 'Favoritos'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    planetas_id = db.Column(db.Integer, db.ForeignKey('Planetas.id'))
    personajes_id = db.Column(db.Integer, db.ForeignKey('Personajes.id'))
    Planetas = db.relationship(Planetas)
    Personajes = db.relationship(Personajes)
    User = db.relationship(User)

    

    def serialize(self):
        return{
            "id":self.id,
            "User_id":self.User_id,
            "planetas_id":self.planetas_id,
            "personajes_id":self.personajes_id
        }
 