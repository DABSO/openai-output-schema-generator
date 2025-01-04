# OpenAI Schema Generator

## Overview
This project provides a Streamlit-based web application for generating and editing valid JSON schemas for OpenAIs structured Output feature using OpenAI's API. It helps developers create, validate, and maintain structured JSON schemas through a chat-like interface. The generated schemas are automatically validated and can be saved for future use.

## 🚀 Features
- Interactive chat interface for schema generation
- Real-time schema preview and validation
- Automatic schema saving with timestamps
- Support for complex schema structures including nested objects and arrays
- Enforced schema validation rules (required fields, additional properties, etc.)
- Streamlit-based user interface

## 📋 Prerequisites
- Python 3.x
- OpenAI API key

## 🛠️ Setup


1. Install dependencies:
    pip install -r requirements.txt

2. Configure environment variables:
    Create a `.env` file in the root directory and add:
    OPENAI_API_KEY=your_api_key_here

## 💻 Usage

### Running the Application
Start the Streamlit application:
    streamlit run app.py

### Using the Interface
1. Enter your schema requirements in natural language in the chat input
2. View the generated schema in the chat interface
3. Click the 💾 button to save any schema you want to keep
4. Generated schemas are saved in the `generated_schemas` directory with timestamps


## 📁 Project Structure
.
├── app.py                  # Main Streamlit application
├── schema_generation.py    # Schema generation logic
├── system_prompt.txt      # System instructions for schema generation
├── meta_schema.json       # Meta schema definition
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (create this)
└── generated_schemas/     # Output directory for saved schemas


## 📝 License
MIT License

