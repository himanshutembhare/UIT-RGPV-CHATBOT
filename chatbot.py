import json
import os
import datetime

# ---------------- OFFLINE COLLEGE CHATBOT ----------------


college_faq = {
    "admission": "Admissions for B.Tech are based on JEE Main scores followed by MP DTE Counselling. M.Tech admissions require a valid GATE score. For the latest application dates (typically May–September), visit the official UIT-RGPV Admission portal.",
    "fees": "The total B.Tech fee is approximately ₹95,325 for the full 4-year duration (approx. ₹24,920 for the first year). M.E./M.Tech total fees are around ₹1.22 Lakhs.",
    "hostel": "On-campus facilities are available for both boys and girls. The hostel room rent is ₹2,400 per semester, with a one-time refundable caution money of ₹4,000. Mess charges are separate and based on actual usage.",
    "library": " The RGPV Central Library is open from 8 AM to 8 PM (Monday–Saturday). It features an e-library section with 180 computers, providing access to over 100,000 physical books and thousands of digital journals (IEEE, ASCE, ASME)",
    "placement": "The Training & Placement Cell maintains ties with companies like TCS, Infosys, Cognizant, and Wipro. Recent placements have seen a highest package of ₹54 LPA and an average of ₹4–6 LPA.",
    "contact": "You can reach the Director's office at +91-0755-2678812 or email uit_director@rgpv.ac.in. For technical support, contact support@uitrgpv.ac.in.",
    "timing": " The college typically operates from 9 AM to 5:30 PM, though library and laboratory hours may extend beyond this.",
    "exam": "Exams follow the official RGPV University schedule. Students should regularly check the online notice board for updates on timetables and results.",
    "attendance": "Minimum 75% attendance is required to appear in exams.",
    "courses": "The institute offers B.Tech (8 branches), M.Tech (9 specializations), MCA, and M.Sc. (Applied Mathematics/Nanotechnology)"
}

chat_history_file = "chat_history.json"

# Toggle this to True if running in an environment that does NOT support input()
USE_PREDEFINED_INPUTS = False
PREDEFINED_INPUTS = [
    "hi",
    "admission",
    "fees",
    "library",
    "exit"
]

# ---------------- FUNCTIONS ----------------
def save_history(user_msg, bot_msg):
    data = []
    if os.path.exists(chat_history_file):
        try:
            with open(chat_history_file, "r") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append({
        "time": str(datetime.datetime.now()),
        "user": user_msg,
        "bot": bot_msg
    })
    with open(chat_history_file, "w") as f:
        json.dump(data, f, indent=4)


def predefined_response(user_input):
    user_input = user_input.lower()
    for key in college_faq:
        if key in user_input:
            return college_faq[key]
    return None


def small_talk(user_input):
    text = user_input.lower()
    if text in ["hi", "hello", "hey"]:
        return "Hello! I am your college chatbot. Ask me about admission, fees, hostel, or placement."
    if "how are you" in text:
        return "I am doing great. How can I help you?"
    return None


# ---------------- MAIN CHAT LOOP ----------------
def chatbot():
    print("\n===== UIT RGPV OFFLINE COLLEGE CHATBOT =====")
    print("Ask about admission, fees, hostel, library, placement, etc.")
    print("Type 'exit' to stop the chatbot.\n")

    predefined_index = 0

    while True:
        try:
            if USE_PREDEFINED_INPUTS:
                if predefined_index >= len(PREDEFINED_INPUTS):
                    break
                user_input = PREDEFINED_INPUTS[predefined_index]
                predefined_index += 1
                print("You:", user_input)
            else:
                user_input = input("You: ")

            if user_input.lower() == "exit":
                print("Chat ended.")
                break

            talk = small_talk(user_input)
            if talk:
                print("Bot:", talk)
                save_history(user_input, talk)
                continue

            response = predefined_response(user_input)
            if response:
                print("Bot:", response)
                save_history(user_input, response)
            else:
                default_reply = "Sorry, I do not have information on that. Please contact the college office."
                print("Bot:", default_reply)
                save_history(user_input, default_reply)

        except OSError:
            print("Input error detected. This environment does not support input().")
            print("Set USE_PREDEFINED_INPUTS = True to run in sandboxed environments.")
            break


# ---------------- TESTS ----------------
def run_tests():
    # Basic functional tests
    assert predefined_response("fees") == college_faq["fees"]
    assert predefined_response("Tell me about hostel") == college_faq["hostel"]
    assert small_talk("hi") is not None
    assert small_talk("how are you") is not None
    assert predefined_response("unknown") is None
    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
    chatbot()
