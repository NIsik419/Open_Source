from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriver 경로 설정
chrome_driver_path = r"C:\Users\Algor\Desktop\chromedriver.exe"


def get_problem_examples(problem_id):
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        url = f"https://www.acmicpc.net/problem/{problem_id}"
        driver.get(url)

        # 문제 제목을 찾기 위해 최대 10초 대기
        title = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "problem_title"))
        ).text

        # 예제 입력 및 출력 추출
        examples = {"input": [], "output": []}
        input_elements = driver.find_elements(By.CLASS_NAME, "sampledata")
        for i, element in enumerate(input_elements):
            if i % 2 == 0:  # 예제 입력
                examples["input"].append(element.text)
            else:  # 예제 출력
                examples["output"].append(element.text)

        # 결과 출력
        print("문제 제목:", title)
        print("예제 입력:", examples["input"])
        print("예제 출력:", examples["output"])
    finally:
        driver.quit()


# 테스트
get_problem_examples(1000)  # 1000번 문제 예시
