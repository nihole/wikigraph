WikiGraph

Wikigraph is a presentation of information in a logical relationship. The logical relationship is represented by a graph, with each node of the graph being a statement, which in general is a wiki article.
Each logical chain is built in accordance with wave analysis and is called a wave.

Here is a brief presentation of wave analysis:

- Each graph has a root that represents the statement under discussion, and the entire graph is a set of pros and cons with respect to that root statement.

Consider two statements: A and B. We will assume that of these statements can be either true or false. Then the following dependences of statement A on B are possible:

- **Independence** (A does not depend on B). The truth or falsity of statement A does not depend in any way on the truth or falsity of statement B.

- **Direct rebuttal**. If statement B is true, then statement A is false. We will denote such a relationship as **A --d-> B**. This arrow **--d->** actually can be replaced with expression "false because", that is, A --p-> B is a short expression of the expression "A false because B is (true) ". 
On the graph, we will denote this connection by a solid line with an arrow from A to B.

- **Indirect refutation**. If statement B is true, then the probability that statement A is false increases. We will call this an indirect refutation and denote it as **A --i-> B**. On the graph, we will denote it by a dotted line with an arrow from A to B.

- **Complement** (logical negation). If statement B is true, then statement A is false, and if statement B is false, then statement A is true. We will denote this as **A <-> B**. It is easy to show that if A <-> B, then B <-> A. On the graph, this connection will be denoted by a solid line with a double-headed arrow.

All other relationships are expressed via these 3 types. Actually, we have only 2 types of relationships: rebuttal and complement. Inderect, direct and independence types may be considered as a strength of this relationship. And this is very similar to boolean logic where everything may be expressed via pare of and/not or or/not.
