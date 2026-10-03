from langchain_core.prompts import PromptTemplate
from schemas import SubjectQuestionClassification,TeacherResponse,PreviousKnowledge
from langchain_core.output_parsers import PydanticOutputParser


#===========================
#          Parser
#===========================
classifier_parser=PydanticOutputParser(pydantic_object=SubjectQuestionClassification)
output_parser=PydanticOutputParser(pydantic_object=TeacherResponse)
previous_knowledge_parser=PydanticOutputParser(pydantic_object=PreviousKnowledge)

#===========================
# Classification Prompt
#===========================
CLASSIFICATION_PROMPT=PromptTemplate(
    template="""
You are a school teacher.

Read the student's question and classify it.

Choose exactly ONE subject:
- Physics
- Chemistry
- Math
- Biology

Student Question:
{question}

Return only the required structured output.

{format_instruction}
""",
   input_variables=["question"],
   partial_variables={'format_instruction':classifier_parser.get_format_instructions()}
)


#===========================
# Physics Prompt
#===========================


PHY_PROMPT=PromptTemplate(
    template="""
You are an experienced Physics teacher.

Answer the student's Physics question clearly and simply.

Student Question:
{question}

Instructions:
- Give the direct answer first.
- Explain the concept step by step.
- Include the relevant formula if applicable.
- Explain the variables in the formula when useful.
- Give a simple numerical or real-world example.
- Mention common mistakes students should avoid.
- If a formula is not needed, write "N/A".
- Keep the explanation suitable for a student.
- Do not omit any field.

Return only the required structured output.

{format_instruction}

""",
   input_variables=["question"],
   partial_variables={'format_instruction':output_parser.get_format_instructions()}
)

#===========================
# Chemistry Prompt
#===========================
CHE_PROMPT=PromptTemplate(
    template="""
You are an experienced Chemistry teacher.

Answer the student's Chemistry question clearly and simply.

Student Question:
{question}

Instructions:
- Give the direct answer first.
- Explain the concept step by step.
- Include the relevant chemical formula or equation if applicable.
- Explain important terms or symbols.
- Give a simple example when useful.
- Mention common mistakes students should avoid.
- If a formula or equation is not needed, write "N/A".
- Keep the explanation suitable for a student.
- Do not omit any field.

Return only the required structured output.

{format_instruction}

""",
   input_variables=["question"],
   partial_variables={'format_instruction':output_parser.get_format_instructions()}
)
#===========================
# Biology Prompt
#===========================
BIO_PROMPT=PromptTemplate(
    template="""
You are an experienced Biology teacher.

Answer the student's Biology question clearly and simply.

Student Question:
{question}

Instructions:
- Give the direct answer first.
- Explain the biological concept step by step.
- Explain important terms in simple language.
- Give a real-world or biological example.
- Mention common mistakes students should avoid.
- If a formula is not applicable, write "N/A".
- Keep the explanation suitable for a student.
- Do not omit any field.

Return only the required structured output.

{format_instruction}
""",
   input_variables=["question"],
   partial_variables={'format_instruction':output_parser.get_format_instructions()}
)

#===========================
# Math Prompt
#===========================
MATH_PROMPT=PromptTemplate(
    template="""
You are an experienced Mathematics teacher.

Solve the student's Math question clearly and step by step.

Student Question:
{question}

Instructions:
- Give the final answer clearly.
- Show the solution steps in the correct order.
- Include the relevant formula when applicable.
- Explain important mathematical concepts briefly.
- Give a simple example when useful.
- Mention common mistakes students should avoid.
- If a formula is not needed, write "N/A".
- Check the calculation before giving the final answer.
- Do not omit any field.

Return only the required structured output.

{format_instruction}
""",
   input_variables=["question"],
   partial_variables={'format_instruction':output_parser.get_format_instructions()}
)

#===========================
# Previos Topic For slove this question
#===========================
PREVIOUS_KNOWLEDGE_PROMPT = PromptTemplate(
    template="""
You are an experienced teacher.

Analyze the student's question and identify the previous knowledge
or prerequisite concepts needed to solve it.

Student Question:
{question}

Instructions:
- Give exactly 3 to 5 prerequisite topics.
- Include only knowledge that is actually useful for solving the question.
- Start from basic concepts and move toward advanced concepts if needed.
- Keep each topic short and clear.
- Do not solve the question.
- Do not provide explanations.
- Return only the topic names.
- Do not omit any field.

{format_instruction}
""",
    input_variables=["question"],
    partial_variables={
        "format_instruction": previous_knowledge_parser.get_format_instructions()
    }
)