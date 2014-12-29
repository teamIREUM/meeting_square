# -*- coding: utf-8 -*-
from server.models import db
from server.models.meeting import Meeting
from werkzeug import check_password_hash,generate_password_hash
import re

tb_user_friends = db.Table('friends',
        db.Column('user_id',db.Integer,db.ForeignKey('user.id'),primary_key=True),
        db.Column('friend_id',db.Integer,db.ForeignKey('user.id'),primary_key=True),
        )

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(30),unique=True)
    pw = db.Column(db.String(20))

    role = db.Column(db.Integer,default=0)
    
    profile_name = db.Column(db.String(30))
    profile_stat = db.Column(db.String(60))
    profile_img = db.Column(db.String(30))

    socialoauth_id = db.Column(db.Integer,db.ForeignKey('social_oauth.id'))

    meetings = db.relationship('MeetingAssociation',backref="user",lazy='dynamic')
    friends = db.relationship('User',
            secondary=tb_user_friends,
            backref='user_friends',
            primaryjoin=(id == tb_user_friends.c.user_id),
            secondaryjoin=(id == tb_user_friends.c.friend_id),
            lazy='dynamic'
            )


    def __init__(self,email,pw):
        self.email = email
        self.pw = generate_password_hash(pw)

    @classmethod
    def login(cls,email,pw):
        user = cls.query.filter_by(email=email).first()
        if not user:
            return False,(u"없는 ID 입니다","")
        if not user.check_password(pw):
            return False,(user.uid,u"비밀번호를 다시 한번 확인해주십시오")
        return True,user

    def check_password(self,password):
        return check_password_hash(self.pw,password)

    @classmethod
    def validate_email(cls, email=None):
        if re.match("[^@]+@[^@]+\.[^@]+", email or ''):
            user = cls.query.filter_by(email=email).first()
            if user:
                return False, u'이미 존재하는 이메일 입니다.'
            return True,None

        return False, u'올바른 이메일을 입력해주세요.'

    @staticmethod
    def register(email,pw):
        user = User(email,pw)
        status,msg = user.validate_email(email)
        if status:
            db.session.add(user)
            db.session.commit()
            return status,user
        return status,msg

        

class SocialOAuth(db.Model):
    __tablename__ = 'social_oauth'
    FACEBOOK = 1
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer)
    user = db.relationship('User',backref='user',lazy='joined')
    provider =  db.Column(db.Integer)

    def __init__(self,uid,user,provider):
        self.uid = uid
        self.user = user
        self.provider = provider


    @classmethod
    def join(cls,uid,provider,profile=None):
        if not profile:
            return None
        if provider == cls.FACEBOOK:
            uid = profile
            return cls.facebook_oauth(uid,profile)




    @classmethod
    def facebook_oauth(cls,uid,profile):
        user_info = {
            'email': '{account}@facebook.com'.format(account=profile.get('id', '')),
            'pw': md5(profile.get('name', '') + SECRET_KEY).hexdigest(),
        }
        new_user = User(**user_info)
        db.add(new_user)
        new_oauth = cls(uid,new_user,cls.FACEBOOK)
        db.add(new_oauth)
        db.commit()
        return new_oauth 



        



class MeetingAssociation(db.Model):
    __tablename__ = 'user_meeting'
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    meeting_id = db.Column(db.Integer,db.ForeignKey('meeting.id'),primary_key=True)
    opinion = db.Column(db.Integer,default=0)
    meeting = db.relationship("Meeting",backref="user")

    def __init__(self,meeting):
        self.meeting = meeting
