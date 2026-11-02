
const API_URL = "http://127.0.0.1:8000";

interface ChatResponse {
  answer: string;
}

export async function sendMessage(
  videoId: string,
  question: string
): Promise<string> {

  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_id: videoId,
      question: question,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Something went wrong");
  }

  const data: ChatResponse = await response.json();

  return data.answer;
}
