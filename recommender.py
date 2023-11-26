import numpy as np
import pandas as pd
import sklearn.metrics as skmt
import math
from tqdm import tqdm

def get_recommendations(searchReqList):
    # 受け取り手データの読み込み
    recipient_data = pd.read_csv('./data/recipient.csv')
    # 受け取り手タイプをチェックする
    recipient_type = 0
    for index, data in recipient_data.iterrows():
        if searchReqList[0] == data["sex"] and searchReqList[1] == data["age_group"] and searchReqList[2] == data["relationship"] and searchReqList[3] == data["scene"]:
            recipient_type = data["recipient_type"]
            break

    print(recipient_type)

    # 評価データの読み込み
    rating_data = pd.read_csv('./data/rating.csv')

    # item_id × recipient_typeの行列にする
    item_list = rating_data.sort_values('item_id').item_id.unique()
    recipient_list = rating_data.sort_values('recipient_type').recipient_type.unique()
    rating_matrix_item = np.zeros([len(item_list), len(recipient_list)])
    for item_id in tqdm(range(1, len(item_list)+1)):
        user_list_item = rating_data[rating_data['item_id'] == item_id].sort_values('recipient_type').recipient_type.unique()
        for type in user_list_item:
            try:
                user_rate = rating_data[(rating_data['item_id'] == item_id) & (rating_data['recipient_type'] == type)].loc[:, 'rating']
            except:
                user_rate = -1
            rating_matrix_item[item_id-1, type-1] = user_rate
    #print(rating_matrix_item)
    # item × userの評価したかどうか{0, 1}がわかる行列作成
    #rating_matrix_calc = rating_matrix_item.copy()
    #rating_matrix_calc[pd.notna(rating_matrix_calc)] = 1
    #rating_matrix_calc[pd.isna(rating_matrix_calc)] = 0
    #print(rating_matrix_calc)

    # 評価していないアイテムに1が立つ行列を作成。後で使う
    #rating_matrix_train = np.abs(rating_matrix_calc - 1)
    #print(rating_matrix_train)

    # NaNを0に変換
    rating_matrix_item[pd.isna(rating_matrix_item)] = 0

    # scikit-learnのpairwise_distancesを用いてコサイン類似度行列を出す
    similarity_matrix = 1 - skmt.pairwise_distances(rating_matrix_item, metric='cosine')
    # 対角成分の値はゼロにする
    np.fill_diagonal(similarity_matrix, 0)
    #print(similarity_matrix)

    # 各ユーザの評価値を抜き出し「類似度×評価点」を算出
    rating_matrix_user = rating_matrix_item[:, recipient_type - 1]
    #print(rating_matrix_user)
    pred_rating_user = similarity_matrix * rating_matrix_user
    #print(pred_rating_user)
    # アイテム（行）ごとに「類似度×評価点」を合計
    pred_rating_user = pred_rating_user.sum(axis=1)
    #print(pred_rating_user)

    # ユーザが既に評価したアイテムのスコアはゼロに直す
    #pred_rating_user_item = pred_rating_user * rating_matrix_train[:,recipient_type - 1]
    #print(pred_rating_user_item)

    #ここからレコメンドされたアイテムがどれだけあっていたかを評価していく
    recommend_list = np.argsort(pred_rating_user)[::-1][:3] + 1
    print(recommend_list)

    # 商品情報を取得する
    item_data = pd.read_csv('./data/item.csv')
    index_1 = recommend_list[0] - 1
    index_2 = recommend_list[1] - 1
    index_3 = recommend_list[2] - 1
    item_1 = [item_data.iloc[index_1,1], item_data.iloc[index_1,3], item_data.iloc[index_1,4], item_data.iloc[index_1,5]]
    item_2 = [item_data.iloc[index_2,1], item_data.iloc[index_2,3], item_data.iloc[index_2,4], item_data.iloc[index_2,5]]
    item_3 = [item_data.iloc[index_3,1], item_data.iloc[index_3,3], item_data.iloc[index_3,4], item_data.iloc[index_3,5]]

    recommended_items = [item_1, item_2, item_3]
    return recommended_items
