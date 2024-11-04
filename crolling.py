import requests


# solved.ac API를 통해 문제 정보 가져오기
def get_problem_info(problem_id):
    url = f'https://solved.ac/api/v3/problem/show?problemId={problem_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        problem_data = response.json()
        title = problem_data.get('titleKo', '제목 없음')
        difficulty = problem_data.get('level', '난이도 없음')
        print(f"문제 제목: {title}")
        print(f"난이도: {difficulty}")
    else:
        print("문제 정보를 불러오지 못했습니다. 상태 코드:", response.status_code)


# 예시 호출
get_problem_info(1000)
