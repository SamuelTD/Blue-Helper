from django.views.generic import TemplateView
from django.shortcuts import redirect
import requests
import os
from .utils import Login

# global in‐memory list of messages
messages = []

class ChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # pass the list of messages to the template
        ctx["messages"] = messages[-2:]
        return ctx

    def post(self, request, *args, **kwargs):
        text = request.POST.get("message", "").strip()
        if text:
            
            # Store both the sender and the text
            messages.append({
                "user": request.user,
                "text": text,
            })
            
            response = requests.post(f"{os.getenv("API_URL")}/question", json={"question": text, "top_k":1}, headers=Login())
            if response.json()[0]["score"] < 0.5:
                messages.append({
                    "user": 0,
                    "text": "Sorry I don't understand your question, please try again.",
                })
            else:
                messages.append({
                    "user": 0,
                    "text": response.json()[0]["reponse_associee"],
                })
        # redirect to GET to avoid form‐resubmit on reload
        return redirect("chat")
