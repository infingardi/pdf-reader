import re

def extract_with_regex(text: str, schema: dict) -> dict:
    """
    Aplica padrões simples para campos comuns.
    """
    results = {field: None for field in schema.keys()}

    patterns = {
        "cpf": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
        "cnpj": r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",
        "data": r"\b\d{2}/\d{2}/\d{4}\b",
        "telefone": r"\(?\d{2}\)?\s?\d{4,5}-\d{4}\b",
        "inscricao": r"\b\d{4,6}\b"
    }

    for field, desc in schema.items():
        for key, pattern in patterns.items():
            if key in field.lower():
                match = re.search(pattern, text)
                if match:
                    results[field] = match.group()
                    break
    return results
