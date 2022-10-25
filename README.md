# Bombardiers

### Summary

This project was created for the Fundamentals of Programming and Computer Science (15-112)
class at Carnegie Mellon during the Fall 2019 semester.

It is a turn-based game where players aim and launch missiles across a planetary gravity field in order to eliminate the other player's forcefield.

The trajectory of the missiles are affected by the gravity fields of the planets that it passes. This program uses kinematic equations taking into account the relative mass, velocity, and position of missiles and planets to calculate the path of the missile and any collisions.

The game is built on top of the cmu_112_graphics.py MVC framework which provides an interface for rendering and loading different game modes. All other aspects of the game are hand coded.

![Screen captures from Bombardiers game]()

There are three different game modes: Single Player, Multiplayer, and Multiplayer + Planets

### Single Player

In the single player mode, players can take on the challenge of battling an AI agent. Currently, the CPU is quite difficult to beat because it can compute optimal moves which deal damage to the other player and eliminate optimal moves of the opponent. In the future, I would like to introduce different levels of difficulty in order to make the experience more balanced. This can be acheived through limiting the damage done by the AI and including a randomness factor so that it may not always hit the other player's base.

### Multiplayer & Multiplayer + Planets

In multiplayer mode, two players take turns trying to defeat the other player. Multiplayer + Planets mode adds an interesting twist on top of this. For every missile that a player launches, they also have the opportunity to add an additional planet to the gravity field. This way, players can create more complex gravity fields with each turn to counter the opponents moves.

### Future Work

In the future, I think the most interesting aspect to work on would be improving the game AI for the single player mode. It would be nice to implement different levels of difficulty and reduce the computation time. I think these strategies can go hand in hand - instead of finding the most optimal moves, the AI would only need to find moves that are "good enough" according to the level of selected difficulty.

Thank you for reading!
