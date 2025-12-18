import streamlit as st
import json
from openai import OpenAI

# ページ設定
st.set_page_config(
    page_title="🧠 ブレインロッド キャラクター生成器",
    page_icon="🧠",
    layout="wide"
)

# タイトルとヘッダー
st.title("🧠 ブレインロッド キャラクター生成器")
st.markdown("---")
st.markdown("""
### 🎨 シュールで奇妙なキャラクターを自動生成！
このアプリは、AIを使ってブレインロット風のシュールなキャラクターを生成します。
""")

# OpenAIクライアントの初期化
@st.cache_resource
def get_openai_client():
    return OpenAI()

client = get_openai_client()

# セッション状態の初期化
if 'character_data' not in st.session_state:
    st.session_state.character_data = None
if 'image_prompt' not in st.session_state:
    st.session_state.image_prompt = None
if 'image_url' not in st.session_state:
    st.session_state.image_url = None


def generate_character_data():
    """
    LLMを使用してキャラクター情報を生成します。
    """
system_prompt = (
    "あなたは『Brainrot meme』風のキャラクターを生成するアーティストです。"
    "シュールで混沌としており、少し不気味だがユーモラスなキャラクターを考えてください。"
    "キャラクターは以下を必ずランダムに組み合わせます："
    "・動物または昆虫"
    "・無機物や機械"
    "・異なる文化・時代・架空文明の要素"
    "特定の国や文化（例：イタリア）に偏らないでください。"
    "出力は必ずJSON形式で、キーは 'name', 'traits', 'backstory', 'image_prompt' としてください。"
)

    
user_prompt = (
    "1. 名前 (name): ミーム的で音の響きが変な名前（実在言語でなくてよい）\n"
    "2. 特徴 (traits): 3〜4個。矛盾・不条理・異種融合を含める\n"
    "3. 背景 (backstory): 非論理的で短い起源\n"
    "4. 画像プロンプト (image_prompt): 英語。\n"
    "Brainrot meme style, low resolution texture, uncanny eyes, chaotic fusion, vivid colors.\n"
    "Do NOT reference real people.\n"
)


try:
    with st.spinner("✨ キャラクターを生成中..."):
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )

        character_data = json.loads(response.choices[0].message.content)
        return character_data

except Exception as e:
    st.error(f"❌ エラーが発生しました: {e}")
    return None

def generate_image(prompt):
    try:
        with st.spinner("🖼️ 画像を生成中..."):
            result = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024"
            )
            return result.data[0].url
    except Exception as e:
        st.error(f"画像生成エラー: {e}")
        return None



# メインのUI
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎲 キャラクター生成")
    
if st.button("🚀 新しいキャラクターを生成", use_container_width=True, key="generate_btn"):
    character_data = generate_character_data()
    if character_data:
        st.session_state.character_data = character_data
        
        image_prompt = character_data.get("image_prompt", "")
        st.session_state.image_prompt = image_prompt
        
        # ★ここで画像生成
        st.session_state.image_url = generate_image(image_prompt)

        st.success("✅ キャラクター生成完了！")


with col2:
    st.subheader("📋 生成されたキャラクター")
    
    if st.session_state.character_data:
        character = st.session_state.character_data
        
        st.markdown(f"### 👤 {character.get('name', 'N/A')}")
        
        st.markdown("**特徴:**")
        traits = character.get('traits', [])
        if isinstance(traits, list):
            for trait in traits:
                st.markdown(f"- {trait}")
        else:
            st.markdown(f"- {traits}")
        
        st.markdown("**背景:**")
        st.markdown(character.get('backstory', 'N/A'))

        if st.session_state.image_url:
            st.image(
        st.session_state.image_url,
        caption="🧠 Generated Brainrot Character",
        use_container_width=True
    )

        
        # コピーボタン
        st.markdown("---")
        st.markdown("**画像生成用プロンプト:**")
        image_prompt = character.get('image_prompt', '')
        st.text_area("", value=image_prompt, height=100, disabled=True, key="prompt_display")
        
        if st.button("📋 プロンプトをコピー", use_container_width=True):
            st.info("✅ プロンプトがコピーされました！")
    else:
        st.info("🎲 「新しいキャラクターを生成」ボタンをクリックしてください。")

# 下部セクション
st.markdown("---")
st.subheader("💡 使い方")
st.markdown("""
1. **「新しいキャラクターを生成」ボタンをクリック** → AIがシュールなキャラクターを作成します
2. **生成されたキャラクター情報を確認** → 名前、特徴、背景が表示されます
3. **画像プロンプトをコピー** → 画像生成AIに入力して、キャラクター画像を生成できます

### 🎨 画像生成について
生成されたプロンプトを以下のサービスで使用できます：
- [DALL-E 3](https://openai.com/dall-e-3/)
- [Midjourney](https://www.midjourney.com/)
- [Stable Diffusion](https://stability.ai/)

### 📝 注意事項
- 各キャラクターはランダムに生成されます
- 同じキャラクターが生成されることもあります
- 画像生成には別途APIキーが必要な場合があります
""")

st.markdown("---")
st.markdown("*Made with ❤️ using Streamlit and OpenAI*")

