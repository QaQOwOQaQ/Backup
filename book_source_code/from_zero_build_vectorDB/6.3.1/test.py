from vector_db_sdk import VectorDatabaseSDK

def test_vector_db_sdk():
    db_sdk = VectorDatabaseSDK(host="localhost", port=8080)

    # 测试 upsert 接口
    upsert_result = db_sdk.upsert(id=6, vectors=[0.9], int_field=47, index_type="FLAT")
    print("Upsert Result:", upsert_result)

    # 测试 search 接口
    search_result = db_sdk.search(vectors=[0.9], k=5, index_type="FLAT", field_name="int_field", value=47, op="!=")
    print("Search Result:", search_result)

if __name__ == "__main__":
    test_vector_db_sdk()
