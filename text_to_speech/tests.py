from django.test import TestCase

# Create your tests here.


{
    "pipeline": [],
    "policies": [],
    "domain": "",
    "intents": "- greet/n -goodbye/n",
    "entities": [],
    "slots": {},
    "config": "language: vn",
    "actions": [],
    "forms": {},
    "e2e_actions": [],
    "responses": "",
    "session_config": {
        "session_expiration_time": 60,
        "carry_over_slots_to_new_session": true
    },
    "nlu":
        "##intent : - greet \n examples: - hey\n- hello\n ## intent:deny\\n- no\\n- never\\n ## intent: - chao examples: -ok \n -conde\n"
    ,
    "rules": [
        {
            "rule": "Say goodbye anytime the user says goodbye",
            "steps": [
                {
                    "intent": "goodbye"
                },
                {
                    "action": "utter_goodbye"
                }
            ]
        }
    ],
    "stories": "None"
}
