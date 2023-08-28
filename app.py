import streamlit as st
import json
from util import num_tokens_from_string, num_tokens_from_string_aleph_alpha
import streamlit.components.v1 as components
import webbrowser

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

def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    components.html(open_script)

PROD = True

f = open('data/model_metadata.json')
model_metadata = json.load(f)

st.title("💰 LLMCostMate")

# Introductory Information
with st.expander("What is LLMCostMate?", expanded=False):

    title_col, gif_col = st.columns(2)
    with title_col:
        description = """
        **LLMCostMate** is your LLM Pricing Assistant.
        
        Say goodbye to uncertainty and hello to accurate cost estimates for your Language Model Market (LLM) usage. 
        LLMCostMate guides you through the model selection process, presenting a wide array of models from leading providers like OpenAI, Aleph Alpha and more to come. 
        
        Just enter your input prompt, select an estimated volume for your task, and watch LLMCostMate calculates a tailored cost estimate.
        
        Take control of your budget 💰, make better scalability decisions 📈, and experience LLM pricing transparency like never before. 🚀
        """
        st.write(description)

    with gif_col:
        st.markdown("<div style='text-align: center; width:20px'> <img src='http://www.reactiongifs.com/r/funds.gif' alt='gif' /></div>", unsafe_allow_html=True)

# Contribute, connect, donate
# contribute_col, connect_col, coffee_col = st.columns(3)
connect_col, coffee_col = st.columns(2)

# with contribute_col:
#     if st.button("Want to contribute? \n\n 🔀 Create a Pull Request", use_container_width=True):
#         webbrowser.open_new_tab("https://github.com/kaankork/LLMCostMate")
with connect_col:
    st.button('Want to connect? \n\n 🔗 Add me on LinkedIn', use_container_width=True, on_click=open_page, args=('https://www.linkedin.com/in/kaankorkmaz/',))
    # if st.button("Want to connect? \n\n 🔗 Add me on LinkedIn", use_container_width=True):
    #     webbrowser.open_new_tab("https://www.linkedin.com/in/kaankorkmaz/")
with coffee_col:
    st.button('Enjoy using LLMCostMate? \n\n ☕ Donate a Coffee', use_container_width=True, on_click=open_page, args=('https://www.buymeacoffee.com/kaankorkmaz',))
    # if st.button("Enjoy using LLMCostMate? \n\n ☕ Donate a Coffee", use_container_width=True):
    #     webbrowser.open_new_tab("https://www.buymeacoffee.com/kaankorkmaz")
    

st.write('---')

# Main Section
selection_left_col, selection_mid_col, remarks_cost_col = st.columns(3)
with selection_left_col:
    st.subheader("Model Selection")
    # Select modality
    modalities = model_metadata.keys()
    selected_modality = st.selectbox(label="Select Modality",
                                    options=modalities,
                                    label_visibility="visible")

    # Select provider
    providers = model_metadata[selected_modality].keys()
    selected_provider = st.selectbox(label="Select provider",
                                    options=providers,
                                    label_visibility="visible")

    # Select use-case
    use_cases = model_metadata[selected_modality][selected_provider]["use_cases"]
    selected_use_case = st.selectbox(label="Select use-case",
                                    options=sorted(use_cases),
                                    index=7,
                                    label_visibility="visible")

    # All available models for selected modality and provider
    models = model_metadata[selected_modality][selected_provider]["models"]

    # Models containing the selected use case
    models = [model for model in model_metadata[selected_modality][selected_provider]["models"] if selected_use_case in model['use_cases'] ]
    
    # Model names
    model_names = [model['name'] for model in models]
    
    # Selected model
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
    
with selection_mid_col:    
    # Input/Output Parameters
    st.subheader("Input/Output Parameters")
    input_text = st.text_area(label="Enter/Paste your input prompt text.",
                            height=100,
                            max_chars=None,
                            label_visibility="visible",
                            key=None)
    
    # Calculate number of tokens for the input string
    if selected_provider == "OpenAI":
        num_input_tokens = num_tokens_from_string(input_text, model_name=selected_model)
    elif selected_provider == "Aleph Alpha":
        num_input_tokens = num_tokens_from_string_aleph_alpha(input_text, model_name=selected_model, prod=PROD)
  
    # Number of output tokens
    num_output_tokens = st.slider(label="Enter the max. number of output tokens to generate.",
                                min_value=1,
                                max_value=model_max_tokens - num_input_tokens,
                                label_visibility='visible',
                                value=256,
                                step=1)
    
    # Volume of expected LLM usage
    num_task_volume = st.slider(label="Enter the estimated volume of this task - e.g. number of times you expect to run this task.",
                                min_value=0,
                                max_value=1000000,
                                label_visibility='visible',
                                value=100000,
                                step=10000)
    
# Remarks and Cost Estimate
with remarks_cost_col: 
    # Remarks
    st.subheader("Remarks")
    st.markdown(f"""
                - Your input text has **{num_input_tokens}** tokens.
                - Your selected model, **{selected_model}** can use up to {model_max_tokens} tokens shared between prompt and completion.
                - {selected_provider}'s **{selected_model}** model used for **{selected_use_case}** costs **{model_cost_currency}{round(model_cost, 5)}{model_cost_unit}**.
                """)
    
    # Cost Estimate
    st.subheader("Cost Estimate")

    # Measure total amount of tokens in the request
    total_tokens = num_input_tokens + num_output_tokens
    cost_estimate = model_cost * total_tokens / 1000
    st.write(f"Running this task once will cost **{model_cost_currency}{round(cost_estimate, 6)}**.")
    st.write(f"Running this task {num_task_volume:,} times will cost **{model_cost_currency}{round(cost_estimate * num_task_volume, 2):,}**.")