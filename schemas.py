from pydantic import BaseModel,Field
from typing import List,Literal,Optional

#===========================
#Subject and Question Classifier
#===========================

class SubjectQuestionClassification(BaseModel):
    subject:Literal["Physics","Chemistry","Math","Biolgoy"]=Field(description="The Topic's of the student Question")


#===========================
# Teacher Response Model
#===========================
class TeacherResponse(BaseModel):

    definition:str=Field("Simple defination or direct answer of the question or direct Answer")

    explanation:str=Field("Clear a to z explanation of this qustion answer .")

    formula:str=Field("Relavant formula for this question if not needed simple return N/A ")

    common_mistake:List[str]=Field("Common mistake for slove this question ")

    example:str=Field("A simple real word or numerical example ")

    confidence:float=Field(gt=0.0 ,le=1.0,description="Model Confidence between o and 1")



#===========================
# Knowledge Need for slove this question
#===========================

class PreviousKnowledge(BaseModel):
    topic:List[str]=Field(description="3-5 prerequisite topics or concepts needed to solve the question")
