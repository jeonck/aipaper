import streamlit as st
from openai import OpenAI

# Set a default model
# edited by Lucas
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
# edited by Lucas
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set the sidebar title
st.sidebar.title("Navigation")

# Create API Key input in the sidebar
api_key = st.sidebar.text_input("Enter your API Key", type="password")
if api_key:
    st.sidebar.write("API Key is set.")
    st.session_state.api_key = api_key
else:
    st.sidebar.write("API Key를 입력해 주세요.")

# 사이드바 메뉴 항목 정의
menu = ['AI 논문 검색', '요약', '번역', 'AI 알고리즘']
choice = st.sidebar.selectbox('메뉴', menu)

# AI 논문 검색 페이지
def ai_paper_search():
    st.title('AI 논문 검색')
    query = st.text_input('논문 검색어 입력')
    if query:
        st.write(f"'{query}'에 대한 논문 검색 결과를 표시합니다.")
        # 여기에 논문 검색 기능을 구현

# 요약 페이지
def summary():

    ## Set OpenAI API key from Streamlit secrets
    ## edited by Lucas
    client = OpenAI(api_key=api_key)

    ## Initialize chat history
    if "summary_messages" not in st.session_state:
        st.session_state.summary_messages = []

    st.title('요약')
    text = st.text_area('요약할 텍스트를 입력하세요')
    if st.button('요약하기'):
        if text:
            st.write('요약된 결과:')
            # 여기에 요약 알고리즘을 구현

            # Add user message to chat history
            st.session_state.summary_messages.append({"role": "user", "content": text})

            # Display user message in chat message container
            stream = client.chat.completions.create (
                model = st.session_state["openai_model"],
                messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.summary_messages
                ],
            )

            # Parsing stream 
            message_content = stream.choices[0].message.content

            # Write result
            st.write (message_content)

            # Empty chat history
            st.session_state.summary_messages.clear()
            
            
        else:
            st.write('요약할 텍스트를 입력하세요.')

# 번역 페이지
def translation():
    st.title('번역')
    text = st.text_area('번역할 텍스트를 입력하세요')
    target_lang = st.selectbox('번역할 언어 선택', ['영어', '한국어', '중국어', '일본어'])
    if st.button('번역하기'):
        if text:
            st.write(f'번역된 결과 ({target_lang}):')
            # 여기에 번역 알고리즘을 구현
        else:
            st.write('번역할 텍스트를 입력하세요.')

# AI 알고리즘 페이지
def ai_algorithm():
    st.title('AI 알고리즘')
    algorithm = st.selectbox('알고리즘 선택', ['알고리즘 1', '알고리즘 2', '알고리즘 3'])
    st.write(f'{algorithm}에 대한 설명과 예제를 제공합니다.')
    # 여기에 선택된 알고리즘에 대한 설명과 예제 코드를 구현

# 메뉴 선택에 따라 해당 페이지 호출
if choice == 'AI 논문 검색':
    ai_paper_search()
elif choice == '요약':
    summary()
elif choice == '번역':
    translation()
elif choice == 'AI 알고리즘':
    ai_algorithm()