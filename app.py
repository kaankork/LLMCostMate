import streamlit as st
import json
from util import num_tokens_from_string, num_tokens_from_string_aleph_alpha
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LLMCostMate",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': None,
        'Get help': None,
        'Report a Bug': None
    }
)

f = open('data/model_metadata.json')
model_metadata = json.load(f)

title_col, gif_col = st.columns(2)
with title_col:
    st.markdown("# LLMCostMate")
    description = """
    Introducing **LLMCostMate**: Your Ultimate LLM Pricing Assistant 🎉 
    
    Say goodbye to uncertainty and hello to accurate cost estimates for your Language Model Market (LLM) needs. 
    LLMCostMate seamlessly guides you through the selection process, presenting a wide array of models from leading providers. 
    Input your text and select an estimated volume for your task, and watch as LLMCostMate swiftly calculates a tailored cost estimate.
    
    Take control of your budget 💰, maximize your investment 📈, and experience LLM pricing transparency like never before. 🚀
    """
    st.write(description)

with gif_col:
    st.markdown("<div style='text-align: center; width:20px'> <img src='http://www.reactiongifs.com/r/funds.gif' alt='gif' /></div>", unsafe_allow_html=True)

st.write('---')
selection_left_col, selection_mid_col, cost_col = st.columns(3)
with selection_left_col:
    # with st.expander("**Step 1: Select modality**"):
    modalities = model_metadata.keys()
    selected_modality = st.selectbox(label="Select Modality",
                                    options=modalities,
                                    label_visibility="visible")

    # with st.expander("**Step 2: Select provider**"):
    providers = model_metadata[selected_modality].keys()
    selected_provider = st.selectbox(label="Select provider",
                                    options=providers,
                                    label_visibility="visible")

    # with st.expander("**Step 3: Select use case**"):
    use_cases = model_metadata[selected_modality][selected_provider]["use_cases"]
    selected_use_case = st.selectbox(label="Select use-case",
                                    options=sorted(use_cases),
                                    label_visibility="visible")

    # with st.expander("**Step 4: Select model**"):
    models = model_metadata[selected_modality][selected_provider]["models"]
    # output_dict = [x for x in input_dict if x['type'] == '1']

    # Models containing the selected use case
    models = [model for model in model_metadata[selected_modality][selected_provider]["models"] if selected_use_case in model['use_cases'] ]
    
    # Model names
    model_names = [model['name'] for model in models]
    

    selected_model = st.selectbox(label="Select model",
                                options=model_names,
                                label_visibility="visible")
    
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
    
    # st.write(f"{selected_provider}'s **{selected_model}** model used for **{selected_use_case}** costs **{model_cost_currency}{round(model_cost, 5)}{model_cost_unit}**.")

with selection_mid_col:    
    # with st.expander("**Step 5: Enter/Paste your input prompt text**"):
              
    input_text = st.text_area(label="Enter/Paste your input prompt text.",
                            height=100,
                            max_chars=None,
                            label_visibility="visible",
                            key=None)
    
    # Calculate number of tokens for the input string
    if selected_provider == "OpenAI":
        num_input_tokens = num_tokens_from_string(input_text, model_name=selected_model)
    elif selected_provider == "Aleph Alpha":
        num_input_tokens = num_tokens_from_string_aleph_alpha(input_text, model_name=selected_model)
    # if st.button("Calculate number of tokens", use_container_width=True):
    # st.write(f"Your input text has **{num_input_tokens}** tokens.")

    # with st.expander("**Step 6: Enter max. number of output tokens to generate.**"):
    # st.write(f"Your selected model, **{selected_model}** can use up to {model_max_tokens} tokens shared between prompt and completion.")
    num_output_tokens = st.slider(label="Enter the max. number of output tokens to generate.",
                                min_value=1,
                                max_value=model_max_tokens - num_input_tokens,
                                label_visibility='visible',
                                value=256,
                                step=1)
    
    num_task_volume = st.slider(label="Enter the estimated volume of this task - e.g. number of times you expect to run this task.",
                                min_value=0,
                                max_value=1000000,
                                label_visibility='visible',
                                value=100000,
                                step=10000)
    

with cost_col: 
    st.subheader("Remarks")
    st.markdown(f"""
                - Your input text has **{num_input_tokens}** tokens.
                - Your selected model, **{selected_model}** can use up to {model_max_tokens} tokens shared between prompt and completion.
                - {selected_provider}'s **{selected_model}** model used for **{selected_use_case}** costs **{model_cost_currency}{round(model_cost, 5)}{model_cost_unit}**.
                """)
    st.subheader("Cost Estimate")
    # with st.expander('**Step 7: Get a cost estimate**'):
    total_tokens = num_input_tokens + num_output_tokens
    cost_estimate = model_cost * total_tokens / 1000
    st.write(f"Running this task once will cost **{model_cost_currency}{round(cost_estimate, 6)}**.")
    st.write(f"Running this task {num_task_volume:,} times will cost **{model_cost_currency}{round(cost_estimate * num_task_volume, 2):,}**.")
    
st.write('---')
st.write('For questions, comments, or suggestions, please contact me directly on LinkedIn https://www.linkedin.com/in/kaankorkmaz/.')