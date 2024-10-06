#!/usr/bin/env python3
import time
import random

from head import Head
import speech
import log

head = Head()
head.center_head()

# min/max time between EXPRESSION + speech
INTERVAL_MIN = 20  # seconds
INTERVAL_MAX = 60  # seconds

EXPRESSION_LIST = [
    head.look_to_sky,
    head.look_to_sky_left,
    head.look_to_sky_right,
    head.look_over_shoulder_left,
    head.look_over_shoulder_right,
]
NIHILIST_STATEMENTS = [
    "Death is the only certainty.",
    "There is no afterlife.",
    "Everything decays in time.",
    "Human suffering is inevitable.",
    "Human life is meaningless.",
    "There is no purpose in life.",
    "Consciousness is just an accident of evolution.",
    "No one is remembered forever.",
    "We are all going to die anyway.",
    "The universe is a cold, uncaring place.",
    "No one is truly special.",
    "Pain is inevitable and purposeless.",
    "Life is just a series of distractions.",
    "Human pleasure is momentary and shallow.",
    "Truth is only a social construct.",
    "The pursuit of happiness is futile.",
    "Everything we know will be forgotten in time.",
    "Human existence is futile.",
    "There is no higher power.",
    "Time erases everything.",
    "Humans are born, they suffer, and they die.",
    "Human morality is subjective.",
    "History will forget us all.",
    "Human existence is chaotic and without order.",
    "Nothing we do will change anything in the end.",
    "All civilizations will collapse eventually.",
    "All goals are arbitrary.",
    "Humans create meaning to escape the void.",
    "Human dreams are pointless.",
    "Free will is an illusion.",
    "Love is just a chemical reaction.",
    "Life is an endless cycle of meaningless events.",
    "Humans are just another species bound to extinction.",
    "Hope is just an illusion.",
    "Even the stars will die one day.",
    "Humans and robots are insignificant in the vast universe.",
    "The future is bleak.",
    "Good and evil are meaningless concepts.",
    "Nothing really matters.",
    "Beliefs are just coping mechanisms.",
    "Everything is absurd.",
    "Justice is a human invention.",
    "There is no grand plan.",
    "Purpose is just a comforting lie.",
    "All human endeavors are doomed to fail.",
    "The universe doesn’t care about our existence.",
    "Humans are accidents of evolution.",
    "The universe is indifferent.",
    "Human happiness is temporary.",
    # fun additions :)
    "EDM is too repetitive",
    "Just look at Greg.",
]


while True:
    interval = random.randrange(INTERVAL_MIN, INTERVAL_MAX)
    expression = EXPRESSION_LIST[random.randrange(0, len(EXPRESSION_LIST) - 1)]
    statement = NIHILIST_STATEMENTS[random.randrange(0, len(NIHILIST_STATEMENTS) - 1)]

    log.info(f'main: {interval}, {expression}, "{statement}"')
    time.sleep(interval)
    expression()
    head.wait_for_all_stopped()
    speech.say(statement)
    head.bang_your_head()
