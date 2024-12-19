from query_data import query_rag
from langchain_community.llms.ollama import Ollama


EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


### Positive test cases. We provide the correct answer and expect the model to agree.
def test_nome_warming_rate_pos():
    assert query_and_validate(
        question="By how much with the average annual temperature change in Nome by 2100? Answer with the number only, plus 'degrees warmer' or 'degrees cooler'.",
        expected_response="14 degrees warmer",
    )


def test_nome_precip_month_pos():
    assert query_and_validate(
        question="What time(s) of year will have more precipitation in Nome? Answer using only the following words: 'winter', 'spring', 'summer', 'fall'.",
        expected_response="Fall",
    )


def test_fbx_elevation_pos():
    assert query_and_validate(
        question="How many feet above sea level is Fairbanks? Answer this question using only a number and the unit of measurement. Don't use abbreviations in the unit of measurement.",
        expected_response="433 feet",
    )


### Negative test cases. We provide the incorrect answer and expect the model to disagree.
def test_nome_warming_rate_neg():
    assert not query_and_validate(
        question="By how much with the average annual temperature change in Nome by 2100? Answer with the number only, plus 'degrees warmer' or 'degrees cooler'.",
        expected_response="24 degrees warmer",
    )


def test_nome_precip_month_neg():
    assert not query_and_validate(
        question="What time(s) of year will have more precipitation in Nome? Answer using only the following words: 'winter', 'spring', 'summer', 'fall'.",
        expected_response="Winter",
    )


def test_fbx_elevation_neg():
    assert not query_and_validate(
        question="How many feet above sea level is Fairbanks? Answer this question using only a number and the unit of measurement. Dont't use abbreviations in the unit of measurement.",
        expected_response="400 feet",
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
