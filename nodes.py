import os
import logging
from pocketflow import Node, BatchNode
from utils.parse_script import parse_raw_script
from utils.call_llm import call_llm
from utils.tts_gemini import text_to_speech
from utils.merge_audio import merge_audio_files


class ParseScriptNode(Node):
    def prep(self, shared):
        logging.info("[ParseScriptNode] Preparing to parse script...")
        script_path = shared.get("input_script_path")
        if not script_path or not os.path.exists(script_path):
            logging.error(f"Script file not found at {script_path}")
            raise FileNotFoundError(f"Script file not found at {script_path}")
        
        with open(script_path, 'r', encoding='utf-8') as f:
            return f.read()

    def exec(self, raw_script_content):
        logging.info("[ParseScriptNode] Executing script parsing...")
        return parse_raw_script(raw_script_content)

    def post(self, shared, prep_res, exec_res):
        shared["structured_script"] = exec_res
        logging.info(f"[ParseScriptNode] Script parsed successfully. Found {len(exec_res)} dialogues.")
        return "default"

class ActScriptNode(BatchNode):
    def prep(self, shared):
        logging.info("[ActScriptNode] Preparing to act out script...")
        return enumerate(shared.get("structured_script", []))

    def exec(self, indexed_item):
        index, script_item = indexed_item
        role = script_item["role"]
        dialogue = script_item["dialogue"]
        
        logging.info(f"[ActScriptNode] Processing dialogue {index + 1} for role: {role}")

        # --- CRITICAL FIX: Updated prompts to generate speakable text directly ---
        if role == "Chuyên gia tư vấn":
            system_prompt = "Bạn là một diễn viên lồng tiếng chuyên nghiệp, vào vai một chuyên gia tư vấn tâm lý. Hãy diễn lại câu thoại sau một cách tự nhiên, ấm áp và truyền cảm nhất. Chỉ trả về câu thoại đã được diễn lại, không thêm bất kỳ ghi chú hay chỉ dẫn nào."
        elif role == "Người cao tuổi":
            system_prompt = "Bạn là một diễn viên lồng tiếng chuyên nghiệp, vào vai một người cao tuổi. Hãy diễn lại câu thoại sau với giọng điệu phù hợp với tâm trạng của nhân vật (có thể là hoài niệm, mệt mỏi, hoặc trầm ngâm). Chỉ trả về câu thoại đã được diễn lại, không thêm bất kỳ ghi chú hay chỉ dẫn nào."
        else:
            system_prompt = "Bạn là một diễn viên lồng tiếng. Hãy diễn lại câu thoại sau một cách tự nhiên nhất. Chỉ trả về câu thoại đã được diễn lại."

        prompt = f'Câu thoại gốc: "{dialogue}"'
        
        logging.info(f"[ActScriptNode] Calling LLM for dialogue {index + 1}...")
        acted_dialogue = call_llm(prompt, system_prompt)
        # Clean up potential markdown like quotes
        acted_dialogue = acted_dialogue.strip().replace('"', '')
        logging.info(f"[ActScriptNode] LLM response received for dialogue {index + 1}: '{acted_dialogue}'")
        
        return {"role": role, "acted_dialogue": acted_dialogue}

    def post(self, shared, prep_res, exec_res_list):
        shared["acted_script"] = exec_res_list
        logging.info("[ActScriptNode] Script acted out successfully.")
        return "default"

class SynthesizeAudioNode(BatchNode):
    def prep(self, shared):
        logging.info("[SynthesizeAudioNode] Preparing to synthesize audio...")
        return enumerate(shared.get("acted_script", []))

    def exec(self, indexed_item):
        segment_index, acted_item = indexed_item
        role = acted_item["role"]
        acted_dialogue = acted_item["acted_dialogue"]
        
        logging.info(f"[SynthesizeAudioNode] Processing segment {segment_index} for role: {role}")
        
        voice_map = {"Chuyên gia tư vấn": "Kore", "Người cao tuổi": "Zephyr"}
        voice_name = voice_map.get(role, "Puck") 
        output_path = f"output/segments/segment_{segment_index}.mp3"
        logging.info(f"[SynthesizeAudioNode] Calling TTS API for segment {segment_index}...")
        result_path = text_to_speech(acted_dialogue, voice_name, output_path)
        logging.info(f"[SynthesizeAudioNode] TTS API call finished for segment {segment_index}.")

        return result_path

    def post(self, shared, prep_res, exec_res_list):
        shared["audio_segments_paths"] = [path for path in exec_res_list if path]
        logging.info(f"[SynthesizeAudioNode] Audio synthesized successfully. {len(shared['audio_segments_paths'])} segments created.")
        return "default"

class MergeAudioNode(Node):
    def prep(self, shared):
        logging.info("[MergeAudioNode] Preparing to merge audio segments...")
        return shared.get("audio_segments_paths", [])

    def exec(self, audio_paths):
        logging.info(f"[MergeAudioNode] Merging {len(audio_paths)} audio segments...")
        output_path = "output/final_podcast.mp3"
        return merge_audio_files(audio_paths, output_path)

    def post(self, shared, prep_res, exec_res):
        shared["final_podcast_path"] = exec_res
        logging.info(f"[MergeAudioNode] Podcast finished. Saved to: {exec_res}")
        return "default"
