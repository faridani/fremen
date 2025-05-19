import os
import re

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None

from fremen import Fremen

class StepExtractor:
    """Generate step-by-step instructions for website tasks using an LLM."""
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.fremen = Fremen()

    def _call_openai(self, prompt: str) -> str:
        if openai is None:
            raise ImportError("openai package is required for this feature")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"].strip()

    def generate_instructions(self, description: str, use_openai: bool = True) -> str:
        """Return raw LLM output describing how to perform the task."""
        prompt = (
            "Provide numbered step-by-step instructions for the following task:\n"
            f"{description}\n"
            "Respond with a short numbered list."
        )
        if use_openai:
            try:
                return self._call_openai(prompt)
            except Exception:
                pass
        # Fallback to Fremen.ask if OpenAI fails
        return self.fremen.ask(question=prompt)

    def parse_steps(self, text: str) -> list:
        """Parse numbered steps from text and return them as a list."""
        steps = []
        for line in text.splitlines():
            match = re.match(r"\s*\d+[\.\-]?\s*(.*)", line)
            if match:
                step = match.group(1).strip()
                if step:
                    steps.append(step)
        return steps

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python step_extractor.py 'description of task'")
        sys.exit(1)
    description = sys.argv[1]
    extractor = StepExtractor()
    instructions = extractor.generate_instructions(description)
    for idx, step in enumerate(extractor.parse_steps(instructions), 1):
        print(f"{idx}. {step}")
