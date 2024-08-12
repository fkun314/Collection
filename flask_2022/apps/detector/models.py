from datetime import datetime

from apps.app import db

class UserImage(db.Model):
    __tablename__ = 'user_images'
    id = db.Column(db.Integer, primary_key=True)
    # user_idはusersテーブルのidカラムを外部キーとして設定する
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_path = db.Column(db.String)
    is_detected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    upload_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class UserVideo(db.Model):
    __tablename__ = "user_videos"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    total_frame = db.Column(db.Integer)
    fps_info = db.Column(db.Integer)
    video_title = db.Column(db.String)
    video_path = db.Column(db.String)
    is_detected = db.Column(db.Integer, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    detected_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class DetectedLists(db.Model):
    __tablename__="detected_lists"
    # id = db.Column(db.Integer, db.ForeignKey('user_videos.id'), primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.String, db.ForeignKey('user_videos.id'))
    fps_number = db.Column(db.Integer)
    detected_name = db.Column(db.String)
    detected_score = db.Column(db.Float)
    detected_x_min = db.Column(db.Float)
    detected_y_min = db.Column(db.Float)
    detected_x_max = db.Column(db.Float)
    detected_y_max = db.Column(db.Float)
    center_x = db.Column(db.Float)
    center_y = db.Column(db.Float)
    
class DetectedImages(db.Model):
    __tablename__="detected_images"
    # id = db.Column(db.Integer, db.ForeignKey('user_videos.id'), primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.String, db.ForeignKey('user_images.id'))
    detected_name = db.Column(db.String)
    detected_score = db.Column(db.Float)
    detected_x_min = db.Column(db.Float)
    detected_y_min = db.Column(db.Float)
    detected_x_max = db.Column(db.Float)
    detected_y_max = db.Column(db.Float)
    center_x = db.Column(db.Float)
    center_y = db.Column(db.Float)

class IndexVideos(db.Model):
    __tablename__="index_videos"
    number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.String, db.ForeignKey('user_videos.id'))
    fps_number = db.Column(db.Integer)
    detected_count = db.Column(db.Integer)

class RelationshipTables(db.Model):
    __tablename__="relationship_tables"
    number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.String, db.ForeignKey('user_videos.id'))
    index_number = db.Column(db.Integer)
    detected_name = db.Column(db.String)
    detected_score = db.Column(db.Float)
    center_x = db.Column(db.Float)
    center_y = db.Column(db.Float)
    r = db.Column(db.Float)
    theta = db.Column(db.Float)

    