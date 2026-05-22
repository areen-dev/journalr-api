class JournalEntry:
    def __init__(self, content: str):
        self.content = content

    def preview(self) -> str:
        return self.content[0:50]
