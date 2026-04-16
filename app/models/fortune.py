from datetime import datetime
from . import db

class FortuneRecord(db.Model):
    __tablename__ = 'fortune_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    fortune_type = db.Column(db.String(20), nullable=False)  # 'draw' 或 'tarot'
    result_data = db.Column(db.Text, nullable=False) # JSON 格式化結果
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, fortune_type, result_data):
        record = cls(user_id=user_id, fortune_type=fortune_type, result_data=result_data)
        db.session.add(record)
        db.session.commit()
        return record

    @classmethod
    def get_by_id(cls, record_id):
        return cls.query.get(record_id)

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
