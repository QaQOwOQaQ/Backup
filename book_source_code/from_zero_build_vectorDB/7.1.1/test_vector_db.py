import logging
from vector_db_sdk import VectorDatabaseSDK
from image_eb import extract_features

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def insert_image_to_db(image_path, image_id, db_sdk):
    # 提取图像特征
    image_features = extract_features(image_path)

    # 将 NumPy 数组转换为列表
    image_features_list = image_features.tolist()

    # 将图像特征向量插入到数据库中
    upsert_result = db_sdk.upsert(id=image_id, vectors=image_features_list, int_field=47, index_type="FLAT")
    
    # 记录日志
    logging.info("Upsert Result: %s", upsert_result)

    # 返回图像特征向量
    return image_features_list



def search_in_db(query_vector, k, db_sdk, field_name, value, op):
    # 使用 search 接口进行查询
    search_result = db_sdk.search(vectors=query_vector, k=k, index_type="FLAT", field_name=field_name, value=value, op=op)
    
    # 记录日志
    logging.info("Search Result: %s", search_result)


def test_vector_db_sdk():
    # 初始化向量数据库SDK
    db_sdk = VectorDatabaseSDK(host="172.19.0.9", port=80)
    db_sdk.authenticate(username="user2", password="newpassword456")

    # 插入图像并获取其特征向量
    image_path = "personal.jpeg"
    image_id = 4
    image_features = insert_image_to_db(image_path=image_path, image_id=image_id, db_sdk=db_sdk)

    # 如果插入成功，进行搜索
    if image_features is not None:
        # 使用相同或相似的特征向量进行搜索
        search_in_db(query_vector=image_features, k=5, db_sdk=db_sdk, field_name="int_field", value=47, op="=")

if __name__ == "__main__":
    test_vector_db_sdk()




