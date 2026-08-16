export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold mb-4">Second Brain</h1>
      <p className="text-gray-500 mb-8">Your personal AI knowledge base</p>
      <div className="flex gap-4">
        <a href="/upload" className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Upload Documents
        </a>
        <a href="/chat" className="px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-900">
          Ask a Question
        </a>
      </div>
    </main>
  )
}