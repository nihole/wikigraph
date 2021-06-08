# WikiGraph

Wikigraph (or Wave Graph) is a presentation of information in a logical relationship. These logical relationships can be displayed as a graph, where each node is a statement or wiki article, and each edge represents one of three possible types of logical relationships: direct refutation, indirect refutation and complement (see description below in this document). 

This approach is called  [wave analysis](https://habr.com/ru/post/506670/) . With this approach, logical chains are created, consisting of arguments for and against the main statement. It looks like a wave. Therefore, we will call this logical chain **wave**.

The idea behind this project is to describe this structure in a YAML file and use a wiki repository for articles related to nodes. A graph is automatically generated from this YAML file.

Example:

##How to start

Create a folder YOUR_GIT_PATH and enter this folder (cd YOUR_GIT_PATH)

- git clone https://github.com/nihole/wikigraph.git
- git clone https://github.com/nihole/wg_examples.git
- install
  - PyYAML
  - graphviz

Why two repositories?

We have 2 types of repositories. 

- Repositories with data for wave analysis. Example of this repository is **wg_example repository**. There are no scripts here, information only. In this example, the root node (the statement under discussion) is "Alice was at home yesterday at 7 p.m.". Then all the analysis in this repository is a logical sequence of arguments for and against this statement. The main file here is a YAML file describing the logical relationships between nodes, and the svg file, which is the graph itself, created based on this YAML file. The wiki of this repository is used for articles correlated to nodes.

  Each statement you want to investigate can with wave analysis can require the creation of a new separate repository for that. For example, you can find another repository [wg_nav](https://github.com/nihole/wg_nav) that is used for analysis of the statement "The poisoning of Navalny was an operation of special services of Russia."

  It can be any difficult or controversial question. This can be used as a platform for controversy, a way to prepare for a discussion and just to understand yourself and other people.

- **Wikigraph repository** is used for scripts only. This is a common repository for all wikigraphs, and it is always a single repository. The main script is **wgraph.py**. It takes a YAML file (from repositories of first type) as input and generates a graph. Another important script is **mkgraph.py**, which is used to automatic  graph **resolving**  (see vocabulary below), but it is still under development.


Examples with explanations:

**EXAMPLE1. Root and direct contradiction**

Open YAML file in the directory YOUR_GIT_PATH/wg_examples/yaml/example1.yml (or https://github.com/nihole/wg_examples/blob/main/yaml/example1.yml in my github repository).

This YAML file represents a **direct contradiction example**. To create graph based on this structure run the python file:

 python3 YOUR_GIT_PATH/wikigraph/**wgraph.py** YOUR_GIT_PATH/wg_examples/yaml/**example1.yml** YOUR_GIT_PATH/wg_examples/**example4**

 The script wgraph.py executes some logical verification of your YAML file and creates 2 files: NetworkX file and svg file. 
 You can use NetworkX to cretate graphs with other tools, but in our case svg file is esufficient. You can open this file in any browser.

 In this particular case it will be 

 - **example1** (NetworkX, you can investigate it clicking the link in my github repository https://github.com/nihole/wg_examples/blob/main/example1)
 - **example1.svg** (svg, NetworkX, you can investigate it clicking the link in my gothub repository https://github.com/nihole/wg_examples/blob/main/example1.svg)

Open the svg file in any browser or just by clicking on it. You will find two nodes here. Navigate to each of them, click on the links and check out the wiki articles related to those two nodes (in the case of a github repository, you must select "raw" to get these links).

Also check out example2, example3 and examples4 with articles corresponding to the nodes for these graphs:

- **Example2. Direct and indirect contradictions**
- **Example3. Contradictions, complements and proofs**
- **Example4. Logical chain with all logical dependencies**

So if you want to start your own wikigraph you have to create yaml file with the same structure as you see in the examples and run wrgaph.py script.

Of course, you can use git for this, which provides unique opportunities for structured discussion and creation a collective wikigraph.


# Wave Analysis

This approach relies on the mathematics (wave analysis) described here. In fact, examples above are enough to understand the principles. 

Here is a brief presentation of wave analysis:

- **Root** Each graph has a root that represents the statement under discussion, and the entire graph is a set of pros and cons with respect to that root statement.

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
