# WikiGraph

## What is it?

Wikigraph (or Wave Graph) is a presentation of information in logical dependencies, displayed as a graph, where each node is a statement linked to wiki article, and each edge represents one of three types of logical relationships: **direct refutation**, **indirect refutation** and **complement** (see description below in this document). 

This method is called  [wave analysis](https://habr.com/ru/post/506670/) . With this approach, logical chains are created, consisting of alternately changing arguments (nodes) for and against the main statement (root node). It looks like a wave: yes, no, yes, no... Therefore, we will call this logical chain as a **wave**.

The idea behind this project is to describe this structure in a YAML file and use a github repository wiki for articles related to nodes. A graph is automatically generated from this YAML file.

Click the link below to see an example of a wikigraph, which will be discussed later in this document (example4).

[example4](https://raw.githubusercontent.com/nihole/wg_examples/main/example4.svg?token=ACHUZVRISMV3N5EMGYNTMCDAZEIPS)

The statement under investigation (root node) in this example: "Alice was at home yesterday at 19:00." All other nodes are arguments for or against: blue nodes are supportive claims, and red nodes are rebuttals. Navigate to any node and click on the link. You can now read the wiki article related to this node. This is usually an article with proofs, citations, justification ... whatever to support this node's claim. But in this example, we are using this link to explain how to understand and create this graph.

Click the link below to see the YAML file used for the graph above creation.

[YAML for example4](https://github.com/nihole/wg_examples/blob/main/yaml/example4.yml)

If you want a real-world example, refer to the repository [wg_nav](https://github.com/nihole/wg_nav), which is used to analyze the statement "Navalny's poisoning was an operation of the Russian special services." This only covers about 20% of all possible waves but you will already find hundreds of nodes there. 


## When to use?

  It can be used as a platform for discussion, a way to prepare for debates or even a tool for understanding yourself and other people. If you try to plot this graph, you will better understand why your opponents have such a “weird point of view”. In fact, it follows from the **basic axiom of wave analysis** (see below) that there are no 100% reliable arguments and facts, and your events interpretation is always based, among other things, on intuitive assumptions, that help you to cover huge holes in your picture of the world due to hidden or incorrect data. This method can help you to identify what irrational postulates (**reference points**) underlie your or your opponent's worldview and lead to a certain interpretation of events.
  
It should also be pretty clear that in the case of analyzing something essential, it must be a collective effort. Even a simple statements can lead to hundreds of articles and relationships between them. Moreover, a single person cannot imagine all possible waves, arguments and contradictions.

## How to start

Create a folder YOUR_GIT_PATH and enter this folder (cd YOUR_GIT_PATH)

- git clone https://github.com/nihole/wikigraph.git
- git clone https://github.com/nihole/wg_examples.git
- install
  - PyYAML
  - graphviz

Then investigate examples.

**Example1. Root node and direct contradiction**

Open YAML file in the directory YOUR_GIT_PATH/wg_examples/yaml/example1.yml ([example1 YAML](https://github.com/nihole/wg_examples/blob/main/yaml/example1.yml) in my github repository.

This YAML file represents a **direct contradiction example**. To create graph based on this structure run the python file:

 python3 YOUR_GIT_PATH/wikigraph/**wgraph.py** YOUR_GIT_PATH/wg_examples/yaml/**example1.yml** YOUR_GIT_PATH/wg_examples/**example4**

 The script wgraph.py executes some logical verification of your YAML file and creates 2 files with NetworkX and svg types. 
 You can use NetworkX to cretate graphs with other tools, but in our case svg file is sufficient. You can open this file in any browser.

 In this particular case it will be 

 - **example1** (NetworkX, you can investigate it clicking the link in my github repository [example1 NetworkX file ](https://github.com/nihole/wg_examples/blob/main/example1)
 - **example1.svg** (svg, you can investigate it clicking the link in my github repository [example1 svg file](https://github.com/nihole/wg_examples/blob/main/example1.svg)

Open the svg file in any browser or just by clicking on it. You will find two nodes here. Navigate to each of them, click on the links and check out the wiki articles related to those two nodes (in the case of a github repository, you must select "raw" to get these links).

Also check out example2, example3 and examples4 with articles corresponding to the nodes for these graphs:

- **Example2. Direct and indirect contradictions**
- **Example3. Contradictions, complements and proofs**
- **Example4. Logical chain with all logical dependencies**

So if you want to start your own wikigraph you have to create yaml file with the same structure as you see in the examples and run wrgaph.py script.

Of course, you can use git for this, which provides unique opportunities for structured discussion and creation a collective wikigraph.

## Repositories

The idea is to have a single repository with scripts (wikigraph.git) and multiple data repositories (wg_examples in this case) used for investigation of root statement. Each time you initiate a discussion or investigation, you can create a separate data repository for this. And sctipts used for analysis and graph creation are always located in the common single script repository.

So we have 2 types of repositories:

- **Repositories with data** for wave analysis. Example of this repository is **wg_example.git repository**. There are no scripts here. It is used for articles (correlated to nodes), dependencies (edges) and graphs only. In this example, the root node (the statement under discussion) is "Alice was at home yesterday at 7 p.m.". Then all the wave analysis is a logical sequence of arguments for and against this statement. The main files here are YAML file describing the logical relationships between nodes, and the svg file, which is the graph itself, created based on this YAML file. The wiki of this repository is used for articles correlated to nodes.

- **Script repository**. This is **wikigraph.git repository**. It is used only for scripts and is used  to analyze the structure and generate graphs for each data repository. That is why we have only a single repository of this type. The main script is **wgraph.py**. It takes a YAML file (from repositories of first type) as input and generates a graph. Another important script is **mkgraph.py**, which is used to automatic  graph **resolving**  (see vocabulary below), but it is still under development.

# Wave Analysis

Here is a brief presentation of [wave analysis](https://habr.com/ru/post/506670/):

- **Root**. Each graph has a root that represents the statement under discussion, and the entire graph is a set of pros and cons with respect to that root statement.

Consider two statements: A and B. We will assume that each of these statements can be either true or false. Then the following dependences of statement A on B are possible:

- **Independence**. (A does not depend on B). The truth or falsity of statement A does not depend in any way on the truth or falsity of statement B.

- **Direct rebuttal**. If statement B is true, then statement A is false. We will denote such a relationship as **A --d-> B**. This arrow **--d->** actually can be replaced with expression "false because", that is, A --p-> B is a short expression of the statement "A is false because B is (true) ". 
  On the graph, we will represent this dependency by a solid line with an arrow from A to B.

- **Indirect rebuttal**. If statement B is true, then the probability that statement A is false increases. We will call this an indirect rebuttal and denote it as **A --i-> B**. On the graph, we will represent it by a dotted line with an arrow from A to B.

- **Complement** (logical negation). If statement B is true, then statement A is false, and if statement B is false, then statement A is true. We will denote this as **A <-> B**. It is easy to show that if A <-> B, then B <-> A. On the graph, this connection will be represented by a solid line with a double-headed arrow.

All other relationships are expressed via these 3 types. Actually, we have only 2 types of relationships: rebuttal and complement. Inderect, direct and independence types may be considered as a strength of this relationship. And this is very similar to boolean logic where everything may be expressed via pare of and/not or or/not.

### Wikigraph Analysis

- **Graph convergence**. We will call a graph decidable (or convergent) if the analysis of this graph unambiguously leads to the conclusion about whether the root statement is true or false.  You can find more information about this [here](https://habr.com/ru/post/506670/).

- **Dead-end (edge) nodes**. We will call a node N a dead-end if not a single arrow leaves it, including a bidirectional one. This means that this is not refuted by any statements and can be considered true. This means that if the connection is strong enough (direct refutation), this statement can refute the statement of the upstream node in the logical wave, which, in turn, can create other dead-end nodes and so on to the very top, thus leading to the resolution of the graph.

- **Reference Points**. This definition is not precise and rather intuitive. We are talking about a small set of dead-end nodes, with rather general statements (for example, philosophical views, or emotional preferences) that lead to the resolution of the graph.

The bottom line is that these are the statements on which "the picture of the world" rests or at least the attitude to the root statement.

- **Basic axiom of wave analysis**. There is always hidden information that does not allow unambiguous resolution of a full wave graph
(See definition of full wave graph here)

- **Consequence** of the basic axiom. If the resolution of the wave graph occurs, then this indicates the presence of an irrational element, a logic error, or the incompleteness of the wave graph.
