# AI-Chat-Assistant
An intelligent, real-time chat application featuring streaming responses, persistent conversation history, and a dynamic "Vibe Check" tone modifier. Developed for the Quantiphi assessment.

## Key Features:

* **Real-Time Streaming Chat Interface:** A responsive frontend featuring distinct, scrollable chat bubbles for user inputs and AI responses. Responses stream character-by-character to replicate a live conversational experience.


* **The Vibe Check (Tone Toggle):** Allows users to instantly switch the conversational tone between **"Professional," "Casual,"** or **"Concise."** The backend dynamically translates this preference into system instruction modifiers sent directly to the AI API.


* **History Sidebar:** Persistent panel displaying past conversation threads for easy retrieval and navigation.


* **Robust Backend & Persistence:** Powered by a secure server-side architecture connecting to AI endpoints (OpenAI/Claude) and storing conversation objects (timestamps, prompts, and responses) securely in MongoDB.



## Architecture & Tech Stack

* **Frontend:** Modern, clean UI handling user interactions, scrollable views, and dynamic rendering.


* **Backend:** Secure server-side architecture handling all API integrations, business logic, computations, and database operations.


* **Database:** MongoDB for robust conversation state and history persistence.
