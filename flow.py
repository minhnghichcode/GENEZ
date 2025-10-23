from pocketflow import Flow
from nodes import (
    ParseScriptNode,
    ActScriptNode,
    SynthesizeAudioNode,
    MergeAudioNode
)

def create_podcast_production_flow() -> Flow:
    """
    Creates and connects the nodes to form the podcast production flow.
    """
    parse_script_node = ParseScriptNode()
    act_script_node = ActScriptNode()
    synthesize_audio_node = SynthesizeAudioNode()
    merge_audio_node = MergeAudioNode()

    parse_script_node >> act_script_node >> synthesize_audio_node >> merge_audio_node

    podcast_flow = Flow(start=parse_script_node)
    
    return podcast_flow

if __name__ == '__main__':
    flow = create_podcast_production_flow()
    print("Podcast production flow created successfully.")
    print("Flow structure:")
    
    current_node = flow.start
    while current_node:
        print(f"- {current_node.__class__.__name__}")
        next_nodes = current_node.get_next()
        current_node = next_nodes.get("default") if next_nodes else None
