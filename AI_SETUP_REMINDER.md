# 🤖 AI Setup Reminder

## Don't Forget to Add Your Groq API Key!

To use the AI financial advisor feature, you need to add your Groq API key:

1. **Get your API key from [Groq Console](https://console.groq.com/keys)**
2. **Edit the `.env` file** in the project root
3. **Replace the placeholder** with your actual key:

```bash
# Before
GROQ_API_KEY=your_copied_key_here

# After (example)
GROQ_API_KEY=gsk_1234567890abcdef...
```

## What the AI Advisor Does

- **Analyzes your recent spending data** from the database
- **Provides witty, helpful saving tips** based on your patterns
- **Uses Groq's Llama 3.3 70B model** for intelligent responses
- **Gives concise, practical advice** (under 50 words)

## How to Use

1. Start both backend and frontend servers
2. Click the "✨ Get AI Advice" button in the app
3. Wait for the AI to analyze your spending
4. Get personalized financial tips!

## Troubleshooting

- **"Please add your Groq API key"** → Add your key to `.env` file
- **"No transaction data available"** → Run the database setup script first
- **"Something went wrong"** → Check your internet connection and API key

---

*The AI advisor is optional - the app works perfectly without it, but it's much more fun with AI-powered tips!* 🚀
