from query_data import query_rag
from langchain_community.llms.ollama import Ollama


EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


### Positive test cases. We provide the correct answer and expect the model to agree.
def test_arctic_warming_rate_pos():
    assert query_and_validate(
        question="How fast is the Arctic warming? (Answer with the number only, plus 'times faster' or 'times slower')",
        expected_response="3 times faster",
    )

def test_alaska_precip_trend_pos():
    assert query_and_validate(
        question="In general, is precipitation increasing or decreasing across Alaska? (Answer with the word 'increasing' or 'decreasing')",
        expected_response="Increasing",
    )

def test_fbx_freezing_rain_trend_pos():
    assert query_and_validate(
        question="In Fairbanks, are there more freezing rain events now than in the past? (Answer with a simple 'yes' or 'no')",
        expected_response="Yes",
    )

### Negative test cases. We provide the incorrect answer and expect the model to disagree.
def test_arctic_warming_rate_neg():
    assert not query_and_validate(
        question="How fast is the Arctic warming? (Answer with the number only, plus 'times faster' or 'times slower')",
        expected_response="2 times faster",
    )

def test_alaska_precip_trend_neg():
    assert not query_and_validate(
        question="In general, is precipitation increasing or decreasing across Alaska? (Answer with the word 'increasing' or 'decreasing')",
        expected_response="Decreasing",
    )

def test_fbx_freezing_rain_trend_neg():
    assert not query_and_validate(
        question="In Fairbanks, are there more freezing rain events now than in the past? (Answer with a simple 'yes' or 'no')",
        expected_response="No",
    )


### The validation function using the LLM to compare the expected and actual responses.
def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="phi3:medium")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
