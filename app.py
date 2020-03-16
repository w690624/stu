from flask import Flask, request,g,jsonify
from flask_cors import CORS
import sqlite3,json
from flask_restful import Resource, Api
import settings
from contextlib import closing

app = Flask(__name__)
app.config.from_object(settings)
# print(app.config['DATABASE'])
CORS(app)
api = Api(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db())as db:
        with app.open_resource('schema.sql') as f:
            print(type(f.read()))
            db.cursor().executescript(f.read().decode('GBK'))
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()

class StudentsList(Resource):
    # 显示全部sqlite_sequence
    def get(self):
        cur = g.db.execute('select * from student')
        entries = [dict(id=row[0],name=row[1],age=row[2]) for row in cur.fetchall()]
        return jsonify(entries)
    # 添加
    def post(self):
        data = request.get_json()
        g.db.execute('insert into student (name, age) values (?, ?)',
                     [data['name'], data['age']])
        g.db.commit()
        return jsonify(data)
class Student(Resource):
    # 查询
    def get(self,stu_id):
        cur= g.db.execute('select * from student where id=?', (stu_id))
        entries = [dict(id=row[0],name=row[1], age=row[2]) for row in cur.fetchall()]
        return jsonify(entries)
    # 修改
    def put(self,stu_id):
        entry = json.loads(request.data)
        g.db.execute('update student set name=?,age=? where id = ?', (entry['name'],entry['age'],stu_id))
        g.db.commit()
        return jsonify(entry)
    # 删除
    def delete(self,stu_id):
        g.db.execute("delete from student where id = ?",(stu_id))
        g.db.commit()
        return jsonify({"msg": "删除成功"})
api.add_resource(StudentsList, '/students')
api.add_resource(Student, '/student/<stu_id>')

if __name__ == '__main__':
    # connect_db()
    app.run()
