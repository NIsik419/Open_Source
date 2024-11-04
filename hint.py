import openai

# OpenAI API 키 설정
# openai.api_key =
def generate_hint_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 비용 절약을 위한 저비용 모델 사용
            messages=[
                {"role": "system", "content": "You are an assistant providing hints for coding problems."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.7,
        )
        hint = response.choices[0].message['content'].strip()
        return hint
    except Exception as e:
        print("힌트 생성 오류:", e)
        return "힌트를 생성할 수 없습니다."

# 예제: 문제 설명을 기반으로 첫 번째 힌트를 요청
problem_description = "두 수를 입력받아 합을 출력하는 프로그램을 작성하세요."
prompt = f"문제 설명: {problem_description}\n이 문제를 푸는 첫 번째 힌트를 제공해 주세요."
hint = generate_hint_with_gpt(prompt)
print("힌트:", hint)
