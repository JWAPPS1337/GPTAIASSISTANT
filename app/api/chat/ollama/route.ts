import { ServerRuntime } from "next"
import { StreamingTextResponse } from "ai"

export const runtime: ServerRuntime = "edge"

// Define constants for Ollama configuration
const OLLAMA_API_URL = process.env.NEXT_PUBLIC_OLLAMA_URL || "http://localhost:11434"
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || "llama3"

export async function POST(request: Request) {
  const json = await request.json()
  const { chatSettings, messages } = json as {
    chatSettings: any
    messages: any[]
  }

  try {
    // Prepare the request body for Ollama
    const ollama_request = {
      model: chatSettings.model || OLLAMA_MODEL,
      prompt: formatPrompt(messages),
      stream: true
    };

    // Call Ollama API
    const response = await fetch(`${OLLAMA_API_URL}/api/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(ollama_request)
    });

    if (!response.ok) {
      throw new Error(`Ollama API returned ${response.status}: ${await response.text()}`);
    }

    // Create a transformer to convert Ollama streaming format to the format expected by the client
    const transform = createOllamaTransformer();

    // Return a streaming response
    return new StreamingTextResponse(response.body!.pipeThrough(transform));
  } catch (error: any) {
    let errorMessage = error.message || "An unexpected error occurred";
    const errorCode = error.status || 500;

    return new Response(JSON.stringify({ message: errorMessage }), {
      status: errorCode
    });
  }
}

// Format messages array into a single prompt string for Ollama
function formatPrompt(messages: any[]): string {
  let formattedPrompt = "";
  for (const message of messages) {
    formattedPrompt += `${message.role}: ${message.content}\n`;
  }
  // Add the assistant prefix to indicate we're awaiting the model's response
  formattedPrompt += "assistant: ";
  return formattedPrompt;
}

// Create a transformer that converts Ollama streaming format to the client-expected format
function createOllamaTransformer() {
  const encoder = new TextEncoder();
  const decoder = new TextDecoder();
  let buffer = '';

  return new TransformStream({
    transform(chunk, controller) {
      // Add the new chunk to our buffer
      buffer += decoder.decode(chunk, { stream: true });
      
      // Process any complete lines in the buffer
      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // The last line may be incomplete, so put it back in the buffer
      
      for (const line of lines) {
        if (line.trim() === '') continue;
        
        try {
          // Parse the JSON response from Ollama
          const parsedLine = JSON.parse(line);
          
          // Extract just the response text
          const deltaText = parsedLine.response;
          
          // Format in the way the client expects (similar to OpenAI format)
          const formattedData = JSON.stringify({ 
            delta: { content: deltaText }
          });
          
          // Send the formatted chunk to the client
          controller.enqueue(encoder.encode(`data: ${formattedData}\n\n`));
          
          // If this is the final chunk, send the "[DONE]" message
          if (parsedLine.done) {
            controller.enqueue(encoder.encode('data: [DONE]\n\n'));
          }
        } catch (error) {
          console.error('Error parsing Ollama response:', error, 'Line:', line);
          // Continue processing other lines even if one fails
        }
      }
    },
    flush(controller) {
      // Process any remaining data in the buffer when the stream completes
      if (buffer.trim()) {
        try {
          const parsedLine = JSON.parse(buffer);
          const deltaText = parsedLine.response;
          const formattedData = JSON.stringify({ 
            delta: { content: deltaText }
          });
          controller.enqueue(encoder.encode(`data: ${formattedData}\n\n`));
        } catch (error) {
          console.error('Error processing final buffer:', error);
        }
      }
      
      // Send the final [DONE] message if it wasn't sent in the last chunk
      controller.enqueue(encoder.encode('data: [DONE]\n\n'));
    }
  });
} 