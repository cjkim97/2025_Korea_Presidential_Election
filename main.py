import streamlit as st
import requests
from PIL import Image


def main():
    ## 서비스 URL
    search_url = st.secrets["PROMISE_SEARCH_SERVICE_URL"]
    LJM_chat_session = st.secrets["LJM_DEBATE_URL"]
    KMS_chat_session = st.secrets["KMS_DEBATE_URL"]
    LJS_chat_session = st.secrets["LJS_DEBATE_URL"]
    
    
    ## 페이지 디자인 영역 
    st.set_page_config(
    page_title="제21대 대선 후보 공약 RAG",
    page_icon="🗳️",
    # layout='wide'
    ) 
    with open( "asset/style.css", encoding='utf-8-sig' ) as css:
        st.markdown(f"""<style>{css.read()}</style>""", unsafe_allow_html=True)
    
    ## 메인 타이틀
    # _,main_title,_ = st.columns([1,10,1], vertical_alignment = "center")
    # main_title.subheader('21대 대선 후보들은 어떤 공약을 냈을까?')
    st.write('''<div class="page_links">
            <div class="link"> <a href="https://github.com/cjkim97/2025_Korea_Presidential_Election"> 📝 사용설명서 </a> </div>
            <div class="link"> <a href="https://blog.naver.com/nuang0530"> 🏠 제작자의 블로그 </a> </div>
         </div>''', 
         unsafe_allow_html=True)
    for _ in range(5) : st.write('') # 공백 
    st.html('''<h1 class="title">21대 대선 후보들은 어떤 공약을 했을까요?</h1>''')

    ## 공약 검색  
    _,search,_ = st.columns([1,6,1], vertical_alignment = "top")
    question = search.text_input("3명의 후보에게 대한민국의 미래를 물어보세요!", 
                      help="질문을 하면, 각 후보들이 어떤 공약을 준비했는지 알려드립니다.",
                      placeholder="대한민국이 AI 강국이 되기 위해서는 어떻게 준비하실 건가요?",
                      icon = "🤔" )
    search.markdown(f"""<p class="notice">🚫주의🚫<br>실제 후보의 의견이 아닙니다!! <br> AI의 답변이므로 절대 신뢰하지 마세요!!</p>""", unsafe_allow_html=True)  
    # st.write(search_url)
    # n8n Webhook으로 POST 요청
    if question : 
        try : 
            with st.spinner("후보들의 공약을 찾아보고 있습니다...", show_time=True) : 
                response = requests.post(search_url, {"chatInput": question})
                response.raise_for_status()
                data = response.json()
        except : 
            raise

        ## 후보들의 답변
        ### 데이터 가공
        LJM_result = {} 
        KMS_result = {}
        LJS_result = {}
        for answer in data : 
            if answer['candidates_name'] == '이재명' : LJM_result = answer
            elif answer['candidates_name'] == '김문수' : KMS_result = answer
            else : LJS_result = answer
        
        
        ## 3대 후보의 답변
        promise_tab_title = "답변과 관련된 공약보기"
        # LJM.image('asset/imgs/LJM.webp', use_container_width= True)
        with st.chat_message('human', avatar='asset/imgs/LJM.jpg') : 
            st.write(LJM_result['answer'])
            expander_box, button_box = st.columns([4,1], vertical_alignment="top", )
            with expander_box.expander(promise_tab_title) : 
                st.markdown(LJM_result['context'].replace('\n', '<br>'), unsafe_allow_html=True)
            button_box.link_button('더 대화하기', LJM_chat_session ,type='primary', use_container_width = True)

        with st.chat_message('human', avatar='asset/imgs/KMS.jpg') : 
            st.write(KMS_result['answer'])
            expander_box, button_box = st.columns([4,1], vertical_alignment="top", )
            with expander_box.expander(promise_tab_title) : 
                st.markdown(KMS_result['context'].replace('\n', '<br>'), unsafe_allow_html=True)
            button_box.link_button('더 대화하기', KMS_chat_session ,type='primary', use_container_width = True)

        with st.chat_message('human', avatar='asset/imgs/LJS.jpg') : 
            st.write(LJS_result['answer'])
            expander_box, button_box = st.columns([4,1], vertical_alignment="top", )
            with expander_box.expander(promise_tab_title) : 
                st.markdown(LJS_result['context'].replace('\n', '<br>'), unsafe_allow_html=True) 
            button_box.link_button('더 대화하기', LJS_chat_session ,type='primary', use_container_width = True)
    else : 
        # 기본화면에서는 바로 더 대화해보기 버튼만 뜨게끔
        st.link_button('대통령 후보 공약 보러가기', "https://policy.nec.go.kr/", use_container_width = True)
        LJM, KMS, LJS = st.columns(3)
        LJM.image('asset/imgs/LJM.jpg')
        LJM.link_button('심도있게 대화하기', LJM_chat_session ,type='primary', use_container_width = True)
        KMS.image('asset/imgs/KMS.jpg')
        KMS.link_button('심도있게 대화하기', KMS_chat_session ,type='primary', use_container_width = True)
        LJS.image('asset/imgs/LJS.jpg')
        LJS.link_button('심도있게 대화하기', LJS_chat_session ,type='primary', use_container_width = True)

if __name__ == "__main__":
    main() 
 