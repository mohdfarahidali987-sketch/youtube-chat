
import { useState } from "react";
import { sendMessage } from "./services/api";

interface Message {
  role: "user" | "assistant";
  text: string;
}

function App() {
  const [isOpen, setIsOpen] = useState(true);
  const [videoId, setVideoId] = useState("");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      text: "Hi! I'm your YouTube AI Assistant. Ask me anything about the video.",
    },
  ]);

  const handleSend = async () => {
    if (!question.trim() || !videoId.trim() || loading) return;

    const currentQuestion = question.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", text: currentQuestion },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const answer = await sendMessage(videoId, currentQuestion);

      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: answer },
      ]);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Something went wrong";

      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: `Error: ${errorMessage}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 rounded-full bg-red-600 p-4 text-white shadow-xl"
      >
        AI
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 flex h-[550px] w-[360px] flex-col overflow-hidden rounded-2xl border border-gray-700 bg-[#171717] text-white shadow-2xl">

      <header className="flex items-center justify-between border-b border-gray-700 p-4">
        <div>
          <h2 className="font-semibold">YouTube AI Assistant</h2>
          <p className="text-xs text-gray-400">
            Ask anything about this video
          </p>
        </div>

        <button onClick={() => setIsOpen(false)}>✕</button>
      </header>

      <div className="border-b border-gray-700 p-3">
        <label className="mb-2 block text-xs text-gray-400">
          YouTube Video ID
        </label>

        <input
          value={videoId}
          onChange={(e) => setVideoId(e.target.value)}
          placeholder="Paste video ID here..."
          className="w-full rounded-lg border border-gray-700 bg-[#252525] p-3 text-sm outline-none focus:border-red-500"
        />
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`max-w-[90%] whitespace-pre-wrap rounded-xl p-3 text-sm ${
              message.role === "user"
                ? "ml-auto bg-red-600"
                : "bg-[#292929]"
            }`}
          >
            {message.text}
          </div>
        ))}

        {loading && (
          <div className="w-fit rounded-xl bg-[#292929] p-3 text-sm text-gray-400">
            AI is thinking...
          </div>
        )}
      </div>

      <div className="border-t border-gray-700 p-3">
        <div className="flex gap-2">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend();
            }}
            placeholder="Ask a question..."
            disabled={loading}
            className="min-w-0 flex-1 rounded-lg bg-[#292929] p-3 text-sm outline-none"
          />

          <button
            onClick={handleSend}
            disabled={loading || !question.trim() || !videoId.trim()}
            className="rounded-lg bg-red-600 px-4 hover:bg-red-700 disabled:opacity-40"
          >
            ↑
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
