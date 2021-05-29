# WikiGraph

Wikigraph (or Wave Graph) is a presentation of information in a logical relationship. The logical relationship is represented by a graph, where each node in the graph is a statement, which in general is a wiki article. Each logical chain is built in accordance with wave analysis and is called a wave. The structure of these logical chains (waves) is discribed in YAML file. Based on this YAML file graph is created. Each node of this graph is linked to a wiki article.

To start to use it:

Create a folder YOUR_GIT_FOLDER and enter this folder (cd YOUR_GIT_FOLDER_PATH)

- git clone https://github.com/nihole/wikigraph.git
- git clone https://github.com/nihole/wg_examples.git
- install
  - PyYAML
  - graphviz
  - wgraph

You have 4 examples in wg_examples. So you have 4 graphs and 4 YAML files discribing the structure of these graphs.

Refer to examples with explanations:

**EXAMPLE1. Root and direct contradiction**

Open YAML file in the directory YOUR_GIT_FOLDER_PAT/wg_examples/example1.yml (or https://github.com/nihole/wg_examples/blob/main/yaml/example1.yml in my github repository).

This YAML file represents a **direct contradiction example**. To create graph based on this structure run the python file:

 python3 YOUR_GIT_FOLDER_PAT/wikigraph/**wgraph.py** YOUR_GIT_FOLDER_PATH/wg_examples/yaml/**example1.yml** YOUR_GIT_FOLDER_PATH/wg_examples/**example4**
 
 The script wgraph.py executes some logical verification of your YAML file and creates 2 files: NetworkX file and svg file. In this particular case it will be 
 - example1 (NetworkX, you can investigate it clicking the link in my github repository https://github.com/nihole/wg_examples/blob/main/example1)
 - example1.svg (svg, NetworkX, you can investigate it clicking the link in my gothub repository https://github.com/nihole/wg_examples/blob/main/example1)

You will find two nodes here. Navigate to each of them, click on the links and investigate the articles relted to those 2 nodes (in the case of a github repository, you have to select 'raw' to get these links).

Also check out example2, example3 and examples4 with articles corresponding to the nodes for these graphs:

- **Example2. Direct and indirect contradictions**
- **Example3. Contradictions and proofs**
- **Example4. Logical chain with all logical dependencies**



## Wave Analysis

Here is a brief presentation of wave analysis:

- **Root.** Each graph has a root that represents the statement under discussion, and the entire graph is a set of pros and cons with respect to that root statement.

Consider two statements: A and B. We will assume that of these statements can be either true or false. Then the following dependences of statement A on B are possible:

- **Independence** (A does not depend on B). The truth or falsity of statement A does not depend in any way on the truth or falsity of statement B.

- **Direct rebuttal**. If statement B is true, then statement A is false. We will denote such a relationship as **A --d-> B**. This arrow **--d->** actually can be replaced with expression "false because", that is, A --p-> B is a short expression of the expression "A false because B is (true) ". 
On the graph, we will denote this connection by a solid line with an arrow from A to B.

- **Indirect refutation**. If statement B is true, then the probability that statement A is false increases. We will call this an indirect refutation and denote it as **A --i-> B**. On the graph, we will denote it by a dotted line with an arrow from A to B.

- **Complement** (logical negation). If statement B is true, then statement A is false, and if statement B is false, then statement A is true. We will denote this as **A <-> B**. It is easy to show that if A <-> B, then B <-> A. On the graph, this connection will be denoted by a solid line with a double-headed arrow.

All other relationships are expressed via these 3 types. Actually, we have only 2 types of relationships: rebuttal and complement. Inderect, direct and independence types may be considered as a strength of this relationship. And this is very similar to boolean logic where everything may be expressed via pare of and/not or or/not.

## Wave graph analysis

### Graph convergence

We will call a graph decidable (or convergent) if the analysis of this graph unambiguously leads to the conclusion about whether the root statement is true or false. 

You can find the the description of algorithm for resolving the wave graph here.
The most key concept here are dead-end nodes and reference points.

**Dead-end (edge) nodes:**

We will call a node N dead-end if not a single arrow leaves it, including a bidirectional one (), that is, it is not refuted by any statement.

If there are no refutation, then we consider this statement as true. This means that with a sufficiently strong connection (direct refutation), this statement can refute the statement of the "previous wave", which in turn can create other dead-end nodes and so on to the very top. Thus, leading to the resolution of the graph.

**Reference Points:**

This definition is not precise and rather intuitive. We are talking about a small set of dead-end (edge) nodes, with rather general statements (for example, philosophical views, or emotional preferences) that lead to the resolution of the graph.

The bottom line is that these are the statements on which "the picture of the world" rests or at least the attitude to the root statement.

**Basic axiom of wave analysis**

There is always hidden information that does not allow unambiguous resolution of a full wave graph
(See definition of full wave graph here)

**Consequence**

If the resolution of the wave graph occurs, then this indicates the presence of an irrational element, a logic error, or the incompleteness of the wave graph.
