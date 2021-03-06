from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index= True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role',lazy='dynamic')

    def insert_roles():
        roles = {
                'User':(Permission.FOLLOW |
                        Permission.COMMENT |
                        Permission.WRITE_ARTICLES, True),
                'Moderator': (Permission.FOLLOW |
                                Permission.COMMENT |
                                Permission.WRITE_ARTICLES |
                                Permission.MODERATE_COMMENTS,False),
                'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    '''kwargs = keyword arguments'''

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default = True).first()

    def can(self, permissions):
        return self.role is not None and \
                (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


    '''For email confirmation by sending confirmation email.'''

    # confirmed = db.Column(db.Boolean, default=False)
    #
    # '''TimedJSONWebSignatureSerializer generates JSON Web Signatures (JWS) with a
    #     time expiration'''
    #
    # def generate_confirmation_token(self,expiration=3600):
    #
    #     '''The dumps() method generates a cryptographic signature for the data given as an ar‐
    #         gument and then serializes the data plus the signature as a convenient token string.
    #         The expires_in argument sets an expiration time for the token expressed in seconds'''
    #
    #     s = Serializer(current_app.config['SECRET_KEY'],expiration)
    #     return s.dumps({'confirm':self.id})
    #
    # def confirm(self,token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         '''To decode the token, the serializer object provides a loads() method that
    #             takes the token as its only argument. The function verifies the signature
    #             and the expiration time and, if found valid, it returns the original data'''
    #         data = s.loads(token)
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
