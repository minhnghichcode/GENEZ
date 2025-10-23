import os
import logging
from flow import create_podcast_production_flow
from dotenv import load_dotenv

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    """
    Main function to run the podcast production pipeline.
    """
    load_dotenv()

    shared = {
        "input_script_path": "input/kichban.txt",
        "structured_script": [],
        "acted_script": [],
        "audio_segments_paths": [],
        "final_podcast_path": ""
    }

    logging.info("Starting the podcast production pipeline...")
    
    podcast_flow = create_podcast_production_flow()
    
    podcast_flow.run(shared)

    logging.info("--- Pipeline Finished ---")
    final_path = shared.get("final_podcast_path")
    if final_path and os.path.exists(final_path):
        logging.info(f"Success! Your podcast is ready at: {final_path}")
    else:
        logging.error("Failure. The podcast could not be generated. Please check the logs for errors.")
    logging.info("------------------------")


if __name__ == "__main__":
    os.makedirs("input", exist_ok=True)
    os.makedirs("output/segments", exist_ok=True)    
    main()
