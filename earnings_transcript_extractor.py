import json

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

        Args:
            json_data (dict): A dictionary that contains a 'transcript' key with a list of speech entries.

        Returns:
            str: A single string containing the full transcript content.
        """
        if "transcript" not in json_data:
            return ""

        contents = [entry["content"] for entry in json_data["transcript"] if "content" in entry]
        return "\n\n".join(contents)

    def process(self):
        data = self.load_json()
        self.transcript_text = self.extract_transcript(data)

        if self.debug:
            return self.transcript_text[:100]
        return self.transcript_text