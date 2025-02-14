from typing import List

from dataclasses import dataclass
from typing import Union, Optional

from data_questionnaire_agent.model.openai_schema import ResponseQuestions


@dataclass
class QuestionAnswer:
    question: str
    answer: Union[str, dict]
    clarification: Optional[str]

    def answer_str(self):
        if not self.answer:
            return ""
        elif isinstance(self.answer, str):
            return self.answer
        else:
            return self.answer["content"]

    def __repr__(self) -> str:
        return f"""{self.question}
{self.answer_str()}"""

    @staticmethod
    def question_answer_factory(question: str, answer: dict):
        return QuestionAnswer(question=question, answer=answer, clarification="")

    @staticmethod
    def question_factory(question: str):
        return QuestionAnswer(question=question, answer="", clarification="")


@dataclass
class Questionnaire:
    questions: List[QuestionAnswer]

    def __repr__(self) -> str:
        return "\n\n".join([str(qa) for qa in self.questions])

    def __len__(self):
        return len(self.questions)

    def answers_str(self) -> str:
        return "\n\n".join(
            [
                qa.answer["content"] if isinstance(qa.answer, dict) else qa.answer
                for qa in self.questions
            ]
        )

    def to_html(self) -> str:
        html = """<table>       
"""
        for qa in self.questions:
            answer = qa.answer
            html += f"""
<tr>
    <td class="onepoint-blue">
        <br />
        Q: {qa.question}
    </td>
</tr>
<tr>
    <td>A: {answer}</td>
</tr>
"""
        html += "</table>"
        return html


def convert_to_question_answers(
    response_questions: ResponseQuestions,
) -> List[QuestionAnswer]:
    return [QuestionAnswer.question_factory(q) for q in response_questions.questions]
