import re
from typing import Any


def extract_action_items(text: str) -> list[dict[str, Any]]:
    items = []
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]

    for line in lines:
        # Extract tags (words starting with #)
        tags = re.findall(r"#(\w+)", line)

        # Check if it's an action item
        is_action_item = (
            line.endswith("!")
            or line.lower().startswith("todo:")
            or re.match(r"^#\w+:", line)
            or len(tags) > 0  # Lines with tags are action items
        )

        if is_action_item:

            # Clean description (remove #pattern: prefix if present)
            description = line
            match = re.match(r"^#\w+:\s*", line)
            if match:
                description = line[match.end() :]

            items.append({"description": description.strip(), "tags": tags})

    return items
