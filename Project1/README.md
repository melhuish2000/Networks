Strategy: 

I first wrote the command line parts, configuring for the port and the encrypted ports. This was my first time coding in python, so it was very challenging to learn the syntax. There could very well be an easy way to shorten some of this code, so if you are reviewing this code feel free to leave some tips on how I could have improved. With that being said, I will get into my strategy and some of the challenges I faced:

1. First I wanted to analyze the word list. I ran a few commands (seen in the link posted below), to determine the frequencies of letters. I found the most common 5 letters and proceeded to find a word in the list that contained them. I landed on "OREAS". This will be the first guess made by my code every single game. The result of the analysis is below:

21060 R
 8392 A
 7800 E
 6537 S
 5219 O
 5067 I
 4246 L
 4189 T
 4043 N
 3361 U
 2811 D
 2744 C
 2521 Y
 2494 M
 2299 P
 2284 H
 2089 B
 1971 G
 1743 K
 1238 F
 1171 W
  878 V
  474 Z
  376 J
  361 X
  139 Q

  https://devblogs.microsoft.com/scripting/letter-frequency-analysis-of-a-text-using-powershell/

2. At first I wanted to try and save the places of correct(2) letters and somewhat correct(1) letters. I thought I could have a list of characters of length 5. It all just got super complicated, and it was way too ambitious for me in the moment. I was scared about focusing too much on the extra credit at the moment and never getting it to work (I had only tested up to the game id at this point). That led me to a strategy I am still proud of however.

3. I came up with a strategy of two lists. One list was just the alphabet, and the other was blank. As the marks came in, letters of 1 and 2 would be added to the blank list and characters of 0 would get removed from the alphabet list. Now the next part is dumb luck that I realized it. I realized I can have two different ways to get a solution. If there are no repeats of a letter, then the blank list will fill up to length 5, and then I just have it search for words with only those letters. If there is a repeat, then the alphabet will eventually become small enough to guess correctly. I did run into an issue where a repeated letter would be 0, for example pekes with the letter 'e' would be 0,2,1,0,0. This would cause 'e' to be removed from the alphabet. I corrected it on line 61.

Tests:

Most of my tests were just the basic print() "tests". It was very effective because the json would print very nicely. I have no idea how to run any real tests in python.


