from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from schemas import TeacherResponse,SubjectQuestionClassification,PreviousKnowledge
from langchain_core.runnables import RunnableParallel,RunnableBranch
from prompts import (
    CLASSIFICATION_PROMPT,
    PHY_PROMPT,CHE_PROMPT,
    BIO_PROMPT,MATH_PROMPT,
    PREVIOUS_KNOWLEDGE_PROMPT
)

#===========================
#          Load ENV
#===========================

load_dotenv()

#===========================
#          Parser
#===========================
classifier_parser=PydanticOutputParser(pydantic_object=SubjectQuestionClassification)
output_parser=PydanticOutputParser(pydantic_object=TeacherResponse)
previous_knowledge_parser=PydanticOutputParser(pydantic_object=PreviousKnowledge)

#===========================
#         Model
#===========================
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)



#===========================
#         ALL CHAIN
#===========================

classificaiton_chain=CLASSIFICATION_PROMPT | model | classifier_parser

phy_chain=PHY_PROMPT | model | output_parser

che_chain=CHE_PROMPT | model | output_parser

bio_chain=BIO_PROMPT | model | output_parser

math_chain=MATH_PROMPT | model | output_parser

previous_concept_chain=PREVIOUS_KNOWLEDGE_PROMPT | model | previous_knowledge_parser




#===========================
# Run Chatbot
#===========================
def run_chatbot(user_question: str):

    #===========================
    #   Question Classifier
    #===========================

    classification = classificaiton_chain.invoke({
        "question": user_question
    })

    

    #===========================
    #     Runnable Branch
    #===========================

    conditional_chain = RunnableBranch(
        (lambda x: x["subject"] == "Physics",phy_chain),
        (lambda x: x["subject"] == "Chemistry",che_chain),
        (lambda x: x["subject"] == "Biology",bio_chain),
        math_chain
        
    )

    #===========================
    #     Runnable Parallel
    #===========================

    parallel_chain = RunnableParallel(
        Answer=conditional_chain,
        PreviousKnowledge=previous_concept_chain
    )

    #===========================
    #      Invoke
    #===========================

    result = parallel_chain.invoke({
        "question": user_question,
        "subject": classification.subject
    })

    #===========================
    # 5. GET RESULTS
    #===========================

    answer = result["Answer"]
    previous_knowledge = result["PreviousKnowledge"]

    return {
        "subject": classification.subject,
        "answer": answer,
        "previous_knowledge": previous_knowledge
    }











