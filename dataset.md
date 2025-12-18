For every game of Nertz, we tracked the date and the scores of each participant. The highest possible score is 52,
which would coincide with playing every card from the starting piles into the center, then playing the last card from
the hand into the center: ```+1 * 52 in center, -1 * 0 in hand, 0 * 0 in piles = 52 points```. The lowest possible score
results from not playing any cards into the center, neither from the piles nor from the hand:
```+1 * 0 in center, -1 * 24 in hand, 0 * 28 in piles = -24 points```. The following actions improve a player's score:

- Play a card from the hand to the starting piles: ```+1 point``` by changing a negative point to a 0.
- Play a card from the starting piles to the center: ```+1 point``` by changing a 0 to a positive point.
- Play a card from the hand to the center: ```+2 points``` by changing a -1 to a +1.

In addition, for many games we tracked which player "Nertz-ed". The player who gets rid of all cards from their hand
first calls "Nertz" and stops the game. They may not necessarily have the most points, though it is usually beneficial
to be the first one done. It is a speed game, after all! We didn't think to track this stat for the first few months, so
it does not exist in every record. For analyses which use Nertz, we restrict the dataset to only games where it was
recorded.

Games are indexed in order. On the same date, a game with a higher index was played after a game with a lower index.