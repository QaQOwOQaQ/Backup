#include "in_mem_vector_similarity.h"
#include <iostream>

int main() {
    // 示例向量和查询向量
    std::vector<float> query_vector = {1.0, 2.0, 3.0};
    std::vector<std::vector<float>> vectors = {
        {1.0, 2.0, 3.0},
        {4.0, 5.0, 6.0},
        {7.0, 8.0, 9.0}
    };

    // 测试余弦相似度
    auto cosine_results = VectorSimilarity::find_top_k_similar_vectors(query_vector, vectors, 2, VectorSimilarity::MetricType::COSINE);
    std::cout << "Top 2 vectors by cosine similarity:" << std::endl;
    for (const auto& result : cosine_results) {
        std::cout << "Vector Index: " << result.second << ", Similarity: " << result.first << std::endl;
    }

    // 测试内积
    auto dot_product_results = VectorSimilarity::find_top_k_similar_vectors(query_vector, vectors, 2, VectorSimilarity::MetricType::DOT_PRODUCT);
    std::cout << "\nTop 2 vectors by dot product:" << std::endl;
    for (const auto& result : dot_product_results) {
        std::cout << "Vector Index: " << result.second << ", Similarity: " << result.first << std::endl;
    }

    // 测试欧氏距离
    auto euclidean_results = VectorSimilarity::find_top_k_similar_vectors(query_vector, vectors, 2, VectorSimilarity::MetricType::EUCLIDEAN);
    std::cout << "\nTop 2 vectors by euclidean distance:" << std::endl;
    for (const auto& result : euclidean_results) {
        std::cout << "Vector Index: " << result.second << ", Similarity: " << -result.first << std::endl; // 注意: 欧氏距离是负值
    }

    return 0;
}
