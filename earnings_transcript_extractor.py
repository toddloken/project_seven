import json
import tiktoken


class TranscriptExtractor:
    def __init__(self, filepath, debug=True):
        self.filepath = filepath
        self.debug = debug
        self.transcript_text = ""

    def load_json(self):
        with open(self.filepath, "r") as f:
            return json.load(f)

    def extract_transcript(self, json_data):
        """
        Extracts and concatenates all 'content' fields from the 'transcript' list in the provided JSON.
        """
        if "transcript" not in json_data:
            return ""

        contents = [entry["content"] for entry in json_data["transcript"] if "content" in entry]
        return "\n\n".join(contents)

    def count_tokens(self, text, encoding_name="cl100k_base"):
        """
        Count the number of tokens in a text string.
        """
        encoding = tiktoken.get_encoding(encoding_name)
        tokens = encoding.encode(text)
        token_count = len(tokens)
        print(f"Earnings Call Transcript = Token count: {token_count}")
        return token_count

    def process(self):
        data = self.load_json()
        self.transcript_text = self.extract_transcript(data)
        earnings_call_tokens = self.count_tokens(self.transcript_text)
        if self.debug:
            self.transcript_text = self.transcript_text[:25000]
        else:
            self.transcript_text = self.transcript_text[:50000]
        earnings_call_tokens = self.count_tokens(self.transcript_text)
        return self.transcript_text