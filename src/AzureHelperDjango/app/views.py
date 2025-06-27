# from django.views.generic import TemplateView
# from django.shortcuts import redirect
# import requests
# import os
# from .utils import Login

# # global in‐memory list of messages
# answers = []
# question_index=0
# max_index = 0
# user_question = ""

# class ChatView(TemplateView):
#     template_name = "chat.html"

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         # pass the list of messages to the template
#         ctx["answers"] = answers[-2:]
#         ctx["question"] = user_question
#         return ctx

#     def post(self, request, *args, **kwargs):
#         text = request.POST.get("message", "").strip()
#         if text:
#             # Store both the sender and the text
#             # answers.append({
#             #     "user": request.user,
#             #     "text": text,
#             # })
#             user_question = text

#             answers = []
#             response = requests.post(f"{os.getenv("API_URL")}/question", json={"question": text, "top_k":3}, headers=Login())
#             for x in range(0, len(response.json())):
#                 if response.json()[x]["score"] >= 0.5:
#                     answers.append(response.json()[0]["reponse_associee"])
                   
#             if len(answers) == 0:
#                 answers.append("Sorry I don't understand your question, please try again.")
                  
#         # redirect to GET to avoid form‐resubmit on reload
#         return redirect("chat")

# views.py

import os
import requests
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .utils import Login

class ChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # pull everything out of the session (or use sensible defaults)
        question = self.request.session.get("question", "")
        answers  = self.request.session.get("answers", [])
        idx      = self.request.session.get("index", 0)

        # pick the current answer (if any)
        current_answer = ""
        if answers and 0 <= idx < len(answers):
            current_answer = answers[idx]

        # “More” should be enabled only if there's more than one answer
        has_next = len(answers) > 1

        ctx.update({
            "question": question,
            "answer": current_answer,
            "has_next": has_next,
        })
        return ctx

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")

        if action == "ask":
            text = request.POST.get("message", "").strip()
            if text:
                resp = requests.post(
                    f"{os.getenv('API_URL')}/question",
                    json={"question": text, "top_k": 3},
                    headers=Login(),
                ).json()

                answers = [
                    item["reponse_associee"]
                    for item in resp
                    if item.get("score", 0) >= 0.5
                ] or ["Sorry, I don't understand your question; please try again."]

                request.session["question"] = text
                request.session["answers"]  = answers
                request.session["index"]    = 0

        elif action == "next":
            answers = request.session.get("answers", [])
            if len(answers) > 1:
                idx = request.session.get("index", 0)
                # cycle around
                request.session["index"] = (idx + 1) % len(answers) 

        return redirect("chat")


