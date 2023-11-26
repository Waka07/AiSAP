import streamlit as st
from recommender import get_recommendations
from PIL import Image

# タイトルと説明文を設定
st.write('忙しい人のためのギフト提案型AI')
st.title('AiSAP!')
# st.markdown("<hr>", unsafe_allow_html=True)
st.write('ギフトを贈りたい相手のことを教えてください')
st.text('')

# 検索条件を保持するリスト
searchReqList = []

# 性別を選択
sex = st.selectbox('性別', ['男性', '女性'])
searchReqList.append(sex)

# 年齢を選択
#age_group = st.selectbox('年齢', ['10代', '20代前半','20代後半', '30代', '40代', '50代', '60代', '70代', '80代', '90代', '0-1歳', '2歳', '3歳', '4歳', '5歳', '6-9歳'])
age_group = st.selectbox('年齢', ['20代', '30代', '40代'])
searchReqList.append(age_group)

# 関係性を選択
#relationship = st.selectbox('関係性', ['友達', '恋人', '夫婦', '親', '祖父母', '同僚', '上司', '部下', '親戚', 'ペット', 'その他'])
relationship = st.selectbox('関係性', ['友達', '恋人', '上司'])
searchReqList.append(relationship)

# シーンを選択
scene = st.selectbox('シーン', ['誕生日', '記念日', 'お礼'])
searchReqList.append(scene)

# 予算を選択
#price = st.selectbox('予算', ['3000円未満', '3000~5000円未満', '5000~1万円未満', '1万~3万円未満', '3万円以上'])
#searchReqList.append(price)

st.text('')

# 検索ボタン押下時
if st.button("検索"):
    # おすすめ商品を検索
    recommended_items = get_recommendations(searchReqList)

    # 結果を表示
    st.markdown("<hr>", unsafe_allow_html=True)
    for index, item in enumerate(recommended_items):
        link = f'[{index+1}.{item[0]}]({item[2]})'
        st.markdown(link, unsafe_allow_html=True)
        st.write(f'{item[1]}円')
        image = Image.open(f'./img/{item[3]}')
        st.image(image,width=200)
        st.text('')
        st.text('')




