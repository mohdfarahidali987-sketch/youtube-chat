
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document


def load_transcript(video_id):
    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id, languages=["hi"])

    text = " ".join(
        snippet.text for snippet in transcript
    )

    document = Document(
        page_content=text,
        metadata={
            "source": "youtube",
            "video_id": video_id
        }
    )

    return [document]