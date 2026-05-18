import { useState, useRef, useEffect } from "react";

export default function DocuSenseAI() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);
  
  const BASE_URL = "https://docusenseai-backend.onrender.com";

  useEffect(() => {
  if (messages.length > 0) {
    chatEndRef.current?.scrollIntoView({
      behavior: messages.length === 1 ? "auto" : "smooth"
    });
  }
}, [messages]);

  const uploadPdf = async () => {
    if (!file) {
      alert("Please select a PDF");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await fetch(`${BASE_URL}/upload-pdf`, {
  method: "POST",
  body: formData,
});

      const data = await response.json();

      alert(data.message || "PDF uploaded successfully!");
    } catch (error) {
      console.error(error);
      alert("Upload failed");
    }

    setLoading(false);
  };

  const askQuestion = async () => {
    if (!question.trim()) return;

    const userMessage = {
      type: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentQuestion = question;

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
  `${BASE_URL}/ask?query=${encodeURIComponent(currentQuestion)}`
);

      const data = await response.json();

      const aiMessage = {
        type: "ai",
        text: data.answer,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          text: "Something went wrong.",
        },
      ]);
    }

    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      askQuestion();
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex">
      {/* Sidebar */}
      <div className="w-[320px] border-r border-white/10 bg-[#050505] p-6 hidden lg:flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-3 mb-12">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-r from-violet-600 to-blue-500 flex items-center justify-center text-2xl shadow-lg shadow-violet-500/30">
              DS
            </div>

            <div>
              <h1 className="text-3xl font-bold">DocuSenseAI</h1>
              <p className="text-gray-400 text-sm">
                AI Powered RAG Assistant
              </p>
            </div>
          </div>

          <div className="space-y-4">
            {[
              "Semantic Search",
              "Vector Embeddings",
              "FAISS Retrieval",
              "Local LLM",
              "Context-Aware Answers",
            ].map((item, index) => (
              <div
                key={index}
                className="bg-white/[0.03] border border-white/10 rounded-2xl p-5 hover:border-violet-500/50 transition"
              >
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full bg-violet-500"></div>
                  <span className="font-medium">{item}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gradient-to-br from-violet-500/20 to-blue-500/10 border border-violet-500/20 rounded-3xl p-5">
          <p className="text-sm text-gray-300 leading-relaxed">
            Built using FastAPI, React, LangChain, FAISS, Ollama and local AI
            models.
          </p>
        </div>
      </div>

      {/* Main */}
      <div className="flex-1 p-8 overflow-hidden">
        <div className="max-w-6xl mx-auto">
          <div className="mb-10">
            <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-5 py-2 rounded-full mb-6">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-300">
                Production Grade AI Interface
              </span>
            </div>

            <h1 className="text-7xl font-black leading-tight mb-6">
              Chat With{" "}
              <span className="bg-gradient-to-r from-violet-400 to-blue-400 bg-clip-text text-transparent">
                Your PDFs
              </span>{" "}
              Using AI.
            </h1>

            <p className="text-xl text-gray-400 max-w-3xl leading-relaxed">
              Upload documents and generate grounded AI answers with semantic
              search and retrieval-augmented generation.
            </p>
          </div>

          {/* Upload */}
          <div className="bg-gradient-to-r from-violet-500/10 to-blue-500/10 border border-violet-500/20 rounded-[32px] p-8 mb-8 shadow-2xl shadow-violet-500/10">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
              <div>
                <h2 className="text-4xl font-bold mb-2">Upload PDF</h2>

                <p className="text-gray-400">
                  Select a PDF to build vector embeddings.
                </p>
              </div>

              <div className="flex items-center gap-4">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="text-sm text-gray-300"
                />

                <button
                  onClick={uploadPdf}
                  disabled={loading}
                  className="px-8 py-4 rounded-2xl bg-gradient-to-r from-violet-600 to-blue-500 hover:scale-105 transition-all duration-300 font-semibold shadow-lg shadow-violet-500/30"
                >
                  {loading ? "Uploading..." : "Upload"}
                </button>
              </div>
            </div>
          </div>

          {/* Chat */}
          <div className="bg-white/[0.03] border border-white/10 rounded-[36px] h-[600px] flex flex-col overflow-hidden">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-8 space-y-6">
              {messages.length === 0 && (
                <div className="h-full flex items-center justify-center text-gray-500 text-lg">
                  Ask anything from your document...
                </div>
              )}

              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${
                    msg.type === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-3xl px-6 py-5 rounded-3xl text-lg leading-relaxed shadow-lg ${
                      msg.type === "user"
                        ? "bg-gradient-to-r from-violet-600 to-blue-500"
                        : "bg-white/[0.05] border border-white/10"
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white/[0.05] border border-white/10 px-6 py-5 rounded-3xl flex gap-2">
                    <div className="w-3 h-3 bg-violet-400 rounded-full animate-bounce"></div>
                    <div className="w-3 h-3 bg-violet-400 rounded-full animate-bounce delay-100"></div>
                    <div className="w-3 h-3 bg-violet-400 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              )}

              <div ref={chatEndRef}></div>
            </div>

            {/* Input */}
            <div className="p-6 border-t border-white/10 bg-black/20">
              <div className="flex gap-4">
                <input
                  type="text"
                  placeholder="Ask anything from your document..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={handleKeyDown}
                  className="flex-1 bg-white/[0.05] border border-white/10 rounded-2xl px-6 py-5 text-lg outline-none focus:border-violet-500"
                />

                <button
                  onClick={askQuestion}
                  disabled={loading}
                  className="px-10 py-5 rounded-2xl bg-gradient-to-r from-violet-600 to-blue-500 hover:scale-105 transition-all duration-300 font-bold shadow-lg shadow-violet-500/30"
                >
                  Ask AI
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}