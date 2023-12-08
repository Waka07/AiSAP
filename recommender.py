import numpy as np
import pandas as pd
import sklearn.metrics as skmt

def get_recommendations(searchReqList):
    # 受け取り手データの読み込み
    recipient_data = pd.read_csv('./data/recipient.csv')

    # 受け取り手タイプをチェックする
    recipient_type = 0
    for index, data in recipient_data.iterrows():
        if searchReqList[0] == data["sex"] and searchReqList[1] == data["age_group"] and searchReqList[2] == data["relationship"] and searchReqList[3] == data["scene"]:
            recipient_type = data["recipient_type"]
            break

    # 評価データの読み込み
    rating_data = pd.read_csv('./data/rating.csv')

    # item_id × recipient_typeの行列を作成（とりあえずゼロで埋める）
    item_list = rating_data.sort_values('item_id').item_id.unique()
    recipient_list = rating_data.sort_values('recipient_type').recipient_type.unique()
    rating_matrix = np.zeros([len(item_list), len(recipient_list)])

    # それぞれのitem_idとrecipient_typeの組み合わせの時の評価値を埋める
    for item_id in range(1, len(item_list)+1):
        recipient_list = rating_data[rating_data['item_id'] == item_id].sort_values('recipient_type').recipient_type.unique()
        for type in recipient_list:
            try:
                rating = rating_data[(rating_data['item_id'] == item_id) & (rating_data['recipient_type'] == type)].loc[:, 'rating']
            except:
                rating = 0
            rating_matrix[item_id-1, type-1] = rating

    # scikit-learnのpairwise_distancesを用いてコサイン類似度行列を計算
    similarity_matrix = 1 - skmt.pairwise_distances(rating_matrix, metric='cosine')

    # 対角成分の値はゼロにする
    np.fill_diagonal(similarity_matrix, 0)

    # 対象の受け取り手タイプの評価値を抜き出し、「類似度×評価点」を算出
    rating_matrix_recipient = rating_matrix[:, recipient_type - 1]
    pred_rating = similarity_matrix * rating_matrix_recipient

    # 商品（行）ごとに「類似度×評価点」を合計
    pred_rating_sum = pred_rating.sum(axis=1)
    print(pred_rating_sum)

    # 上位３商品をレコメンドリストに格納
    recommend_list = np.argsort(pred_rating_sum)[::-1][:3] + 1

    # 商品情報を取得する
    item_data = pd.read_csv('./data/item.csv')
    index_1 = recommend_list[0] - 1
    index_2 = recommend_list[1] - 1
    index_3 = recommend_list[2] - 1
    item_1 = [item_data.iloc[index_1,1], item_data.iloc[index_1,3], item_data.iloc[index_1,4]]
    item_2 = [item_data.iloc[index_2,1], item_data.iloc[index_2,3], item_data.iloc[index_2,4]]
    item_3 = [item_data.iloc[index_3,1], item_data.iloc[index_3,3], item_data.iloc[index_3,4]]

    recommended_items = [item_1, item_2, item_3]
    return recommended_items
