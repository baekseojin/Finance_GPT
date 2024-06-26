import streamlit as st
from dotenv import load_dotenv
import openai
import time
import logging

load_dotenv()

# OpenAI 클라이언트 초기화
client = openai.OpenAI()

# Assistant 및 thread ID 설정 
assistant_id = "asst_dYAbCRtvM7PHz0e9zhU2BFxb"
thread_id = "thread_yEDHhL3B08OEMvd3CK2PC7LQ"

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    실행 완료를 기다리고 Assistant의 응답을 출력합니다.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                # 마지막 메시지 가져오기
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value

                st.write(f"Assistant 응답: {response}")
                break

        except Exception as e:
            logging.error(f"실행을 가져오는 중 오류 발생: {e}")
            break

        logging.info("실행 완료 대기 중...")
        time.sleep(sleep_interval)

# Streamlit 앱 시작
def main():
    st.title('Economy AI')
    st.write('AI가 내는 금융/경제 상식 문제를 맞춰보세요.')

    # 사용자 입력 기능 구현
    user_input = st.text_input('질문을 해보세요.')

    if st.button('질문하기'):
        # 스레드에 메시지 추가
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # AI 실행 시작
        run = client.beta.threads.runs.create(
            assistant_id=assistant_id,
            thread_id=thread_id,
            instructions="사용자에게 답변을 제공하세요."
        )

        # 실행 완료 대기
        wait_for_run_completion(client, thread_id, run.id)

# Streamlit 애플리케이션 실행
if __name__ == '__main__':
    main()
