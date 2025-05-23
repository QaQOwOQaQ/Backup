from flask import Flask, request, jsonify
from flask import Flask, render_template
from image_eb import extract_features
from vector_db_sdk import VectorDatabaseSDK
import logging
import os

app = Flask(__name__)

db_sdk = VectorDatabaseSDK(host="172.19.0.9", port=80)
db_sdk.authenticate(username="user2", password="newpassword456")

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_image():
    image_file = request.files['image']
    image_path = os.path.join('static/images', 'temp_image.jpg')
    image_file.save(image_path)

    image_features = extract_features(image_path)
    
    # 使用提取的特征向量进行搜索
    search_result = db_sdk.search(vectors=image_features.tolist(), k=5, index_type="FLAT")

    # 将搜索结果转换为图片路径或相应的数据
    # 这取决于您的数据库中图片信息的存储方式

    # 将图片 ID 转换为 URL
    image_urls = [f"/static/images/{int(image_id)}" for image_id in search_result['vectors']]

    return jsonify({"data":search_result, "distances": search_result['distances'], "image_urls": image_urls})


@app.route('/upload', methods=['POST'])
def upload_image():
    image_file = request.files['image']
    image_id_str = request.form.get('image_id')

    # 检查 image_id 是否存在
    if not image_id_str:
        return jsonify({"message": "Image ID is required."}), 400

    # 尝试将 image_id 转换为整型
    try:
        image_id = int(image_id_str)
    except ValueError:
        return jsonify({"message": "Invalid image ID. It must be an integer."}), 400

    filename = image_file.filename  # 直接使用上传的文件名
    image_path = os.path.join('static/images', image_id_str)
    image_file.save(image_path)

    image_features = extract_features(image_path)
    
    # 更新数据库中的记录
    upsert_result = db_sdk.upsert(id=image_id, vectors=image_features.tolist(), index_type="FLAT")
    
    return jsonify({"message": "Image uploaded successfully", "id": image_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)