import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('url')
db = client.dbsparta

SECRET_KEY = 'SPARTA'

import jwt

import datetime

import hashlib


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.wishtree.find_one({"id": payload['id']})
        return render_template('tree.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return  redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.wishtree.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.wishtree.find_one({'id': id_receive, 'pw': pw_hash})
    print(result)

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])  # jwt.decode는 jwt페이지에서 보는 decode와 같음
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.wishtree.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route("/wish", methods=["POST"])
def save_wish():
    wish_receive = request.form['wish_give']
    id_receive = request.form['id_give']

    wish_list = list(db.wish.find({}, {'_id': False}))
    count = len(wish_list) + 1

    doc = {
        'wish': wish_receive,
        'num': count,
        'id': id_receive,
        'done': 0
    }
    db.wish.insert_one(doc)
    return jsonify({'msg': '소원빌기 완료'})

@app.route("/wish", methods=["GET"])
def wish_get():
    wish_list = list(db.wish.find({}, {'_id': False}))
    return jsonify({'wishes': wish_list})

@app.route("/wish/done", methods=["POST"])
def wish_done():
    num_receive = request.form['num_give']
    db.wish.update_one({'num': int(num_receive)}, {'$set':{'done':1}})
    return jsonify({'msg': '소원성취!!'})







@app.route("/goTree/get", methods=["GET"])
def set_temp():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get("https://kr.freepik.com/free-photos-vectors/wish", headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')  # soup (data의 html 가져오기)
    images = soup.find_all('img', attrs={
        'class': "min-size-to-snippet"})  # 전체 html 에서 class가 min-size-to-snippet인 전체로 이미지 가져오기 ->images는 한줄한줄, img태그, img태그, img태그 형태이다.

    # tt = soup.find('img', attrs={'class': 'min-size-to-snippet'})     # find는 태그 하나만 찾는다.
    arrayimage = []  # image 값을 담을 배열
    for image in images:  # 반복문을 통해 images 를 image로 떼어낸다.
        img = image['src']  # img태그에서 src 속성을 불러온다.
        arrayimage.append(img)  # 반복문 돌때마다 img를 배열에 담는다.
    # all_id = list(db.tree.find({}, {'_id': False}))
    user_list = list(db.wishtree.find({}, {'_id': False}))
    return jsonify({'user': user_list, 'img': arrayimage})
    # return jsonify({"all_id": all_id, "img": arrayimage})  # json화 시켜서 클라이언트로 보낸다.

# @app.route('/tree', methods=["GET"])
# def tree():










@app.route('/<path>')
def get_path(path):
    return render_template(path + '.html')

@app.route('/tree/<id>')
def get_tree_path(id):
    return render_template('tree.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
