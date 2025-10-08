from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
import asyncio

from app.text_processor import read_story, split_into_sentences
from app.video_generator import generate_video_from_text

app = FastAPI()

async def video_streamer():
    """
    A generator function that yields video chunks for streaming.
    """
    story_text = read_story()
    sentences = split_into_sentences(story_text)

    for sentence in sentences:
        print(f"--- Generating video for sentence: '{sentence}' ---")
        try:
            # Generate the video for the current sentence
            video_path = generate_video_from_text(sentence)

            # Stream the generated video file
            with open(video_path, "rb") as video_file:
                while chunk := video_file.read(1024 * 1024): # Read 1MB chunks
                    yield chunk
                    await asyncio.sleep(0.001) # Small sleep to prevent blocking

            # Clean up the generated video file
            os.remove(video_path)
            print(f"--- Finished streaming and cleaned up {video_path} ---")

        except Exception as e:
            print(f"Error generating or streaming video for a sentence: {e}")
            # Decide if you want to stop or continue on error
            continue

@app.get("/stream")
async def stream_video():
    """
    API endpoint to stream the lip-synced video.
    """
    return StreamingResponse(video_streamer(), media_type="video/mp4")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Lip-Sync Video Streaming API. Go to /stream to start the video."}

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server. Access the stream at http://127.0.0.1:8000/stream")
    uvicorn.run(app, host="0.0.0.0", port=8000)
