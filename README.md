# LLMCostMate
The usage of LLMs has recently become mainstream. While most LLMs are free-for-use and open-sourced, best performing LLMs provided by [OpenAI](https://openai.com/), [AlephAlpha](https://www.aleph-alpha.com/) charge users based on the amount of tokens passed into their API. 

This project aims to provide a cost estimation tool for LLMs. It is a simple web app that allows users to input prompt text and get an estimated cost of using LLMs to generate the text.

## How to use
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
4. Go to `localhost:8051` in your browser and start using the app!

## How to add new LLMs
1. Add the model name and the corresponding cost per token to `model_costs.json`
2. Add the model to `model_dict` in `app.py`

## How to contribute
Feel free to open an issue or pull request. I will review it as soon as I can.

## To-do
- [X] Add a "How to use" section
- [ ] Add a landing page
- [ ] Add more LLMs
- [ ] Add more info about LLMs

## Credits
- [Huggingface](https://huggingface.co/)
- [OpenAI](https://openai.com/)
- [AlephAlpha](https://www.aleph-alpha.com/)