from flask import Flask, request, render_template, jsonify
from openai import OpenAI
from markdown_processor import markdown_to_html, split_html_into_segments, vectorize_segments
from vector_db_sdk import VectorDatabaseSDK
import json


app = Flask(__name__)

# 初始化VectorDatabaseSDK并进行授权
db_sdk = VectorDatabaseSDK(host="172.19.0.9", port=80)
db_sdk.authenticate(username="user2", password="newpassword456")

client = OpenAI(api_key='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')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    markdown_text = file.read().decode('utf-8')
    html_text = markdown_to_html(markdown_text)
    segments = split_html_into_segments(html_text)
    vectors = vectorize_segments(segments)

    # 使用VectorDatabaseSDK将向量上传到数据库
    for i, (segment, vector) in enumerate(zip(segments, vectors)):
        vector_id = i + 1  # 使用段落的索引作为ID
        db_sdk.upsert(id=vector_id, vectors=vector.tolist(), text=segment)

    return jsonify({'message': '文件已处理并上传向量到数据库'})

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    search_text = data.get('search')

    # 添加前缀到查询字符串
    instruction = "为这个句子生成表示以用于检索相关文章："
    search_text_with_instruction = instruction + search_text

    # 向量化修改后的查询
    search_vector = vectorize_segments([search_text_with_instruction])[0].tolist()

    # 使用VectorDatabaseSDK搜索最相近的向量
    search_results = db_sdk.search(vectors=search_vector, k=5)

    # 构建与 LLM API 交互的消息列表
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer questions based solely on the provided content without making assumptions or adding extra information."}
    ]

    # 解析搜索结果
    result_ids = search_results.get('vectors', [])

    # 根据搜索结果的ID查询对应的文本内容
    for result_id in result_ids:
        # 确保ID是整数类型
        if not isinstance(result_id, int):
            result_id = int(result_id)

        query_result = db_sdk.query(id=result_id)
        text = query_result.get('text', '')
        messages.append({"role": "assistant", "content": text})

    messages.append({"role": "user", "content": search_text})

    # 向 OpenAI 发送请求并获取答案
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    answer = response.choices[0].message.content

    return jsonify({'answer': answer})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
