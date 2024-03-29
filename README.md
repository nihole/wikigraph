# Wikigraph

## What is this?

Wikigraph (or Wave Graph) is a presentation of information in logical dependencies, displayed as a graph, where each node is a statement linked to wiki article, and each edge represents one of three types of logical relationships: **direct refutation**, **indirect refutation** and **complement** (see description below in this document). 

This method is called  [wave analysis](https://habr.com/ru/post/506670/) . With this approach, logical chains are created, consisting of alternately changing arguments (nodes) for and against the main statement (root node). It looks like a wave: yes, no, yes, no... Therefore, we will call this logical chain as a **wave**.

The idea behind this project is to describe this structure in a YAML file. In the current implementation, for node-related articles, I use the markdown files located in the folder 'wiki' in the data repositories (see explanation below), but this can be any kind of wiki or any article on the Internet. A graph with all necessary links is automatically generated from this YAML file.

Click the link below to see an example of a wikigraph, which will be discussed later in this document (example4).

[example4](https://github.com/nihole/wg_examples/blob/main/graphs/examples/example4.svg) (click 'Raw' to get access to links)

![example4](https://github.com/nihole/wg_examples/blob/main/tmp/Example4.png)

The statement under investigation (root node) in this example: "Alice was at home yesterday at 19:00." All other nodes are arguments for or against: blue nodes are supportive statements, and red nodes are rebuttals. Navigate to any node and click on the link ('Raw' should be chosen to get access to the links). You can now read the wiki articles related to these nodes. This is usually an article with proofs, citations, justification ... whatever to support this node's statement. But in this example, we are using this link to explain how to understand and create this graph.

Click the link below to see the YAML file used for the graph above creation.

[YAML for example4](https://github.com/nihole/wg_examples/blob/main/yaml/examples/example4.yml)

If you want a real-world example, refer to the repository [wg_navalny](https://github.com/nihole/wg_navalny), which is used to analyze the statement "Navalny's poisoning was an operation of the Russian special services." This only covers about 20% of all possible waves but you will already find hundreds of nodes there. 


## When to use?

  It can be used as a platform for discussion, a way to prepare for debates or even a tool for understanding yourself and other people. If you try to plot this graph, you will better understand why your opponents have such a “weird point of view”. In fact, it follows from the **basic axiom of wave analysis** (see below) that there are no 100% reliable arguments and facts, and your events interpretation is always based, among other things, on intuitive assumptions, that help you to cover huge holes in your picture of the world due to hidden or incorrect data. This method can help you to identify what irrational postulates (**reference points**) underlie your or your opponent's worldview and lead to a certain interpretation of events.
  
It should also be pretty clear that in the case of analyzing something essential, it must be a collective effort. Even a simple statement can lead to dozens of waves and hundreds of articles and relationships between them. Moreover, a single person cannot imagine all possible waves, arguments and contradictions.

## How to start

Create a folder YOUR_GIT_PATH and enter this folder (cd YOUR_GIT_PATH)

- git clone https://github.com/nihole/wikigraph.git
- git clone https://github.com/nihole/wg_examples.git

Then investigate examples.

**Example1. Root node and direct contradiction**

Open YAML file in the directory wg_examples/yaml/examples/example1.yml or [example1 YAML](https://github.com/nihole/wg_examples/blob/main/yaml/examples/example1.yml) in my github repository.

This YAML file represents a **direct contradiction example**. To create graph based on this structure run the python script **wgraph.py** (use python3 wgraph.py -h for help):

- python3 **wgraph.py** path_to_yaml_file.yml path_to_graph_to_be_created
 
 And in case of this example it will be:
 
- python3 wikigraph/**wgraph.py** wg_examples/yaml/examples/**example1.yml** wg_examples/graphs/examples/**example1**

 The script wgraph.py executes some logical verification of your YAML file and creates **svg** file:

 - **example1.svg**. You can investigate it by clicking the link in my github repository 
 
<img src="https://github.com/nihole/wg_examples/blob/main/graphs/examples/example1.svg" alt="Example1" width="200" height="200">

Open the svg file in any browser or just by clicking on it. You will find two nodes here. Navigate to each of them, click on the links and check out the wiki articles related to those two nodes (in the case of a github repository, you must select "raw" to get these links).

Also check out example2, example3 and examples4 with articles corresponding to the nodes for these graphs:

**Example2. Direct and indirect contradictions**

<img src="https://github.com/nihole/wg_examples/blob/main/graphs/examples/example2.svg" alt="Example2" width="300" height="300">

**Example3. Contradictions, complements and proofs**

<img src="https://github.com/nihole/wg_examples/blob/main/graphs/examples/example3.svg" alt="Example3" width="400" height="400">

**Example4. Wikigraph with all logical dependencies**

<img src="https://github.com/nihole/wg_examples/blob/main/graphs/examples/example4.svg" alt="Example4" width="500" height="500">

Therefore, if you want to start your own wikigraph you need to create a yaml file with the same structure as in the examples and run the wrgaph.py script.

## Data and Script Repositories

The idea is to have a single repository with scripts (wikigraph.git) and multiple data repositories (wg_examples in this case) used for investigation of root statement. Each time you initiate a discussion or investigation, you can create a separate data repository for this. And sctipts used for analysis and graphs creation are always located in the common single script repository.

So, we have 2 types of repositories:

- **Repositories with data** for wave analysis. Example of this repository is **wg_example.git** repository. There are no scripts here. It is used for articles (correlated to nodes), dependencies (edges) and graphs only. The main files here are YAML file describing the logical relationships between nodes, and the svg file, which is the graph itself, created based on this YAML file. The wiki of this repository is used for articles correlated to nodes.

- **Script repository**. This is **wikigraph.git** repository. Only scripts are located here (no data) which are used for structure analyzis and graphs generation for each data repository. That is why we have only a single repository of this type. The main script is **wgraph.py**. It takes a YAML file (from repositories of first type) as input and generates a graph. Another important script is **mkgraph.py**, which is used to automatic  graph **resolving**  (see vocabulary below), but it is still under development. You will also find some useful scripts in the folder **tools**. For example, the wgmerge.py script is used to merge / extract some parts of the graph. This way you can extract all waves with node_x as root into a separate yaml file, work with that subtree, and then merge it back into the original parent graph (yaml file). It is useful because real graphs can be quite large and it can be quite tricky to manage one huge yaml file.

# Wave Analysis

The best way to undesratand what is [wave analysis](https://habr.com/ru/post/506670/) is to refer to the examples. 

Here is a brief vocabular and main concepts of wave analysis.

- **Root**. Each graph has a root that represents the statement under discussion, and the entire graph is a set of pros and cons with respect to that root statement.

Consider two statements: A and B. We will assume that each of these statements can be either true or false. Then the following dependences of statement A on B are possible in wave analysis:

- **Independence**. (A does not depend on B). The truth or falsity of statement A does not depend in any way on the truth or falsity of statement B.

- **Direct rebuttal**. If statement B is true, then statement A is false. We will denote such a relationship as **A --d-> B**. This arrow **--d->** actually can be replaced with expression "false because", that is, A --p-> B is a short expression of the statement "A is false because B (is true) ". 
  On the graph, we will represent this dependency by a solid line with an arrow directed from A to B.

- **Indirect rebuttal**. If statement B is true, then the probability that statement A is false increases. We will call this an indirect rebuttal and denote it as **A --i-> B**. On the graph, we will represent it by a dotted line with an arrow directed from A to B.

- **Complement** (logical negation). If statement B is true, then statement A is false, and if statement B is false, then statement A is true. We will denote this as **A <-> B**. It is easy to show that if A <-> B, then B <-> A. On the graph, this connection will be represented by a solid line with a double-headed arrow.

All other relationships are expressed via these 3 types. Actually, we have only 2 types of relationships: rebuttal and complement. Inderect, direct and independence types may be considered as a strength of this relationship. And this is very similar to boolean logic where everything may be expressed via pare of and/not or or/not.

### Wikigraph Analysis

- **Graph convergence**. We will call a graph decidable (or convergent) if the analysis of this graph unambiguously leads to the conclusion about whether the root statement is true or false.  You can find more information about this [here](https://habr.com/ru/post/506670/).

- **Dead-end (edge) nodes**. We will call a node N a dead-end if not a single arrow leaves it, including a bidirectional one. This means that this is not refuted by any statements and can be considered true. Then if the connection is strong enough (direct refutation), this statement can refute the upstream  in the logical wave, which, in turn, can create other dead-end nodes and so on to the very top, thus leading to the resolution of the graph.

- **Reference Points**. This definition is not precise and rather intuitive. We are talking about a set of dead-end nodes, with rather general statements (for example, philosophical views, or emotional preferences) that lead to the resolution of the graph. The main idea here is that they are irational postulates that underlie the perception of the situation.

- **Basic axiom of wave analysis**: there is always hidden information that does not allow unambiguous resolution of a full wave graph
(See definition of full wave graph [here](https://habr.com/ru/post/506670/))

- **Consequence** of the basic axiom: If the resolution of the wave graph occurs, then this indicates the presence of an irrational element, a logic error, or the incompleteness of the wave graph.
