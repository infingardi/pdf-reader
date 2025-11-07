import json
from openai import AsyncOpenAI

async def extract_with_llm(client: AsyncOpenAI, text: str, schema: dict):
    prompt = f"""
    Irei te passar um Texto e um Schema, você precisa extrair as informações do Texto e me retornar um JSON:
    
    Schema: {json.dumps(schema, indent=2, ensure_ascii=False)}

    Este é o Texto que você deve extrair as informações que constam no Schema:
    {text}
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "Você é um extrator de dados estruturados."},
                {"role": "user", "content": prompt}
            ],
        )

        answer = response.choices[0].message.content.strip()

        try:
            data = json.loads(answer)
            
            def normalize_empty_fields(d):
                for k, v in d.items():
                    if isinstance(v, str) and not v.strip():
                        d[k] = None
                    elif isinstance(v, dict):
                        normalize_empty_fields(v)
                return d

            return normalize_empty_fields(data)
        except json.JSONDecodeError:
            return {"raw_response": answer}

    except Exception as e:
        return {field: None for field in schema }
