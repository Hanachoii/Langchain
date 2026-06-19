from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from chains.prompt_templates import REVIEW_PROMPT_TEMPLATE

load_dotenv()


def generate_handoff_review(
    code: str,
    analysis_result: dict,
    style_comparison: dict,
    handoff_score: dict,
    handoff_report: str
) -> str:
    prompt = ChatPromptTemplate.from_template(REVIEW_PROMPT_TEMPLATE)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "code": code,
        "analysis_result": analysis_result,
        "style_comparison": style_comparison,
        "handoff_score": handoff_score,
        "handoff_report": handoff_report,
    })