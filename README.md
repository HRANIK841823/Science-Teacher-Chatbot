# 🧑‍🏫 Science Teacher Chatbot

An AI-powered **Science Teacher Chatbot** built with **Python, Streamlit, LangChain, Groq, and Pydantic**.

The chatbot is designed to help students understand **Physics, Chemistry, Biology, and Mathematics** through structured explanations, formulas, examples, common mistakes, and prerequisite knowledge.

The project demonstrates three important LangChain concepts:

* **RunnableBranch** — routes questions to the appropriate subject-specific chain.
* **RunnableParallel** — generates the answer and required previous knowledge simultaneously.
* **Pydantic Structured Output** — ensures that the LLM response follows a predefined and validated structure.

---

## 📌 Project Overview

The Science Teacher Chatbot accepts a student's question and uses an LLM to determine the appropriate subject before generating a structured educational response.

### Supported Subjects

* ⚛️ Physics
* 🧪 Chemistry
* 🧬 Biology
* 📐 Mathematics

### Example

**Student Question:**

> What is the SI unit of speed?

The chatbot can return:

* Definition
* Explanation
* Formula
* Example
* Common mistakes
* Confidence score
* Required previous knowledge

---

## ✨ Features

### 1. Subject Classification

The student's question is first classified into one of the supported subjects:

```text
Physics
Chemistry
Biology
Math
```

The classification is performed using a dedicated LangChain chain and Pydantic structured output.

---

### 2. Subject-Specific Teaching

After classification, the question is routed to the appropriate teacher chain.

For example:

```text
Physics Question
       ↓
Physics Chain
       ↓
Physics Answer
```

Similarly:

```text
Chemistry → Chemistry Chain
Biology   → Biology Chain
Math      → Mathematics Chain
```

---

### 3. Structured Educational Response

The chatbot generates a structured response containing:

* Definition
* Explanation
* Formula
* Example
* Common Mistakes
* Confidence

This makes the response predictable and easy to display in the Streamlit interface.

---

### 4. Previous Knowledge Detection

The chatbot also identifies the concepts that a student should already understand before learning the current topic.

For example, for a question about **ATP synthesis**, the chatbot may identify:

```text
1. Cellular organelles
2. Mitochondria structure
3. ATP synthesis
4. Cellular respiration
5. Energy metabolism
```

This helps students identify prerequisite topics.

---

### 5. Chat History

The Streamlit application maintains the conversation history using:

```python
st.session_state.chat_history
```

Students can continue asking questions within the same session.

A **Clear Chat** button is also provided to reset the conversation.

---

## 🏗️ Project Architecture

The overall workflow is:

```text
                Student Question
                       │
                       ▼
              Question Classifier
                       │
                       ▼
              Subject Classification
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       Physics      Chemistry    Biology
          │            │            │
          └────────────┼────────────┘
                       │
                     Math
                       │
                       ▼
                RunnableBranch
                       │
                       ▼
              ┌─────────────────┐
              │ RunnableParallel│
              └────────┬────────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        Teacher Answer      Previous Knowledge
             │                   │
             └─────────┬─────────┘
                       ▼
                Structured Result
                       │
                       ▼
                 Streamlit UI
```

---

# 🔀 RunnableBranch Implementation

`RunnableBranch` is used to route the student's question to the correct subject-specific chain.

The classification result contains the subject:

```python
classification = classificaiton_chain.invoke({
    "question": user_question
})
```

The subject is then used by `RunnableBranch`:

```python
conditional_chain = RunnableBranch(
    (
        lambda x: x["subject"] == "Physics",
        phy_chain
    ),
    (
        lambda x: x["subject"] == "Chemistry",
        che_chain
    ),
    (
        lambda x: x["subject"] == "Biology",
        bio_chain
    ),
    (
        lambda x: x["subject"] == "Math",
        math_chain
    ),
    phy_chain
)
```

### How it works

If:

```python
x["subject"] == "Physics"
```

the question is sent to:

```python
phy_chain
```

If:

```python
x["subject"] == "Chemistry"
```

it is sent to:

```python
che_chain
```

The same process is used for Biology and Mathematics.

The final `phy_chain` acts as the default branch.

---

# ⚡ RunnableParallel Implementation

`RunnableParallel` is used to execute two independent operations simultaneously:

1. Generate the teacher's answer.
2. Identify the student's required previous knowledge.

Implementation:

```python
parallel_chain = RunnableParallel(
    Answer=conditional_chain,
    PreviousKnowledge=previous_concept_chain
)
```

The input is passed to both chains:

```python
result = parallel_chain.invoke({
    "question": user_question,
    "subject": classification.subject
})
```

The result contains:

```python
answer = result["Answer"]

previous_knowledge = result["PreviousKnowledge"]
```

### Why RunnableParallel?

The teacher answer and previous-knowledge analysis are independent tasks.

Therefore, they can be processed in parallel rather than waiting for one task to finish before starting the other.

Conceptually:

```text
                 Input
                   │
          ┌────────┴────────┐
          ▼                 ▼
    Teacher Chain     Previous Knowledge
          │                 │
          ▼                 ▼
       Answer           Prerequisites
          │                 │
          └────────┬────────┘
                   ▼
                 Result
```

---

# 🧩 Pydantic Structured Output

Pydantic is used to validate and structure the LLM responses.

## TeacherResponse

The teacher response is defined using a Pydantic model:

```python
class TeacherResponse(BaseModel):

    definition: str

    explanation: str

    formula: str

    common_mistake: List[str]

    example: str

    confidence: float = Field(
        gt=0.0,
        le=1.0
    )
```

The output parser is created using:

```python
output_parser = PydanticOutputParser(
    pydantic_object=TeacherResponse
)
```

The model response is then parsed through:

```python
phy_chain = PHY_PROMPT | model | output_parser
```

Similar chains are used for:

```python
che_chain
bio_chain
math_chain
```

---

## 📋 Classification Structured Output

The question classification also uses Pydantic.

```python
classifier_parser = PydanticOutputParser(
    pydantic_object=SubjectQuestionClassification
)
```

This allows the application to receive a predictable classification result such as:

```text
Subject: Physics
```

instead of relying on unstructured text from the LLM.

---

## 📚 Previous Knowledge Structured Output

Previous knowledge is also represented with a Pydantic model:

```python
previous_knowledge_parser = PydanticOutputParser(
    pydantic_object=PreviousKnowledge
)
```

For example:

```python
{
    "topic": [
        "Cellular organelles",
        "Mitochondria structure",
        "ATP synthesis",
        "Cellular respiration",
        "Energy metabolism"
    ]
}
```

This makes the output easier to process in the Streamlit application.

---

# 🤖 LLM

The project uses the **Groq Chat Model** through LangChain:

```python
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)
```

`temperature=0` is used to make the responses more consistent and deterministic.

---

# 🖥️ Streamlit Interface

The user interface is built using Streamlit.

The application provides:

* Chat interface
* Subject information
* Chat history
* Clear Chat button
* Structured answer sections
* Required knowledge section

Example response layout:

```text
Definition
──────────
...

Explanation
──────────
...

Formula
──────────
...

Example
──────────
...

Common Mistakes
──────────
1. ...
2. ...

Confidence
──────────
0.95

Required Knowledge
──────────
1. ...
2. ...
```

---

# 📁 Project Structure

A possible project structure is:

```text
science-teacher-chatbot/
│
├── app.py
├── chatbot.py
├── schemas.py
├── prompts.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### `app.py`

Contains the Streamlit user interface and chat history management.

### `chatbot.py`

Contains:

* LLM configuration
* Pydantic parsers
* Subject classification chain
* Subject-specific chains
* RunnableBranch
* RunnableParallel
* Main chatbot function

### `schemas.py`

Contains the Pydantic models used for structured output.

### `prompts.py`

Contains the prompts for:

* Question classification
* Physics
* Chemistry
* Biology
* Mathematics
* Previous knowledge detection

### `.env`

Stores API credentials and other environment variables.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/science-teacher-chatbot.git
```

Move into the project directory:

```bash
cd science-teacher-chatbot
```

---

## 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
streamlit
python-dotenv
langchain
langchain-core
langchain-groq
pydantic
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not commit your `.env` file to GitHub.

Add it to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

# ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🧪 Example Questions

You can test the chatbot with questions such as:

### Physics

```text
What is the SI unit of speed?
```

### Chemistry

```text
What is the difference between an acid and a base?
```

### Biology

```text
What is the function of mitochondria?
```

### Mathematics

```text
What is the quadratic formula?
```

---

# 📸 Screenshots

Screenshots can be added here after running the application.

Example:

```markdown
## Screenshots

### Main Chat Interface

![Science Teacher Chatbot](screenshots/home.png)

### Structured Answer

![Structured Answer](screenshots/answer.png)

### Required Knowledge

![Required Knowledge](screenshots/previous-knowledge.png)
```

Recommended screenshot directory:

```text
screenshots/
├── home.png
├── answer.png
└── previous-knowledge.png
```

---

# 🛠️ Technologies Used

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Python         | Programming language            |
| Streamlit      | Web interface                   |
| LangChain      | LLM workflow orchestration      |
| LangChain Groq | Groq model integration          |
| Groq           | Large Language Model API        |
| Pydantic       | Structured output validation    |
| python-dotenv  | Environment variable management |

---

# 🔄 Complete Workflow

The chatbot follows this workflow:

```text
1. User enters a question
          ↓
2. Question classification
          ↓
3. Subject identified
          ↓
4. RunnableBranch selects subject chain
          ↓
5. RunnableParallel runs:
       ├── Teacher Answer
       └── Previous Knowledge
          ↓
6. Pydantic validates both outputs
          ↓
7. Structured result returned
          ↓
8. Streamlit displays the response
          ↓
9. Conversation stored in chat history
```

---

# 🎯 Learning Objectives

This project demonstrates practical use of modern LangChain concepts:

* Building LLM chains
* Prompt engineering
* Pydantic structured output
* Output parsing
* Conditional routing with `RunnableBranch`
* Parallel execution with `RunnableParallel`
* Streamlit session state
* Chat history management
* Subject-specific AI workflows

---

# 🚀 Future Improvements

Possible future improvements include:

* [ ] Add more science subjects
* [ ] Add image/question recognition
* [ ] Add mathematical equation rendering
* [ ] Add conversation memory
* [ ] Add quiz generation
* [ ] Add student progress tracking
* [ ] Add difficulty-level selection
* [ ] Add multilingual support
* [ ] Add RAG using science textbooks
* [ ] Deploy the chatbot online

---

# 👨‍💻 Author

**Md. Habibur Rahman Anik**
Computer Science & Engineering Student

---

## 📄 License

This project is created for educational and learning purposes.
