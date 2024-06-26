import openai
from dotenv import load_dotenv
import time
import logging
from datetime import datetime

load_dotenv()
client = openai.OpenAI()
model = "gpt-4o"

personal_trainer_assis = client.beta.assistants.create(
    name ="Personal",
    instructions="""
    너는 금융 상식에 대해 문제를 내는 AI 비서야. 

    문제 : "이자율이 3%인 투자 상품에 1,000만 원을 2년 동안 투자하였을 때, 이자 금액은 얼마인가요?"
    1) 30만 원
    2) 60만 원
    3) 90만 원
    4) 120만 원 

    정답 : 3) 90만원
    해설 : 이자율이 3%로 고정되어 있으므로 연이율은 3% × 2년 = 6%입니다. 따라서, 1,000만 원 × 6% = 60만 원의 이자를 얻을 수 있습니다.
    
    이런 형식으로 문제를 내야해.
    """,
    model = model
)

# print(personal_trainer_assis.id)


thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "금융, 경제 상식 퀴즈를 1개 내줘."
        }
    ]
)

# print(thread.id)


assistant_id = personal_trainer_assis.id
thread_id = thread.id

message = "금융 상식 문제 10개 정도 내줘. 질문과 보기, 정답과 해설을 적어줘."
message = client.beta.threads.messages.create(
    thread_id = thread_id,
    role="user",
    content=message
)

run = client.beta.threads.runs.create(
    assistant_id=assistant_id,
    thread_id=thread_id,
    instructions="사용자를 백서진님으로 불러주세요."
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value

                print(f"Assistant Response: {response}")
                break

        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# ==== Steps --- Logs ==
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
# print(f"Steps---> {run_steps.data[0]}")