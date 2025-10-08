import os
import subprocess
from glob import glob

# --- Configuration ---
# Path to the cloned MuseTalk repository
MUSE_TALK_DIR = "MuseTalk"
# Path to the pre-trained models
MODEL_DIR = "models"
# Path to the output directory for generated videos
OUTPUT_DIR = "output"

def generate_video_from_text(text, image_path="image.png"):
    """
    Generates a video from a sentence of text and an image using the MuseTalk model.
    Returns the path to the generated video file.
    """
    if not os.path.exists(MUSE_TALK_DIR):
        raise NotADirectoryError(f"MuseTalk directory not found at: {MUSE_TALK_DIR}")

    # Create a temporary audio file for the input text
    # MuseTalk's inference script takes an audio file as input, not raw text.
    # We will need to add a Text-to-Speech (TTS) step here later.
    # For now, we'll use a placeholder audio file that is included with MuseTalk.
    # THIS IS A TEMPORARY WORKAROUND.
    audio_input_path = os.path.join(MUSE_TALK_DIR, "data", "audio", "eng.wav")

    # Clean the output directory before generation
    for f in glob(os.path.join(OUTPUT_DIR, "*")):
        os.remove(f)

    # Construct the command to run MuseTalk's inference script
    # Note: We are using the Python executable from the container's environment
    python_executable = "python"
    inference_script = os.path.join(MUSE_TALK_DIR, "scripts", "inference.py")

    command = [
        python_executable,
        inference_script,
        "--video", image_path,
        "--audio", audio_input_path,
        "--output_dir", OUTPUT_DIR,
    ]

    print(f"Running MuseTalk inference with command: {' '.join(command)}")

    # Add the MuseTalk directory to the Python path
    env = os.environ.copy()
    muse_talk_abs_path = os.path.abspath(MUSE_TALK_DIR)
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = f"{muse_talk_abs_path}:{env['PYTHONPATH']}"
    else:
        env['PYTHONPATH'] = muse_talk_abs_path

    # Execute the command
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, env=env)
    except subprocess.CalledProcessError as e:
        print("--- MuseTalk Inference Failed ---")
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
        raise

    # Find the generated video file
    generated_files = glob(os.path.join(OUTPUT_DIR, "*.mp4"))
    if not generated_files:
        raise FileNotFoundError("MuseTalk did not generate a video file.")

    # Return the path to the first generated video
    return generated_files[0]

if __name__ == '__main__':
    # Example usage:
    print("--- Running Video Generation Example ---")
    try:
        # This example uses a placeholder text, as the audio is hardcoded for now
        placeholder_text = "This is a test sentence."
        video_path = generate_video_from_text(placeholder_text)
        print(f"Successfully generated video at: {video_path}")
    except Exception as e:
        print(f"An error occurred during video generation: {e}")
