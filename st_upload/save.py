import os

import streamlit as st
from PIL import Image


IMG_PATH = 'imgs'


def list_imgs():
    # IMG_PATH 内の画像ファイルを列挙
    return [
        filename
        for filename in os.listdir(IMG_PATH)
        if filename.split('.')[-1] in ['jpg', 'jpeg', 'png']
    ]

def main():
    st.markdown('# 画像を保存するデモ')
    file = st.file_uploader('画像をアップロードしてください.', type=['jpg', 'jpeg', 'png'])
    if file:
        st.markdown(f'{file.name} をアップロードしました.')
        img_path = os.path.join(IMG_PATH, file.name)
        # 画像を保存する
        with open(img_path, 'wb') as f:
            f.write(file.read())
            
        # 保存した画像を表示
        img = Image.open(img_path)
        st.image(img)
        
    # IMG_DIR 以下の画像から選択
    filename = st.selectbox('ダウンロードする画像を選択', list_imgs())
    # ダウンロード
    st.download_button(
        'ダウンロード',
        open(os.path.join(IMG_PATH, filename), 'br'),
        filename
    )

if __name__ == '__main__':
    main()