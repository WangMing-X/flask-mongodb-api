from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# 替换为你的 MongoDB 连接字符串（务必确保准确）
client = MongoClient("mongodb+srv://wangmingwindyrabbitx_db_user:wamTMFUa1ZVIC1Je@clusterdailytools.xrhfmmo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDailyTools")
db = client["testdatabase"]
collection = db["testtable"]

@app.route('/get_latest', methods=['GET'])
def get_latest():
    try:
        latest_list = list(collection.find().sort("time", -1).limit(1))
        if latest_list:
            return jsonify({
                "status": "success",
                "result": latest_list[0]["result"],
                "time": str(latest_list[0]["time"])
            })
        else:
            return jsonify({"status": "error", "message": "暂无数据"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"服务器错误：{str(e)}"})

if __name__ == '__main__':
    app.run()
