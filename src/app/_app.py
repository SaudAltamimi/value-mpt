from io import BytesIO
import chainlit as cl
from openai import OpenAI
import mimetypes
from pydub import AudioSegment

client = OpenAI()

@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.AudioChunk):
    if chunk.isStart:
        buffer = BytesIO()
        # This is required for whisper to recognize the file type
        buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
        # Initialize the session for a new audio stream
        cl.user_session.set("audio_buffer", buffer)
        cl.user_session.set("audio_mime_type", chunk.mimeType)

    # Write the chunks to a buffer and transcribe the whole audio at the end
    cl.user_session.get("audio_buffer").write(chunk.data)

@cl.on_audio_end
async def on_audio_end():
    audio_buffer = cl.user_session.get("audio_buffer")
    audio_buffer.seek(0)  # Reset buffer position to the beginning
    audio_file = audio_buffer.read()
    # Get the MIME type of the audio
    mime_type = cl.user_session.get("audio_mime_type")

    try:

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_buffer,
            response_format="text"
        )
        
        await cl.Message(content=f"Transcription: {transcript}").send()
    except Exception as e:
        await cl.Message(content=f"Error during transcription: {str(e)}").send()

    # Clear the buffer after transcription
    cl.user_session.set("audio_buffer", None)