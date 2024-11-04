document.getElementById("fetchData").addEventListener("click", async function () {
  const problemId = document.getElementById("problemId").value;
  const output = document.getElementById("output");

  if (!problemId) {
    output.textContent = "문제 ID를 입력하세요.";
    return;
  }

  output.textContent = "데이터를 불러오는 중...";

  try {
    // solved.ac API 요청
    const response = await fetch(`https://solved.ac/api/v3/problem/show?problemId=${problemId}`);

    if (response.ok) {
      const data = await response.json();
      output.innerHTML = `<strong>문제 제목:</strong> ${data.titleKo}<br><strong>난이도:</strong> ${data.level}`;
    } else {
      output.textContent = "문제 정보를 불러오지 못했습니다.";
    }
  } catch (error) {
    output.textContent = "오류 발생: " + error.message;
  }
});
