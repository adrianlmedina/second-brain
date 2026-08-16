const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";


export async function ingestFile(file: File): Promise<string> {
    const formData = new FormData()

    formData.append("file", file);
    
    const response = await fetch(`${API_URL}/upload-file/`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error('Ingest failed: ${response.statusText}');
    }
    const data = await response.json();
    return data.message;
}



export async function queryBrain(question: string): Promise<string> {
    const response = await fetch(`${API_URL}/query/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({question}),
    });
    if (!response.ok) {
        throw new Error('Query failed: ${response.statusText}');
    }
    const data = await response.json();
    return data.answer;
}
