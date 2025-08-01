# File: /facebook-ui-tool/facebook-ui-tool/src/models/comment.py

class Comment:
    def __init__(self, author, content, timestamp):
        self.author = author
        self.content = content
        self.timestamp = timestamp

    def __repr__(self):
        return f"Comment(author={self.author}, content={self.content}, timestamp={self.timestamp})"

    def edit(self, new_content):
        self.content = new_content

    def get_summary(self):
        return f"{self.author}: {self.content[:20]}..." if len(self.content) > 20 else self.content