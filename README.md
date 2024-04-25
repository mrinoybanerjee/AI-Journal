# Pen-pal: AI Journaling Chatbot

Pen-pal is an AI-enabled journaling application designed to help users maintain a digital journal and interact with their past entries through a sophisticated chatbot interface. Using cutting-edge AI technologies like Pinecone for vector database management and Google's generative AI for natural language processing, Pen-pal provides a unique tool for personal reflection and journaling.

## Features

- **Journal Entry Management**: Add and store journal entries in a vector database.
- **Intelligent Search**: Retrieve relevant journal entries using natural language queries.
- **AI-driven Interaction**: Engage with past journal entries through a generative AI that provides insights and summaries.

## Installation

To get started with Pen-pal, follow these installation steps. Ensure you have Python 3.8 or newer installed on your machine.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourgithubusername/AI-Journal.git
   cd AI-Journal
   ```

2. **Set up a Virtual Environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory and add your Pinecone and Google Generative AI API keys:
   ```
   PINECONE_API_KEY=your_pinecone_api_key
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

## Usage

Pen-pal is built using Streamlit and can be run locally. Start the application with the following command:

```bash
streamlit run app.py
```

Navigate through the app using the sidebar to add journal entries or interact with the chatbot.

## Repo Tree
```
.
├── README.md
├── app.py
├── notebooks
├── pages
│   ├── chatbot.py
│   └── journal.py
├── requirements.txt
└── src
    └── logic.py

7 directories, 10 files

``` 

### Adding Journal Entries

- Go to the "Add Journal Entry" page.
- Enter your journal entry in the text area and submit.

### Interacting with the Chatbot

- Select "Interact with Chatbot" from the sidebar.
- The chatbot will interact based on your past entries and can answer queries based on the stored journal data.


## Contact

For any inquiries or further assistance, feel free to reach out to Mrinoy Banerjee at mrinoybanerjee@gmail.com.



