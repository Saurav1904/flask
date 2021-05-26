from flask import Flask
from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)


class VideoModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    views=db.Column(db.Integer,nullable=False)
    likes=db.Column(db.Integer,nullable=False)
    
    def __repr__(self):
        return f"Video(name={name},views={views},likes={likes})"


video_put_args=reqparse.RequestParser()
video_put_args.add_argument("name",type=str,help="Name of video is required",required=True)
video_put_args.add_argument("views",type=int,help="Views of video",required=True)
video_put_args.add_argument("likes",type=int,help="Likes on video",required=True)

video_update_args=reqparse.RequestParser()
video_update_args.add_argument("name",type=str,help="Name of video is required")
video_update_args.add_argument("views",type=int,help="Views of video")
video_update_args.add_argument("likes",type=int,help="Likes on video")

resource_fields={'id':fields.Integer,
                 'name':fields.String,
                 'views':fields.Integer,
                 'likes':fields.Integer}

class Video(Resource):
    
    @marshal_with(resource_fields)
    def get(self,video_id):
        result=VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="coudnt find the video")
        return result
    
    @marshal_with(resource_fields)
    def put(self,video_id): 
        args=video_put_args.parse_args()
        result=VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message="Video Already Exist")
        video=VideoModel(id=video_id, views=args['views'],likes=args['likes'],
                         name=args['name'])
        return video,201
    @marshal_with(resource_fields)
    def patch(self,video_id):
        args=video_update_args.parse_args()
        result=VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="coudnt find the video id")
        if args['name']:
            result.name=args['name']
        if args['views'] :
            result.views=args['views']
        if args['likes']:
            result.name=args['likes']
        db.session.commit()
        return result
            
    
    def delete(self,video_id):
        return '',204
    
    
@app.route('/')
def test():
        BASE="http://127.0.0.1:5000/"
        response=requests.get(BASE+"video/1/")
        return response.json()

    
    

api.add_resource(Video,"/video/<int:video_id>/")

if __name__ == "__main__":
    app.run(debug=True)
