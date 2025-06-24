from django.views.generic import TemplateView
from django.shortcuts import redirect

# global in‐memory list of messages
messages = []

class ChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # pass the list of messages to the template
        ctx["messages"] = messages
        return ctx

    def post(self, request, *args, **kwargs):
        text = request.POST.get("message", "").strip()
        if text:
            # Store both the sender and the text
            messages.append({
                "user": request.user,
                "text": text,
            })
            messages.append({
                "user": 0,
                "text": "Answer",
            })
        # redirect to GET to avoid form‐resubmit on reload
        return redirect("chat")
