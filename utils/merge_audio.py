import os
from pydub import AudioSegment

def merge_audio_files(audio_paths: list, output_path: str) -> str:
    """
    Merges multiple MP3 files into a single MP3 file.
    """
    if not audio_paths:
        print("No audio paths provided to merge.")
        return ""

    combined = AudioSegment.empty()
    
    for path in audio_paths:
        try:
            # Read the MP3 file
            sound = AudioSegment.from_mp3(path)
            combined += sound
        except Exception as e:
            print(f"Could not process file {path}: {e}")
            continue

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        combined.export(output_path, format="mp3")
        print(f"Successfully merged audio to {output_path}")
        return output_path
    except Exception as e:
        print(f"Could not export combined audio: {e}")
        return ""

if __name__ == '__main__':
    # This test requires ffmpeg to be installed.
    from pydub.generators import Sine
    
    os.makedirs("output/segments", exist_ok=True)
    
    dummy_path_1 = "output/segments/dummy1.mp3"
    dummy_path_2 = "output/segments/dummy2.mp3"
    
    Sine(440).to_audio_segment(duration=1000).export(dummy_path_1, format="mp3")
    Sine(880).to_audio_segment(duration=1500).export(dummy_path_2, format="mp3")

    test_paths = [dummy_path_1, dummy_path_2]
    test_output = "output/final_podcast.mp3"
    
    merge_audio_files(test_paths, test_output)
