# Budget-Tracking

 #Backend Setup
Prerequisites

Python 3.8 or higher
MongoDB 4.4 or higher
pip (Python package manager)

1.Installation Steps
***Create and activate virtual environment:
python -m venv venv
venv\Scripts\activate

***Install required packages:
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install pymongo
pip install pyjwt


 #Frontend Setup

Prerequisites
Node.js 14 or higher
npm (Node package manager)

Installation Steps

1.Install dependencies:
cd frontend
npm install

2.Install required packages:
npm install react-router-dom
npm install @tailwindcss/forms
npm install tailwindcss postcss autoprefixer


3.Initialize Tailwind CSS:
npx tailwindcss init -p

Start development server:
npm start
The frontend will be running on http://localhost:3000


Environment Variables
Backend (.env)
SECRET_KEY=your_secret_key
DEBUG=True

MONGODB_URI=mongodb+srv://avasanth081:vasanth@cluster1.ed7yf.mongodb.net/?retryWrites=true&w=majority&appName=cluster1
MONGODB_NAME=budget

Frontend (.env)
REACT_APP_API_URL=http://localhost:8000/api
