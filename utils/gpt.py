import asyncio
import json
import os

import aiohttp
from dotenv import load_dotenv
from openai import OpenAI

from utils.llm_cost import get_llm_price

load_dotenv()


def show_llm_price(model, response_data):
    input_token = response_data['usage']['prompt_tokens']
    output_token = response_data['usage']['completion_tokens']
    print(f"""
    #####################################
    Using model: {model}
    Input token: {input_token}
    Output token: {output_token}
    Total cost: {get_llm_price(model)['input'] * input_token
                 + get_llm_price(model)['output'] * output_token}
    #####################################
    """)


class LLM:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.llm = OpenAI(api_key=self.api_key)
        self.model = model

    def get_messages(self, prompt: list):
        if isinstance(prompt, list) and isinstance(prompt[0], str):
            messages = [{'role': 'user', 'content': f'{p}'} for p in prompt]
        elif isinstance(prompt, str):
            messages = [{'role': 'user', 'content': f'{prompt}'}]
        else:
            messages = prompt

        return messages

    def chat(self, prompt: list, model=None, temperature=0.1, json_mode=False, stream=False):
        if not model:
            model = self.model

        messages = self.get_messages(prompt)

        response = self.llm.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream,
            response_format={"type": "json_object" if json_mode else "text"},
        )

        if stream:
            return response

        response_str = response.choices[0].message.content
        response_json = json.loads(response.model_dump_json())

        show_llm_price(model, response_json)

        if json_mode:
            rsp_dict = json.loads(response_str)
            return rsp_dict

        return response_str

    async def chat_async(self, prompt, model=None, temperature=0.1, json_mode=False, stream=False):
        if not model:
            model = self.model

        messages = self.get_messages(prompt)

        url = "https://api.openai.com/v1/chat/completions"

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            "response_format": {"type": "json_object" if json_mode else "text"},
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:

                if stream:
                    return response

                response_data = await response.json()
                res_content = response_data["choices"][0]["message"]["content"]

                show_llm_price(model, response_data)

                if json_mode:
                    return json.loads(res_content)
                else:
                    return res_content


llm = LLM()

if __name__ == '__main__':
    test_prompt = "what is the meaning of life?"
    asyncio.run(llm.chat_async(test_prompt, json_mode=False))
