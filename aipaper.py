import streamlit as st
from openai import OpenAI

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
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
    # 애플리케이션 제목 설정
    st.title("문장 요약기")

    # 사이드바에 OpenAI API 키 입력 필드 추가
    api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요:", type="password")

    # 요약할 텍스트 입력 필드 추가
    text_to_summarize = st.text_area("요약할 텍스트를 입력하세요:", "")

    # 프롬프트 템플릿 정의
    template = """
    당신은 문서 요약 전문가입니다. 주어진 텍스트를 간단하고 명확하게 요약해 주세요.
    텍스트: {text}
    요약:
    """
    prompt = PromptTemplate.from_template(template)

    # OpenAI 채팅 모델 초기화
    if api_key:
        model = ChatOpenAI(
            model="gpt-4",
            max_tokens=1024,
            temperature=0.5,
            api_key=api_key,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )

        # 문자열 출력 파서 초기화
        output_parser = StrOutputParser()

        # 프롬프트, 모델, 출력 파서를 연결하여 처리 체인 구성
        chain = prompt | model | output_parser

        # 버튼 클릭 시 체인 실행
        if st.button("요약 시작"):
            if text_to_summarize:
                result = chain.invoke({"text": text_to_summarize})
                st.write("### 요약 결과:")
                st.write(result)
            else:
                st.write("요약할 텍스트를 입력하세요.")
    else:
        st.warning("사이드바에서 API 키를 입력하세요.")
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
