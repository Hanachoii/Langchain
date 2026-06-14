from chains.prompt_templates import REVIEW_PROMPT_TEMPLATE
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def generate_review(code: str, analysis_result: dict) -> str:
    # 프롬프트
    prompt = ChatPromptTemplate.from_template(template=REVIEW_PROMPT_TEMPLATE)
    # 모델
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
    # 파서
    output_parser = StrOutputParser()

    # 체인
    chain = prompt | llm | output_parser
    # 인보크
    return chain.invoke({'code': code, 'analysis_result': analysis_result})