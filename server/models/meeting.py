# -*- coding: utf-8 -*-

from server.models import db
import random,string
tb_meeting_users = db.Table('meeting_users',
        db.Column('meeting_id',db.Integer,db.ForeignKey('meeting.id')),
        db.Column('users',db.Integer,db.ForeignKey('user.id'))
        )
tb_validtime_attendance = db.Table('validtime_attendance',
        db.Column('validtime',db.Integer,db.ForeignKey('validtime.id')),
        db.Column('user',db.Integer,db.ForeignKey('user.id'))
        )

class Meeting(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    link = db.Column(db.String(100),unique=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(100))
    end_vote_date = db.Column(db.DateTime())
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    times = db.Column(db.String(100))
    isprivate = db.Column(db.Boolean,default=True)
    
    setted_date = db.Column(db.DateTime(),default=None)
    updated = db.Column(db.DateTime(),default=db.func.now(),onupdate=db.func.now())

    author = db.relationship("User",backref='meeting',lazy='joined')
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    users = db.relationship('User',secondary=tb_meeting_users,
            backref='attendees',lazy='dynamic')
    
    timetable = db.relationship('ValidTime',
            backref='meeting',lazy='dynamic')

    def __init__(self,
            title,
            content,
            end_vote_date,
            start_date,
            end_date,
            times,
            author):
        self.link = Meeting.generateLink()
        self.title = title
        self.content = content
        self.end_vote_date = end_vote_date
        self.start_date = start_date
        self.end_date = end_date
        self.times = times
        self.author = author

    def get_timetable(self):
        return self.timetable.all()
    @staticmethod
    def generateLink():
        link = Meeting.generateToken()
        while Meeting.query.filter_by(link=link).first():
            link = Meeting.generateToken()
        return link

    @staticmethod
    def generateToken():
        return ''.join(random.sample((string.letters+string.digits)*40,40))

    def meeting_info(self):
        return {"id":self.id,
                "title":self.title,
                "content":self.content,
                "setted_date":self.setted_date,
                "end_vote_date":self.end_vote_date,
                "start_date":self.start_date,
                "end_date":self.end_date,
                "times":self.times}

class ValidTime(db.Model):
    __tablename__ = 'validtime'
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime)
    time = db.Column(db.String(30))
    meeting_id = db.Column(db.Integer,db.ForeignKey('meeting.id'))

    attendance = db.relationship('User',secondary=tb_validtime_attendance,
            backref='attendance',lazy='dynamic')

    def __init__(self,date,time):
        self.date = date
        self.time = time

    def isattend(self,user):
        return map(lambda attenduser: user == attenduser,
                self.attendance)
