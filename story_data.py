'''
Define story events, choices, outcomes, and transitions.
Each event has one story and three options.
Some event's option will continue to some small game and some will just go to next event or ending.
'''

boss_event = {
    "title": "A Message from Your Boss",
    "background": "boss",
    "story": [
        "You have taken the day off for the concert.",
        "Just as you are leaving, your boss sends a message:",
        '"Something came up at work. Can you come back to help?"'
    ],
    "options": [
        {
            "text": "Sure, I will come back.",
            "result": [
                "The work takes longer than you expected.",
                "You think your concert plans are ruined.",
                "Then your boss surprises you with a VIP box ticket",
                "and arranges a car to get you there on time!",
                "Good Ending: Overtime to VIP!"
            ],
            "next": "boss_ending"
        },
        {
            "text": "I am on leave. What do you need help with?",
            "result": [
                "Your boss cannot find a file.",
                "You send its location and leave for the concert."
            ],
            "next": "transport"
        },
        {
            "text": "Ignore the message and leave.",
            "result": [
                "A little later, your boss sends another message:",
                '"Found it. Enjoy your day off!"',
                "You continue your journey."
            ],
            "next": "transport"
        }
    ]
}

transport_event = {
    "title": "Train Trouble",
    "background": "transport",
    "story": [
        "Your train breaks down. The restart time is unknown.",
        "High-speed rail will get you there on time.",
        "But the extra fare will use up your merch budget.",
        "News: An accident is blocking the inner highway lane."
    ],
    "options": [
        {
            "text": "Take high-speed rail. Give up buying merch.",
            "result": [
                "You spend your merch budget on the extra fare.",
                "But the platform is packed with other fans!",
                "You must squeeze aboard before the doors close."
            ],
            "next": "train",
            "spend_merch_budget": True
        },
        {
            "text": "Wait for the train. It should restart soon.",
            "result": [
                "You wait... and wait... and wait.",
                "The train finally restarts late that night.",
                "Unfortunately, the concert is already over.",
                "You missed the concert!"
            ],
            "next": "failed"
        },
        {
            "text": "Share a taxi with other fans. Try your luck!",
            "result": [
                "You find other fans to share a taxi.",
                "The shared fare is cheaper than high-speed rail.",
                "You can keep your merch budget!",
                "But will the accident clear in time?",
                "A Lucky Wheel will decide your fate!"
            ],
            "next": "lucky_wheel"
        }
    ]
}

help_event = {
    "title": "Someone Needs Help",
    "background": "help",
    "story": [
        "Near the venue, you notice a woman sitting by the road.",
        "She looks unwell, and nobody is helping her.",
        "The concert will begin soon.",
        "What will you do?"
    ],
    "options": [
        {
            "text": "Stay with her and help until everything is settled.",
            "result": [
                "You call an ambulance and accompany her to hospital.",
                "At her request, you help contact her family.",
                "By the time they arrive, the concert is over.",
                "Days later, you discover she is your idol's mother!",
                "She sends you a VIP invitation to the next concert.",
                "Good Ending: An Unexpected VIP Invitation!"
            ],
            "next": "help_ending"
        },
        {
            "text": "Call an ambulance. Leave after help takes over.",
            "result": [
                "You call an ambulance and stay until help arrives.",
                "Once the paramedics take over, you head to the venue.",
                "You still have time to get inside!"
            ],
            "next": "ticket_swap"
        },
        {
            "text": "Keep walking. You do not want to miss the concert.",
            "result": [
                "You continue towards the venue.",
                "You never find out who the woman is."
            ],
            "next": "ticket_swap"
        }
    ]
}

ticket_swap_event = {
    "title": "A Free Seat Upgrade?",
    "background": "ticket_swap",
    "story": [
        "Outside the venue, a stranger approaches you.",
        '"My friend is sitting in your section."',
        '"My seat is closer to the stage. Want to swap for free?"',
        "The offer sounds tempting..."
    ],
    "options": [
        {
            "text": "A better seat for free? Let's swap!",
            "result": [
                "You exchange tickets and hurry to the entrance.",
                "The scanner flashes red. Your new ticket is fake!",
                "You turn around, but the stranger has disappeared.",
                "Your front-row dream ends outside the venue."
            ],
            "next": "failed"
        },
        {
            "text": "Check their ticket screenshot, then swap.",
            "result": [
                "The screenshot shows a seat number and barcode.",
                "Everything looks convincing, so you agree to swap.",
                "But the ticket is rejected at the entrance.",
                "A convincing screenshot does not mean a valid ticket!",
                "You cannot enter the concert."
            ],
            "next": "failed"
        },
        {
            "text": "No thanks. I'll keep my own ticket.",
            "result": [
                "You politely decline and keep your original ticket.",
                "You are almost there!"
            ],
            "next": "merch"
        }
    ]
}

merch_event = {
    "title": "The Merch Stand",
	"background": "merch",
    "story": [
        "You reach the official merch stand near the entrance.",
        "There is one limited-edition item left!",
        "Luckily, you still have your merch budget."
    ],
    "options": [
        {
            "text": "Buy it, then head inside!",
            "result": [
                "You buy the last limited-edition item!",
                "Your original ticket scans successfully.",
                "You take your seat, holding your new merch.",
                "The lights dim. The opening song begins.",
                "Good Ending: Finally, Here You Are!"
            ],
            "next": "concert_ending",
            "buy_merch": True
        },
        {
            "text": "Save the money and head inside.",
            "result": [
                "You decide to keep your money.",
                "Your original ticket scans successfully.",
                "You find your seat and look towards the stage.",
                "The lights dim. The opening song begins.",
                "Good Ending: Finally, Here You Are!"
            ],
            "next": "concert_ending"
        }
    ]
}


no_merch_event = {
    "title": "The Merch Stand",
    "background": "merch",
    "story": [
        "You reach the official merch stand near the entrance.",
        "There is one limited-edition item left!",
        "But your merch budget went towards high-speed rail.",
        "You take one last look before walking away."
    ],
    "options": [
        {
            "text": "At least I made it. Head inside!",
            "result": [
                "You leave the merch stand empty-handed.",
                "Your original ticket scans successfully.",
                "You made it here, and that still matters.",
                "The lights dim. The opening song begins.",
                "Good Ending: Finally, Here You Are!"
            ],
            "next": "concert_ending"
        }
    ]
}