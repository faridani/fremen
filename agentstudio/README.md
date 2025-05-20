# Agent Studio

`agentstudio` contains utilities for generating step-by-step website instructions.

The main module `step_extractor.py` provides the `StepExtractor` class, which can
leverage an LLM (such as OpenAI's models or `Fremen.ask` as a fallback) to
convert a natural language description of a task into a list of executable
steps. These steps can be passed to other components of this repository to
automate browser actions.

Example usage:
```bash
python agentstudio/step_extractor.py "figure out how to log in to chase bank"
```
