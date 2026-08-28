from google import genai
from google.genai import types


class Gemini:
    def __init__(self, model: str, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def add_user_message(self, messages: list, message):
        messages.append({"role": "user", "content": message})

    def add_assistant_message(self, messages: list, message):
        parts = []
        for part in message.parts:
            if part.text:
                parts.append({"text": part.text})
            if part.function_call:
                fc = part.function_call
                parts.append(
                    {
                        "function_call": {
                            "id": fc.id,
                            "name": fc.name,
                            "args": fc.args or {},
                        }
                    }
                )
        messages.append({"role": "assistant", "content": parts})

    def text_from_message(self, message) -> str:
        return "\n".join(
            [part.text for part in message.parts if part.text]
        )

    def _build_parts(self, content) -> list[types.Part]:
        if isinstance(content, str):
            return [types.Part(text=content)]

        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(types.Part(text=item))
            elif "text" in item:
                parts.append(types.Part(text=item["text"]))
            elif "function_call" in item:
                fc = item["function_call"]
                parts.append(
                    types.Part(
                        function_call=types.FunctionCall(
                            id=fc.get("id"),
                            name=fc["name"],
                            args=fc.get("args", {}),
                        )
                    )
                )
            elif "function_response" in item:
                fr = item["function_response"]
                parts.append(
                    types.Part(
                        function_response=types.FunctionResponse(
                            id=fr.get("id"),
                            name=fr["name"],
                            response=fr.get("response", {}),
                        )
                    )
                )
        return parts

    def _build_contents(self, messages) -> list[types.Content]:
        contents = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append(
                types.Content(role=role, parts=self._build_parts(msg["content"]))
            )
        return contents

    def chat(
        self,
        messages,
        tools=None,
        temperature=1.0,
        system=None,
    ) -> types.GenerateContentResponse:
        config = types.GenerateContentConfig(
            temperature=temperature,
            tools=tools or [],
        )

        if system:
            config.system_instruction = system

        return self.client.models.generate_content(
            model=self.model,
            contents=self._build_contents(messages),
            config=config,
        )