## Design Guide

**Philosophy**

+ Design to protect the user. It should be hard (or impossible) to misuse this software.
+ Make the experience as fluid and seamless for the user as possible, at the expense of more complicated code.
+ Support for the greatest amount of scriptability.

**Printing**

Each notable action that is taken should be printed in a stylized manner, before it occurs. This serves both to update the user on progress and also to make debug messages readily accessible when things go wrong.

Status messages should be colored and bolded.
Paths should be colored and not be bolded.

**Colors**

+ RED: Errors and "dangerous" actions, like removal.
+ GREEN: Prompt questions.
+ YELLOW: Git-related.
+ BLUE: Not sure tbh. Log messages maybe?
