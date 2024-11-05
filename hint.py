import openai
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# OpenAI API 키 설정
openai.api_key = ""  # 실제 API 키로 대체


def get_problem_data(problem_id):
    # Selenium으로 문제 정보 크롤링
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        url = f"https://www.acmicpc.net/problem/{problem_id}"
        driver.get(url)

        # 문제 설명, 입력 및 출력 형식을 각각 ID로 가져오기
        problem_description = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "problem_description"))
        ).text

        input_format = driver.find_element(By.ID, "problem_input").text
        output_format = driver.find_element(By.ID, "problem_output").text


        # problem_info 테이블의 각 <tr> 태그에서 시간 제한 및 메모리 제한을 가져오기
        problem_info = driver.find_element(By.ID, "problem-info")
        rows = problem_info.find_elements(By.TAG_NAME, "tr")
        time_limit = rows[0].text  # 첫 번째 <tr> 태그에서 시간 제한 정보
        memory_limit = rows[1].text  # 두 번째 <tr> 태그에서 메모리 제한 정보


        return {
            "description": problem_description,
            "input_format": input_format,
            "output_format": output_format,
            "time_limit": time_limit,
            "memory_limit": memory_limit
        }

    finally:
        driver.quit()


def generate_hint_with_full_context(problem_data, step_description):
    # 문제 설명, 입력 형식, 출력 형식, 시간 제한, 메모리 제한을 모두 포함
    prompt = (
        f"문제 설명: {problem_data['description']}\n"
        f"입력 형식: {problem_data['input_format']}\n"
        f"출력 형식: {problem_data['output_format']}\n"
        f"시간 제한: {problem_data['time_limit']}\n"
        f"메모리 제한: {problem_data['memory_limit']}\n\n"
        f"{step_description}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant providing hints for coding problems with python."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0,
        )
        hint = response.choices[0].message['content'].strip()
        return hint
    except Exception as e:
        print("힌트 생성 오류:", e)
        return "힌트를 생성할 수 없습니다."


def get_sequential_hints(problem_id):
    # 문제 데이터 크롤링
    problem_data = get_problem_data(problem_id)

    # 각 단계별 요청을 위한 설명
    steps = [
        "이 문제의 분류에 대해 키워드로만 설명해 주세요.",
        "이 문제를 해결하기 위한 최소한의 함수 작성 틀을 제공해 주세요.",
        "문제를 단계별로 해결할 수 있는 접근법을 설명해 주세요.",
        "문제의 전체 솔루션 코드를 보여 주세요."
    ]

    for i, step_description in enumerate(steps, start=1):
        hint = generate_hint_with_full_context(problem_data, step_description)
        input(f"\n힌트 {i}: {hint}\n다음 힌트를 보려면 Enter를 누르세요.")
        time.sleep(1)


# 테스트 실행: 문제 번호 예시
get_sequential_hints(1003)