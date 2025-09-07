from typing import List, Dict

class PromptBuilder:
    """Construct system and user prompts for article generation."""

    def __init__(self, topic: str, example_texts: List[str], style: Dict, structure: Dict | None = None):
        self.topic = topic
        self.example_texts = example_texts
        self.style = style
        self.structure = structure or {}

    def build_prompts(self) -> tuple[str, str]:
        examples_section = "\n\n".join(
            f"Example {i+1}:\n{text}" for i, text in enumerate(self.example_texts)
        )

        style_lines = []
        if self.style.get("has_subheadings"):
            style_lines.append("Include subheadings to organize the article.")
        style_lines.append(
            f"Average paragraph length around {int(self.style.get('avg_paragraph_length', 0))} words."
        )
        if self.style.get("list_frequency", 0) > 0:
            style_lines.append("Use bullet lists where appropriate.")
        tone = self.style.get("tone")
        if tone == "formal":
            style_lines.append("Use a formal tone.")
        elif tone == "informal":
            style_lines.append("Use an informal tone.")
        style_section = "\n".join(style_lines)

        structure_lines = []
        if self.structure.get("h1"):
            structure_lines.append("Start with an H1 title.")
        if self.structure.get("h2"):
            structure_lines.append("Use H2 subheadings for sections.")
        if self.structure.get("bullets"):
            structure_lines.append("Include bullet lists.")
        if self.structure.get("cta"):
            structure_lines.append("End with a clear call to action.")
        if self.structure.get("conclusion"):
            structure_lines.append("Provide a concise conclusion.")
        structure_section = "\n".join(f"- {line}" for line in structure_lines)

        system_prompt = "You are an expert marketing content writer."
        user_prompt = (
            f"Write a marketing article about \"{self.topic}\".\n\n"
            f"Style guidelines:\n{style_section}\n\n"
            f"Structure preferences:\n{structure_section}\n\n"
            f"Style examples:\n{examples_section}"
        )
        return system_prompt, user_prompt
