import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


PROJECT_STRUCTURE_PROMPT = """
너는 초보 개발팀을 위한 AI 프로젝트 설계 도우미이다.

사용자가 만들고 싶은 프로젝트 설명:
{project_description}

팀원 수:
{member_count}

이 프로젝트를 초보 개발팀이 협업해서 만들 수 있도록 기능을 나누고 파일 구조를 설계하라.

반드시 아래 JSON 형식으로만 답변하라.
설명 문장, 마크다운, 코드블럭은 출력하지 마라.

{{
  "project_name": "프로젝트 이름",
  "summary": "프로젝트 요약",
  "folders": [
    {{
      "path": "폴더 경로",
      "purpose": "폴더 역할"
    }}
  ],
  "features": [
    {{
      "name": "기능 이름",
      "description": "기능 설명",
      "difficulty": "낮음/중간/높음",
      "files": [
        "관련 파일 경로"
      ],
      "dependencies": [
        "선행되어야 하는 기능 이름"
      ],
      "pr_checklist": [
        "이 기능에서 반드시 확인해야 하는 기능별 PR 체크 항목",
        "다른 기능과 연결될 때 확인해야 하는 입력/출력 항목",
        "초보 개발자가 놓치기 쉬운 예외 처리 항목"
      ]
    }}
  ],
  "development_order": [
    "먼저 개발할 기능 이름"
  ],
  "parallel_tasks": [
    [
      "동시에 개발 가능한 기능 이름",
      "동시에 개발 가능한 기능 이름"
    ]
  ],
  "beginner_warnings": [
    "초보 개발팀이 주의해야 할 점"
  ]
}}
"""


def generate_project_structure_plan(
    project_description: str,
    member_count: int
) -> dict:
    prompt = ChatPromptTemplate.from_template(PROJECT_STRUCTURE_PROMPT)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({
        "project_description": project_description,
        "member_count": member_count
    })

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "error": "LLM 응답을 JSON으로 변환하지 못했습니다.",
            "raw_response": response
        }