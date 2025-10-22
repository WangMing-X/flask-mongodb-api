from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import pytz  # 新增：导入时区处理库
from datetime import datetime  # 用于时间处理

app = Flask(__name__)
CORS(app)

# MongoDB 连接（不变）
client = MongoClient("mongodb+srv://wangmingwindyrabbitx_db_user:wamTMFUa1ZVIC1Je@clusterdailytools.xrhfmmo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDailyTools")
db = client["testdatabase"]
collection = db["testtable"]

# 定义东八区（北京时间）时区对象
beijing_tz = pytz.timezone('Asia/Shanghai')

@app.route('/get_latest', methods=['GET'])
def get_latest():
    try:
        latest_list = list(collection.find().sort("time", -1).limit(1))
        if latest_list:
            # 获取MongoDB中的UTC时间（默认存储为UTC）
            utc_time = latest_list[0]["time"]
            
            # 关键：将UTC时间转换为北京时间
            # 若MongoDB存储的是datetime对象，直接转换时区
            beijing_time = utc_time.astimezone(beijing_tz)
            
            # 格式化时间为字符串（保留毫秒，与result中的格式一致）
            beijing_time_str = beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            
            return jsonify({
                "status": "success",
                "result": latest_list[0]["result"],
                "time": beijing_time_str  # 返回转换后的北京时间
            })
        else:
            return jsonify({"status": "error", "message": "暂无数据"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"服务器错误：{str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 补充端口，确保Render能正常运行
