import streamlit as st
import json
from util import num_tokens_from_string

f = open('data/model_metadata.json')
model_metadata = json.load(f)

use_cases = ["Summarization", "Translation", "Question Answering", "Text Completion", "Text Classification", "Conversational", "Code Generation", "Sentence Similarity", "Semantic Search"]

st.title("LLMCostMate")
st.write("Find out how much your LLM will cost you")

with st.expander("**Step 1: Select modality**"):
    selected_modality = st.selectbox(label="modality",
                                     options=["Text", "Image", "Audio"],
                                     label_visibility="collapsed")

with st.expander("**Step 2: Select provider**"):
    providers = model_metadata[selected_modality].keys()
    selected_provider = st.selectbox(label="provider",
                                     options=providers,
                                     label_visibility="collapsed")

with st.expander("**Step 3: Select use case**"):
    use_cases = model_metadata[selected_modality][selected_provider]["use_cases"]
    selected_use_case = st.selectbox(label="use_case",
                                     options=sorted(use_cases),
                                     label_visibility="collapsed")

with st.expander("**Step 4: Select model**"):
    models = model_metadata[selected_modality][selected_provider]["models"]
    # output_dict = [x for x in input_dict if x['type'] == '1']

    # Models containing the selected use case
    models = [model for model in model_metadata[selected_modality][selected_provider]["models"] if selected_use_case in model['use_cases'] ]
    
    # Model names
    model_names = [model['name'] for model in models]
    

    selected_model = st.selectbox(label="model",
                                  options=model_names,
                                  label_visibility="collapsed")
    
    # Model cost of selected_model
    if selected_provider == "OpenAI":
        model_cost = [model['completion_cost'] for model in models if model['name'] == selected_model][0]
    elif selected_provider == "Aleph Alpha":
        cost = [model['cost'] for model in models if model['name'] == selected_model][0]
        factor_input_tokens = model_metadata[selected_modality][selected_provider]["factor_input_tokens"][selected_use_case]
        factor_output_tokens = model_metadata[selected_modality][selected_provider]["factor_output_tokens"][selected_use_case]
        
        # TODO - integrate calculation using factor output based on user selection for output token numbers
        model_cost = cost * factor_input_tokens
        
    model_cost_unit = [model['cost_unit'] for model in models if model['name'] == selected_model][0]
    model_cost_currency = [model['cost_currency'] for model in models if model['name'] == selected_model][0]
    model_max_tokens = [model['max_tokens'] for model in models if model['name'] == selected_model][0]
    
    st.write(f"{selected_provider}'s **{selected_model}** model used for **{selected_use_case}** costs **{model_cost_currency}{round(model_cost, 5)}{model_cost_unit}**.")
    
with st.expander("**Step 5: Enter/Paste your input prompt text**"):
    
    # def calc():
    #     st.write(num_tokens_from_string(input_text, model_name=selected_model))
    
    input_text = st.text_area(label="input_text",
                              height=200,
                              max_chars=None,
                              label_visibility="collapsed",
                            #   on_change=calc,
                              key=None)
    
    # Calculate number of tokens for the input string
    num_input_tokens = num_tokens_from_string(input_text, model_name=selected_model)
    # if st.button("Calculate number of tokens", use_container_width=True):
    st.write(f"Your input text has **{num_input_tokens}** tokens.")

with st.expander("**Step 6: Enter max. number of output tokens to generate.**"):
    st.write(f"Your selected model, **{selected_model}** can use up to {model_max_tokens} tokens shared between prompt and completion.")
    num_output_tokens = st.slider(label="target_text",
                                  min_value=1,
                                  max_value=model_max_tokens - num_input_tokens,
                                  step=1)
                            
with st.expander('**Step 7: Get a cost estimate**'):
    total_tokens = num_input_tokens + num_output_tokens
    cost_estimate = model_cost * total_tokens / 1000
    st.write(f"This task will cost **{model_cost_currency}{round(cost_estimate, 5)}**.")
