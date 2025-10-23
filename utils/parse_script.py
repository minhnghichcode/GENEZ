import re

def parse_raw_script(raw_script_content: str) -> list:
    """
    Parses a raw script content to identify roles and dialogues.
    Assumes each line of dialogue is prefixed with 'Role:'.
    """
    structured_script = []
    # Regex to find lines that start with a role name followed by a colon
    # The role name can contain letters, spaces, and Vietnamese characters.
    dialogue_pattern = re.compile(r"^\s*([^:]+):\s*(.*)", re.MULTILINE | re.UNICODE)

    matches = dialogue_pattern.finditer(raw_script_content)

    for match in matches:
        role = match.group(1).strip()
        dialogue = match.group(2).strip()
        if role and dialogue:
            structured_script.append({"role": role, "dialogue": dialogue})

    return structured_script

if __name__ == '__main__':
    # Example usage for testing
    script_content = """
    Bối cảnh: Một buổi tư vấn tâm lý ấm cúng.

    Chuyên gia tư vấn: Chào bác An, mời bác ngồi. Hôm nay trông bác có vẻ hơi trầm tư, có chuyện gì bác muốn chia sẻ không ạ?

    Người cao tuổi: (Thở dài, giọng hơi run) Chào cô. Thực sự thì... dạo này tôi hay cảm thấy cô đơn lắm. Con cháu thì bận rộn, bạn bè cũ thì người còn người mất. Nhiều lúc ngồi một mình trong nhà, tôi thấy trống trải quá.

    Chuyên gia tư vấn: Cháu hiểu cảm giác của bác ạ. Đó là một cảm giác rất thật mà nhiều người cao tuổi phải đối mặt. Bác có thể chia sẻ thêm về những lúc bác cảm thấy cô đơn nhất không?
    """
    parsed = parse_raw_script(script_content)
    for item in parsed:
        print(item)
