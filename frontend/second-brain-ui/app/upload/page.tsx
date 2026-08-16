"use client";

// "use client" tells Next.js this component runs in the browser

import { useState } from "react";
import { ingestFile } from "@/lib/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // is called when the user picks file from file picker
  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0] || null;
    setFile(selected);
    setMessage(""); // clears any previous message
  }

  // this is called when the user clicks the 'Upload' button
  async function handleUpload() {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const result = await ingestFile(file);
      setMessage(`✓ ${result}`);
    } catch (error) {
      setMessage(`✗ Something went wrong. Is your FastAPI server running?`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="w-full max-w-md">

        <h1 className="text-3xl font-bold mb-2">Upload a Document</h1>
        <p className="text-gray-500 mb-8">
          Upload a PDF or text file to add it to your Second Brain.
        </p>

        {/* File input */}
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-4">
          <input
            type="file"
            accept=".pdf,.txt,.md"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          {file && (
            <p className="mt-3 text-sm text-gray-600">
              Selected: <span className="font-medium">{file.name}</span>
            </p>
          )}
        </div>

        {/* Upload button */}
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="w-full py-3 px-6 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "Uploading..." : "Upload to Second Brain"}
        </button>

        {/* Status message */}
        {message && (
          <p className={`mt-4 text-sm text-center ${message.startsWith("✓") ? "text-green-600" : "text-red-500"}`}>
            {message}
          </p>
        )}

        {/* Back to home */}
        <a href="/" className="block text-center mt-6 text-sm text-gray-400 hover:text-gray-600">
          ← Back to home
        </a>

      </div>
    </main>
  );
}