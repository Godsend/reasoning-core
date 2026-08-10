Title:

Content selection saved. Describe the issue below:

Description:

![](https://arxiv.org/static/base/1.0.1/images/icons/smileybones-small.svg)arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2601.03220v2 \[cs.LG\] 16 Mar 2026

# From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence

Marc Finzi∗1  Shikai Qiu∗2  Yiding Jiang∗1  Pavel Izmailov2  J. Zico Kolter1

Andrew Gordon Wilson2

1Carnegie Mellon University    2New York University

###### Abstract

Can we learn more from data than existed in the generating process itself? Can new and useful information be constructed from merely applying deterministic transformations to existing data? Can the learnable content in data be evaluated without considering a downstream task? On these questions, Shannon information and Kolmogorov complexity come up nearly empty-handed, in part because they assume observers with unlimited computational capacity and do not target the useful information content.
In this work, we identify and exemplify three seeming paradoxes in information theory: (1) information cannot be increased by deterministic transformations; (2) information is independent of the order of data; (3) likelihood modeling is merely distribution matching. To shed light on the tension between these results and modern practice, and to quantify the value of data, we introduce _epiplexity_†, a formalization of information capturing what computationally bounded observers can learn from data. Epiplexity captures the structural content in data while excluding time-bounded entropy, the random unpredictable content exemplified by pseudorandom number generators and chaotic dynamical systems.
With these concepts, we demonstrate how information can be created with computation, how it depends on the ordering of the data, and how likelihood modeling can produce more complex programs than present in the data generating process itself.
We also present practical procedures to estimate epiplexity which we show capture differences across data sources, track with downstream performance, and highlight dataset interventions that improve out-of-distribution generalization. In contrast to principles of model selection, epiplexity provides a theoretical foundation for _data selection_, guiding how to select, generate, or transform data for learning systems.

## 1 Introduction

00footnotetext: Equal contribution.00footnotetext: Code available at [https://github.com/shikaiqiu/epiplexity](https://github.com/shikaiqiu/epiplexity "").

As AI research progresses towards more general-purpose intelligent systems, cracks are beginning to show in mechanisms for grounding mathematical intuitions.
Much of learning theory is built around controlling generalization error with respect to a given distribution, treating the training distribution as fixed and focusing optimization effort on the choice of model. Yet modern systems are expected to transfer across tasks, domains, and objectives that were not specified at training time, often after large-scale pretraining on diverse and heterogeneous data. In this regime, success or failure frequently hinges less on architectural choices than on what data the model was exposed to in the first place.
Pursuing broad generalization to diverse out-of-distribution tasks forces a shift in perspective: instead of treating data as given and optimizing for in-distribution performance, we need to choose and curate data to facilitate generalization to unseen tasks. This shift makes the value of data itself a central question—how much usable, transferable information can a model acquire from training? In other words, instead of model selection, how do we perform _data selection_? On this question, existing theory offers little guidance and often naively contradicts empirical observations.

Consider synthetic data, crucial for further developing model capabilities (Abdin et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib2 ""); Maini et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib63 "")) when existing natural data are exhausted. Existing concepts in
information theory like the data processing inequality appear
to suggest that synthetic data adds no additional value.
Questions about what information is transferred to a given model seem naturally within the purview of information theory, yet, quantifying this information with existing tools proves to be elusive.
Even basic questions, such as the source of the information in the weights of an AlphaZero game-playing model (Silver et al., [2018](https://arxiv.org/html/2601.03220v2#bib.bib90 "")), are surprisingly tricky to answer. AlphaZero takes in zero human data, learning merely from the deterministic rules of the game and the AlphaZero RL algorithm, both of which are simple to describe. Yet the resulting models achieve superhuman performance and are large in size.
To assert that AlphaZero has learned little to no information in this process is clearly missing the mark, and yet both Shannon and algorithmic information theory appear to say so.

![Refer to caption](https://arxiv.org/html/2601.03220v2/x1.png)

Figure 1: Random vs structural information for computationally bounded observers. (Left) Illustration of random vs structural information of different data for computationally bounded observers, which we formalize with time-bounded entropy and epiplexity ( [Section˜3](https://arxiv.org/html/2601.03220v2#S3 "3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) and can be estimated from loss curves of neural networks trained on that data ( [Section˜4](https://arxiv.org/html/2601.03220v2#S4 "4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")).
(Top Right) Unlike other forms of information, time-bounded entropy and epiplexity can be increased through computational processes, such as simulating dynamical systems (cellular automation, Lorenz equations) and interventions like changing the data ordering, which can produce apparent randomness but also learnable, emergent structures like gliders and the Lorenz attractor invariant measure ( [Section˜5](https://arxiv.org/html/2601.03220v2#S5 "5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")).
(Bottom Right) Whereas time-bounded entropy captures the in-distribution randomness and unpredictability, epiplexity measures the amount of structural information the model extracts from the data to its weights, which can be useful for OOD tasks such as by reusing learned circuits shared between the in-distribution and OOD tasks.

In this paper, we argue that the amount of structural information a _computationally bounded_ observer can extract from a dataset is a fundamental concept that underlies many observed empirical phenomena.
As we will show, existing notions from Shannon and algorithmic information theory are inadequate when forced to quantify this type of information.
These frameworks often lend intuitive or mathematical support to beliefs that, in fact, obscure important aspects of empirical phenomena. To highlight the limitations of classical frameworks and motivate the role of computational constraints in quantifying information, we identify and demonstrate three _apparent paradoxes_: statements which can be justified mathematically by Shannon and algorithmic information theory, and yet are in tension with intuitions and empirical phenomena.

1. Paradox 1:


Information cannot be increased by deterministic processes.
For both Shannon entropy and Kolmogorov complexity, deterministic transformations cannot meaningfully increase the information content of an object. And yet, we use pseudorandom number generators to produce randomness, synthetic data improves model capabilities, mathematicians can derive new knowledge by reasoning from axioms without external information, dynamical systems produce emergent phenomena, and self-play loops like AlphaZero learn sophisticated strategies from games (Silver et al., [2018](https://arxiv.org/html/2601.03220v2#bib.bib90 "")).

2. Paradox 2:


Information is independent of factorization order. A property of both Shannon entropy and Kolmogorov complexity is that total information content is invariant to factorization: the information from observing first XX and then YY is the same as observing YY followed by XX. On the other hand, LLMs learn better on English text ordered left-to-right than reverse ordered text, picking out an “ _arrow of time_” (Papadopoulos et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib74 ""); Bengio et al., [2019](https://arxiv.org/html/2601.03220v2#bib.bib12 "")), and we have cryptography built on the existence of functions that are computationally hard to predict in one direction and easy in another.

3. Paradox 3:


Likelihood modeling is merely distribution matching.
Maximizing the likelihood is often equated with matching the training data generating process: the true data-generating process is a perfect model of itself, and no model can achieve a higher expected likelihood.
As a consequence, it is often assumed that a model trained on a dataset cannot extract more structure or learn useful features that were not used in generating the data.
However, we show that a computationally-limited observer can in fact uncover much more structure than is in the data generating process.
For example, in Conway’s game of life the data are generated via simple programmatic rules that operate on two-dimensional arrays of bits.
Applying these simple rules sequentially, we see emergent structures, such as different species of objects that move and interact in a predictable way.
While an unbounded observer can simply simulate the evolution of the environment exactly, a computationally bounded observer would make use of the emergent structures and learn the different types of objects and their behaviors.


The tension between these theoretical statements and empirical phenomena can be resolved by imposing computational constraints on the observer and separating the random content from the structural content. Drawing on ideas from cryptography, algorithmic information theory, and these unexplained empirical phenomena, we define a new information measure, epiplexity (epistemic complexity), which formally defines the amount of structural information that a computationally bounded observer can extract from the data ( [Section 3](https://arxiv.org/html/2601.03220v2#S3 "3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), Definition [8](https://arxiv.org/html/2601.03220v2#Thmtheorem8 "Definition 8 (Epiplexity and Time-Bounded Entropy) ‣ 3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")).
Briefly, epiplexity is the information in the model that minimizes the description length of data under computational constraints. A simple heuristic measurement is the area under the loss curve above the final loss, while a more rigorous approach uses the cumulative KL divergence between a teacher and student model ( [Section 4](https://arxiv.org/html/2601.03220v2#S4 "4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), [Figure 2](https://arxiv.org/html/2601.03220v2#S4.F2 "Figure 2 ‣ 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")).

Our definitions capture the intuition that an object contains both random, inherently unpredictable information (entropy), and predictable structured information that enables observers to generalize by identifying patterns (epiplexity). In [Figure 1](https://arxiv.org/html/2601.03220v2#S1.F1 "Figure 1 ‣ 1 Introduction ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") (left) we illustrate this divide. In the top row, we have highly redundant and repetitive code and simple color gradients, which have little information content, be it structural or random. In the middle row, we have the inner workings of an algorithm and pictures of animals, showing complex, long-range interdependencies between the elements from which a model can learn complex features and subcircuits that are helpful even for different tasks. In contrast, on the bottom, we have random data with little structure: configuration files with randomly generated API keys, file paths, hashes, arbitrary boolean flags have negligible learnable content and no long-range dependencies or complex circuits that result from learning on this task. Similarly, uniformly shuffled pixels from the animal pictures have high entropy but are fundamentally unpredictable, and no complex features or circuits arise from training on these data.

An essential property of our formulation is that information is _observer dependent_: the same object may appear random or structured depending on the computational resources of the observer. For instance, the output of a strong pseudorandom generator appears indistinguishable from true randomness to any polynomial-time observer lacking the secret key (seed), regardless of the algorithm or function class. In other situations, such as chaotic dynamical systems, both apparently random behavior is produced along with structure: the state of the system cannot be predicted precisely over long time-scales, but such observers may still learn meaningful predictive distributions, as shown by the invariant measure in [Figure˜1](https://arxiv.org/html/2601.03220v2#S1.F1 "In 1 Introduction ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") (top right).

Models trained to represent these distributions are computer programs, and substructures within these programs, like circuits for performing specific tasks, or induction heads (Olsson et al., [2022](https://arxiv.org/html/2601.03220v2#bib.bib72 "")), can be reused even for seemingly unrelated data. This view motivates selecting high epiplexity data that induces more structural information in the model, since these structures can then be reused for unseen out-of-distribution (OOD) tasks, as illustrated in [Figure˜1](https://arxiv.org/html/2601.03220v2#S1.F1 "In 1 Introduction ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") (bottom right). We emphasize, however, that epiplexity is a measure of information, _not_ a guarantee of OOD generalization to specific tasks. Epiplexity quantifies the amount of structural information a model extracts, while being agnostic to whether these structures are relevant to a _specific_ downstream task.

To build intuition, we explore a range of phenomena and provide experimental evidence for behaviours that are poorly accounted for by existing information-theoretic tools, yet naturally accommodated by epiplexity. We show that information _can_ be created purely through computation, giving insights into synthetic data ( [subsection 5.1](https://arxiv.org/html/2601.03220v2#S5.SS1 "5.1 Paradox 1: Information Cannot be Created by Deterministic Transformations ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). We examine how certain factorizations of the same data can increase structural information and downstream OOD performance—even as they result in worse training loss ( [subsection 5.2](https://arxiv.org/html/2601.03220v2#S5.SS2 "5.2 Paradox 2: Information Content is Independent of Factorization ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). We show why likelihood modeling is more than distribution matching, identifying induction and emergence as two settings where the observer can learn more information than was present in the data generating process ( [subsection 5.3](https://arxiv.org/html/2601.03220v2#S5.SS3 "5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). By measuring epiplexity, we can better understand why pre-training on text data transfers more broadly than image data, and why certain data selection strategies for LLMs are empirically successful ( [Section 6](https://arxiv.org/html/2601.03220v2#S6 "6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). Together, our results provide clarity on the motivating questions: the information content of data can be compared independently of a specific task, new information can be created by computation, and models can learn more information than their generating processes contain.

In short, we identify a disparity between existing concepts in information theory and modern practice, embodied by three apparent paradoxes, and introduce epiplexity as a measurement of structural information acquired by a computationally bounded observer to help resolve them. We formally define epiplexity in [Section 3](https://arxiv.org/html/2601.03220v2#S3 "3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") (Definition [8](https://arxiv.org/html/2601.03220v2#Thmtheorem8 "Definition 8 (Epiplexity and Time-Bounded Entropy) ‣ 3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) and present measurement procedures in [Section 4](https://arxiv.org/html/2601.03220v2#S4 "4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). In [Section 5](https://arxiv.org/html/2601.03220v2#S5 "5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), we show how epiplexity and time-bounded entropy shed light on these paradoxes, including induction and emergent phenomena. Finally, in [Section 6](https://arxiv.org/html/2601.03220v2#S6 "6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), we demonstrate that epiplexity correlates with OOD generalization, helping explain why certain data enable broader generalization than others.

## 2 Background

In order to define the interesting, structural, and predictive component of information, we must separate it out from random information—that which is fundamentally unpredictable given the computational constraints of the observer. Along the way, we will review algorithmic randomness as developed in algorithmic information theory as well as notions of pseudo-randomness used in cryptography, and how these concepts crucially depend on the observer.

### 2.1 What Does it Mean for An Object to Be Random?

Random Variables and Shannon Information.
Many common intuitions about randomness start from random variables and Shannon information. A random variable defines a map from a given measurable probability space to different outcomes, with probabilities corresponding to the measure of the space that lead to a certain outcome. Shannon information assigns to each outcome xx a self-information (or surprisal) log⁡1/P​(x)\\log 1/P(x) based on the probability PP, and an entropy for the random variable H​(X)=𝔼​\[log⁡1/P​(X)\]\\mathrm{H}(X)=\\mathbb{E}\[\\log 1/P(X)\], which provides a lower bound on the average code length needed to _communicate_ samples to another party (Shannon, [1948](https://arxiv.org/html/2601.03220v2#bib.bib87 "")). In Shannon’s theory, information comes only from distributions and random variables—objects that are not random must contain no information. As a result, non-random information is seemingly contradictory, and thus we must draw from a broader mathematical perspective to describe such concepts.

In the mid 1900s, mathematicians were interested in formalizing precisely what it means for a given sample to be a random draw from a given distribution, to ground the theory of probability and random variables (Shafer and Vovk, [2006](https://arxiv.org/html/2601.03220v2#bib.bib85 "")). A central consideration involves a uniformly sampled binary sequence u1:∞u\_{1:\\infty} from which other distributions of interest can be constructed. This sequence can also be interpreted as the binary expression of a number \[0,1)\[0,1). Intuitively, one might think that all sequences should be regarded as equally random, as they are all equally likely according to the probability distribution: 1111111​…1111111\\dots has the same probability mass as 10011101​…10011101\\dots and also the same self-information. However, looking at statistics on these sequences reveals something missing from this perspective; from the law of large numbers, for example, it must be that limN→∞1N​∑i=1Nui=0.5\\lim\_{N\\to\\infty}\\frac{1}{N}\\sum\_{i=1}^{N}u\_{i}=0.5, which is clearly not satisfied by the first sequence of 11s.\
\
Martin-Löf Randomness: No algorithm exists to predict the sequence.\
Initial attempts were made to formalize randomness as sequences which pass all statistical tests for randomness, such as the law of large numbers for selected substrings. However, under such definitions all sequences fail to be random since tests like u1:∞≠y1:∞u\_{1:\\infty}\\neq y\_{1:\\infty} for any particular sequence yy must also be included (Downey and Hirschfeldt, [2019](https://arxiv.org/html/2601.03220v2#bib.bib27 "")). The solution to these issues was found by defining random sequences not as those that pass all tests of randomness, but those that pass all _computable_ tests of randomness, in a formalization known as Martin-Löf randomness (Martin-Löf, [1966](https://arxiv.org/html/2601.03220v2#bib.bib64 "")). As it turned out, this definition is equivalent to a number of seemingly distinct definitions, such as the inability for any gambler to exploit properties of the sequence to make a profit, or that all prefixes of the random sequence should be nearly incompressible (Terwijn, [2016](https://arxiv.org/html/2601.03220v2#bib.bib95 "")).\
For this last definition, we must invoke Kolmogorov complexity, a notion of compressibility and a key concept in this paper.\
\
###### Definition 1 (Prefix Kolmogorov complexity (Kolmogorov, [1968](https://arxiv.org/html/2601.03220v2\#bib.bib55 ""); Chaitin, [1975](https://arxiv.org/html/2601.03220v2\#bib.bib20 "")))\
\
Fix a\
\
universal prefix-free Turing machine 𝒰\\mathcal{U}. The (prefix) Kolmogorov complexity of a finite binary string xx is K​(x)=min⁡{\|p\|:𝒰​(p)=x}K(x)\\;=\\;\\min\\{\\,\|p\|:\\;\\mathcal{U}(p)=x\\,\\}.\
That is, K​(x)K(x) is the length of the shortest self-delimiting program (a program which also encodes its length) that outputs xx and halts. The conditional complexity K​(x\|y)K(x\|y) is the length of the shortest program that outputs xx and halts when provided yy as input.\
\
Due to the universality of Turing machines, the Kolmogorov complexity for two Turing machines (or programming languages) 𝒰1\\mathcal{U}\_{1} and 𝒰2\\mathcal{U}\_{2} differ by at most a constant, \|K𝒰1​(x)−K𝒰2​(x)\|≤C\|K\_{\\mathcal{U}\_{1}}(x)-K\_{\\mathcal{U}\_{2}}(x)\|\\leq C, where the constant CC depends only on 𝒰1,𝒰2\\mathcal{U}\_{1},\\mathcal{U}\_{2}, but not on xx(Li et al., [2008](https://arxiv.org/html/2601.03220v2#bib.bib59 "")).\
\
###### Definition 2 (Martin–Löf random sequence (Martin-Löf, [1966](https://arxiv.org/html/2601.03220v2\#bib.bib64 "")))\
\
An infinite sequence\
\
x1:∞∈{0,1}ℕx\_{1:\\infty}\\in\\{0,1\\}^{\\mathbb{N}} is Martin–Löf random iff there exists a constant cc such that for all nn, K​(x1:n)≥n−cK(x\_{1:n})\\;\\geq\\;n-c. Using this criterion, all computable randomness tests are condensed into a single incomputable randomness test concerning Kolmogorov complexity.\
\
One can extend Martin-Löf randomness to finite sequences. We say that a sequence x∈{0,1}nx\\in\\{0,1\\}^{n} is cc-random if K​(x)>n−cK(x)>n-c. Equivalently, _randomness discrepancy_ is defined as δ​(x)=n−K​(x)\\delta(x)=n-K(x), which measures how far away xx is from having maximum Kolmogorov complexity. A sequence xx is cc-random if δ​(x)<c\\delta(x)<c. High Kolmogorov complexity, low randomness discrepancy, sequences are overwhelmingly likely when sampled from uniform randomly sampled random variables. From Kraft’s inequality (Kraft, [1949](https://arxiv.org/html/2601.03220v2#bib.bib57 ""); McMillan, [1956](https://arxiv.org/html/2601.03220v2#bib.bib67 "")), there are at most 2n−c2^{n-c} (prefix-free) programs of length L≤n−cL\\leq n-c, therefore in the 2n2^{n} possibilities in uniformly sampling X∼UnX\\sim U\_{n}, the probability that K​(X)K(X) is size LL or smaller is P​(K​(X)≤n−c)=P​(δ​(X)≥c)<2−cP(K(X)\\leq n-c)=P(\\delta(X)\\geq c)<2^{-c}. The randomness discrepancy of a sequence can thus be viewed as a test statistic for rejecting the null hypothesis that the object XX was indeed sampled uniformly at random (Grünwald et al., [2008](https://arxiv.org/html/2601.03220v2#bib.bib44 "")). For a sequence to have low randomness discrepancy, it must exhibit no discernible pattern, and thus there is an objective sense in which 10010111001001011100 is more random than 01010101010101010101.\
\
Given the Martin-Löf definition of infinite random sequences, every random sequence is incomputable; in other words, there is no program that can implement the function ℕ→{0,1}\\mathbb{N}\\to\\{0,1\\} which produces the bits of the sequence. One should contrast such random numbers from those like π/4\\pi/4 or e/3e/3, which though transcendental, are computable, as there exist programs that can compute the bits of their binary expressions. While the computable numbers in \[0,1)\[0,1) form a countable set, algorithmically random numbers in \[0,1)\[0,1) are uncountably large in number. With the incomputability of random sequences in mind we can appreciate the Von Neumann quote\
\
> _“Anyone who considers arithmetical methods of producing random digits is, of course, in a state of sin.”_(Von Neumann, [1951](https://arxiv.org/html/2601.03220v2#bib.bib100 ""))\
\
which anticipates the Martin–Löf formalization that came later. But this viewpoint also misses something essential, as evidenced by the success of pseudorandom number generation, derandomization, and cryptography.\
\
Cryptographic Randomness: No polynomial time algorithm exists to predict the sequence.\
An important practical and theoretical development of random numbers has come from the cryptography community, by once again limiting the computational model of the observer.\
\
Rather than passing all computable tests as with Martin-Löf randomness, cryptographically secure pseudorandom number generators (CSPRNG or PRG) are defined as functions which produce sequences that pass all _polynomial time_ tests of randomness.\
Such functions are conjectured to be constructible by computer programs and are central to cryptographic research.\
\
###### Definition 3 (Non-uniform PRG (Blum and Micali, [1982](https://arxiv.org/html/2601.03220v2\#bib.bib15 ""); Goldreich, [2006](https://arxiv.org/html/2601.03220v2\#bib.bib40 "")))\
\
A function GG stretching kk input bits into nn output bits is a pseudorandom generator (PRG) if its outputs cannot be distinguished from a random sequence by any polynomial time algorithm more than a negligible fraction of the time. More precisely, GG is a (non-uniform) PRG iff for every non-uniform probabilistic polynomial time algorithm Dk:{0,1}n→{0,1}D\_{k}:\\{0,1\\}^{n}\\to\\{0,1\\} (making use of advice strings {ak}k∈ℕ\\{a\_{k}\\}\_{k\\in\\mathbb{N}} of length poly​(k)\\mathrm{poly}(k))\
has at most negligible advantage ϵ​(k)\\epsilon(k) distinguishing outputs of GG from uniformly random sequences u∼Unu\\sim U\_{n}:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|Prs∼Uk⁡\[Dn​(G​(s))=1\]−Pru∼Un⁡\[Dn​(u)=1\]\|=ϵ​(k)<negl​(k).\\left\|\\Pr\_{s\\sim U\_{k}}\[D\_{n}(G(s))=1\]-\\Pr\_{u\\sim U\_{n}}\[D\_{n}(u)=1\]\\right\|\ =\\epsilon(k)<\ \\mathrm{negl}(k)\\,. |  | (1) |\
\
The definition of indistinguishability via polynomial time tests is equivalent to a definition on the failure to predict the next element of a sequence given the previous elements: no polynomial time predictor can predict the next bit of the sequence with probability negligibly better than random guessing (Yao, [1982](https://arxiv.org/html/2601.03220v2#bib.bib108 "")).\
\
Following from the indistinguishability definition, randomness of this kind can be substituted for Martin-Löf randomness in the vast majority of practical circumstances.222Specifically, when the difference between outcomes can be measured in polynomial time. For a concrete example, if a use-case of randomness that runs in polynomial time like quicksort, and takes more iterations to run with PRG sequences than with truly random sequences, and this difference could be determined within polynomial time such as by measuring the quicksort runtime, then this construction could be used as a polynomial time distinguisher,\
which by the definition of PRG does not exist. If PRGs exist, then quicksort must run nearly as fast using pseudorandom number generation as it does with truly random sequences.\
\
The existence of PRGs hinges on the existence of _one way functions_ (OWF), from which PRGs and other cryptographic primitives are constructed, forming the basis of modern cryptography (Goldreich and Levin, [1989](https://arxiv.org/html/2601.03220v2#bib.bib41 "")). For example, the backbone algorithm for parallel random number generation in Jax (Bradbury et al., [2018](https://arxiv.org/html/2601.03220v2#bib.bib16 "")), works to create random numbers u1,u2,…​uNu\_{1},u\_{2},\\dots u\_{N} by simply encrypting the numbers 1,2,…,N1,2,\\dots,N: uk=E​(k,s)u\_{k}=E(k,s) where the encryption key ss is the random seed and EE is the threefish block cypher (Salmon et al., [2011](https://arxiv.org/html/2601.03220v2#bib.bib82 "")). Block ciphers, like other primitives, are constructed using one way functions.\
\
###### Definition 4 (Non-uniform one-way function, OWF (Yao, [1982](https://arxiv.org/html/2601.03220v2\#bib.bib108 ""); Goldreich, [2006](https://arxiv.org/html/2601.03220v2\#bib.bib40 "")))\
\
Let f:{0,1}n→{0,1}mf:\\{0,1\\}^{n}\\to\\{0,1\\}^{m} (with m>nm>n) be computable in time poly​(n)\\mathrm{poly}(n) where n=\|x\|n=\|x\|.\
We say ff is _one-way against non-uniform PPT adversaries_ if for every non-uniform probabilistic polynomial time\
algorithm AnA\_{n} (i.e., a polynomial-time algorithm AA with advice strings {an}n∈ℕ\\{a\_{n}\\}\_{n\\in\\mathbb{N}} of length poly​(n)\\mathrm{poly}(n)),\
\
|     |     |     |\
| --- | --- | --- |\
|  | Prx∼Un⁡\[An​(f​(x))∈f−1​(f​(x))\]<negl​(n),\\Pr\_{x\\sim U\_{n}}\\!\\left\[\\,A\_{n}(f(x))\\in f^{-1}(f(x))\\,\\right\]\\;<\\;\\mathrm{negl}(n), |  |\
\
where the probability is over the uniform choice of xx (and any internal randomness in AA).\
\
While cryptographers are most interested in the polynomial versus nonpolynomial compute separations for security, cryptographic primitives with respect to less extreme compute separations have been constructed and are believed to exist, for example for quadratic time (Merkle, [1978](https://arxiv.org/html/2601.03220v2#bib.bib68 "")), quasipolynomial time (Liu and Pass, [2024](https://arxiv.org/html/2601.03220v2#bib.bib61 "")), and even constraints on circuit depth (Applebaum, [2016](https://arxiv.org/html/2601.03220v2#bib.bib8 "")). While the results we prove in this paper are based on the polynomial vs nonpolynomial separation in cryptographic primitives, it seems likely that a much wider array of compute separations are relevant for information in the machine learning context even if not as important for cryptography. For example, the separations between quadratic or cubic time and higher order polynomials may be relevant to transformer self attention, or gaps between fixed circuit depth and variable depth as made possible with chain of thought or other mechanisms.\
\
### 2.2 Random vs Structural Information\
\
With these notions of randomness in hand, we can use what is random to define what is not random. In algorithmic information theory, there is a lesser known concept that captures exactly this idea, known as _sophistication_(Koppel, [1988](https://arxiv.org/html/2601.03220v2#bib.bib56 "")), which has no direct analog in Shannon information theory. While several variants of the definition exist, the most straightforward is perhaps the following:\
\
###### Definition 5 (Naive Sophistication (Mota et al., [2013](https://arxiv.org/html/2601.03220v2\#bib.bib70 "")))\
\
Sophistication, like Kolmogorov complexity, is defined on individual bitstrings, and it uses the compressibility criterion from Martin-Löf randomness to carve out the random content of the bitstring. Sophistication is defined as the smallest Kolmogorov complexity of a set SS such that xx is a random element from that set (at randomness discrepancy of cc).\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | nsophc​(x)=minS:{K​(S):K​(x∣S)>log⁡\|S\|−c}\\mathrm{nsoph}\_{c}(x)=\\min\_{S}:\\{K(S):K(x\\mid S)>\\log\|S\|-c\\} |  | (2) |\
\
Informally, sophistication describes the structural component of an object; however, it is surprisingly difficult to give concrete examples of high sophistication objects. The difficulty of finding high sophistication objects\
is a consequence of Chaitin’s incompleteness theorem (Chaitin, [1974](https://arxiv.org/html/2601.03220v2#bib.bib19 "")). This theorem states that in a given formal system there is a constant LL for which there are no proofs that any specific string xx has K​(x)>LK(x)>L, even though nearly all strings have nearly maximal complexity. Since nsophc​(x)>L\\mathrm{nsoph}\_{c}(x)>L implies K​(x)>L−O​(1)K(x)>L-O(1), there can be no proofs that the sophistication of a particular string exceeds a certain constant either. It is known that high sophistication strings exist by a diagonalization argument (Antunes et al., [2005](https://arxiv.org/html/2601.03220v2#bib.bib7 "")), but we cannot pinpoint any specific strings which have high sophistication.\
On typical Turing machines, LL is often not more than a few thousand (Chaitin, [1998](https://arxiv.org/html/2601.03220v2#bib.bib21 "")), far from the terabytes of information that frontier AI models have encoded.\
\
We look towards complex systems and behaviors as likely examples of high sophistication objects; however in many of these cases the objects could conceivably be produced by simpler descriptions given tremendous amounts of computation. The mixing of two fluids for example can produce extremely complex transient behavior due to the complexities of fluid dynamics; however, with access to unlimited computation and some appropriately chosen random initial data one should be able to reproduce the exact dynamics (Aaronson et al., [2014](https://arxiv.org/html/2601.03220v2#bib.bib1 "")).\
Owing to the unbounded compute available for the programs in sophistication, many complex objects lose their complexity. Additionally, for strings that _do_ have high sophistication, the steps of computation required for the optimal program grow faster than any computable function with the sophistication content (Ay et al., [2010](https://arxiv.org/html/2601.03220v2#bib.bib9 "")).\
For a computationally bounded observer, an encrypted message or a _cryptographically secure pseudo-random number generator_ (CSPRNG) output _is_ random, and measurements that do not recognize this randomness do not reflect the circumstances of this observer.\
These limitations of sophistication leads to a disconnect with real systems with observers that have limited computation, and it is our contention that this disconnect is an essential one, central to phenomena such as emergence, induction, chaos, and cryptography.\
\
### 2.3 The Minimum Description Length Principle\
\
Finally, we review the minimum description length principle (MDL), used as a theoretical criterion for model selection, which we will use in defining epiplexity. The principle states that among models for the data, the best explanation minimizes the total description length of the data, including both the description of the data using the model and the description of the model itself (Rissanen, [2004](https://arxiv.org/html/2601.03220v2#bib.bib81 "")). The most common instantiation of this idea is via the statistical two-part code MDL.\
\
###### Definition 6 (Two-part MDL (Rissanen, [2004](https://arxiv.org/html/2601.03220v2\#bib.bib81 ""); Grünwald, [2007](https://arxiv.org/html/2601.03220v2\#bib.bib43 "")))\
\
Let x∈{0,1}n×dx\\in\\{0,1\\}^{n\\times d} be the data and ℋ\\mathcal{H} be a set of candidate models. The two-part MDL is:\
\
|     |     |     |\
| --- | --- | --- |\
|  | L​(x)=minH∈ℋ⁡L​(H)−log⁡P​(x∣H),L(x)=\\min\_{H\\in\\mathcal{H}}L(H)-\\log P(x\\mid H), |  |\
\
where L​(H)L(H) specifies the number of bits required to encode the model HH, and −log⁡P​(x∣H)-\\log P(x\\mid H)\
is the number of bits required to encode the data given the model.\
\
This formulation provides an intuitive implementation of Occam’s Razor: complex models (large L​(H)L(H)) are penalized unless they provide a reduction in the data’s description length (large P​(x∣H)P(x\\mid H)).\
If there are repeating patterns in the data, they can be stored in the model HH rather than being duplicated in the code for the data.\
We review the modern developments of MDL in Appendix [H](https://arxiv.org/html/2601.03220v2#A8 "Appendix H Minimum Description Legnth ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
While MDL is a criterion for model selection given a fixed dataset, epiplexity, which we introduce next, can be viewed as its dual: a criterion for data selection given a fixed computation budget.\
\
## 3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer\
\
Keeping in mind the distinction between structural and random information in the unbounded compute setting, and the computational nature of pseudorandomness in cryptography, we now introduce epiplexity. _Epiplexity_ captures the structural information present to a computationally bounded observer. As the computational constraints of this observer change, so too does the division between random and structured content. After introducing epiplexity here, we present ways of measuring epiplexity in [Section 4](https://arxiv.org/html/2601.03220v2#S4 "4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). In Sections [5](https://arxiv.org/html/2601.03220v2#S5 "5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") and [6](https://arxiv.org/html/2601.03220v2#S6 "6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") we show how epiplexity can shed light on seeming paradoxes in information theory around the value of data, and OOD generalization.\
\
First we will define what it means for a probability distribution to have an efficient implementation, requiring that it be implemented on a prefix-free universal Turing machine (UTM) and halt in a fixed number of steps.\
\
###### Definition 7 (Time-bounded probabilistic model)\
\
Let T:ℕ→ℕT:\\mathbb{N}\\to\\mathbb{N} be a non-decreasing time-constructible function and let 𝒰\\mathcal{U} be a fixed prefix-free universal Turing machine.\
A (prefix-free) program P\\mathrm{P} is a _TT-time probabilistic model_ over {0,1}n\\{0,1\\}^{n} if it supports both sampling and probability evaluation in time T​(n)T(n):\
\
Evaluation. On input (0,x)(0,x) with x∈{0,1}nx\\in\\{0,1\\}^{n}, 𝒰​(P,(0,x))\\mathcal{U}(\\mathrm{P},(0,x)) halts within T​(n)T(n) steps\
and outputs an element in \[0,1\]\[0,1\] (with a finite binary expansion), denoted\
\
|     |     |     |\
| --- | --- | --- |\
|  | ProbP​(x):=𝒰​(P,(0,x)).\\mathrm{Prob}\_{\\mathrm{P}}(x)\\;:=\\;\\mathcal{U}(\\mathrm{P},(0,x)). |  |\
\
Sampling. On input (1,u)(1,u) where u∈{0,1}∞u\\in\\{0,1\\}^{\\infty} is an infinite random tape,\
𝒰​(P,(1,u))\\mathcal{U}(\\mathrm{P},(1,u)) halts within T​(n)T(n) steps and outputs an element of {0,1}n\\{0,1\\}^{n}, denoted\
\
|     |     |     |\
| --- | --- | --- |\
|  | SampleP​(u):=𝒰​(P,(1,u)).\\mathrm{Sample}\_{\\mathrm{P}}(u)\\;:=\\;\\mathcal{U}(\\mathrm{P},(1,u)). |  |\
\
These outputs must define a normalized distribution matching the sampler:\
\
|     |     |     |\
| --- | --- | --- |\
|  | ∑x∈{0,1}nProbP​(x)=1andPru∼U∞⁡\[SampleP​(u)=x\]=ProbP​(x)∀x∈{0,1}n.\\sum\_{x\\in\\{0,1\\}^{n}}\\mathrm{Prob}\_{\\mathrm{P}}(x)=1\\quad\\text{and}\\quad\\Pr\_{u\\sim U\_{\\infty}}\[\\mathrm{Sample}\_{\\mathrm{P}}(u)=x\]=\\mathrm{Prob}\_{\\mathrm{P}}(x)\ \ \\forall x\\in\\{0,1\\}^{n}. |  |\
\
Let 𝒫T\\mathcal{P}\_{T} be the set of all such programs. To simplify the notation, we will use italicized PP to denote the probability mass function ProbP\\mathrm{Prob}\_{\\mathrm{P}} in contrast with the non-italicized P\\mathrm{P}, which denotes the program.\
\
Here, nn denotes the dimension of the underlying sample space (e.g., the length of the binary string.) This definition allows us to constrain the amount of computation the function class can use. Such a model class enforces that the functions of interest are both efficiently sampleable and evaluable, which include most sequence models.\
While in this work we focus primarily on computational constraints which we consider most fundamental, other constraints such as memory or within a given function class ℱ\\mathcal{F} can be accommodated by replacing 𝒫T\\mathcal{P}\_{T} with 𝒫ℱ\\mathcal{P}\_{\\mathcal{F}}, and may be important for understanding particular phenomena.333One such possibility is to constrain the function class to all models reachable by a given optimization procedure with a given neural network architecture. With these preliminaries in place, we can now separate the random and structural components of information.\
\
We define epiplexity and time-bounded entropy in terms of the program which achieves the best expected compression of the random variable XX, minimizing the two-part code length (model and data given model bits) under the given runtime constraint.\
\
###### Definition 8 (Epiplexity and Time-Bounded Entropy)\
\
Consider a random variable XX on {0,1}n\\{0,1\\}^{n}. LetP⋆=arg​minP∈𝒫T⁡{\|P\|+𝔼​\[log⁡1/P​(X)\]}\\mathrm{P^{\\star}}=\\operatorname\*{arg\\,min}\_{\\mathrm{P}\\in\\mathcal{P}\_{T}}\\quantity{\|\\mathrm{P}\|+\\mathbb{E}\[\\log 1/P(X)\]}(3)be the program that minimizes the time bounded MDL with ties broken by the smallest program, and expectations taken over XX. \|P\|\|\\mathrm{P}\| denotes the length of the program P\\mathrm{P} in bits, and logarithms are in base 22. We define the TT-bounded _epiplexity_ ST\\mathrm{S}\_{T} and _entropy_ HT\\mathrm{H}\_{T} of the random variable XX asST​(X):=\|P⋆\|,andHT​(X):=𝔼​\[log⁡1/P⋆​(X)\].\\mathrm{S}\_{T}(X):=\|\\mathrm{P}^{\\star}\|,\\quad\\text{and}\\quad\\mathrm{H}\_{T}(X):=\\mathbb{E}\[\\log 1/P^{\\star}(X)\].(4)\
\
The time-bounded entropy HT\\mathrm{H}\_{T} captures the amount of information in the random variable that is random and unpredictable, whereas the epiplexity ST\\mathrm{S}\_{T} captures the amount of structure and regularity visible within the object at the given level of compute TT. Uniform random variables have trivial epiplexity because a model (or equivalently a program) as simple as the uniform distribution achieves a small two-part code length, despite having large time-bounded entropy. Explicitly, for a uniform random variable UnU\_{n} on {0,1}n\\{0,1\\}^{n}, and even a constant time bound T​(n)≥c1T(n)\\geq c\_{1}, ST​(Un)+HT​(Un)≤n+c2\\mathrm{S}\_{T}(U\_{n})+\\mathrm{H}\_{T}(U\_{n})\\leq n+c\_{2} where c2c\_{2} is the length of a program for the uniform distribution running in time c1c\_{1}, and since HT​(Un)≥H​(Un)=n\\mathrm{H}\_{T}(U\_{n})\\geq\\mathrm{H}(U\_{n})=n, it must be that ST​(Un)≤c2\\mathrm{S}\_{T}(U\_{n})\\leq c\_{2}.\
Random variables with simple patterns, like 0101010101​…0101010101... with probability 1/21/2 and 1010101010​…1010101010... with probability 1/21/2, also have low epiplexity because the time bounded MDL minimal model is simple. In this case with linear time T​(n)=Θ​(n)T(n)=\\Theta(n), both ST​(X)=O​(1)\\mathrm{S}\_{T}(X)=O(1) and HT​(X)=O​(1)\\mathrm{H}\_{T}(X)=O(1). Henceforth, we will abbreviate MDLT​(X):=ST​(X)+HT​(X)\\mathrm{MDL}\_{T}(X):=\\mathrm{S}\_{T}(X)+\\mathrm{H}\_{T}(X), which is the total time-bounded information content. We will now enumerate a few basic consequences of these definitions.\
\
Basic Properties(1)ST​(X)≥0,HT​(X)≥0,\\displaystyle\\mathrm{S}\_{T}(X)\\geq 0,\\quad\\mathrm{H}\_{T}(X)\\geq 0,(2)H​(X)≤ST​(X)+HT​(X)≤n+c1,\\displaystyle\\mathrm{H}(X)\\leq\\mathrm{S}\_{T}(X)+\\mathrm{H}\_{T}(X)\\leq n+c\_{1},(3)MDLT′​(X)≤MDLT​(X)whenever ​T′​(n)≥T​(n),\\displaystyle\\mathrm{MDL}\_{T^{\\prime}}(X)\\leq\\mathrm{MDL}\_{T}(X)\\quad\\text{whenever }\ T^{\\prime}(n)\\geq T(n),(4)MDLT′​(f−1​(X))≤MDLT​(X)+\|f\|+c2,with ​T′​(n)=T​(n)+𝖳𝗂𝗆𝖾​(f).\\displaystyle\\mathrm{MDL}\_{T^{\\prime}}(f^{-1}(X))\\leq\\mathrm{MDL}\_{T}(X)+\|\\mathrm{f}\|+c\_{2},\\text{with }T^{\\prime}(n)=T(n)+\\mathsf{Time}(\\mathrm{f}).\
\
Statement 4 (defined for programs f\\mathrm{f} that run in a fixed time implementing a bijection) is an analog of the information non-increase property K​(f​(x))≤K​(x)+K​(f)+cK(f(x))\\leq K(x)+K(f)+c. However, note that while the Kolmogorov complexity for K​(f)K(f) and K​(f−1)K(f^{-1}) are the same to within an additive constant, in our setting of a fixed computational budget having a short program for f−1f^{-1} does not imply one for ff, and vice versa. This gap between a function and its inverse has important consequences for the three paradoxes as we will see in [Section 5](https://arxiv.org/html/2601.03220v2#S5 "5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
##### Pseudorandom number sequences have high random content and little structure.\
\
Unlike Shannon entropy, Kolmogorov complexity, or even resource bounded forms of Kolmogorov complexity (Allender et al., [2011](https://arxiv.org/html/2601.03220v2#bib.bib5 "")), we show that CSPRNGs have nearly maximal time-bounded entropy for polynomial time observers. Additionally, while CSPRNGs produce random content, they do not produce structured content as the epiplexity is negligibly larger than constant.\
Formally, let UkU\_{k} be the uniform distribution on kk bits.\
\
###### Theorem 9\
\
For any G∈PRGG\\in\\mathrm{PRG} that stretches the input to n=poly​(k)n=\\mathrm{poly}(k) bits and allowing for an advantage of at most ε​(k)\\varepsilon(k), the polynomial time bounded entropy is nearly maximal:\
\
|     |     |     |\
| --- | --- | --- |\
|  | n−2−n​ε​(k)<HPoly​(G​(Uk))≤n+cn-2-\\,n\\varepsilon(k)<\\mathrm{H}\_{\\mathrm{Poly}}(G(U\_{k}))\\leq n+c |  |\
\
for a fixed constant cc, and epiplexity is nearly constant\
\
|     |     |     |\
| --- | --- | --- |\
|  | SPoly​(G​(Uk))≤c+n​ε​(k).\\mathrm{S}\_{\\mathrm{Poly}}(G(U\_{k}))\\leq c+n\\varepsilon(k). |  |\
\
Proof: see Appendix [A.1](https://arxiv.org/html/2601.03220v2#A1.SS1 "A.1 PRGs/CSPRNGs have (nearly) maximal time-bounded Entropy and low epiplexity ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
In contrast, the Shannon entropy is H​(G​(Uk))=k\\mathrm{H}(G(U\_{k}))=k, polynomial time bounded Kolmogorov complexity will be at most k+ck+c (assuming nn is fixed or specified ahead of time) as there is a short and efficiently runnable program GG which produces the output, and similarly with other notions such as Levin complexity (Li and Vitányi, [2008](https://arxiv.org/html/2601.03220v2#bib.bib58 "")) or time bounded Kolmogorov complexity (Allender et al., [2011](https://arxiv.org/html/2601.03220v2#bib.bib5 "")). Taken together, these results show that epiplexity appropriately characterizes pseudorandom numbers as carrying a large amount of time-bounded randomness but essentially no learnable structure, exactly as intuition suggests.\
\
##### Existence of Random Variables with High Epiplexity.\
\
One may wonder whether any high epiplexity random variables exist at all. Indeed, assuming the existence of one-way functions, we can show via a counting argument that there exists a sequence of\
random variables whose epiplexity grows at least logarithmically with the dimension.\
\
###### Theorem 10\
\
Assuming the existence of one-way functions secure against non-uniform probabilistic polynomial-time adversaries, there exists a sequence of random variables {Xn}n=1∞\\{X\_{n}\\}\_{n=1}^{\\infty} over {0,1}n\\{0,1\\}^{n} such that\
\
|     |     |     |\
| --- | --- | --- |\
|  | SPoly​(Xn)=Ω​(log⁡n).\\mathrm{S}\_{\\mathrm{Poly}}(X\_{n})=\\Omega(\\log n). |  |\
\
Proof: see Appendix [A.4](https://arxiv.org/html/2601.03220v2#A1.SS4 "A.4 Existence of High Epiplexity random variables ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
This result implies that epiplexity can be unbounded; however, logarithmically growing information content only admits a very modest amount of structural information, still far from the power law scaling we see with some natural data. We also note that the argument is nonconstructive and hence does not compromise cryptographic security.\
\
Conditional Entropy and Epiplexity.\
To describe situations like image classification,\
where we are only interested in a function which predicts the label from the image, and not the information in generating the images, we define _conditional_ time-bounded entropy and epiplexity.\
\
###### Definition 11 (Conditional epiplexity and time-bounded entropy)\
\
For a pair of random variables XX and YY, define 𝒫T​(n)X\\mathcal{P}\_{T(n)}^{X} as the set of probabilistic models PP such that for each fixed xx, the conditional model PY∣x\\mathrm{P}\_{Y\\mid x} is in 𝒫T​(n)\\mathcal{P}\_{T(n)}. The optimal conditional model with access to XX is:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | PY∣X⋆=arg​minP∈𝒫TX⁡{\|P\|+𝔼(X,Y)​\[−log⁡P​(Y∣X)\]}.\\displaystyle\\mathrm{P}^{\\star}\_{Y\\mid X}=\\operatorname\*{arg\\,min}\_{\\mathrm{P}\\in\\mathcal{P}\_{T}^{X}}\\left\\{\|\\mathrm{P}\|+\\mathbb{E}\_{(X,Y)}\\left\[-\\log P(Y\\mid X)\\right\]\\right\\}. |  | (5) |\
\
The conditional _epiplexity_ and _time-bounded entropy_ are defined as:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ST​(Y∣X):=\|PY∣X⋆\|,HT​(Y∣X):=𝔼(X,Y)​\[−log⁡PY∣X⋆​(y∣x)\].\\displaystyle\\mathrm{S}\_{T}(Y\\mid X):=\\left\|\\mathrm{P}^{\\star}\_{Y\\mid X}\\right\|,\\quad\\mathrm{H}\_{T}(Y\\mid X):=\\mathbb{E}\_{(X,Y)}\\left\[-\\log P^{\\star}\_{Y\\mid X}(y\\mid x)\\right\]. |  | (6) |\
\
These quantities are defined with respect to the time bounded MDL over programs which take as input X,YX,Y and output the probabilities over YY (conditioned on XX), and with expectations taken over both XX and YY. We note that in general this definition is not equivalent to the difference of the joint and individual entropies, HT​(Y,X)−HT​(X)≠HT​(Y\|X)\\mathrm{H}\_{T}(Y,X)-\\mathrm{H}\_{T}(X)\\neq\\mathrm{H}\_{T}(Y\|X).\
Unlike Shannon entropy, we can also condition on deterministic strings, which will change the values on account of not needing such a large program P\\mathrm{P}. For example, we may be interested in the conditional epiplexity ST​(X\|m)\\mathrm{S}\_{T}(X\|m) or entropy HT​(X\|m)\\mathrm{H}\_{T}(X\|m) given a model mm.\
For a deterministic string d∈{0,1}∗d\\in\\{0,1\\}^{\*} we define the conditional epiplexity via\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | PY∣d⋆=minP∈𝒫T{0,1}∗⁡{\|P\|+𝔼Y​\[−log⁡P​(Y∣d)\]},\\displaystyle\\mathrm{P}^{\\star}\_{Y\\mid d}=\\min\_{\\mathrm{P}\\in\\mathcal{P}\_{T}^{\\{0,1\\}^{\*}}}\\left\\{\|\\mathrm{P}\|+\\mathbb{E}\_{Y}\\left\[-\\log P(Y\\mid d)\\right\]\\right\\}, |  | (7) |\
\
where the minimization is over time bounded functions P(⋅\|⋅)P(\\cdot\ \|\ \\cdot) that take in the string dd as the second argument (which we refer to as 𝒫T{0,1}∗\\mathcal{P}\_{T}^{\\{0,1\\}^{\*}}).\
\
For the machine learning setting, we take the random variable XX to refer to the _entire dataset_ of interest, i.e. typically a collection X=\[X1,X2,…\]X=\[X\_{1},X\_{2},\\dots\] of many iid samples from a given distribution, rather than a lone sample from, and 𝔼​\[log⁡1/P​(X)\]\\mathbb{E}\[\\log 1/P(X)\] scales with the dataset size. Epiplexity typically grows with the size of the dataset (see detailed arguments for why this is the case in [Section˜B.4](https://arxiv.org/html/2601.03220v2#A2.SS4 "B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) as larger datasets allow identifying and extracting more intricate structure and patterns, mirroring the practice of ML training. Moreover, as we will see later, the epiplexity of a typical dataset is orders of magnitudes smaller than the random information content. While not a focus of this paper, conditioning on deterministic strings opens up the possibility to understand what additional data is most useful for a specific machine learning model, such as on top of a pretrained LLM.\
\
## 4 Measuring Epiplexity and Time-Bounded Entropy\
\
We have now introduced epiplexity and time-bounded entropy as measures of structural and random information of the data. In this section, we present practical procedures to estimate upper bounds and empirical proxies for these quantities. Intuitively, we want to find a probabilistic model P​(⋅)P(\\cdot) of the data XX that achieves low expected loss 𝔼​\[log⁡1/P​(X)\]\\mathbb{E}\[\\log 1/P(X)\], is described by a short program P,\\mathrm{P}, and evaluating P​(X)P(X) takes time at most T​(\|X\|),T(\|X\|), which we will abbreviate as T.T. Using this model, we thereby decompose the information of the data into its structural and random components, namely, (1) epiplexity ST​(X)\\mathrm{S}\_{T}(X): the length of the program \|P\|,\|\\mathrm{P}\|, accounting for the bits required to model the data distribution, and (2) time-bounded entropy HT​(X)\\mathrm{H}\_{T}(X): the expected length for entropy coding the data using this model, which accounts for the bits required to specify the particular realization of XX within that distribution. We estimate conditional epiplexity analogously, providing random variable conditioning as input into the model.\
\
Since directly searching over the space of programs is intractable, we restrict attention to probabilistic models parameterized by neural networks, as they achieve strong empirical compression across data modalities (MacKay, [2003](https://arxiv.org/html/2601.03220v2#bib.bib62 ""); Goldblum et al., [2023](https://arxiv.org/html/2601.03220v2#bib.bib39 ""); Delétang et al., [2023](https://arxiv.org/html/2601.03220v2#bib.bib25 ""); Ballé et al., [2018](https://arxiv.org/html/2601.03220v2#bib.bib10 "")) and capture the most relevant ML phenomenology. While a naive approach is to let P\\mathrm{P} be a program that directly stores the architecture and weights of a neural network and evaluates it on the given data, this approach can significantly overestimate the information content in the weights, particularly for large models trained on relatively little data. Instead, we will use a more efficient approach that encodes the training process that produces the weights. We will discuss two approaches for encoding neural network training processes, based on _prequential coding_(Dawid, [1984](https://arxiv.org/html/2601.03220v2#bib.bib23 "")) and _requential coding_(Finzi et al., [2026](https://arxiv.org/html/2601.03220v2#bib.bib32 "")), respectively. The former is more straightforward to understand and evaluate, but relies on a heuristic argument to separate structure bits from noise bits, while the latter is rigorous at the cost of being more difficult to evaluate.\
Fortunately, both approaches often yield comparable rankings of epiplexity across datasets ( [Section˜4.3](https://arxiv.org/html/2601.03220v2#S4.SS3 "4.3 Comparison Between the Two Approaches and Practical Recommendations ‣ 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")).\
\
Moving forward, we will measure time by the number of floating-point operations (FLOPs) and dataset size by number of tokens, so that training a model with NN parameters on DD tokens takes time approximately 6​N​D6ND(Kaplan et al., [2020](https://arxiv.org/html/2601.03220v2#bib.bib53 "")), while evaluating it on XX takes time 2​N​𝒟2N\\mathcal{D} with 𝒟=\|X\|\\mathcal{D}=\|X\| the number of tokens in X.X. To distinguish XX from the training dataset, which we are free to choose, we will refer to XX as the test dataset, as it is the data we need to perform inference on.\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x2.png)(a)Estimate information in model\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x3.png)(b)Compute-optimal 2-part code\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x4.png)(c)Requential vs Prequential\
\
Figure 2: How to estimate epiplexity. (a) We consider two approaches for efficiently coding trained neural networks. Prequential estimation estimates information content as the area under the loss curve of a model above its final loss, with the training set matching the test data distribution. Requential coding, which provides an explicit code for PsP^{\\mathrm{s}} with expected length as the cumulative KL between a student model PsP^{\\mathrm{s}} and the teacher PtP^{\\mathrm{t}} that generates its _synthetic_ training data, visualized approximately by their loss gap. We typically choose PtP^{\\mathrm{t}} to be a model trained on the _real_ training set, as in prequential coding.\
(b) Using either approach, we optimize hyperparameters (model size NN, training tokens DD, etc.) to find the shortest two-part code for each compute budget, which decomposes into the estimated epiplexity and time-bounded entropy.\
(c) Comparing prequential and requential coding on four groups of datsets used in this work. The prequential estimate is typically larger, but the two correlate well, particularly within each group.\
\
### 4.1 Approximating Model Description Length with Prequential Coding\
\
Prequential coding provides a classic approach for compressing the training process of a neural network. We assume a batch size of one for simplicity, but generalizing to batch sizes larger than one is straightforward. Starting with a randomly initialized network P0P\_{0} (where the subscript indicates timestep), we proceed iteratively: at each step ii, we entropy encode the current training token ZiZ\_{i} using log⁡1/Pi​(Zi)\\log 1/P\_{i}(Z\_{i}) bits, then train the model on this token to produce Pi+1P\_{i+1}. Typically ZiZ\_{i}’s are drawn i.i.d. from the same distribution as X.X. On the side of the decoder, a synchronized model is maintained; the model decodes ZiZ\_{i} using PiP\_{i} and then trains on it to produce the identical Pi+1P\_{i+1}. Omitting small constant overheads for specifying the random initialization, architecture, and training algorithm, a total of L​(Z:M,PM)=∑i=0M−1log⁡1/Pi​(Zi)L({Z\_{:M},P\_{M}})=\\sum\_{i=0}^{M-1}\\log 1/P\_{i}(Z\_{i}) bits yields an explicit code for both the training data Z:M={Z0,…,ZM−1}Z\_{:M}=\\{Z\_{0},\\ldots,Z\_{M-1}\\} and the final model weights PMP\_{M}, which can be decoded in time 6​N​D6ND for a model with NN parameters trained on DD tokens (typically D>MD>M as each example contains multiple tokens). Despite having an explicit code for Z,PMZ,P\_{M}, we cannot easily separate this into a code for PMP\_{M} alone for estimating epiplexity.\
\
To isolate the description length of PMP\_{M} alone, we adopt the heuristic in Zhang et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib110 "")) and Finzi et al. ( [2025](https://arxiv.org/html/2601.03220v2#bib.bib31 "")): we first estimate the description length of the training data given PMP\_{M} as its entropy code length under the final model, L​(Z:M\|PM)=∑i=0M−1log⁡1/PM​(Zi)L({Z\_{:M}\|P\_{M}})=\\sum\_{i=0}^{M-1}\\log 1/P\_{M}(Z\_{i}). Then, appealing to the symmetry of information, which states K​(PM)=K​(Z:M,PM)−K​(Z:M\|PM)K(P\_{M})=K(Z\_{:M},P\_{M})-K(Z\_{:M}\|P\_{M}) up to constant terms, we estimate the description length of PMP\_{M} as the difference L​(Z:M,PM)−L​(Z:M\|PM)L({Z\_{:M},P\_{M}})-L({Z\_{:M}\|P\_{M}}):\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|Ppreq\|≈∑i=0M−1(log⁡1/Pi​(Zi)−log⁡1/PM​(Zi)).\|\\mathrm{P}\_{\\mathrm{preq}}\|\\,\\approx\\sum\_{i=0}^{M-1}\\quantity(\\log 1/P\_{i}(Z\_{i})-\\log 1/P\_{M}(Z\_{i})). |  | (8) |\
\
If ZiZ\_{i} is sampled i.i.d., as is typically the case, then the code length for the model _can be visualized as the area under the loss curve above the final loss_ in [Figure˜2](https://arxiv.org/html/2601.03220v2#S4.F2 "In 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). Intuitively, the model absorbs a significant amount of information from the data if training yields a sustained and substantial reduction in loss. For random data, log⁡1/Pi​(Zi)\\log 1/P\_{i}(Z\_{i}) never decreases, while for simple data, log⁡1/Pi​(Zi)\\log 1/P\_{i}(Z\_{i}) drops rapidly and stabilizes, both leading to small \|Ppreq\|.\|\\mathrm{P}\_{\\mathrm{preq}}\|. We note that the prequential loss values are effectively taken on estimates of the _test loss_, because they evaluate the log probabilities on a batch before it is trained on, a central detail to the coding scheme. In cases where train and test diverge, such as when there is overfitting, this difference could become important important.\
\
Encoding the test dataset XX (not to be confused with the training data) using this model, we obtain a two-part code of expected length \|Ppreq\|+𝔼​\[log⁡1/PM​(X)\]\|\\mathrm{P}\_{\\mathrm{preq}}\|+\\mathbb{E}\[\\log 1/P\_{M}(X)\] that runs in time 6​N​D+2​N​𝒟.6ND+2N\\mathcal{D}. We optimize the training hyperparameters (e.g., learning rate) and the trade-off between NN and DD subject to the time bound 6​N​D+2​N​𝒟≤T6ND+2N\\mathcal{D}\\leq T to find the optimal P⋆P^{\\star} that minimizes the two-part code within this family, and estimate epiplexity and time-bounded entropy as ST​(X)=\|Ppreq⋆\|\\mathrm{S}\_{T}(X)=\|\\mathrm{P}\_{\\mathrm{preq}}^{\\star}\| and HT​(X)=𝔼​\[log⁡1/P⋆​(X)\].\\mathrm{H}\_{T}(X)=\\mathbb{E}\[\\log 1/P^{\\star}(X)\]. The better these hyperparameters are optimized, the more accurate our estimates become. We use the Maximal Update Parameterization (μ\\muP) (Yang et al., [2022](https://arxiv.org/html/2601.03220v2#bib.bib107 "")) to ensure the optimal learning rate and initialization are consistent across model sizes, simplifying tuning. We estimate the expectation 𝔼​\[log⁡1/PM​(X)\]\\mathbb{E}\[\\log 1/P\_{M}(X)\] by its empirical value on held-out validation data, i.e., the validation loss scaled by the size of XX. We detail the full procedure in [Appendix˜B](https://arxiv.org/html/2601.03220v2#A2 "Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), such as how we choose the hyperparameters and estimate the Pareto frontier of MDL vs compute.\
\
While conceptually simple, practically useful, and easy to evaluate, this prequential approach to approximating epiplexity is not rigorous for two reasons. First, both L​(Z:M,PM)L({Z\_{:M},P\_{M}}) and L​(Z:M\|PM)L({Z\_{:M}\|P\_{M}}) can only upper-bound the respective Kolmogorov complexities, and thus their difference does not yield an upper bound for K​(PM).K(P\_{M}).444We have L​(Z:M,PM)+O​(1)≥K​(Z:M,PM),L({Z\_{:M},P\_{M}})+O(1)\\geq K(Z\_{:M},P\_{M}), but not that L​(Z:M\|PM)+O​(1)≤K​(Z:M\|PM).L({Z\_{:M}\|P\_{M}})+O(1)\\leq K(Z\_{:M}\|P\_{M}). Second, even setting this issue aside, the argument only establishes the existence of a program that encodes PMP\_{M} with length \|Ppreq\|,\|\\mathrm{P}\_{\\mathrm{preq}}\|, but does not guarantee that its runtime falls within 6​N​D,6ND, since the symmetry of information does not extend to time-bounded Kolmogorov complexity. Nevertheless, prequential coding can serve as a useful starting point for crudely estimating epiplexity, particularly convenient when one already has access to the loss curve from an existing training run.\
\
### 4.2 Explicitly Coding the Model with Requential Coding\
\
To address the shortcomings of the previous approach based on prequential coding, we adopt requential coding (Finzi et al., [2026](https://arxiv.org/html/2601.03220v2#bib.bib32 "")) for constructing an explicit code of the model with a known runtime. Rather than trying to code a particular training dataset, with requential coding one can use the insensitivity to the exact data points sampled to code for _a_ sampled dataset that leads to a performant model but without paying for the entropy of the data. Specifically, it encodes a training run where at step ii a student model PisP^{\\mathrm{s}}\_{i} is trained on a synthetic token sampled randomly from a teacher model PitP^{\\mathrm{t}}\_{i}, where the sequence P0t,…,PM−1tP^{\\mathrm{t}}\_{0},\\ldots,P^{\\mathrm{t}}\_{M-1} are arbitrary teacher model checkpoints. We typically choose PitP^{\\mathrm{t}}\_{i} to be the checkpoints from training on the original _real_ training set, as in prequential coding. Using relative entropy coding (Theis and Ahmed, [2022](https://arxiv.org/html/2601.03220v2#bib.bib96 "")), the synthetic tokens Z~i∼Pit\\widetilde{Z}\_{i}\\sim P^{\\mathrm{t}}\_{i} can be coded given only the student PisP^{\\mathrm{s}}\_{i} (synchronized between encoder and decoder) using KL​(Pit∥Pis)+log(1+KL​(Pit∥Pis))+4\\mathrm{KL}(P^{\\mathrm{t}}\_{i}\\\|P^{\\mathrm{s}}\_{i})+\\log\\bigl(1+\\mathrm{KL}(P^{\\mathrm{t}}\_{i}\\\|P^{\\mathrm{s}}\_{i})\\bigr.)+4 bits in expectation.\
Summing over all steps gives the requential code length for PMsP^{\\mathrm{s}}\_{M}:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|Preq\|=∑i=0M−1KL​(Pit∥Pis)+log(1+KL​(Pit∥Pis))+4+O​(1)≈∑i=0M−1KL​(Pit∥Pis),\\displaystyle\|\\mathrm{P}\_{\\mathrm{req}}\|\\,=\\sum\_{i=0}^{M-1}\\mathrm{KL}(P^{\\mathrm{t}}\_{i}\\\|P^{\\mathrm{s}}\_{i})+\\log\\bigl(1+\\mathrm{KL}(P^{\\mathrm{t}}\_{i}\\\|P^{\\mathrm{s}}\_{i})\\bigr.)+4+O(1)\\approx\\sum\_{i=0}^{M-1}\\mathrm{KL}(P^{\\mathrm{t}}\_{i}\\\|P^{\\mathrm{s}}\_{i}), |  | (9) |\
\
where the logarithmic and constant overheads are typically negligible due to large sequence length and batch size, and as before we omit the small constant cost of specifying the random initialization, architecture, and training algorithm. In addition to providing an explicit code, a key advantage of requential coding is its flexibility in choosing the teacher sequence: by selecting teachers PitP^{\\mathrm{t}}\_{i} that remain close to the student PisP^{\\mathrm{s}}\_{i} while still pointing toward the target distribution, we keep the per-step coding cost KL​(Pit∥Pis)\\mathrm{KL}(P^{\\mathrm{t}}\_{i}\\\|P^{\\mathrm{s}}\_{i}) small while effectively guiding the student’s learning.\
\
[Figure˜2](https://arxiv.org/html/2601.03220v2#S4.F2 "In 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") connects requential coding to the student’s and teacher’s loss curves: suppose we take as teachers the checkpoints P0t,…,PM−1tP^{\\mathrm{t}}\_{0},\\ldots,P^{\\mathrm{t}}\_{M-1} from a model trained on real data Z0,…,ZM−2∼PXZ\_{0},\\ldots,Z\_{M-2}\\sim P\_{X}. For visualization, we can then estimate KL​(Pit∥Pis)\\mathrm{KL}(P^{\\mathrm{t}}\_{i}\\\|P^{\\mathrm{s}}\_{i}) by the loss gap log⁡1/Pis​(Zi)−log⁡1/Pit​(Zi)\\log 1/P^{\\mathrm{s}}\_{i}(Z\_{i})-\\log 1/P^{\\mathrm{t}}\_{i}(Z\_{i}), which is accurate when Pit≈PXP^{\\mathrm{t}}\_{i}\\approx P\_{X}.\
We can thus visualize the code length for the student as approximately the area between the teacher’s and student’s loss curves on real data, as shown in [Figure˜2](https://arxiv.org/html/2601.03220v2#S4.F2 "In 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
The two-part code has expected length \|Preq\|+𝔼​\[log⁡1/PMs​(X)\],\|\\mathrm{P}\_{\\mathrm{req}}\|+\\mathbb{E}\[\\log 1/P^{\\mathrm{s}}\_{M}(X)\], consisting of first decoding PMsP^{\\mathrm{s}}\_{M} by replaying the training process, which takes time 6​N​D6ND for a total of DD requential training tokens, and then evaluating PMsP^{\\mathrm{s}}\_{M} on the test dataset X,X, taking an additional time 2​N​𝒟,2N\\mathcal{D}, for a total runtime of 6​N​D+2​N​𝒟6ND+2N\\mathcal{D}. We optimize the training hyperparameters, teacher choices, and the trade-off between NN and DD subject to the specified time bound TT to find the optimal model P⋆P^{\\star} minimizing the two-part code, and estimate ST​(X)=\|Preq⋆\|\\mathrm{S}\_{T}(X)=\|\\mathrm{P}\_{\\mathrm{req}}^{\\star}\| and HT​(X)=𝔼​\[log⁡1/P⋆​(X)\].\\mathrm{H}\_{T}(X)=\\mathbb{E}\[\\log 1/P^{\\star}(X)\]. See details in [Section˜B.1](https://arxiv.org/html/2601.03220v2#A2.SS1 "B.1 Further details on estimating epiplexity ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
### 4.3 Comparison Between the Two Approaches and Practical Recommendations\
\
[Figure˜2](https://arxiv.org/html/2601.03220v2#S4.F2 "In 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") compares the estimated epiplexity obtained by the two approaches across four groups of datasets used in this work: ECA ( [Section˜5.1](https://arxiv.org/html/2601.03220v2#S5.SS1 "5.1 Paradox 1: Information Cannot be Created by Deterministic Transformations ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), easy and hard induction ( [Section˜5.3.1](https://arxiv.org/html/2601.03220v2#S5.SS3.SSS1 "5.3.1 Induction ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), and natural datasets ( [Section˜6.2](https://arxiv.org/html/2601.03220v2#S6.SS2 "6.2 Measuring Structural Information in Natural Data ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). While the prequential estimate is typically several times larger than the requential estimate, the two estimates correlate well, particularly within each group where the datasets yield similar learning dynamics. We detail the datasets and time bounds used in [Section˜C.7](https://arxiv.org/html/2601.03220v2#A3.SS7 "C.7 Prequential vs Requential Comparison ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). This general agreement is expected since the prequential estimate can be viewed as an approximation of requential coding with a static teacher ( [Section˜B.2](https://arxiv.org/html/2601.03220v2#A2.SS2 "B.2 Prequential Coding Approximates Requential Coding with a Static Teacher ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). In general, however, the discrepancy between the two estimates will depend on particular datasets and training configurations, and a good correlation between the two is not guaranteed.\
\
While requential coding is the more rigorous approach, it is typically 2×2\\times to 10×10\\times slower than prequential coding, which requires only standard training. The overhead depends on batch size, sequence length, and inference implementation (smaller overhead for large batches and short sequences), as requential coding requires repeatedly sampling from the teacher, though it is possible that the overhead can be reduced with more efficient algorithms. Therefore, we recommend using prequential coding for crudely estimating epiplexity and ranking the epiplexity of different datasets, particularly when one has access to the loss curve from an existing expensive training run (e.g., see an application in [Section˜6.2](https://arxiv.org/html/2601.03220v2#S6.SS2 "6.2 Measuring Structural Information in Natural Data ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), and requential coding for obtaining the most accurate estimates otherwise.\
\
### 4.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Data\
\
Under natural assumptions about neural network training—namely, that larger models are more sample-efficient and that there are diminishing returns to scaling model size or data alone—we expect epiplexity and time-bounded entropy to exhibit certain generic scaling behavior as a function of the compute budget TT and dataset size 𝒟\\mathcal{D}. In [Section˜B.4](https://arxiv.org/html/2601.03220v2#A2.SS4 "B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), we show that, under these assumptions, the compute-optimal model size N⋆​(T)N^{\\star}(T) and training data size D⋆​(T)D^{\\star}(T) are generally increasing in the compute budget TT, which implies that epiplexity ST​(X)\\mathrm{S}\_{T}(X) typically grows with TT while time-bounded entropy HT​(X)\\mathrm{H}\_{T}(X) decreases. In the infinite-compute limit, epiplexity S∞​(X)\\mathrm{S}\_{\\infty}(X) typically grows with the test set size 𝒟=\|X\|\\mathcal{D}=\|X\|, while the per-token time-bounded entropy H∞​(X)/𝒟\\mathrm{H}\_{\\infty}(X)/\\mathcal{D} decreases. These results align with our intuition that larger compute budgets and more data allow the model to extract more structural information from the dataset and reduce the apparent randomness remaining in each sample. However, they should be understood only as typical trends, with a counterexample shown in [Section˜5.3.2](https://arxiv.org/html/2601.03220v2#S5.SS3.SSS2 "5.3.2 Emergent Phenomena ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") relating to the phenomenon of emergence.\
\
## 5 Three Apparent Paradoxes of Information\
\
To illustrate the lacunae in existing information theory perspectives, we highlight three _apparent paradoxes_ of information: (1) information cannot be created by deterministic transformations; (2) total information content of an object is the same regardless of the factorization; and (3) likelihood modeling can only learn to match the data-generating process. Each statement captures some existing sentiment within the machine learning community, can be justified mathematically by Shannon and algorithmic information theory, and yet seems to be in conflict with intuitions and experimental observations. In this section, we will show with both theoretical results and empirical evidence that time bounding and epiplexity help resolve these apparent paradoxes.\
\
### 5.1 Paradox 1: Information Cannot be Created by Deterministic Transformations\
\
Both Shannon and algorithmic information theory state in some form that the total information cannot be increased by applying deterministic transformations on existing data. The data processing inequality (DPI) states that if some information source WW produces natural data XX that are collected, then no deterministic _or stochastic_ transformations used to produce YY from XX can increase the mutual information with the variable of interest WW: I​(Y;W)≤I​(X;W)I(Y;W)\\leq I(X;W). Similarly, information non-increase states that a deterministic transformation ff can only preserve or decrease the Shannon information, a property that holds pointwise −log⁡PY​(f​(x))≤−log⁡PX​(x)-\\log P\_{Y}(f(x))\\leq-\\log P\_{X}(x) and in expectation: H​(f​(X))≤H​(X)\\mathrm{H}(f(X))\\leq\\mathrm{H}(X) (we note XX here is a discrete random variable). In algorithmic information theory, there is a corresponding property: K​(f​(x))≤K​(x)+K​(f)+cK(f(x))\\leq K(x)+K(f)+c for a fixed constant cc. These inequalities appear to rule out creating new information with deterministic computational processes.\
\
How can we reconcile this fact with algorithms like AlphaZero (Silver et al., [2018](https://arxiv.org/html/2601.03220v2#bib.bib90 "")) that can be run in a closed environment from a small deterministic program on the game of chess, extracting insights about the game, different openings, the relative values of pieces in different positions, tactics and high level strategy, and requiring megabytes of information stored in the weights? Similarly we have dynamical systems with simple descriptions of the underlying laws that produce rich and unexpected structures, from which we can learn new things about them and mathematics.\
\
We also have evidence that synthetic data is helpful for model capabilities (Liu et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib60 ""); Gerstgrasser et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib37 ""); Maini et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib63 ""); OpenAI, [2025](https://arxiv.org/html/2601.03220v2#bib.bib73 "")). Moreover, if we believe that the processes that create natural data could in principle have been simulated to sufficient precision on a large computer, then all data could have been equivalently replaced with synthetic data. For practical synthetic data produced from transformations of samples from a given model and prompt, this sampling is performed with pseudorandom number generators, making the entire transformation deterministic. If we consider ff as the transformations we use to produce synthetic data and xx was the limited real data we started with, these inequalities appear to state very concretely that our synthetic data adds no additional information beyond the model and training data.\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x5.png)\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x6.png)\
\
Figure 3:\
Information created with cellular automata.\
(Left) Example rollouts from random initial conditions of the class II rule 15, class III rule 30, and class IV rule 54. Time flows from up to down.\
(Right) Measuring epiplexity on data produced by these transformations, we see that rule 15 produces little information (low HT\\mathrm{H}\_{T}, low ST)\\mathrm{S}\_{T}), rule 30 produces lots of unpredictable random information (high HT\\mathrm{H}\_{T}, low ST\\mathrm{S}\_{T}), and rule 54 produces both random and structural information (medium HT\\mathrm{H}\_{T}, high ST\\mathrm{S}\_{T}). These observations are reflected in the training loss curve of LLMs, which saturates quickly for rule 15, makes no progress for rule 30, and makes continued progress with compute for rule 54.\
\
Whatever information it is that we mean when we say that AlphaZero has produced new and unexpected insights in chess, or new theoretical results in mathematics, or with synthetic data, it is not Shannon or algorithmic information. We argue that these unintuitive properties of information theory are a consequence of assuming unlimited computation for the observer. With limited computation, a description of the AlphaZero algorithm and the result of running AlphaZero for thousands of TPU hours are distinct. To build intuition, we start with the humble CSPRNG which also creates time-bounded information through computation (albeit random information).\
\
###### Theorem 12\
\
Let G:{0,1}k→{0,1}nG:\\{0,1\\}^{k}\\to\\{0,1\\}^{n} be a PRG\\mathrm{PRG} which admits advantage ε​(k)\\varepsilon(k) and UkU\_{k} be the uniform distribution. HPoly​(G​(Uk))−HPoly​(Uk)>n−k−n​ε​(k)−c\\mathrm{H}\_{\\mathrm{Poly}}(G(U\_{k}))-\\mathrm{H}\_{\\mathrm{Poly}}(U\_{k})>n-k-n\\varepsilon(k)-c for a fixed constant cc.\
\
Proof: see Appendix [A.2](https://arxiv.org/html/2601.03220v2#A1.SS2 "A.2 Deterministic transformation can increase time bounded entropy and epiplexity ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
Notably, we have a deterministic function which dramatically increases the time-bounded information content of the input. It is worth contrasting this result with [Section 3](https://arxiv.org/html/2601.03220v2#S3 "3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), where the time-bounded information content increase from a deterministic function _can_ be bounded if the inverse function has a short program which can run efficiently. The statement highlights an important asymmetry between the function GG and its inverse with fixed computation that does not hold with unlimited computation (e.g. K​(G−1)=K​(G)+O​(1)K(G^{-1})=K(G)+O(1)). Simultaneously, it provides some useful guidance for synthetic data: if we want to produce interesting information, we should make sure the functions we use do not have simple and efficiently computable inverses.\
\
As an illustrative example, consider the iterated dynamics of elementary cellular automata (Wolfram and Gad-el Hak, [2003](https://arxiv.org/html/2601.03220v2#bib.bib104 ""); Zhang et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib109 "")). An elementary cellular automaton (ECA) is a one‑dimensional array of binary cells that evolves in discrete time steps according to a _fixed_ rule mapping each cell’s current state and the states of its two immediate neighbors to its next state. Despite their simple formulation – only 256 possible rules—these systems can produce a rich variety of behaviors, from stable and periodic patterns to chaotic and computationally universal dynamics. We setup the problem of predicting Yi=F​(Xi)Y\_{i}=F(X\_{i}) from random initial data XiX\_{i} for FF being an ECA iterated 4848 times on a grid of size 64, and assemble these pairs into a dataset X=\[X1,…,XK\]X=\[X\_{1},\\dots,X\_{K}\] and Y=\[Y1,…,YK\]Y=\[Y\_{1},\\dots,Y\_{K}\] for a total dataset of 𝒟=100\\mathcal{D}=100M tokens. We measure the conditional information content Y\|XY\|X (epiplexity and entropy) for ECA rules 15, 30, and 54 by training LLMs on this dataset. We provide a visualization of these dynamics in [Figure 3](https://arxiv.org/html/2601.03220v2#S5.F3 "Figure 3 ‣ 5.1 Paradox 1: Information Cannot be Created by Deterministic Transformations ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") (left). For the class II rule 15 in the Wolfram hierarchy (Wolfram and Gad-el Hak, [2003](https://arxiv.org/html/2601.03220v2#bib.bib104 "")), the produced behavior is periodic and has a simple inverse. Consequently, in [Figure 3](https://arxiv.org/html/2601.03220v2#S5.F3 "Figure 3 ‣ 5.1 Paradox 1: Information Cannot be Created by Deterministic Transformations ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") (right), we see that training dynamics that rapidly converge to optimal predictions and with little epiplexity or time-bounded entropy. With the class III rule 30, the computation produces outputs that are inherently intractable to predict with limited computation, and as a result we see that there is maximal time-bounded entropy that is produced but no epiplexity. For the class IV rule 54, we see that the dynamics are complex but also partly understandable: the loss decreases slowly and much epiplexity is produced. These results highlight the sensitivity of epiplexity to the generating process. With the same compute spent and with a very similar program we can have drastically different outcomes, producing simple objects, producing only random content, and producing a mix of random and structured content.\
\
### 5.2 Paradox 2: Information Content is Independent of Factorization\
\
An important property of Shannon’s information is the symmetry of information, which states that the amount of information content does not change with factorization.\
The information we acquire when predicting xx and then yy is exactly equal to when predicting yy and then xx: Shannon entropy satisfies H​(Y∣X)+H​(X)=H​(X,Y)=H​(X∣Y)+H​(Y)\\mathrm{H}(Y\\mid X)+\\mathrm{H}(X)=\\mathrm{H}(X,Y)=\\mathrm{H}(X\\mid Y)+\\mathrm{H}(Y). An analogous property also holds for Kolmogorov complexity, known as the symmetry of information identity: K​(y∣x)+K​(x)=K​(x∣y)+K​(y)+O​(1)K(y\\mid x)+K(x)=K(x\\mid y)+K(y)+O(1).\
\
On the other hand, multiple works have observed that natural text is better compressed (with final model achieving higher likelihoods) when modeled in the left-to-right order (for English) than when modeled in reverse order (Papadopoulos et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib74 ""); Bengio et al., [2019](https://arxiv.org/html/2601.03220v2#bib.bib12 "")), picking out an arrow of time in LLMs where one direction of modeling is preferred over the other. It seems likely that for many documents, other orderings may lead to more information extracted by LLMs. Similarly, as we will show later, small rearrangements of the data can lead to substantially different losses and downstream performance. Cryptographic primitives like one way functions and block cyphers also provide examples where the order of conditioning can make all the difference to how entropic the data appears, for example considering autoregressive modeling of two prime numbers followed by their product vs the reverse ordering. These experimental results and cryptographic ideas indicate what can be learned is dependent on the ordering of the data, which in turn suggests that different amounts of “information” are extracted from these different orderings.\
\
Our time-bounded definitions capture this discrepancy. Under the existence of one way permutations, we can prove that a gap in prediction exists over different factorizations for time bounded entropy.\
\
###### Theorem 13\
\
Let ff be a one-way permutation and let X=UnX=U\_{n} be uniform and Y=f​(X)Y=f(X).\
\
HPoly​(X∣Y)+HPoly​(Y)>HPoly​(Y∣X)+HPoly​(X)+ω​(log⁡n).\\mathrm{H}\_{\\mathrm{Poly}}(X\\mid Y)+\\mathrm{H}\_{\\mathrm{Poly}}(Y)>\\mathrm{H}\_{\\mathrm{Poly}}(Y\\mid X)+\\mathrm{H}\_{\\mathrm{Poly}}(X)+\\omega(\\log n).\
\
Proof: see Appendix [A.5](https://arxiv.org/html/2601.03220v2#A1.SS5 "A.5 Information Content is not Independent of Factorization ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
As a corollary, we show no polynomial time probability model which can fit a one way function’s forward direction can satisfy Bayes theorem (see [26](https://arxiv.org/html/2601.03220v2#Thmtheorem26 "Corollary 26 ‣ Combine. ‣ A.5 Information Content is not Independent of Factorization ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). Adding to these theoretical results, we look empirically at the gap in time-bounded entropy for one way functions, and the gap in both entropy and epiplexity over two orderings of predicting chess data.\
\
In [Figure 4](https://arxiv.org/html/2601.03220v2#S5.F4 "Figure 4 ‣ 5.2 Paradox 2: Information Content is Independent of Factorization ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")(a), we choose ff to be given by the 88 steps of evolution of the ECA rule 30 with state size nn and periodic boundary conditions (Wolfram and Gad-el Hak, [2003](https://arxiv.org/html/2601.03220v2#bib.bib104 "")). Though distinct from the one way functions used in cryptography, rule 30 is believed to be one way (Wolfram and Gad-el Hak, [2003](https://arxiv.org/html/2601.03220v2#bib.bib104 "")) and unlike typical one way functions, the forward pass of rule 30 can be modeled by an autoregressive transformer, which we demonstrate by constructing an explicit RASP-L (Zhou et al., [2023](https://arxiv.org/html/2601.03220v2#bib.bib111 ""); Weiss et al., [2021](https://arxiv.org/html/2601.03220v2#bib.bib102 "")) program in Appendix [D](https://arxiv.org/html/2601.03220v2#A4 "Appendix D RASP-L for Elementary Cellular Automata ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). As shown in [Figure 4](https://arxiv.org/html/2601.03220v2#S5.F4 "Figure 4 ‣ 5.2 Paradox 2: Information Content is Independent of Factorization ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")(a), the model achieves the Shannon entropy (gray) in the forward direction, but has a consistent gap in the reverse direction.\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x7.png)(a)One way functions\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x8.png)(b)Factorization order\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x9.png)(c)Chess orderings\
\
Figure 4: Factorization matters.\
(a) We compare the losses from modeling a conjectured one way function in forward and reverse as the state size nn is increased. The model reaches Shannon entropy in the forward direction, but with a persistent gap in the reverse direction. (b) The two orderings produce different outcomes. Analogous to the OWF, predicting the moves followed by the final board state is the direction that can be predicted with a straightfoward computation. Predicting the board first and then the moves requires more complex behaviors.\
(c) As compute increases, the same chess data presented in the reverse order leads to higher time-bounded entropy and epiplexity, showing it becomes more difficult to predict but allows more structure to be learned.\
\
Beyond just how the random information can vary with orderings, the structural information can also differ as we will show next.\
We demonstrate this fact by training autoregressive transformer models on the Lichess dataset, a large collection of chess games where the moves are recorded in algebraic chess notation. We consider two variants of this dataset: (1) formatting each game as the move sequence followed by final board state in FEN notation, and (2) formatting each game as the final board state followed by the move sequence, as illustrated in [Figure˜4](https://arxiv.org/html/2601.03220v2#S5.F4 "In 5.2 Paradox 2: Information Content is Independent of Factorization ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). We provide full experiment details in [Section˜C.4](https://arxiv.org/html/2601.03220v2#A3.SS4 "C.4 Chess ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). While there is no clear polynomial vs non-polynomial time separation in this setup, the first ordering is analogous to the forward direction as the final board state can be straightforwardly mapped from the moves with a simple function, while the latter ordering is analogous to the reverse direction, where recovering the moves from the final board state requires the inverse function that infers the intermediate moves from the final state. We hypothesize the reverse direction is a more complex task and will lead the model to acquire more structural information, such as a deeper understanding of the board state. [Figure˜4](https://arxiv.org/html/2601.03220v2#S5.F4 "In 5.2 Paradox 2: Information Content is Independent of Factorization ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") confirms this hypothesis, showing that the reverse order has both time-bounded higher entropy and epiplexity. This gap vanishes at small compute budgets where the model likely learns only surface statistics common to both orderings before the additional complexity of the reverse task forces it to develop richer board-state representations.\
\
### 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching\
\
There is a prevailing view that from a particular training distribution, we can at best hope to match the data generating process. If there is a property or function that is not present in the data-generating process, then we should not expect to learn it in our models. As an extension, if the generating process is simple, then so are models that attempt to match it. This viewpoint can be supported by considering the likelihood maximization process abstractly,\
arg​minP⁡𝔼X∼Q​\[−log⁡P​(X)\]=Q;\\operatorname\*{arg\\,min}\_{P}\\mathbb{E}\_{X\\sim Q}\[-\\log P(X)\]=Q;\
the test NLL is minimized when the two distributions match. The extent to which the distributions differ is regarded as a failure either from too limited a function class or insufficient data for generalization. From these arguments we could reasonably believe that AI models cannot surpass human intelligence when pretraining on human data. Here we provide two classes of phenomena that seem to contradict this viewpoint: induction, and emergence. In both cases, restricting the compute available to AI models leads them to extract more structural information than what is required for implementing the generating process itself.\
\
#### 5.3.1 Induction\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x10.png)(a)Data generating process\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x11.png)(b)Induction (hard)\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x12.png)(c)Induction (easy)\
\
Figure 5: Studying induction through epiplexity. (a) Our setup for creating induction problems.\
(b) Predicting Rule 30 ECA with hidden inputs. The LLM must induct on the hh bits missing from the input, paying a cost exponential in hh. For hh small enough but >0>0, epiplexity is increased.\
(c) Predicting Markov chain samples with hidden transition probabilities. Models that need to both use the provided probabilities and induct on the missing ones acquire the most epiplexity.\
\
The generative modeling community is often challenged with simultaneously wanting a tractable sampling process and tractable likelihood evaluation, with autoregressors, diffusion models, VAEs, GANs, and normalizing flows each providing different approaches. For natural generative processes, it is often the case that one direction may be much more straightforward than the other. Here we investigate generative processes which can be constructed by transforming latent variables such that computing likelihoods requires inducting on the values of those latents.\
\
A window into the phenomenon can be appreciated through this quote from Ilya Sutskever:\
\
> “ _You’re reading a murder mystery and at some point the text reveals the identity of the criminal. … If the model can predict \[the name\] then it must have figured out \[who perpetrated the murder from the evidence provided\]._” (Sutskever, [2019](https://arxiv.org/html/2601.03220v2#bib.bib94 ""))\
\
The author of the book on the other hand, need not have made that same induction. Instead, they may have chosen the murderer first and then painted a compelling story of their actions.\
This example highlights a gap between the generating process and the requirements of a predictive model, a gap which we explore with the following more mathematical setup.\
\
As we illustrate in [Figure 5](https://arxiv.org/html/2601.03220v2#S5.F5 "Figure 5 ‣ 5.3.1 Induction ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")(a), consider a simple to model random variable ZZ over {0,1}n\\{0,1\\}^{n} which we transform with two functions mm and ff, which are both short in length and efficient to compute, and produce the data Y=(m​(Z),f​(Z))Y=(m(Z),f(Z)). We choose m:{0,1}n→{0,1}n−hm:\\{0,1\\}^{n}\\to\\{0,1\\}^{n-h} as a masking function which removes the bits at a total of hh fixed locations in the input, leaving the rest unchanged. The generating process is simple to implement and can be executed efficiently. Now consider a likelihood generative model learning to model YY, under any given factorization. With appropriate properties of the function ff, in producing the likelihoods the model must learn to induct on the missing information in the state ZZ, and then apply the transformation given by the data generating process. We consider cases both where the function ff is hard to invert and those where ff is not especially hard to invert. In both cases, predictive circuits must be learned that were not present in the data generating process, but with hard ff these circuits only appear at exponentially high compute.\
\
Induction Hard: Rule 30 ECA. For the first setting we use uniform Z=UnZ=U\_{n} and ff as 44 steps of the rule 30 ECA on state size n=32n=32, mm simply removes the first hh bits, and we also compute the loss only on f​(Z)f(Z) (conditioned on m​(Z)m(Z)) as the bits in m​(Z)m(Z) are uniform and only add noise. We use an LLM, and the loss curves and measured epiplexities are shown in [Figure˜5](https://arxiv.org/html/2601.03220v2#S5.F5 "In 5.3.1 Induction ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). The loss converges to the number of hidden bits −log⁡P​(f​(Z)∣m​(Z))=h-\\log P(f(Z)\\mid m(Z))=h, representing the 2h2^{h} possible inductions on the hidden state. However, the total compute required for this loss to converge grows exponentially with hh, an overall behavior consistent with a strategy of passing all 2h2^{h} candidates through ff and then eliminating inconsistent candidates as values of f​(Z)if(Z)\_{i} are observed with the autoregressive factorization. This complex learned function stands in contrast with the mere f​(Z)f(Z) and simple postprocessing removing bits with masking. This picture is mirrored by the measured epiplexity: as the model is forced to induct on the missing bits, the epiplexity grows.\
\
Induction Easy: Random Markov Chains. In the second setting, we leverage the statistical induction heads setup (Edelman et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib29 "")) with a few modifications. ZZ is given by a random Markov chain transition matrix with V=8V=8 symbols, and mm removes hh columns of the matrix at fixed random locations. The function f​(Z)f(Z) computes a sampled sequence from the Markov chain of length n=512n=512. When h>0h>0, the optimal solution involves 1) using the provided rows ZZ to perfectly predict next-token probabilities on V−hV-h of the symbols, and 2) inducting on the missing rows of ZZ in-context based on the empirically observed transitions to improve remaining predictions. For h=0,h=0, the first is sufficient, and for h=8h=8 the second is sufficient. In [Figure˜5](https://arxiv.org/html/2601.03220v2#S5.F5 "In 5.3.1 Induction ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), we find evidence that both strategies are employed whenever 0<h<80<h<8 as the final loss achieved matches the theoretical loss of both (the lower of the two dotted lines). The higher horizontal line marks the loss achievable using 1) along with a simple unigram strategy (Edelman et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib29 "")), showing that the transformer learns 1) first and later the induction strategy 2). While the data generating program only only involves strategy one followed by the postprocessing masking step, the model must learn both strategies to reach these values.\
Measured epiplexity matches this picture, with values 0<h<80<h<8 having higher epiplexity than h=0h=0 or h=8h=8. We emphasize that the induction strategy was never present in the data-generating process, yet it is learned by a generative model trained on that same data distribution. In [Appendix˜G](https://arxiv.org/html/2601.03220v2#A7 "Appendix G Induction is Not Specific to Autoregressive Factorization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), we argue the induction phenomena are not specific to autoregressive models, but occur more generally for models trained via Maximum Likelihood Estimation as they need to be able to evaluate the likelihood P​(x)P(x) for an arbitrary data point xx rather than merely sample random xx from P.P. VAEs (Kingma et al., [2013](https://arxiv.org/html/2601.03220v2#bib.bib54 "")) provide a clear example of explicitly performing induction in non-autoregressive models: the encoder is trained specifically to approximate the posterior PZ\|XP\_{Z\|X}, enabling tractable likelihood estimation, yet this encoder is entirely unnecessary if the goal is merely to sample from the model.\
\
In both of the hard and easy induction examples, the size of the program needed to perform the induction strategy is greater than the size of the program needed generate the data. We can expect that with limited computational constraints, it will not be generically possible to invert the generation process using brute force, and thus, in cases where alternative inverse strategies exist (like the easy induction example with the statistical induction heads), those additional strategies increase the epiplexity. Given that there is likely no single generally applicable strategy for these computationally efficient inverses across problems, it is likely to be possible as a source of epiplexity.\
\
To make these statements more precise, it seems likely that there are _no_ constants c1c\_{1} and c2c\_{2} for which the following property holds:\
\
Limited Epiplexity Increase Property: Given any program G:{0,1}k→{0,1}n\\mathrm{G}:\\{0,1\\}^{k}\\to\\{0,1\\}^{n} running in time at most T1T\_{1} on random variable ZZ, the epiplexity of G​(Z)G(Z) is increased by at most a constant more than the size of GG:\
ST2​(G​(Uk))≤\|G\|+c1\\mathrm{S}\_{T\_{2}}(G(U\_{k}))\\leq\|\\mathrm{G}\|+c\_{1} for T2​(n)>T1​(k)+c2T\_{2}(n)>T\_{1}(k)+c\_{2}.\
\
In other words, there is no bound on how much larger the MDL optimal probability model will be than the generating program even when the model is allowed more compute than the generating program. We present this phenomenon in contrast to Shannon information or Kolmogorov complexity, where a function and its inverse can differ in complexity by at most a fixed constant: K​(F−1)=K​(F)+O​(1)K(F^{-1})=K(F)+O(1). When the computational constraints are lifted, the brute force inverse is possible, and there is no essential gap between deduction and induction, or between sampling and likelihood computation.\
\
#### 5.3.2 Emergent Phenomena\
\
One of the most striking counterexamples to the “distribution matching” viewpoint is _emergence_. Even when a system’s underlying dynamics admit a simple description, an observer with limited computation may need to learn a richer, and seemingly unrelated, set of concepts to predict or explain its behavior. As articulated by Anderson ( [1972](https://arxiv.org/html/2601.03220v2#bib.bib6 "")), reductionism—that a complex object’s behavior follows from its parts—does not guarantee that knowing those parts lets us predict the whole. Across biology and physics, many‐body interactions give rise to behaviors (e.g. bird flocking, Conway’s Game of Life patterns, molecular chemistry, superconductivity) that are not apparent from the microscopic laws alone. Here we sketch how emergence critically relates to the computational constraints of the observer, demonstrating how observers predicting future states may be required to learn _more_ than their unbounded counterparts who can execute the full generating process.\
\
Consider Type‐Ib emergence in the Carroll and Parola ( [2024](https://arxiv.org/html/2601.03220v2#bib.bib18 "")) classification, in which higher‐level patterns arise from local rules yet resist prediction from those rules. A canonical example is Conway’s Game of Life (see [Appendix E](https://arxiv.org/html/2601.03220v2#A5 "Appendix E Cellular Automata and Game of Life ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") for definition), where iterating a simple computational rule Φ\\Phi on a 22D grid leads to complex emergent behavior. For observers that lack the computational resources to directly compute the iterated evolution Φk\\Phi^{k}, an alternate description must be found. In the state evolution, one can identify localized “species” (static blocks, oscillators, gliders, guns) which propagate through space and time. By classifying these species, learning their velocities, and how they are altered under collisions with other species, as well as the ability to identify their presence in the initial state, computationally more limited observers can make predictions about the future state of the system. Doing so, however, requires a more complex program in the sense of description length, and the epiplexity will be higher. We can formalize this intuition into the following definition of emergence.\
\
###### Definition 14 (Epiplexity Emergent)\
\
Let {Φn}n≥1\\{\\Phi\_{n}\\}\_{n\\geq 1} be a computable family Φn:{0,1}n→{0,1}n\\Phi\_{n}:\\{0,1\\}^{n}\\to\\{0,1\\}^{n}\
and let {Xn}n≥1\\{X\_{n}\\}\_{n\\geq 1} be random variables over {0,1}n\\{0,1\\}^{n}.\
We say (Φ,X)(\\Phi,X) is _epiplexity-emergent_ if there exist\
time bounds T1,T2T\_{1},T\_{2} with T1​(n)=o​(T2​(n))T\_{1}(n)=o(T\_{2}(n)) and an iteration schedule k​(n)k(n) such that as n→∞n\\to\\infty,ST1​(Φ​(X)∣X,n)−ST2​(Φ​(X)∣X,n)\\displaystyle\\mathrm{S}\_{T\_{1}}(\\Phi(X)\\mid X,n)-\\mathrm{S}\_{T\_{2}}(\\Phi(X)\\mid X,n)=Θ​(1),\\displaystyle=\\Theta(1)\\,,(10)ST1​(Φk​(X)∣X,n,k)−ST2​(Φk​(X)∣X,n,k)\\displaystyle\\mathrm{S}\_{T\_{1}}(\\Phi^{k}(X)\\mid X,n,k)-\\mathrm{S}\_{T\_{2}}(\\Phi^{k}(X)\\mid X,n,k)=ω​(1),\\displaystyle=\\omega(1),where we have suppressed the dependence of XnX\_{n} and Φn\\Phi\_{n} on nn for clarity.\
\
In words, Φ,X\\Phi,X displays emergent phenomena if two observers see equivalent structural complexity in the one step map, but asymptotically more structural complexity in the multistep map for the observer with fewer computational resources.\
\
Considering Φ\\Phi from the Game of Life as an example, P​(Φ​(X)∣X,n)P(\\Phi(X)\\mid X,n) could be well estimated by both T1T\_{1} and T2T\_{2}-bounded observers using the exact time evolution rule, using constant bits for both. P​(Φk​(X)∣X,n,k)P(\\Phi^{k}(X)\\mid X,n,k) could be estimated by T2T\_{2} using the iterated rule, but not by T1T\_{1}. Using knowledge of the different pattern species improves predictions of Φk​(X)∣X\\Phi^{k}(X)\\mid X, so they would need to be learned; however, the number of patterns that needs to be considered in the time-bounded optimal solution is unbounded, and grows with the size of the board nn, and thus the gap in epiplexity for the two time bounds grows with nn. We have not proven that the Game of Life satisfies this definition, which is likely difficult as small changes to the evolution rule can destroy the emergent behavior; however, we provide empirical evidence for this set being non-empty with the example below.\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x13.png)Figure 6: Emergence in ECA. Compute-constrained models extract high epiplexity from data generated by simple rules, trading increased program length for reduced computation.\
\
In [Figure˜6](https://arxiv.org/html/2601.03220v2#S5.F6 "In 5.3.2 Emergent Phenomena ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), we empirically demonstrate the emergence phenomenon by training a transformer to predict the iterated dynamics of ECA rule 54, a class IV rule that produces complex patterns. As in Conway’s Game of Life, a model with sufficient computation can exactly simulate the dynamics by directly iterating the per-step rule—a brute-force solution with a short description length. However, a compute-limited model cannot afford this approach and must instead learn emergent patterns (e.g., gliders and their collision rules) that approximately shortcut the infeasible exact simulation. The brute-force solution can be naturally implemented by learning to autoregressively unroll intermediate ECA states rather than directly predicting the final state, resembling the use of chain-of-thought (Wei et al., [2022](https://arxiv.org/html/2601.03220v2#bib.bib101 "")) or looped transformers (Dehghani et al., [2018](https://arxiv.org/html/2601.03220v2#bib.bib24 ""); Giannou et al., [2023](https://arxiv.org/html/2601.03220v2#bib.bib38 ""); Saunshi et al., [2025](https://arxiv.org/html/2601.03220v2#bib.bib83 "")). We provide experiment details in [Section˜C.8](https://arxiv.org/html/2601.03220v2#A3.SS8 "C.8 ECA Emergence ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). While initially the non-looped model (directly predicting final state) gradually achieves better MDL and higher epiplexity as compute increases, we identify a compute threshold beyond which the looped model suddenly becomes favorable, causing an abrupt drop in MDL and epiplexity, likely by learning the simple, brute-force solution. Below this threshold, the looped model underperforms likely because it lacks the compute to fully unroll the dynamics. The non-looped model, unable to rely on brute-force simulation, must instead learn increasingly sophisticated emergent rules, recognizing more species and their interactions, thus causing epiplexity to initially rise with compute before eventually falling.\
\
While this experiment cleanly demonstrates how compute-limited models can learn richer structure from data, it is a more uncommon situation where the brute-force solution is accessible, and where training with more compute reveals a much simpler underlying structure. With natural data and compute bounds that are not extraordinarily high, we expect that expending additional compute leads to increased rather than decreased observed structure.\
\
We explore other kinds of emergence, such as in chaotic dynamical systems or in the optimal strategies of game playing agents in [Appendix F](https://arxiv.org/html/2601.03220v2#A6 "Appendix F Emergence ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). Each of these examples presents clear evidence that in pursuit of the best probability distribution to explain the data, observers with limited compute will require models with greater description length than the minimal data generating process in order to achieve comparable predictive performance (Martínez et al., [2006](https://arxiv.org/html/2601.03220v2#bib.bib65 ""); Redeker, [2010](https://arxiv.org/html/2601.03220v2#bib.bib80 "")). Epiplexity provides a general tool for understanding and quantifying these phenomena of emergence, and how simple rules can create meaningful, complex structures that AI models can learn from, as recently demonstrated empirically by Zhang et al. ( [2024](https://arxiv.org/html/2601.03220v2#bib.bib109 "")).\
\
## 6 Epiplexity, Pre-Training, and OOD Generalization\
\
Pre-training on internet-scale data has led to remarkable OOD generalization, yet a thorough understanding of this phenomenon remains elusive. What kinds of data provide the best signal for enabling broad generalization? Why does pre-training on text yield capabilities that transfer across domains while image data does not? As high-quality internet data becomes exhausted, what metric should guide the selection or synthesis of new pre-training data? In this section, we show how epiplexity helps answer these foundational questions.\
\
OOD generalization is fundamentally about how much reusable structure the model acquires, not how well it predicts in-distribution. Two models trained on different corpora can achieve the same in-distribution loss, yet differ dramatically in their ability to transfer to OOD tasks. This happens because loss captures only the residual unpredictability, corresponding to the time-bounded entropy, not how much reusable structure the model has internalized to achieve that loss. Epiplexity measures exactly this missing component: the amount of information in the learned program. Intuitively, loss indicates how random the data looks to the model, while epiplexity indicates how much structure the model must acquire to explain away the non-random part. If OOD generalization depends on reusing learned mechanisms rather than memorizing superficial statistics, then epiplexity is a natural lens through which to understand the relationship between pre-training data and OOD transfer.\
As a motivating toy example, Zhang et al. ( [2024](https://arxiv.org/html/2601.03220v2#bib.bib109 "")) observed that downstream task performance benefits most from training on type IV ECA rules over the other ECA rules, aligned with Figure [3](https://arxiv.org/html/2601.03220v2#S5.F3 "Figure 3 ‣ 5.1 Paradox 1: Information Cannot be Created by Deterministic Transformations ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") where we showed that rule 54 (a type IV rule) induces much higher epiplexity compared to other rules.\
\
### 6.1 Epiplexity Correlates with OOD Generalization in Chess\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x14.png)Figure 7: Epiplexity and OOD performance in chess. Models trained on the higher epiplexity reverse order performs better in OOD tasks.\
\
We finetune models trained on either ordering from [Section˜5.2](https://arxiv.org/html/2601.03220v2#S5.SS2 "5.2 Paradox 2: Information Content is Independent of Factorization ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") on two downstream tasks: (1) solving chess puzzles, where the model must predict the _optimal_ next move given a board state (Burns et al., [2023](https://arxiv.org/html/2601.03220v2#bib.bib17 "")), and (2) predicting centipawn evaluation, where the model evaluates positional advantage from FEN notation—a more substantial distribution shift from next-move prediction learned in pre-training. Experiment details are in [Section˜C.4](https://arxiv.org/html/2601.03220v2#A3.SS4 "C.4 Chess ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
As shown in [Figure 7](https://arxiv.org/html/2601.03220v2#S6.F7 "Figure 7 ‣ 6.1 Epiplexity Correlates with OOD Generalization in Chess ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), the reverse (board-then-moves) ordering yields higher epiplexity and better downstream performance: matching accuracy on chess puzzles but significantly higher accuracy on the centipawn task. This result supports our hypothesis: the reverse order forces the model to develop richer board-state representations needed to infer the intermediate moves, and these representations transfer to OOD tasks like centipawn evaluation that similarly require understanding the board state. This example reflects a more general principle: epiplexity measures the learnable structural information a model extracts from data to its weights, which is precisely the source of the information transferable to novel tasks, making epiplexity a plausible indicator for the potential of OOD generalization. However, we emphasize that higher epiplexity does not guarantee better generalization to any specific task: epiplexity measures the amount of structural information, irrespective of its content. A model trained on high epiplexity data can learn a lot of structures, but these structures may or may not be relevant to the particular downstream task of interest.\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x15.png)(a)Epiplexity in natural data\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x16.png)(b)Estimation via scaling laws\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x17.png)(c)ADO: epiplexity and downstream metrics\
\
Figure 8: Epiplexity reveals differences in the structural information across data modalities and can guide pre-training data selection.\
(a) Estimated epiplexity and time-bounded entropy using requential coding for 1B OpenWebText, Chess, and CIFAR-5M tokens at 6×10186\\times 10^{18} FLOPs.\
(b) Estimated values based on scaling laws and prequential coding for 1T language, image, and video tokens at 102510^{25} FLOPs.\
(c) Selecting pre-training data using ADO (Jiang et al., [2025](https://arxiv.org/html/2601.03220v2#bib.bib52 "")) leads to different loss curves than standard sampling (natural). Our measurement shows ADO selects data with higher epiplexity, in line with the improved downstream performance and OOD perplexity on different text corpora.\
\
### 6.2 Measuring Structural Information in Natural Data\
\
Among different modalities of natural data, language has proven uniquely fruitful for pre-training, not only for improving in-distribution performance such as language understanding (Radford et al., [2019](https://arxiv.org/html/2601.03220v2#bib.bib78 "")), but also for out-of-distribution tasks such as robotics control (Ahn et al., [2022](https://arxiv.org/html/2601.03220v2#bib.bib4 "")), formal theorem proving (Song et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib92 "")), and time-series forecasting (Gruver et al., [2023](https://arxiv.org/html/2601.03220v2#bib.bib45 "")). While equally abundant total information is available in other modalities, such as images and videos, pre-training on those data sources typically does not confer a similarly broad increase in capabilities. We now show that epiplexity helps explain this asymmetry by revealing differences in their structural information content. In [Figure˜8](https://arxiv.org/html/2601.03220v2#S6.F8 "In 6.1 Epiplexity Correlates with OOD Generalization in Chess ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), we show the estimated decomposition of the information in 5B tokens of data from OpenWebText, Lichess, and CIFAR-5M (Nakkiran et al., [2020](https://arxiv.org/html/2601.03220v2#bib.bib71 "")) into epiplexity (structural) and time-bounded entropy (random) with a time-bound of 6×10186\\times 10^{18} FLOPs, by training models of up to 160M parameters on at most 5B tokens using requential coding. In all cases, epiplexity accounts for only a tiny fraction of the total information, with the OpenWebText carrying the most epiplexity, followed by chess data. Despite having the most total information, CIFAR-5M data has the least epiplexity, as over 99%99\\% of its information is random (e.g., unpredictability of the exact pixels).\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x18.png)Figure 9: Epiplexity and optimal training tokens for each fixed dataset converge to predictable limits as compute increases.\
\
### 6.3 Estimating Epiplexity from Scaling Laws\
\
We can estimate the epiplexities of larger datasets at higher compute budgets using reported scaling laws,\
which describe the loss achieved by an NN-parameter model trained on DD tokens as ℒ​(N,D)=E+(N/N0)−α+(D/D0)−β\\mathcal{L}(N,D)=E+\\quantity(N/N\_{0})^{-\\alpha}+\\quantity(D/D\_{0})^{-\\beta}, for some dataset-specific constants α,β,N0,D0,E\\alpha,\\beta,N\_{0},D\_{0},E(Hoffmann et al., [2022](https://arxiv.org/html/2601.03220v2#bib.bib49 ""); Kaplan et al., [2020](https://arxiv.org/html/2601.03220v2#bib.bib53 ""); Henighan et al., [2020](https://arxiv.org/html/2601.03220v2#bib.bib48 "")). By estimating the model’s description length via the prequential coding approach ( [Section˜4.3](https://arxiv.org/html/2601.03220v2#S4.SS3 "4.3 Comparison Between the Two Approaches and Practical Recommendations ‣ 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), we obtain estimates for the epiplexity and time-bounded entropy for language, image, and video datasets, with varying resolutions and tokenizations of size 𝒟=1012\\mathcal{D}=10^{12} (1T) tokens under a compute budget of 102510^{25} FLOPs (equivalent to the training compute of Llama3 70B), illustrated in [Figure˜8](https://arxiv.org/html/2601.03220v2#S6.F8 "In 6.1 Epiplexity Correlates with OOD Generalization in Chess ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") (see details in [Section˜C.9](https://arxiv.org/html/2601.03220v2#A3.SS9 "C.9 Scaling Laws ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). Consistent with our smaller-scale experiments, we find that language data has the highest epiplexity, while image data has the least. For image data, applying VQ tokenization leads to a significant increase in epiplexity, likely as a result of allowing the model to focus on higher-level semantic structures. Video data has less time-bounded entropy and epiplexity than image data with the same resolution, likely due to significant redundancy across the temporal dimension.\
\
Using this approach, we can also gain some analytical insights about epiplexity for data admitting scaling laws of this form. As we derive in [Section˜B.3](https://arxiv.org/html/2601.03220v2#A2.SS3 "B.3 A Solvable Model Using Scaling Laws ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), for a fixed dataset XX with 𝒟\\mathcal{D} tokens, the optimal split of the compute budget between training and inference (evaluating the trained model on XX) approaches a fixed ratio as compute increases, with the optimal asymptotic training tokens D∞⋆=𝒟D^{\\star}\_{\\infty}=\\mathcal{D} and asymptotic epiplexity S∞​(X)=β1−β​D0β​𝒟1−β,\\mathrm{S}\_{\\infty}(X)=\\frac{\\beta}{1-\\beta}D\_{0}^{\\beta}\\mathcal{D}^{1-\\beta}, both illustrated in [Figure˜9](https://arxiv.org/html/2601.03220v2#S6.F9 "In 6.2 Measuring Structural Information in Natural Data ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). As expected, the maximum amount of extractable structural information is ultimately capped by the dataset size 𝒟\\mathcal{D} when compute is not the bottleneck, and epiplexity can increase further if we also grow the dataset size. For large 𝒟,\\mathcal{D}, the scale of the asymptotic epiplexity is primarily determined by β\\beta and D0,D\_{0}, with smaller β\\beta and larger D0D\_{0} leading to higher epiplexity, corresponding to slower improvement in loss and thus more (estimated) information absorbed per token. In line with our discussion on emergence in [Section˜5.3.2](https://arxiv.org/html/2601.03220v2#S5.SS3.SSS2 "5.3.2 Emergent Phenomena ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), it is possible that with significantly more compute much simpler programs can model these natural datasets, such as by directly simulating the basic laws of physics from which the natural world emerges, but the amount of required computation is likely so high that such programs remain inaccessible to any physically realizable observer and we must treat natural data as having high epiplexity for all practical purposes.\
\
### 6.4 Pre-Training Data Selection and Curriculum for Language Models\
\
A crucial step in pretraining a language model is designing the composition of the pretraining data, but there lack clear guidelines for this step.\
Existing data mixtures are designed through extensive trial-and-error and rely on heuristic guidelines such as “diversity” or “high-quality”.\
More importantly, the primary way of comparing different training data is via perplexity metrics of held-out datasets and downstream performance.\
These procedures are highly susceptible to data contamination, overfitting to a narrow set of downstream evaluations, and Goodhart’s law. After all, no suite of downstream evaluations is extensive enough to faithfully capture the range of tasks that a general-purpose language model will encounter in the real world.\
\
As we argued above, epiplexity measures the structural information learned by the model, which could be affected by data selection strategies.\
Jiang et al. ( [2025](https://arxiv.org/html/2601.03220v2#bib.bib52 "")) demonstrated that models of the loss curves for different data subsets can be used to dynamically adjust the data distribution online to favor data subsets whose training losses are _decreasing faster_ 555It is worth noting that choosing data subsets with faster-decreasing loss does not mean that the observed training loss would be smaller because such data subsets tend to have higher loss values since there is more learnable information in them. Consequently, training on them often leads to a larger area under the training loss curve..\
Intuitively, this objective aligns with increasing the prequential estimate of epiplexity described in [Section˜4.1](https://arxiv.org/html/2601.03220v2#S4.SS1 "4.1 Approximating Model Description Length with Prequential Coding ‣ 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") by maximizing information absorbed per token.\
We hypothesize that the proposed algorithm, Adaptive Data Optimization (ADO), inadvertently achieves higher epiplexity.\
Experiments of Jiang et al. ( [2025](https://arxiv.org/html/2601.03220v2#bib.bib52 "")) are conducted on decoder-only transformers with 1.3B parameters trained on 125B tokens from the Pile dataset (Gao et al., [2020](https://arxiv.org/html/2601.03220v2#bib.bib34 "")).\
The models are evaluated on a suite of 7 zero-shot downstream tasks and two OOD validation datasets, SlimPajama (Soboleva et al., [2023](https://arxiv.org/html/2601.03220v2#bib.bib91 "")) and FineWeb (Penedo et al., [2024](https://arxiv.org/html/2601.03220v2#bib.bib76 "")).\
\
In Figure [8](https://arxiv.org/html/2601.03220v2#S6.F8 "Figure 8 ‣ 6.1 Epiplexity Correlates with OOD Generalization in Chess ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")(c), we show the estimated epiplexity and the downstream performance as well as perplexity on two OOD datasets, adapted from Jiang et al. ( [2025](https://arxiv.org/html/2601.03220v2#bib.bib52 "")).\
As shown in Jiang et al. ( [2025](https://arxiv.org/html/2601.03220v2#bib.bib52 "")), ADO achieves higher downstream performance than a standard data sampling strategy that uniformly samples from the entire dataset (denoted by _Natural_ in Figure [8](https://arxiv.org/html/2601.03220v2#S6.F8 "Figure 8 ‣ 6.1 Epiplexity Correlates with OOD Generalization in Chess ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), despite not being optimized for any of these metrics.\
Interestingly, we see that ADO indeed achieves higher epiplexity measured by prequential coding.\
While these downstream evaluations do not capture everything about a pretrained model, they do offer evidence that epiplexity is a potentially useful concept for understanding the intrinsic value of pretraining data without particular downstream evaluations.\
\
## 7 Additional Related Work\
\
Epiplexity builds on a number of related ideas in algorithmic information theory and complexity science that attempt to theoretically characterize _meaningful information_.\
A group of closely related concepts are sophistication ( [subsection 2.2](https://arxiv.org/html/2601.03220v2#S2.SS2 "2.2 Random vs Structural Information ‣ 2 Background ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), effective complexity, and logical depth. Similar to sophistication, effective complexity aims to separate random from structural content (Gell-Mann and Lloyd, [1996](https://arxiv.org/html/2601.03220v2#bib.bib36 "")). From a different starting point, Bennett ( [1988](https://arxiv.org/html/2601.03220v2#bib.bib13 "")) introduced logical depth, measuring the number of time steps required by a nearly optimal program to produce a given string, and which was later shown to be equivalent to sophistication through the busy beaver function (Antunes et al., [2005](https://arxiv.org/html/2601.03220v2#bib.bib7 ""); Ay et al., [2010](https://arxiv.org/html/2601.03220v2#bib.bib9 "")). Several other formal measures have been developed to quantify structured or meaningful complexity. Algorithmic statistics offers a principled decomposition of data into regular versus random components by introducing the notion of an algorithmic sufficient statistic (Vereshchagin and Vitányi, [2004](https://arxiv.org/html/2601.03220v2#bib.bib98 "")), a concept closely tied to sophistication. Relatedly, statistical complexity in computational mechanics (Shalizi and Crutchfield, [2001](https://arxiv.org/html/2601.03220v2#bib.bib86 "")) measures the entropy of causal states in an optimally predictive model, capturing structure in time-series data. As we argued above, these existing notions of complexity do not account for the limited computation available to the observer, which is essential for understanding machine learning algorithms.\
Being oblivious to computational limits means that they cannot characterize CSPRNGs or encrypted objects as being random. One might think that these failures are surface-level; for example, a plausible strategy would be to upgrade sophistication by replacing Kolmogorov complexity with time-bounded Kolmogorov complexity in (Definition [5](https://arxiv.org/html/2601.03220v2#Thmtheorem5 "Definition 5 (Naive Sophistication (Mota et al., 2013)) ‣ 2.2 Random vs Structural Information ‣ 2 Background ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). However, this approach does not work for several reasons, the most obvious being that CSPRNG outputs do have short and efficiently runnable generating programs and thus their time-bounded Kolmogorov complexities are small.\
A more subtle reason is that doing so results in trivial sophistication for all strings, which we discuss in more detail in Appendix [A.6](https://arxiv.org/html/2601.03220v2#A1.SS6 "A.6 Problems with time-bounded sophistication ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
Our work is also closely related to several lines of work trying to characterize observer-dependent notions of information. In cryptography, Barak et al. ( [2003](https://arxiv.org/html/2601.03220v2#bib.bib11 "")) and Hsiao et al. ( [2007](https://arxiv.org/html/2601.03220v2#bib.bib50 "")) discuss several possible definitions for _computational pseudoentropy_, an observer-dependent analogue of entropy.\
HILL-pseudoentropy (Håstad et al., [1999](https://arxiv.org/html/2601.03220v2#bib.bib47 "")) is defined relative to a class of tests: a source is considered random if no test within the class can distinguish it from a high-entropy distribution with nontrivial advantage, and Yao-pseudoentropy is defined via compressing and decompressing an object for example.\
Both definitions are closely related to time-bounded entropy, which measures the random content to a given computationally bounded observer; however, our formulation directly maps on to machine learning practice and allows for separating out the structural information content, a key contribution of our work. More recently, Xu et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib105 "")) propose 𝒱\\mathcal{V}-entropy, a generalization of Shannon entropy to the minimum expected negative log probability over a given family of probability models, such as those with given computational constraints. With 𝒱\\mathcal{V}-entropy, the symmetry of information can be violated, and so too can the data processing inequality, though neither is explicitly proven in the paper. Unlike time-bounded entropy, the computational constraint in 𝒱\\mathcal{V}-entropy only limits the inference time, and does not account for the time to find such a model.\
Hence, the minimizer can be far away from the regime that is practically evaluated (such as models that are _trained_ on infinite data or with infinite compute).\
While these undesirable behaviors can be overcome by imposing further data constraints, we believe our formulation of imposing a single bound on both training and inference time leads to fewer complications.\
More importantly, both pseudoentropy and 𝒱\\mathcal{V}-entropy, much like time-bounded entropy, capture only the random component of information since it still measures the unpredictability of the random variable under the best feasible model.\
For understanding what useful information a model has learned, we are more interested in the non-random component of information as measured by epiplexity. Using existing measures of complexity, such as the Lempel-Ziv complexity and Wolfram classification, Zhang et al. ( [2024](https://arxiv.org/html/2601.03220v2#bib.bib109 "")) showed that models trained on complex data like Class IV ECA rules tend to perform better on downstream tasks.\
\
Other parts, such as the area under the curve estimate of epiplexity, have seen some related exploration in prior work. The concept of excess entropy, independently introduced under various names (Crutchfield and Packard, [1983](https://arxiv.org/html/2601.03220v2#bib.bib22 ""); Shaw, [1984](https://arxiv.org/html/2601.03220v2#bib.bib89 ""); Grassberger, [1986](https://arxiv.org/html/2601.03220v2#bib.bib42 "")) and reviewed in Feldman ( [1998](https://arxiv.org/html/2601.03220v2#bib.bib30 "")), is defined as the area between finite-block entropy density estimates and the asymptotic entropy rate of a stationary process, an analogous construction to our prequential estimate of epiplexity. However, excess entropy is defined for stationary processes observed by computationally unbounded agents, lacking the explicit dependence on the observer’s compute budget that we view as essential for the machine learning setting. More recently, Whitney et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib103 "")) introduced surplus description length (SDL), which is the summed online loss of the training algorithm, with either the entropy of the data or a fixed baseline performance subtracted out. The authors use this measurement to evaluate pre-trained representations for solving a downstream task, arguing that smaller SDL is preferred as they lead to more efficient downstream learning. In contrast, we seek to create datasets and interventions to the data which _increase_ epiplexity. More analogous to the spirit of epiplexity is information transfer from Zhang et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib110 "")), which sums a variant of a loss difference, adapted to held out test data and for the classification setting. In this work, the authors present information transfer to measure how much is learned from the data. Epiplexity is complementary to these works, clarifying the role of computation in defining information, and explicitly separating random and structural information.\
\
Several works have also explored how to quantify data complexity. Dziugaite and Roy ( [2025](https://arxiv.org/html/2601.03220v2#bib.bib28 "")) suggests that the complexity of a minimal near-optimal reference model can be viewed as a measure of data complexity under the PAC-Bayes framework and how such data complexity gives rise to empirical scaling laws.\
This perspective is related to epiplexity in that both associate data complexity with the size of compact models that explain the data well.\
However, the two notions differ in important ways.\
In particular, the PAC-Bayes formulation is concerned with the existence of some small reference model achieving good in-distribution performance, whereas epiplexity characterizes the amount of structural information extractable by a computationally bounded observer, formalized through a two-part code that explicitly accounts for the cost of obtaining such a model.\
Further, our primary interest is not in characterizing in-distribution generalization, but in using epiplexity to measure the intrinsic value of data in settings that extend beyond supervised learning.\
Relatedly, Hutter ( [2021](https://arxiv.org/html/2601.03220v2#bib.bib51 "")) shows that power-law learning curves can emerge under specific assumptions on the data-generating distribution, illustrating how properties of the data itself can shape empirical scaling behavior. While this line of work focuses on explaining observed learning dynamics rather than defining a complexity measure, it similarly emphasizes the role of data structure in determining learning outcomes.\
These perspectives on data complexity can be viewed as instances of _coarse graining_, where one seeks a compressed representation that preserves some notion of “relevant” structure. A canonical example is the information bottleneck framework, which formalizes coarse graining as a trade-off between compression and retained information about a relevant variable (Tishby et al., [2000](https://arxiv.org/html/2601.03220v2#bib.bib97 "")).\
Epiplexity is aligned with this perspective, but rather than defining relevance through a task variable or through distinguishability to tests, it measures the amount of structural information extractable by a computationally bounded learner, while explicitly accounting for the cost of obtaining the model.\
\
More broadly, our work is related to several lines of work on how resource constraints fundamentally alter the notion of simplicity and learnability. In algorithmic information theory, Schmidhuber ( [2002](https://arxiv.org/html/2601.03220v2#bib.bib84 "")) proposes the speed prior, which replaces Solomonoff’s universal prior with a _computable_ semimeasure that favors both shorter program length and smaller computation time, thereby incorporating computational resources directly into the definition of simplicity.\
Achille and Soatto ( [2025](https://arxiv.org/html/2601.03220v2#bib.bib3 "")) argue that in the transductive setting, the role of information from past data is to reduce the time needed to solve new tasks rather than to reduce uncertainty, with the optimal speedup tightly characterized by the amount of shared algorithmic information between past data and future tasks.\
In this setting, _larger_ information content is shown to be more conducive to better performance.\
In learning theory, a related line of work shows that computational limitations can directly affect what can be learned from data.\
For instance, in the problem of sparse PCA detection, Berthet and Rigollet ( [2013](https://arxiv.org/html/2601.03220v2#bib.bib14 "")) show that although there exist procedures that succeed with an information-theoretically minimal number of samples, any algorithm that runs in polynomial time necessarily requires more data under widely used average-case hardness assumptions.\
Memory and space constraints alone can also qualitatively change learnability.\
Steinhardt et al. ( [2016](https://arxiv.org/html/2601.03220v2#bib.bib93 "")) show that restricting a learner’s memory can dramatically increase the amount of data required to learn, even when the target concept itself has a very concise description.\
They identify parity functions as a canonical example where this tension is conjectured to be sharp.\
Raz ( [2018](https://arxiv.org/html/2601.03220v2#bib.bib79 "")) later resolves this conjecture by proving that any learner with sub-quadratic memory requires exponentially many samples to learn parity from random examples.\
\
## 8 Discussion\
\
Much of classical information theory is concerned with the representation and transmission of information, and abstracts away key aspects of the computational processes by which information is extracted and used. While complexity theory and cryptography treat computation as fundamental, machine learning theory typically does not.\
Yet learning, whether biological or artificial, is an inherently computational process. What can be learned from data depends not only on statistical feasibility, but on the available resources. This perspective calls for more theoretical tools that place computation on an equal footing with information.\
\
This work reframes information as a property of data relative to a computationally bounded observer, and demonstrates that information can be decomposed into time-bounded entropy and epiplexity, a formalization of structural information. It also sheds light on how perceived information can be changed through computation. This perspective resolves several tensions between information theory and empirical machine learning—including the usefulness of synthetic data, the dependence of learning on factorization and ordering, and the emergence of structure beyond the data-generating process itself. Technically, epiplexity connects ideas from algorithmic statistics, cryptography, and learning theory, showing that standard assumptions (i.e., existence of one-way functions) suffice to produce distributions with high structural complexity for efficient learners.\
\
Our framework opens several exciting directions for future work. On the theoretical side, it invites a systematic and more fine-grained understanding of how structural information changes with computational budget, model class, and data transformations, potentially yielding new lower bounds and impossibility results for representation learning and transfer. Taking information and computation as the fundamental resources may offer new explanations for the relative universality observed in large-scale training, including why scaling law exponents depend only weakly on architectural and optimizer details.\
There is also a possibility of a compute-aware analogue of classical notions such as sufficient statistics and information bottlenecks.\
More broadly, framing emergence, induction, and generalization through the lens of computationally bounded observers may offer a unifying language across learning theory, algorithmic information theory, cryptography, and complexity theory.\
\
On the empirical side, epiplexity provides a way to reason about why some data sources, formatting, and transformations can lead to more transferable models than others, even when they do not improve training loss.\
The framework suggests that pretraining data should be evaluated not only by held-out perplexity, but by how much reusable structural information it induces in a computationally bounded model.\
This perspective helps explain empirical successes of curriculum design, data ordering, augmentation strategies, and even synthetic data that appear counterintuitive from a purely statistical viewpoint.\
Our empirical estimator offers a concrete starting point for comparing datasets and interventions in data centric research.\
In the long run, we believe epiplexity could provide guidance on how to generate new synthetic data from existing data.\
\
Finally, representation learning can be understood as the gradual accumulation of epiplexity: the construction of increasingly rich internal programs that approximate a data distribution within a fixed time budget. While epiplexity in isolation is not a measure of generalization, or a complete theory of learning, this perspective raises the possibility of new notions of hardness for learning and transfer that are orthogonal to classical PAC-style measures, capturing not sample complexity but the size of the structure that must be extracted.\
Such notions may help explain why certain tasks appear to require disproportionately large models or long training horizons despite admitting simple generative descriptions, and why improvements in generalization sometimes correlate more strongly with training dynamics or data structure than with likelihood alone.\
\
Acknowledgements. We thank NSF CAREER IIS-2145492, NSF CDS&E-MSS 2134216, and DARPA AIQ\
HR00112590066 for support, and Scott Aaronson, Alan Amin, Brandon Amos, Martin Marek, Zhili Feng, Vaishnavh Nagarajan, Patrick Shafto, Charlie Chen, Alex Ozdemir, Andres Potapczynski, and Ethan Baron for helpful feedback. This work was supported by\
Google’s TPU Research Cloud (TRC) program: [https://sites.research.google/trc](https://sites.research.google/trc ""). YJ thanks the support of the Google PhD Fellowship, and SQ thanks the support of the Two Sigma Fellowship.\
\
## References\
\
- Aaronson et al. (2014)\
Scott Aaronson, Sean M Carroll, and Lauren Ouellette.\
\
Quantifying the rise and fall of complexity in closed systems: the coffee automaton.\
\
_arXiv preprint arXiv:1405.6903_, 2014.\
\
- Abdin et al. (2024)\
Marah Abdin, Jyoti Aneja, Harkirat Behl, Sébastien Bubeck, Ronen Eldan, Suriya Gunasekar, Michael Harrison, Russell J Hewett, Mojan Javaheripi, Piero Kauffmann, et al.\
\
Phi-4 technical report.\
\
_arXiv preprint arXiv:2412.08905_, 2024.\
\
- Achille and Soatto (2025)\
Alessandro Achille and Stefano Soatto.\
\
Ai agents as universal task solvers.\
\
_arXiv preprint arXiv:2510.12066_, 2025.\
\
- Ahn et al. (2022)\
Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al.\
\
Do as i can, not as i say: Grounding language in robotic affordances.\
\
_arXiv preprint arXiv:2204.01691_, 2022.\
\
- Allender et al. (2011)\
Eric Allender, Michal Kouckỳ, Detlef Ronneburger, and Sambuddha Roy.\
\
The pervasive reach of resource-bounded kolmogorov complexity in computational complexity theory.\
\
_Journal of Computer and System Sciences_, 77(1):14–40, 2011.\
\
- Anderson (1972)\
Philip W Anderson.\
\
More is different: Broken symmetry and the nature of the hierarchical structure of science.\
\
_Science_, 177(4047):393–396, 1972.\
\
- Antunes et al. (2005)\
Luis Antunes, Lance Fortnow, Dieter van Melkebeek, and N. V. Vinodchandran.\
\
Sophistication revisited.\
\
_Theory of Computing Systems_, 38(4):535–555, 2005.\
\
- Applebaum (2016)\
Benny Applebaum.\
\
Cryptographic hardness of random local functions: Survey.\
\
_Computational complexity_, 25(3):667–722, 2016.\
\
- Ay et al. (2010)\
Nihat Ay, Markus Müller, and Arleta Szkola.\
\
Effective complexity and its relation to logical depth.\
\
_IEEE transactions on information theory_, 56(9):4593–4607, 2010.\
\
- Ballé et al. (2018)\
Johannes Ballé, David Minnen, Saurabh Singh, Sung Jin Hwang, and Nick Johnston.\
\
Variational image compression with a scale hyperprior.\
\
_arXiv preprint arXiv:1802.01436_, 2018.\
\
- Barak et al. (2003)\
Boaz Barak, Ronen Shaltiel, and Avi Wigderson.\
\
Computational analogues of entropy.\
\
In _International Workshop on Randomization and Approximation Techniques in Computer Science_, pages 200–215. Springer, 2003.\
\
- Bengio et al. (2019)\
Yoshua Bengio, Tristan Deleu, Nasim Rahaman, Rosemary Ke, Sébastien Lachapelle, Olexa Bilaniuk, Anirudh Goyal, and Christopher Pal.\
\
A meta-transfer objective for learning to disentangle causal mechanisms.\
\
_arXiv preprint arXiv:1901.10912_, 2019.\
\
- Bennett (1988)\
Charles H Bennett.\
\
Logical depth and physical complexity.\
\
_The Universal Turing Machine: A Half-Century Survey_, 1:227–257, 1988.\
\
- Berthet and Rigollet (2013)\
Quentin Berthet and Philippe Rigollet.\
\
Computational lower bounds for sparse pca.\
\
_arXiv preprint arXiv:1304.0828_, 2013.\
\
- Blum and Micali (1982)\
Manuel Blum and Silvio Micali.\
\
How to generate cryptographically strong sequences of pseudo random bits.\
\
In _23rd Annual Symposium on Foundations of Computer Science (sfcs 1982)_, pages 112–117, 1982.\
\
doi: 10.1109/SFCS.1982.72.\
\
- Bradbury et al. (2018)\
James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, George Necula, Adam Paszke, Jake VanderPlas, Skye Wanderman-Milne, and Qiao Zhang.\
\
JAX: composable transformations of Python+NumPy programs, 2018.\
\
URL [http://github.com/jax-ml/jax](http://github.com/jax-ml/jax "").\
\
- Burns et al. (2023)\
Collin Burns, Pavel Izmailov, Jan Hendrik Kirchner, Bowen Baker, Leo Gao, Leopold Aschenbrenner, Yining Chen, Adrien Ecoffet, Manas Joglekar, Jan Leike, et al.\
\
Weak-to-strong generalization: Eliciting strong capabilities with weak supervision.\
\
_arXiv preprint arXiv:2312.09390_, 2023.\
\
- Carroll and Parola (2024)\
Sean M Carroll and Achyuth Parola.\
\
What emergence can possibly mean.\
\
_arXiv preprint arXiv:2410.15468_, 2024.\
\
- Chaitin (1974)\
Gregory J Chaitin.\
\
Information-theoretic limitations of formal systems.\
\
_Journal of the ACM (JACM)_, 21(3):403–424, 1974.\
\
- Chaitin (1975)\
Gregory J Chaitin.\
\
A theory of program size formally identical to information theory.\
\
_Journal of the ACM (JACM)_, 22(3):329–340, 1975.\
\
- Chaitin (1998)\
Gregory J Chaitin.\
\
_The limits of mathematics: A course on information theory and the limits of formal reasoning_.\
\
Springer, 1998.\
\
- Crutchfield and Packard (1983)\
James P Crutchfield and NH719053 Packard.\
\
Symbolic dynamics of noisy chaos.\
\
_Physica D: Nonlinear Phenomena_, 7(1-3):201–223, 1983.\
\
- Dawid (1984)\
A Philip Dawid.\
\
Present position and potential developments: Some personal views statistical theory the prequential approach.\
\
_Journal of the Royal Statistical Society: Series A (General)_, 147(2):278–290, 1984.\
\
- Dehghani et al. (2018)\
Mostafa Dehghani, Stephan Gouws, Oriol Vinyals, Jakob Uszkoreit, and Lukasz Kaiser.\
\
Universal transformers.\
\
_arXiv preprint arXiv:1807.03819_, 2018.\
\
- Delétang et al. (2023)\
Grégoire Delétang, Anian Ruoss, Paul-Ambroise Duquenne, Elliot Catt, Tim Genewein, Christopher Mattern, Jordi Grau-Moya, Li Kevin Wenliang, Matthew Aitchison, Laurent Orseau, et al.\
\
Language modeling is compression.\
\
_arXiv preprint arXiv:2309.10668_, 2023.\
\
- Dey et al. (2025)\
Nolan Dey, Bin Claire Zhang, Lorenzo Noci, Mufan Li, Blake Bordelon, Shane Bergsma, Cengiz Pehlevan, Boris Hanin, and Joel Hestness.\
\
Don’t be lazy: Completep enables compute-efficient deep transformers.\
\
_arXiv preprint arXiv:2505.01618_, 2025.\
\
- Downey and Hirschfeldt (2019)\
Rod Downey and Denis R Hirschfeldt.\
\
Algorithmic randomness.\
\
_Communications of the ACM_, 62(5):70–80, 2019.\
\
- Dziugaite and Roy (2025)\
Gintare Karolina Dziugaite and Daniel M Roy.\
\
The size of teachers as a measure of data complexity: Pac-bayes excess risk bounds and scaling laws.\
\
In _The 28th International Conference on Artificial Intelligence and Statistics_, 2025.\
\
- Edelman et al. (2024)\
Benjamin L Edelman, Ezra Edelman, Surbhi Goel, Eran Malach, and Nikolaos Tsilivis.\
\
The evolution of statistical induction heads: In-context learning markov chains.\
\
_arXiv preprint arXiv:2402.11004_, 2024.\
\
- Feldman (1998)\
David Feldman.\
\
Information theory, excess entropy.\
\
1998.\
\
- Finzi et al. (2025)\
Marc Finzi, Sanyam Kapoor, Diego Granziol, Anming Gu, Christopher De Sa, J Zico Kolter, and Andrew Gordon Wilson.\
\
Compute-optimal llms provably generalize better with scale.\
\
_arXiv preprint arXiv:2504.15208_, 2025.\
\
- Finzi et al. (2026)\
Marc Finzi, et, and al.\
\
Requential coding.\
\
Forthcoming, 2026.\
\
- Fraenkel and Lichtenstein (1981)\
Aviezri S Fraenkel and David Lichtenstein.\
\
Computing a perfect strategy for n×\\times n chess requires time exponential in n.\
\
In _International Colloquium on Automata, Languages, and Programming_, pages 278–293. Springer, 1981.\
\
- Gao et al. (2020)\
Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles Foster, Jason Phang, Horace He, Anish Thite, Noa Nabeshima, et al.\
\
The pile: An 800gb dataset of diverse text for language modeling.\
\
_arXiv preprint arXiv:2101.00027_, 2020.\
\
- Gardner (1970)\
Martin Gardner.\
\
Mathematical games.\
\
_Scientific american_, 222(6):132–140, 1970.\
\
- Gell-Mann and Lloyd (1996)\
Murray Gell-Mann and Seth Lloyd.\
\
Information measures, effective complexity, and total information.\
\
_Complexity_, 2(1):44–52, 1996.\
\
- Gerstgrasser et al. (2024)\
Matthias Gerstgrasser, Rylan Schaeffer, Apratim Dey, Rafael Rafailov, Henry Sleight, John Hughes, Tomasz Korbak, Rajashree Agrawal, Dhruv Pai, Andrey Gromov, et al.\
\
Is model collapse inevitable? breaking the curse of recursion by accumulating real and synthetic data.\
\
_arXiv preprint arXiv:2404.01413_, 2024.\
\
- Giannou et al. (2023)\
Angeliki Giannou, Shashank Rajput, Jy-yong Sohn, Kangwook Lee, Jason D Lee, and Dimitris Papailiopoulos.\
\
Looped transformers as programmable computers.\
\
In _International Conference on Machine Learning_, pages 11398–11442. PMLR, 2023.\
\
- Goldblum et al. (2023)\
Micah Goldblum, Marc Finzi, Keefer Rowan, and Andrew Gordon Wilson.\
\
The no free lunch theorem, kolmogorov complexity, and the role of inductive biases in machine learning.\
\
_arXiv preprint arXiv:2304.05366_, 2023.\
\
- Goldreich (2006)\
Oded Goldreich.\
\
_Foundations of Cryptography: Volume 1, Basic Tools_.\
\
Cambridge University Press, 2006.\
\
- Goldreich and Levin (1989)\
Oded Goldreich and Leonid A Levin.\
\
A hard-core predicate for all one-way functions.\
\
In _Proceedings of the twenty-first annual ACM symposium on Theory of computing_, pages 25–32, 1989.\
\
- Grassberger (1986)\
Peter Grassberger.\
\
Toward a quantitative theory of self-generated complexity.\
\
_International Journal of Theoretical Physics_, 25(9):907–938, 1986.\
\
- Grünwald (2007)\
Peter D Grünwald.\
\
_The minimum description length principle_.\
\
MIT press, 2007.\
\
- Grünwald et al. (2008)\
Peter D Grünwald, PM Vitányi, et al.\
\
Algorithmic information theory, 2008.\
\
- Gruver et al. (2023)\
Nate Gruver, Marc Finzi, Shikai Qiu, and Andrew G Wilson.\
\
Large language models are zero-shot time series forecasters.\
\
_Advances in Neural Information Processing Systems_, 36:19622–19635, 2023.\
\
- Hägele et al. (2024)\
Alex Hägele, Elie Bakouch, Atli Kosson, Leandro Von Werra, Martin Jaggi, et al.\
\
Scaling laws and compute-optimal training beyond fixed training durations.\
\
_Advances in Neural Information Processing Systems_, 37:76232–76264, 2024.\
\
- Håstad et al. (1999)\
Johan Håstad, Russell Impagliazzo, Leonid A Levin, and Michael Luby.\
\
A pseudorandom generator from any one-way function.\
\
_SIAM Journal on Computing_, 28(4):1364–1396, 1999.\
\
- Henighan et al. (2020)\
Tom Henighan, Jared Kaplan, Mor Katz, Mark Chen, Christopher Hesse, Jacob Jackson, Heewoo Jun, Tom B Brown, Prafulla Dhariwal, Scott Gray, et al.\
\
Scaling laws for autoregressive generative modeling.\
\
_arXiv preprint arXiv:2010.14701_, 2020.\
\
- Hoffmann et al. (2022)\
Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, et al.\
\
Training compute-optimal large language models.\
\
_arXiv preprint arXiv:2203.15556_, 2022.\
\
- Hsiao et al. (2007)\
Chun-Yuan Hsiao, Chi-Jen Lu, and Leonid Reyzin.\
\
Conditional computational entropy, or toward separating pseudoentropy from compressibility.\
\
In _Annual International Conference on the Theory and Applications of Cryptographic Techniques_, pages 169–186. Springer, 2007.\
\
- Hutter (2021)\
Marcus Hutter.\
\
Learning curve theory.\
\
_arXiv preprint arXiv:2102.04074_, 2021.\
\
- Jiang et al. (2025)\
Yiding Jiang, Allan Zhou, Zhili Feng, Sadhika Malladi, and J Zico Kolter.\
\
Adaptive data optimization: Dynamic sample selection with scaling laws.\
\
In _The Thirteenth International Conference on Learning Representations_, 2025.\
\
URL [https://openreview.net/forum?id=aqok1UX7Z1](https://openreview.net/forum?id=aqok1UX7Z1 "").\
\
- Kaplan et al. (2020)\
Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei.\
\
Scaling laws for neural language models.\
\
_arXiv preprint arXiv:2001.08361_, 2020.\
\
- Kingma et al. (2013)\
Diederik P Kingma, Max Welling, et al.\
\
Auto-encoding variational bayes, 2013.\
\
- Kolmogorov (1968)\
A. N. Kolmogorov.\
\
Three approaches to the quantitative definition of information \*.\
\
_International Journal of Computer Mathematics_, 2(1-4):157–168, 1968.\
\
doi: 10.1080/00207166808803030.\
\
URL [https://doi.org/10.1080/00207166808803030](https://doi.org/10.1080/00207166808803030 "").\
\
- Koppel (1988)\
Moshe Koppel.\
\
Structure.\
\
In Rolf Herken, editor, _The Universal Turing Machine: A Half-Century Survey_, pages 435–452. Oxford University Press, 1988.\
\
- Kraft (1949)\
Leon G. Kraft.\
\
A device for quantizing, grouping, and coding amplitude-modulated pulses.\
\
S.m. thesis, Massachusetts Institute of Technology, Cambridge, MA, 1949.\
\
URL [https://hdl.handle.net/1721.1/12390](https://hdl.handle.net/1721.1/12390 "").\
\
- Li and Vitányi (2008)\
Ming Li and Paul Vitányi.\
\
_An introduction to Kolmogorov complexity and its applications_.\
\
Springer, New York, NY, 2008.\
\
- Li et al. (2008)\
Ming Li, Paul Vitányi, et al.\
\
_An introduction to Kolmogorov complexity and its applications_, volume 3.\
\
Springer, 2008.\
\
- Liu et al. (2024)\
Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al.\
\
Deepseek-v3 technical report.\
\
_arXiv preprint arXiv:2412.19437_, 2024.\
\
- Liu and Pass (2024)\
Yanyi Liu and Rafael Pass.\
\
A direct prf construction from kolmogorov complexity.\
\
In _Annual International Conference on the Theory and Applications of Cryptographic Techniques_, pages 375–406. Springer, 2024.\
\
- MacKay (2003)\
David JC MacKay.\
\
_Information theory, inference and learning algorithms_.\
\
Cambridge university press, 2003.\
\
- Maini et al. (2024)\
Pratyush Maini, Skyler Seto, He Bai, David Grangier, Yizhe Zhang, and Navdeep Jaitly.\
\
Rephrasing the web: A recipe for compute and data-efficient language modeling.\
\
_arXiv preprint arXiv:2401.16380_, 2024.\
\
- Martin-Löf (1966)\
Per Martin-Löf.\
\
The definition of random sequences.\
\
_Information and control_, 9(6):602–619, 1966.\
\
- Martínez et al. (2006)\
Genaro Juárez Martínez, Andrew Adamatzky, and Harold V McIntosh.\
\
Phenomenology of glider collisions in cellular automaton rule 54 and associated logical gates.\
\
_Chaos, Solitons & Fractals_, 28(1):100–111, 2006.\
\
- McLeish et al. (2025)\
Sean McLeish, John Kirchenbauer, David Yu Miller, Siddharth Singh, Abhinav Bhatele, Micah Goldblum, Ashwinee Panda, and Tom Goldstein.\
\
Gemstones: A model suite for multi-faceted scaling laws.\
\
_arXiv preprint arXiv:2502.06857_, 2025.\
\
- McMillan (1956)\
Brockway McMillan.\
\
Two inequalities implied by unique decipherability.\
\
_IRE Transactions on Information Theory_, 2(4):115–116, December 1956.\
\
doi: 10.1109/TIT.1956.1056818.\
\
- Merkle (1978)\
Ralph C Merkle.\
\
Secure communications over insecure channels.\
\
_Communications of the ACM_, 21(4):294–299, 1978.\
\
- Metzger (2000)\
Roger J. Metzger.\
\
Sinai-ruelle-bowen measures for contracting Lorenz maps and flows.\
\
_Annales de l’I.H.P. Analyse non linéaire_, 17(2):247–276, 2000.\
\
URL [https://www.numdam.org/item/AIHPC\_2000\_\_17\_2\_247\_0/](https://www.numdam.org/item/AIHPC_2000__17_2_247_0/ "").\
\
- Mota et al. (2013)\
Francisco Mota, Scott Aaronson, Luís Antunes, and André Souto.\
\
Sophistication as randomness deficiency.\
\
In _Descriptional Complexity of Formal Systems: 15th International Workshop, DCFS 2013, London, ON, Canada, July 22-25, 2013. Proceedings 15_, pages 172–181. Springer, 2013.\
\
- Nakkiran et al. (2020)\
Preetum Nakkiran, Behnam Neyshabur, and Hanie Sedghi.\
\
The deep bootstrap framework: Good online learners are good offline generalizers.\
\
_arXiv preprint arXiv:2010.08127_, 2020.\
\
- Olsson et al. (2022)\
Catherine Olsson, Nelson Elhage, Neel Nanda, Nicholas Joseph, Nova DasSarma, Tom Henighan, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, et al.\
\
In-context learning and induction heads.\
\
_arXiv preprint arXiv:2209.11895_, 2022.\
\
- OpenAI (2025)\
OpenAI.\
\
GPT-5 System Card.\
\
[https://cdn.openai.com/gpt-5-system-card.pdf](https://cdn.openai.com/gpt-5-system-card.pdf ""), August 2025.\
\
Version dated August 13, 2025. Accessed: 2026-01-05.\
\
- Papadopoulos et al. (2024)\
Vassilis Papadopoulos, Jérémie Wenger, and Clément Hongler.\
\
Arrows of time for large language models.\
\
In _Forty-first International Conference on Machine Learning_, 2024.\
\
URL [https://openreview.net/forum?id=UpSe7ag34v](https://openreview.net/forum?id=UpSe7ag34v "").\
\
- Pearce and Song (2024)\
Tim Pearce and Jinyeop Song.\
\
Reconciling kaplan and chinchilla scaling laws.\
\
_arXiv preprint arXiv:2406.12907_, 2024.\
\
- Penedo et al. (2024)\
Guilherme Penedo, Hynek Kydlíček, Anton Lozhkov, Margaret Mitchell, Colin A Raffel, Leandro Von Werra, Thomas Wolf, et al.\
\
The fineweb datasets: Decanting the web for the finest text data at scale.\
\
_Advances in Neural Information Processing Systems_, 37:30811–30849, 2024.\
\
- Pesin (1977)\
Ya B Pesin.\
\
Characteristic lyapunov exponents and smooth ergodic theory.\
\
_Russian Mathematical Surveys_, 32(4):55, 1977.\
\
- Radford et al. (2019)\
Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al.\
\
Language models are unsupervised multitask learners.\
\
_OpenAI blog_, 1(8):9, 2019.\
\
- Raz (2018)\
Ran Raz.\
\
Fast learning requires good memory: A time-space lower bound for parity learning.\
\
_Journal of the ACM (JACM)_, 66(1):1–18, 2018.\
\
- Redeker (2010)\
Markus Redeker.\
\
A language for particle interactions in one-dimensional cellular automata.\
\
_arXiv preprint arXiv:1012.0158_, 2010.\
\
- Rissanen (2004)\
Jorma Rissanen.\
\
Minimum description length principle.\
\
_Encyclopedia of statistical sciences_, 7, 2004.\
\
- Salmon et al. (2011)\
John K Salmon, Mark A Moraes, Ron O Dror, and David E Shaw.\
\
Parallel random numbers: as easy as 1, 2, 3.\
\
In _Proceedings of 2011 international conference for high performance computing, networking, storage and analysis_, pages 1–12, 2011.\
\
- Saunshi et al. (2025)\
Nikunj Saunshi, Nishanth Dikkala, Zhiyuan Li, Sanjiv Kumar, and Sashank J Reddi.\
\
Reasoning with latent thoughts: On the power of looped transformers.\
\
_arXiv preprint arXiv:2502.17416_, 2025.\
\
- Schmidhuber (2002)\
Jürgen Schmidhuber.\
\
The speed prior: a new simplicity measure yielding near-optimal computable predictions.\
\
In _International conference on computational learning theory_, pages 216–228. Springer, 2002.\
\
- Shafer and Vovk (2006)\
Glenn Shafer and Vladimir Vovk.\
\
The sources of kolmogorov’s grundbegriffe.\
\
2006.\
\
- Shalizi and Crutchfield (2001)\
Cosma Rohilla Shalizi and James P Crutchfield.\
\
Computational mechanics: Pattern and prediction, structure and simplicity.\
\
_Journal of Statistical Physics_, 104(3–4):817–879, 2001.\
\
- Shannon (1948)\
Claude E Shannon.\
\
A mathematical theory of communication.\
\
_The Bell system technical journal_, 27(3):379–423, 1948.\
\
- Shannon (1950)\
Claude E. Shannon.\
\
Programming a computer for playing chess.\
\
_Philosophical Magazine_, 41(314):256–275, 1950.\
\
- Shaw (1984)\
Robert Shaw.\
\
The dripping faucet as a model chaotic system.\
\
_(No Title)_, 1984.\
\
- Silver et al. (2018)\
David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Graepel, et al.\
\
A general reinforcement learning algorithm that masters chess, shogi, and go through self-play.\
\
_Science_, 362(6419):1140–1144, 2018.\
\
- Soboleva et al. (2023)\
Daria Soboleva, Faisal Al-Khateeb, Robert Myers, Jacob R Steeves, Joel Hestness, and Nolan Dey.\
\
SlimPajama: A 627B token cleaned and deduplicated version of RedPajama.\
\
[https://cerebras.ai/blog/slimpajama-a-627b-token-cleaned-and-deduplicated-version-of-redpajama](https://cerebras.ai/blog/slimpajama-a-627b-token-cleaned-and-deduplicated-version-of-redpajama ""), 2023.\
\
URL [https://huggingface.co/datasets/cerebras/SlimPajama-627B](https://huggingface.co/datasets/cerebras/SlimPajama-627B "").\
\
- Song et al. (2024)\
Peiyang Song, Kaiyu Yang, and Anima Anandkumar.\
\
Towards large language models as copilots for theorem proving in lean.\
\
_arXiv preprint arXiv:2404.12534_, 2024.\
\
- Steinhardt et al. (2016)\
Jacob Steinhardt, Gregory Valiant, and Stefan Wager.\
\
Memory, communication, and statistical queries.\
\
In _Conference on Learning Theory_, pages 1490–1516. PMLR, 2016.\
\
- Sutskever (2019)\
Ilya Sutskever.\
\
Gpt-2.\
\
Presented at the Scaled Machine Learning Conference 2019, Computer History Museum, 2019.\
\
[https://www.youtube.com/watch?v=T0I88NhR\_9M](https://www.youtube.com/watch?v=T0I88NhR_9M "").\
\
- Terwijn (2016)\
Sebastiaan A Terwijn.\
\
The mathematical foundations of randomness.\
\
In _The Challenge of Chance: A Multidisciplinary Approach from Science and the Humanities_, pages 49–66. Springer International Publishing Cham, 2016.\
\
- Theis and Ahmed (2022)\
Lucas Theis and Noureldin Y Ahmed.\
\
Algorithms for the communication of samples.\
\
In _International Conference on Machine Learning_, pages 21308–21328. PMLR, 2022.\
\
- Tishby et al. (2000)\
Naftali Tishby, Fernando C Pereira, and William Bialek.\
\
The information bottleneck method.\
\
_arXiv preprint physics/0004057_, 2000.\
\
- Vereshchagin and Vitányi (2004)\
Nikolay Vereshchagin and Paul M.B. Vitányi.\
\
Kolmogorov’s structure functions and model selection.\
\
_IEEE Transactions on Information Theory_, 50(12):3265–3290, 2004.\
\
- von Neumann (1928)\
John von Neumann.\
\
Zur theorie der gesellschaftsspiele.\
\
_Mathematische Annalen_, 100(1):295–320, 1928.\
\
- Von Neumann (1951)\
John Von Neumann.\
\
Various techniques used in connection with random digits.\
\
_Appl. Math Ser_, 12(36-38):3, 1951.\
\
- Wei et al. (2022)\
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.\
\
Chain-of-thought prompting elicits reasoning in large language models.\
\
_Advances in neural information processing systems_, 35:24824–24837, 2022.\
\
- Weiss et al. (2021)\
Gail Weiss, Yoav Goldberg, and Eran Yahav.\
\
Thinking like transformers.\
\
In _International Conference on Machine Learning_, pages 11080–11090. PMLR, 2021.\
\
- Whitney et al. (2020)\
William F Whitney, Min Jae Song, David Brandfonbrener, Jaan Altosaar, and Kyunghyun Cho.\
\
Evaluating representations by the complexity of learning low-loss predictors.\
\
_arXiv preprint arXiv:2009.07368_, 2020.\
\
- Wolfram and Gad-el Hak (2003)\
Stephen Wolfram and M Gad-el Hak.\
\
A new kind of science.\
\
_Appl. Mech. Rev._, 56(2):B18–B19, 2003.\
\
- Xu et al. (2020)\
Yilun Xu, Shengjia Zhao, Jiaming Song, Russell Stewart, and Stefano Ermon.\
\
A theory of usable information under computational constraints.\
\
_arXiv preprint arXiv:2002.10689_, 2020.\
\
- Yang and Littwin (2023)\
Greg Yang and Etai Littwin.\
\
Tensor programs ivb: Adaptive optimization in the infinite-width limit.\
\
_arXiv preprint arXiv:2308.01814_, 2023.\
\
- Yang et al. (2022)\
Greg Yang, Edward J Hu, Igor Babuschkin, Szymon Sidor, Xiaodong Liu, David Farhi, Nick Ryder, Jakub Pachocki, Weizhu Chen, and Jianfeng Gao.\
\
Tensor programs v: Tuning large neural networks via zero-shot hyperparameter transfer.\
\
_arXiv preprint arXiv:2203.03466_, 2022.\
\
- Yao (1982)\
Andrew Chi-Chih Yao.\
\
Theory and applications of trapdoor functions (extended abstract).\
\
In _23rd Annual Symposium on Foundations of Computer Science (FOCS)_, pages 80–91. IEEE Computer Society, 1982.\
\
doi: 10.1109/SFCS.1982.95.\
\
- Zhang et al. (2024)\
Shiyang Zhang, Aakash Patel, Syed A Rizvi, Nianchen Liu, Sizhuang He, Amin Karbasi, Emanuele Zappala, and David van Dijk.\
\
Intelligence at the edge of chaos.\
\
_arXiv preprint arXiv:2410.02536_, 2024.\
\
- Zhang et al. (2020)\
Xiao Zhang, Xingjian Li, Dejing Dou, and Ji Wu.\
\
Measuring information transfer in neural networks.\
\
_arXiv preprint arXiv:2009.07624_, 2020.\
\
- Zhou et al. (2023)\
Hattie Zhou, Arwen Bradley, Etai Littwin, Noam Razin, Omid Saremi, Josh Susskind, Samy Bengio, and Preetum Nakkiran.\
\
What algorithms can transformers learn? a study in length generalization.\
\
_arXiv preprint arXiv:2310.16028_, 2023.\
\
\
## Appendix Outline\
\
This appendix provides the technical details, proofs, and experimental specifications supporting the main text.\
\
Appendix [A](https://arxiv.org/html/2601.03220v2#A1 "Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") presents rigorous proofs of all theoretical results, including properties of cryptographically secure pseudorandom number generators under time-bounded entropy and epiplexity (Theorem [9](https://arxiv.org/html/2601.03220v2#Thmtheorem9 "Theorem 9 ‣ Pseudorandom number sequences have high random content and little structure. ‣ 3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), creation of information through deterministic transformations (Theorem [12](https://arxiv.org/html/2601.03220v2#Thmtheorem12 "Theorem 12 ‣ 5.1 Paradox 1: Information Cannot be Created by Deterministic Transformations ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), the existence of high-epiplexity random variables (Theorem [10](https://arxiv.org/html/2601.03220v2#Thmtheorem10 "Theorem 10 ‣ Existence of Random Variables with High Epiplexity. ‣ 3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), the factorization dependence of information content (Theorem [13](https://arxiv.org/html/2601.03220v2#Thmtheorem13 "Theorem 13 ‣ 5.2 Paradox 2: Information Content is Independent of Factorization ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")).\
\
Appendix [B](https://arxiv.org/html/2601.03220v2#A2 "Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") details the practical methodology for estimating epiplexity, covering both prequential and requential coding implementations, hyperparameter optimization procedures for compute-optimal two-part codes, the connection between prequential and requential estimates under a static teacher assumption, and a solvable analytical model combining neural scaling laws with prequential coding. We also establish general properties showing that optimal model size and training tokens increase monotonically with compute budget, that optimal training tokens for prequential coding generally saturate at the test set size for large compute budgets, and that epiplexity and per-token entropy exhibit predictable monotonicity with respect to dataset size.\
\
Appendix [C](https://arxiv.org/html/2601.03220v2#A3 "Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") provides comprehensive experimental specifications for all empirical results, including architectural choices, hyperparameters, and dataset details for elementary cellular automata experiments, easy and hard variants of induction tasks, chess experiments (with both pre-training data formatting and downstream evaluation tasks), natural data experiments on OpenWebText and CIFAR-5M, comparisons between prequential and requential coding estimates, and scaling law estimation procedures.\
\
Appendix [D](https://arxiv.org/html/2601.03220v2#A4 "Appendix D RASP-L for Elementary Cellular Automata ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") presents executable RASP-L code demonstrating that elementary cellular automaton evolution rules can be implemented within the transformer computational model, providing constructive evidence that autoregressive transformers are capable of solving these tasks.\
\
Appendix [E](https://arxiv.org/html/2601.03220v2#A5 "Appendix E Cellular Automata and Game of Life ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") contains definitions of elementary cellular automata and Conway’s Game of Life, emergence examples referenced in the paper.\
\
Appendix [F](https://arxiv.org/html/2601.03220v2#A6 "Appendix F Emergence ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") explores additional examples illustrating the relationship between emergence and epiplexity, including the Lorenz system as a case study in chaotic dynamics where entropy is created at a rate determined by Lyapunov exponents, and chess strategy as exemplified by the contrast between AlphaZero’s multi-million parameter networks solution at moderate compute and the simple minimax algorithm available at very high compute.\
\
Appendix [G](https://arxiv.org/html/2601.03220v2#A7 "Appendix G Induction is Not Specific to Autoregressive Factorization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") argues that induction phenomena occur not merely in autoregressive models; instead, the key requirement is maximum likelihood estimation rather than autoregressive factorization specifically.\
\
Appendix [H](https://arxiv.org/html/2601.03220v2#A8 "Appendix H Minimum Description Legnth ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") provides a more comprehensive review of MDL, in particular on two-part code, one-part code and the notion of regret, related to epiplexity.\
\
Compute Resources. A cluster of 6 2080Ti was used for many of the smaller scale experiments. A cluster of 6 Titan RTX and 32 TPUv4 provided by the Google TPU Research Cloud was used for the more computationally expensive natural data experiments. We refer the reader to Jiang et al. ( [2025](https://arxiv.org/html/2601.03220v2#bib.bib52 "")) for computational resources required in evaluating ADO.\
\
Licenses. The Chess data used in [Section˜5.2](https://arxiv.org/html/2601.03220v2#S5.SS2 "5.2 Paradox 2: Information Content is Independent of Factorization ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") is released under Creative Commons CC0 license ( [database.lichess.org/](https://database.lichess.org/ "")).\
The OpenWebText dataset used in [Section˜6.2](https://arxiv.org/html/2601.03220v2#S6.SS2 "6.2 Measuring Structural Information in Natural Data ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") is released under Creative Commons CC0 license.\
\
## Appendix A Proofs\
\
First, we prove two short lemmas about the basic properties of epiplexity and time-bounded entropy.\
\
###### Lemma 15 (Maximum expected description length)\
\
For any random variable XX on {0,1}n\\{0,1\\}^{n} there exists constants c1,c2,c3c\_{1},c\_{2},c\_{3} such that:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ST​(X)+HT​(X)≤n+c1\\mathrm{S}\_{T}(X)+\\mathrm{H}\_{T}(X)\\leq n+c\_{1} |  | (11) |\
\
for time bounds T​(n)≥c2​n+c3T(n)\\geq c\_{2}n+c\_{3}.\
\
Proof\
Let UnU\_{n} be the uniform distribution Qunif​(x)=2−nQ\_{\\mathrm{unif}}(x)=2^{-n}.\
QunifQ\_{\\mathrm{unif}} can be computed in linear time (just by outputting 2−n2^{-n} for each input) and with a program of constant size c1c\_{1} and in time c2​n+c3c\_{2}n+c\_{3} with constants depending on the Turing machine..\
\
|     |     |     |\
| --- | --- | --- |\
|  | \|QX⋆\|+𝔼​\[−log⁡QX⋆​(x)\]≤\|Qunif\|+𝔼​\[−log⁡Qunif​(x)\]≤c+n.\|Q^{\\star}\_{X}\|+\\mathbb{E}\[-\\log Q^{\\star}\_{X}(x)\]\\leq\|Q\_{\\mathrm{unif}}\|+\\mathbb{E}\[-\\log Q\_{\\mathrm{unif}}(x)\]\\leq c+n. |  |\
\
###### Lemma 16 (Time-bounded entropy of uniform distribution)\
\
Let X=UnX=U\_{n} be the uniform distribution on {0,1}n\\{0,1\\}^{n}. The time-bounded entropy of UnU\_{n} for T​(n)≥c2​n+c3T(n)\\geq c\_{2}n+c\_{3} is:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | n≤HT​(X)≤n+c1.n\\leq\\mathrm{H}\_{T}(X)\\leq n+c\_{1}. |  | (12) |\
\
Proof\
\
For the lower bound, we have\
\
|     |     |     |\
| --- | --- | --- |\
|  | 𝔼X​\[−log⁡Q​(X)\]=H​(X)+DKL​(PX∥Q)≥H​(X)=n\\mathbb{E}\_{X}\[-\\log Q(X)\]=\\mathrm{H}(X)+D\_{\\mathrm{KL}}(P\_{X}\\\|Q)\\geq\\mathrm{H}(X)=n |  |\
\
given that the KL is always positive.\
For the upper bound, we have that\
\
|     |     |     |\
| --- | --- | --- |\
|  | HT​(X)≤MDLT​(X)≤n+c\\mathrm{H}\_{T}(X)\\leq\\mathrm{MDL}\_{T}(X)\\leq n+c |  |\
\
.\
\
\
### A.1 PRGs/CSPRNGs have (nearly) maximal time-bounded Entropy and low epiplexity\
\
###### Theorem 17\
\
Let X=UkX=U\_{k} and n=ℓ​(k)n=\\ell(k) for a non-uniform PRG GG that admits advantage ε​(n)\\varepsilon(n).\
Then, for every polynomial time bound T​(n)T(n),\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | HT​(G​(Uk))≥n−2−n​ε​(k).\\mathrm{H}\_{T}\\bigl(G(U\_{k})\\bigr)\ \\geq\ n-2-n\\,\\varepsilon(k). |  | (13) |\
\
Proof\
Fix P∈𝒫T\\mathrm{P}\\in\\mathcal{P}\_{T} and let L​(x)=−log⁡P​(x)L(x)=-\\log P(x). For each precision level t∈{1,2,…,n}t\\in\\{1,2,\\dots,n\\}, we define the following distinguisher:\
\
|     |     |     |\
| --- | --- | --- |\
|  | Dt​(x)=𝟙​{L​(x)≤n−t}=𝟙​{P​(x)≥2−(n−t)}.D\_{t}(x)=\\mathbbm{1}\\{L(x)\\leq n-t\\}=\\mathbbm{1}\\{P(x)\\geq 2^{-(n-t)}\\}. |  |\
\
For any solution PP for MDLT\\mathrm{MDL}\_{T}, we have that MDLT​(X)=\|P\|+𝔼​\[−log⁡P​(X)\]≤n+c\\mathrm{MDL}\_{T}(X)=\|\\mathrm{P}\|+\\mathbb{E}\[-\\log P(X)\]\\leq n+c. Since both quantities are positive, it must be the case that \|P\|≤n+c\|\\mathrm{P}\|\\leq n+c, which means that \|P\|∈poly​(n)\|\\mathrm{P}\|\\in\\mathrm{poly}(n).\
Since P\\mathrm{P} belongs in 𝒫T\\mathcal{P}\_{T} and cannot be longer than nn, each DtD\_{t} is a non-uniform PPT algorithm with polysized advice (i.e., P\\mathrm{P}) that PRGs are secure against.\
\
##### Uniform threshold bound.\
\
Let UnU\_{n} be uniform on {0,1}n\\{0,1\\}^{n} and set At:={x:Dt​(x)=1}A\_{t}:=\\{x:D\_{t}(x)=1\\}.\
\
|     |     |     |\
| --- | --- | --- |\
|  | 1≥∑xP​(x)≥∑x∈AtP​(x)≥\|At\|​2−(n−t)⇒\|At\|≤2n−t.1\\geq\\sum\_{x}P(x)\\geq\\sum\_{x\\in A\_{t}}P(x)\\geq\|A\_{t}\|2^{-(n-t)}\\Rightarrow\|A\_{t}\|\\leq 2^{n-t}. |  |\
\
Hence ,\
\
|     |     |     |\
| --- | --- | --- |\
|  | Pr⁡\[Dt​(Un)=1\]=\|At\|2n≤2n−t2n=2−t.\\Pr\[D\_{t}(U\_{n})=1\]=\\frac{\|A\_{t}\|}{2^{n}}\\leq\\frac{2^{n-t}}{2^{n}}=2^{-t}. |  |\
\
##### PRG transfers bound to X:=G​(Uk)X:=G(U\_{k}).\
\
By the security of GG, for each tt,\
\
|     |     |     |\
| --- | --- | --- |\
|  | Pr⁡\[Dt​(X)=1\]≤Pr⁡\[Dt​(Un)=1\]+ε​(k)≤ 2−t+ε​(k),\\Pr\[D\_{t}(X)=1\\bigr\]\ \\leq\ \\Pr\[D\_{t}(U\_{n})=1\\bigr\]+\\varepsilon(k)\ \\leq\ 2^{-t}+\\varepsilon(k), |  |\
\
##### From threshold probabilities to an entropy lower bound.\
\
For any non-negative random variable ZZ, we have the layercake representation:\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | 𝔼​\[Z\]\\displaystyle\\mathbb{E}\[Z\] | =∑u=0∞(1−P​(Z≤u))\\displaystyle=\\sum\_{u=0}^{\\infty}(1-P(Z\\leq u)) |  | (14) |\
|  | n−𝔼​\[Z\]\\displaystyle n-\\mathbb{E}\[Z\] | =∑u=0n−11−∑u=0∞(1−P​(Z≤u))\\displaystyle=\\sum\_{u=0}^{n-1}1-\\sum\_{u=0}^{\\infty}(1-P(Z\\leq u)) |  | (15) |\
|  |  | =∑u=0n−11−∑u=0n−1(1−P​(Z≤u))−∑u=n∞(1−P​(Z≤u))\\displaystyle=\\sum\_{u=0}^{n-1}1-\\sum\_{u=0}^{n-1}(1-P(Z\\leq u))-\\sum\_{u=n}^{\\infty}(1-P(Z\\leq u)) |  | (16) |\
|  |  | =∑u=0n−1P​(Z≤u)−∑u=n∞(1−P​(Z≤u))\\displaystyle=\\sum\_{u=0}^{n-1}P(Z\\leq u)-\\sum\_{u=n}^{\\infty}(1-P(Z\\leq u)) |  | (17) |\
|  |  | ≤∑u=0n−1P​(Z≤u).\\displaystyle\\leq\\sum\_{u=0}^{n-1}P(Z\\leq u). |  | (18) |\
\
Now we change the bounds to be in terms of tt with t=n−ut=n-u. The lower bound becomes t=nt=n. The upper bound becomes t=1t=1, which yields\
\
|     |     |     |\
| --- | --- | --- |\
|  | n−𝔼​\[Z\]≤∑u=0n−1P​(Z≤u)=∑t=1nP​(Z≤n−t).n-\\mathbb{E}\[Z\]\\leq\\sum\_{u=0}^{n-1}P(Z\\leq u)=\\sum\_{t=1}^{n}P(Z\\leq n-t). |  |\
\
Let Z=L​(X)=−log⁡P​(X)Z=L(X)=-\\log P(X):\
\
|     |     |     |\
| --- | --- | --- |\
|  | n−𝔼​\[Z\]≤∑t=1nP​(Z≤n−t)=∑t=1nP​(Dt​(X)=1)≤∑t=1n2−t+ε​(k)≤1+n​ε​(k).n-\\mathbb{E}\[Z\]\\leq\\sum\_{t=1}^{n}P(Z\\leq n-t)=\\sum\_{t=1}^{n}P(D\_{t}(X)=1)\\leq\\sum\_{t=1}^{n}2^{-t}+\\varepsilon(k)\\leq 1+n\\varepsilon(k). |  |\
\
The last two steps come from the fact that XX is a CSPRNG. This means that:\
\
|     |     |     |\
| --- | --- | --- |\
|  | n−𝔼​\[L​(X)\]≤1+n​ε​(k)⇒𝔼​\[−log⁡P​(X)\]≥n−n​ε​(k)−1.n-\\mathbb{E}\[L(X)\]\\leq 1+n\\varepsilon(k)\\Rightarrow\\mathbb{E}\[-\\log P(X)\]\\geq n-n\\varepsilon(k)-1. |  |\
\
Since this is true for any P∈𝒫TP\\in\\mathcal{P}\_{T}, taking the minimum yields:\
\
|     |     |     |\
| --- | --- | --- |\
|  | HT​(X)=HT​(G​(Un))=minP∈𝒫T⁡𝔼​\[−log⁡P​(X)\]≥n−n​ε​(k)−1.\\mathrm{H}\_{T}(X)=\\mathrm{H}\_{T}(G(U\_{n}))=\\min\_{P\\in\\mathcal{P}\_{T}}\\mathbb{E}\[-\\log P(X)\]\\geq n-n\\varepsilon(k)-1. |  |\
\
### A.2 Deterministic transformation can increase time bounded entropy and epiplexity\
\
###### Theorem 18\
\
Let G:{0,1}k→{0,1}nG:\\{0,1\\}^{k}\\to\\{0,1\\}^{n} be a CSPRNG\\mathrm{CSPRNG} which admits advantage ε​(k)\\varepsilon(k) and UkU\_{k} be the uniform distribution. HPoly​(G​(Uk))>HPoly​(Uk)+n−k−n​ε​(k)−c\\mathrm{H}\_{\\mathrm{Poly}}(G(U\_{k}))>\\mathrm{H}\_{\\mathrm{Poly}}(U\_{k})+n-k-n\\varepsilon(k)-c for a fixed constant cc. Proof: see Appendix [A.1](https://arxiv.org/html/2601.03220v2#A1.SS1 "A.1 PRGs/CSPRNGs have (nearly) maximal time-bounded Entropy and low epiplexity ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
Proof\
By Lemma [15](https://arxiv.org/html/2601.03220v2#Thmtheorem15 "Lemma 15 (Maximum expected description length) ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") applied to the uniform distribution on {0,1}k\\{0,1\\}^{k},\
there is an absolute constant cc such that\
\
|     |     |     |\
| --- | --- | --- |\
|  | Hpoly​(Uk)≤k+c.\\mathrm{H}\_{\\mathrm{poly}}(U\_{k})\\leq k+c. |  |\
\
Rearranging gives k≥Hpoly​(Uk)−O​(1)k\\geq\\mathrm{H}\_{\\mathrm{poly}}(U\_{k})-O(1).\
Combining this with the assumed CSPRNG lower bound (Lemma [17](https://arxiv.org/html/2601.03220v2#Thmtheorem17 "Theorem 17 ‣ A.1 PRGs/CSPRNGs have (nearly) maximal time-bounded Entropy and low epiplexity ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")),\
\
|     |     |     |\
| --- | --- | --- |\
|  | Hpoly​(G​(Uk))≥n−2−n​ε​(k),\\mathrm{H}\_{\\mathrm{poly}}(G(U\_{k}))\\geq n-2-n\\varepsilon(k), |  |\
\
we obtain,\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  |  | Hpoly​(G​(Uk))−Hpoly​(Uk)≥n−2−n​ε​(k)−(k+c)\\displaystyle\\mathrm{H}\_{\\mathrm{poly}}(G(U\_{k}))-\\mathrm{H}\_{\\mathrm{poly}}(U\_{k})\\geq n-2-n\\varepsilon(k)-(k+c) |  |\
|  | ⇒\\displaystyle\\Rightarrow | HPoly​(G​(Uk))>HPoly​(Uk)+n−n​ε​(k)−k−O​(1).\\displaystyle\\mathrm{H}\_{\\mathrm{Poly}}(G(U\_{k}))>\\mathrm{H}\_{\\mathrm{Poly}}(U\_{k})+n-n\\varepsilon(k)-k-O(1). |  |\
\
### A.3 CSPRNGs have low epiplexity\
\
###### Theorem 19\
\
Let X=UkX=U\_{k} and n=ℓ​(k)n=\\ell(k) for CSPRNG GG that admits advantange ε​(n)\\varepsilon(n).\
Then, for every polynomial time bound T​(n)T(n), the epiplexity of Y=G​(X)Y=G(X) is,\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ST​(Y)≤c+n​ε​(k).\\mathrm{S}\_{T}(Y)\\leq c+n\\varepsilon(k). |  | (19) |\
\
Proof\
We know from Theorem [17](https://arxiv.org/html/2601.03220v2#Thmtheorem17 "Theorem 17 ‣ A.1 PRGs/CSPRNGs have (nearly) maximal time-bounded Entropy and low epiplexity ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") that HT​(G​(Uk))≥n−n​ε​(k)−2\\mathrm{H}\_{T}(G(U\_{k}))\\geq n-n\\varepsilon(k)-2, which means:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ST​(Y)+HT​(Y)≥ST​(Y)+n−n​ε​(k)−2.\\displaystyle\\mathrm{S}\_{T}(Y)+\\mathrm{H}\_{T}(Y)\\geq\\mathrm{S}\_{T}(Y)+n-n\\varepsilon(k)-2. |  | (20) |\
\
We also have from Lemma [15](https://arxiv.org/html/2601.03220v2#Thmtheorem15 "Lemma 15 (Maximum expected description length) ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") that ST​(Y)+HT​(Y)≤n+c\\mathrm{S}\_{T}(Y)+\\mathrm{H}\_{T}(Y)\\leq n+c. Combining these two results yields:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ST​(Y)+n−n​ε​(k)−1≤n+c⇒ST​(Y)≤c+n​ε​(k).\\displaystyle\\mathrm{S}\_{T}(Y)+n-n\\varepsilon(k)-1\\leq n+c\\Rightarrow\\mathrm{S}\_{T}(Y)\\leq c+n\\varepsilon(k). |  | (21) |\
\
### A.4 Existence of High Epiplexity random variables\
\
###### Definition 20 (Pseudorandom functions (PRF))\
\
Let PRF\\mathrm{PRF} be the class of keyed functions F:{0,1}k×{0,1}n→{0,1}mF:\\{0,1\\}^{k}\\times\\{0,1\\}^{n}\\to\\{0,1\\}^{m} that are computable in polynomial time and satisfy the following property: For any probabilistic polynomial-time distinguisher DD with oracle access to the provided function,\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|PrK∼Uk⁡\[DFK​(⋅)\]−Prf∼ℱn⁡\[Df​(⋅)\]\|<1nc,\|\\Pr\_{K\\sim U\_{k}}\[D^{F\_{K}(\\cdot)}\]-\\Pr\_{f\\sim\\mathcal{F}\_{n}}\[D^{f(\\cdot)}\]\|<\\frac{1}{n^{c}}, |  | (22) |\
\
for all integers c>0c>0 and sufficiently large nn. Here, FK​(⋅)F\_{K}(\\cdot) denotes the function F​(K,⋅)F(K,\\cdot) with the key KK fixed, and ℱn\\mathcal{F}\_{n} is the set of all functions mapping {0,1}n\\{0,1\\}^{n} to {0,1}m\\{0,1\\}^{m}.\
\
##### Cryptographic assumptions.\
\
Assume one-way functions exist (secure against non-uniform PPT adversaries with inversion probability at most\
ε​(n)\\varepsilon(n)). By standard constructions (Håstad et al., [1999](https://arxiv.org/html/2601.03220v2#bib.bib47 "")), this implies the existence of PRFs secure against non-uniform PPT distinguishers with advantage poly​(ε​(n))\\mathrm{poly}(\\varepsilon(n)) (and in particular negligible if ε​(n)\\varepsilon(n) is negligible).\
\
###### Definition 21 (Heavy set)\
\
For a distribution QQ on {0,1}n\\{0,1\\}^{n}, m<nm<n, and a fixed threshold t≥0t\\geq 0, the (Q,t)(Q,t)-heavy set is:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | AQ,t:={z:Q​(z)≥2−2​(m+t)}.\\displaystyle A\_{Q,t}:=\\{z:Q(z)\\geq 2^{-2(m+t)}\\}. |  | (23) |\
\
###### Lemma 22\
\
Let PP be a distribution on {0,1}n\\{0,1\\}^{n} with entropy H​(P)=m\\mathrm{H}(P)=m. If KL​(P,Q)≤t\\mathrm{KL}(P,Q)\\leq t, then P​(AQ,t)≥12P(A\_{Q,t})\\geq\\frac{1}{2}.\
\
Proof\
First, observe the standard inequality:\
\
|     |     |     |\
| --- | --- | --- |\
|  | 𝔼z∼P​\[log⁡1Q​(z)\]=H​(P)+KL​(P∥Q)≤m+t.\\mathbb{E}\_{z\\sim P}\\left\[\\log\\frac{1}{Q(z)}\\right\]=\\mathrm{H}(P)+\\mathrm{KL}(P\\\|Q)\\leq m+t. |  |\
\
Applying Markov’s inequality, we get:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | Prz∼P⁡\[log⁡1Q​(z)≥2​(m+t)\]≤𝔼​\[−log⁡Q​(z)\]2​(m+t)≤12.\\displaystyle\\Pr\_{z\\sim P}\\left\[\\log\\frac{1}{Q(z)}\\geq 2(m+t)\\right\]\\leq\\frac{\\mathbb{E}\[-\\log Q(z)\]}{2(m+t)}\\leq\\frac{1}{2}. |  | (24) |\
\
Taking the complement gives:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | Prz∼P⁡\[log⁡1Q​(z)≤2​(m+t)\]=Prz∼P⁡\[Q​(z)≥2−2​(m+t)\]=P​(AQ,t)≥12.\\displaystyle\\Pr\_{z\\sim P}\\left\[\\log\\frac{1}{Q(z)}\\leq 2(m+t)\\right\]=\\Pr\_{z\\sim P}\\left\[Q(z)\\geq 2^{-2(m+t)}\\right\]=P(A\_{Q,t})\\geq\\frac{1}{2}. |  | (25) |\
\
###### Lemma 23\
\
Let UnU\_{n} be the uniform distribution over {0,1}n\\{0,1\\}^{n}, the weights of AQ,tA\_{Q,t} under UnU\_{n} is Un​(AQ,t)≤2−(n−2​(m+t))U\_{n}(A\_{Q,t})\\leq 2^{-(n-2(m+t))}\
\
Proof\
For z∼Unz\\sim U\_{n}, we have 𝔼z∼Un​\[Q​(z)\]=∑z2−n​Q​(z)=2−n\\mathbb{E}\_{z\\sim U\_{n}}\[Q(z)\]=\\sum\_{z}2^{-n}Q(z)=2^{-n}. Applying Markov’ inequaltiy:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | Prz∼Un⁡\[Q​(z)≥2−2​(m+t)\]≤𝔼z∼Un​\[Q​(z)\]2−2​(m+t)≤2−n+2​(m+t)=2−(n−2​(m+t)).\\displaystyle\\Pr\_{z\\sim U\_{n}}\\left\[Q(z)\\geq 2^{-2(m+t)}\\right\]\\leq\\frac{\\mathbb{E}\_{z\\sim U\_{n}}\[Q(z)\]}{2^{-2(m+t)}}\\leq 2^{-n+2(m+t)}=2^{-(n-2(m+t))}. |  | (26) |\
\
###### Theorem 24\
\
If there exists a PRF family FK:{0,1}m→{0,1}kF\_{K}:\\{0,1\\}^{m}\\rightarrow\\{0,1\\}^{k} that is indexed by K∈{0,1}mK\\in\\{0,1\\}^{m} and secure against a non-uniform PPT distinguisher DmD\_{m} allowing for an advantage of at most ε​(m)\\varepsilon(m), there exists n0n\_{0} such that for all n=m+k≥n0n=m+k\\geq n\_{0}, there exists a sequence of random variables {Xk}k=1n\\{X\_{k}\\}\_{k=1}^{n} over {0,1}n\\{0,1\\}^{n} such that SPoly​(Xn)=Ω​(log⁡n)\\mathrm{S}\_{\\mathrm{Poly}}(X\_{n})=\\Omega(\\log n).\
\
Proof\
We will prove the existence of such PP via a counting argument. First, we define the family of distributions of interest. Concretely, we draw a sample PKP\_{K} as follows:\
\
1. 1.\
\
\
Sample x∼Umx\\sim U\_{m}\
\
2. 2.\
\
\
Output z=(x,FK​(x))∈{0,1}nz=(x,F\_{K}(x))\\in\\{0,1\\}^{n}\
\
\
Since FKF\_{K} is a deterministic function, H​(PK)=m\\mathrm{H}(P\_{K})=m.\
\
We also defined a _keyed model_ QK\\mathrm{Q}\_{K} that models PKP\_{K} by directly storing the key KK and the program for generating PRF from KK inside its program:\
\
|     |     |     |\
| --- | --- | --- |\
|  | QK​(x,y)=2−m​𝟙​{y=FK​(x)}.Q\_{K}(x,y)=2^{-m}\\mathbbm{1}\\{y=F\_{K}(x)\\}. |  |\
\
This model matches the density of PKP\_{K} so KL​(PK∥QK)=0\\mathrm{KL}(P\_{K}\\\|Q\_{K})=0, and:\
\
|     |     |     |\
| --- | --- | --- |\
|  | L​(QK,PK)=\|QK\|+H​(PK)≤m+c1+m=2​m+c1.L(Q\_{K},P\_{K})=\|\\mathrm{Q}\_{K}\|+\\mathrm{H}(P\_{K})\\leq m+c\_{1}+m=2m+c\_{1}. |  |\
\
c1c\_{1} is the constant overhead to implement the PRF evaluation and sampling wrapper under a fixed encoding (i.e., a UTM).\
\
##### Constructing distinguisher from QQ.\
\
Given a model QQ and its heavy set AQ,tA\_{Q,t} (Definition [21](https://arxiv.org/html/2601.03220v2#Thmtheorem21 "Definition 21 (Heavy set) ‣ Cryptographic assumptions. ‣ A.4 Existence of High Epiplexity random variables ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), we can turn QQ into a _single-query_ distinguisher DOD^{O}:\
\
1. 1.\
\
\
Sample x∼Umx\\sim U\_{m} and query the oracle y=O​(x)y=O(x) and set z=(x,y)z=(x,y).\
\
2. 2.\
\
\
Output 11 if z∈AQ,tz\\in A\_{Q,t} i.e., Q​(z)≥2−2​(m+t)Q(z)\\geq 2^{-2(m+t)} else 0.\
\
\
If OO is a truly random function RR, then (x,R​(x))(x,R(x)) follows UnU\_{n} and by Lemma [23](https://arxiv.org/html/2601.03220v2#Thmtheorem23 "Lemma 23 ‣ Cryptographic assumptions. ‣ A.4 Existence of High Epiplexity random variables ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"):\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | Pr⁡\[DR=1\]=Prz∼Un⁡\[z∈AQ,t\]≤2−(n−2​(m+t))\\displaystyle\\Pr\[D^{R}=1\]=\\Pr\_{z\\sim U\_{n}}\\left\[z\\in A\_{Q,t}\\right\]\\leq 2^{-(n-2(m+t))} |  | (27) |\
\
If OO is the PRF FKF\_{K} for a KK that satisfies KL​(PK∥Q)≤t\\mathrm{KL}(P\_{K}\\\|Q)\\leq t, Lemma [22](https://arxiv.org/html/2601.03220v2#Thmtheorem22 "Lemma 22 ‣ Cryptographic assumptions. ‣ A.4 Existence of High Epiplexity random variables ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") gives:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | Pr\[DFK=1∣KL(PK∥Q)≤t\]≥12.\\displaystyle\\Pr\\left\[D^{F\_{K}}=1\\mid\\mathrm{KL}(P\_{K}\\\|Q)\\leq t\\right\]\\geq\\frac{1}{2}. |  | (28) |\
\
Let pQ,t=PrK⁡\[KL​(PK∥Q)≤t\]p\_{Q,t}=\\Pr\_{K}\[\\mathrm{KL}(P\_{K}\\\|Q)\\leq t\]. We can average over all possible KK and obtain the following bound:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | Pr\[DFK=1\]≥PrK\[KL(PK∥Q)≤t\]Pr\[DFK=1∣KL(PK∥Q)≤t\]≥12pQ,t.\\displaystyle\\Pr\\left\[D^{F\_{K}}=1\\right\]\\geq\\Pr\_{K}\[\\mathrm{KL}(P\_{K}\\\|Q)\\leq t\]\\Pr\\left\[D^{F\_{K}}=1\\mid\\mathrm{KL}(P\_{K}\\\|Q)\\leq t\\right\]\\geq\\frac{1}{2}p\_{Q,t}. |  | (29) |\
\
Therefore, the distinguishing advantage of DOD^{O} is:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | 𝖠𝖽𝗏​(DO)=Pr⁡\[DFK=1\]−Pr⁡\[DR=1\]≥12​pQ,t−2−(n−2​(m+t)).\\displaystyle\\mathsf{Adv}(D^{O})=\\Pr\\left\[D^{F\_{K}}=1\\right\]-\\Pr\[D^{R}=1\]\\geq\\frac{1}{2}p\_{Q,t}-2^{-(n-2(m+t))}. |  | (30) |\
\
Rearranging:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | pQ,t≤2​𝖠𝖽𝗏​(DO)+2⋅2−(n−2​(m+t)).\\displaystyle p\_{Q,t}\\leq 2\\mathsf{Adv}(D^{O})+2\\cdot 2^{-(n-2(m+t))}. |  | (31) |\
\
Since FKF\_{K} is a PRF and DOD\_{O} is a PPT distinguisher, the advantage is upperbounded by ε​(m)\\varepsilon(m):\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | pQ,t≤2​ε​(m)+2⋅2−(n−2​(m+t)).\\displaystyle p\_{Q,t}\\leq 2\\varepsilon(m)+2\\cdot 2^{-(n-2(m+t))}. |  | (32) |\
\
##### Union bound over short models.\
\
Given a maximum program length ss, there are at most 2s+12^{s+1} candidate programs Q\\mathrm{Q} with \|Q\|≤s\|\\mathrm{Q}\|\\leq s. Applying union bound on all such QQ’s:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | PrK⁡\[∃Q:\|Q\|≤s∧KL​(PK∥Q)≤t\]≤2s+1​pQ,t≤2s+1​(2​ε​(m)+2⋅2−(n−2​(m+t))).\\displaystyle\\Pr\_{K}\\left\[\\exists\\mathrm{Q}:\|\\mathrm{Q}\|\\leq s\\,\\wedge\\,\\mathrm{KL}(P\_{K}\\\|Q)\\leq t\\right\]\\leq 2^{s+1}p\_{Q,t}\\leq 2^{s+1}\\left(2\\varepsilon(m)+2\\cdot 2^{-(n-2(m+t))}\\right). |  | (33) |\
\
Now, it suffices to choose parameters such that the RHS of equation [33](https://arxiv.org/html/2601.03220v2#A1.E33 "Equation 33 ‣ Union bound over short models. ‣ A.4 Existence of High Epiplexity random variables ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") is smaller than 11, which implies there exists a hard key K⋆K^{\\star} such that:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | KL​(PK⋆∥Q)>t,∀Q​satisfying​\|Q\|≤s.\\displaystyle\\mathrm{KL}(P\_{K^{\\star}}\\\|Q)>t,\\,\\,\\forall\\mathrm{Q}\\,\\,\\text{satisfying}\\,\\,\|\\mathrm{Q}\|\\leq s. |  | (34) |\
\
##### MDL lower bound from K⋆K^{\\star}.\
\
For K⋆K^{\\star}, every \|Q\|≤s\|\\mathrm{Q}\|\\leq s satisfies:\
\
|     |     |     |\
| --- | --- | --- |\
|  | L​(Q,PK⋆)=\|Q\|+H​(P⋆)+KL​(PK⋆∥Q)≥H​(P⋆)+KL​(PK⋆∥Q)≥m+t.L(Q,P\_{K^{\\star}})=\|\\mathrm{Q}\|+\\mathrm{H}(P^{\\star})+\\mathrm{KL}(P\_{K^{\\star}}\\\|Q)\\geq\\mathrm{H}(P^{\\star})+\\mathrm{KL}(P\_{K^{\\star}}\\\|Q)\\geq m+t. |  |\
\
Meanwhile, the keyed model QK⋆Q\_{K^{\\star}} satisfies: L​(QK⋆,PK⋆)≤2​m+c1.L(Q\_{K^{\\star}},P\_{K^{\\star}})\\leq 2m+c\_{1}.\
If we set:\
\
|     |     |     |\
| --- | --- | --- |\
|  | t=m+c1+Δ,t=m+c\_{1}+\\Delta, |  |\
\
we get a margin of Δ\\Delta:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | L​(Q,PK⋆)≥m+m+c1+Δ>2​m+c1≥L​(QK⋆,PK⋆).\\displaystyle L(Q,P\_{K^{\\star}})\\geq m+m+c\_{1}+\\Delta>2m+c\_{1}\\geq L(Q\_{K^{\\star}},P\_{K^{\\star}}). |  | (35) |\
\
This implies that there exists at least one model that achieves a lower description length than any Q\\mathrm{Q} with \|Q\|≤s\|\\mathrm{Q}\|\\leq s and the MDL minimizer must have \|Q⋆\|>s\|\\mathrm{Q}^{\\star}\|>s.\
\
##### Choosing parameters.\
\
Set:\
\
- •\
\
\
s=log⁡ms=\\log m\
\
- •\
\
\
Δ=log⁡m\\Delta=\\log m\
\
- •\
\
\
t=m+c1+Δ=m+c1+log⁡mt=m+c\_{1}+\\Delta=m+c\_{1}+\\log m\
\
- •\
\
\
k=4​m+4​Δ+2​c1k=4m+4\\Delta+2c\_{1}\
\
\
We now plug these values into [Equation 33](https://arxiv.org/html/2601.03220v2#A1.E33 "Equation 33 ‣ Union bound over short models. ‣ A.4 Existence of High Epiplexity random variables ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). First, 2s+1=poly​(m)2^{s+1}=\\mathrm{poly}(m) and limm→∞2s+1⋅2​ε​(m)=0\\lim\_{m\\rightarrow\\infty}2^{s+1}\\cdot 2\\varepsilon(m)=0. For the second term:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  |  | 2s+1⋅2⋅2−(n−2​(m+t))\\displaystyle 2^{s+1}\\cdot 2\\cdot 2^{-(n-2(m+t))} |  |\
|  | =\\displaystyle= | 2log⁡m+1⋅2⋅2−(m+4​m+4​Δ+2​c1−2​(m+m+c1+log⁡m))\\displaystyle 2^{\\log m+1}\\cdot 2\\cdot 2^{-(m+4m+4\\Delta+2c\_{1}-2(m+m+c\_{1}+\\log m))} |  |\
|  | =\\displaystyle= | 2log⁡m+2⋅2−(5​m+4​log⁡m+2​c1−2​(2​m+c1+log⁡m))\\displaystyle 2^{\\log m+2}\\cdot 2^{-(5m+4\\log m+2c\_{1}-2(2m+c\_{1}+\\log m))} |  |\
|  | =\\displaystyle= | 2log⁡m+2⋅2−(m+2​log⁡m)\\displaystyle 2^{\\log m+2}\\cdot 2^{-(m+2\\log m)} |  |\
|  | =\\displaystyle= | 2−m−log⁡m+2.\\displaystyle 2^{-m-\\log m+2}. |  |\
\
This term also approaches 0 as mm increases. So for sufficiently large mm the RHS of [Equation 33](https://arxiv.org/html/2601.03220v2#A1.E33 "Equation 33 ‣ Union bound over short models. ‣ A.4 Existence of High Epiplexity random variables ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") is less than 11 as desired.\
\
### A.5 Information Content is not Independent of Factorization\
\
###### Theorem 25 (OWP induces entropy asymmetry)\
\
Let f:{0,1}n→{0,1}nf:\\{0,1\\}^{n}\\to\\{0,1\\}^{n} be a polynomial-time computable one-way permutation secure\
against non-uniform PPT inverters with negligible success probability. Let\
X=UnX=U\_{n} and Y=f​(X)Y=f(X).\
Let Hpoly​(⋅)\\mathrm{H}\_{\\mathrm{poly}}(\\cdot) and Hpoly(⋅∣⋅)\\mathrm{H}\_{\\mathrm{poly}}(\\cdot\\mid\\cdot) be defined as in\
Definition [8](https://arxiv.org/html/2601.03220v2#Thmtheorem8 "Definition 8 (Epiplexity and Time-Bounded Entropy) ‣ 3 Epiplexity: Structural Information Extractable by a Computationally Bounded Observer ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). Then for every constant c>0c>0 there exists NN such that\
for all n≥Nn\\geq N,\
\
|     |     |     |\
| --- | --- | --- |\
|  | Hpoly​(X∣Y)+Hpoly​(Y)>Hpoly​(Y∣X)+Hpoly​(X)+c​log⁡n.\\mathrm{H}\_{\\mathrm{poly}}(X\\mid Y)+\\mathrm{H}\_{\\mathrm{poly}}(Y)>\\mathrm{H}\_{\\mathrm{poly}}(Y\\mid X)+\\mathrm{H}\_{\\mathrm{poly}}(X)+c\\log n. |  |\
\
Proof\
We prove bounds on each term.\
\
##### Unconditional terms Hpoly​(X)\\mathrm{H}\_{\\mathrm{poly}}(X) and Hpoly​(Y)\\mathrm{H}\_{\\mathrm{poly}}(Y).\
\
Since X=UnX=U\_{n} and ff is a permutation, Y=f​(X)Y=f(X) is also uniform on {0,1}n\\{0,1\\}^{n}.\
By Lemma [15](https://arxiv.org/html/2601.03220v2#Thmtheorem15 "Lemma 15 (Maximum expected description length) ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") (time-bounded entropy of the uniform distribution),\
there is a constant c0c\_{0} such that\
\
|     |     |     |\
| --- | --- | --- |\
|  | n≤Hpoly​(X)≤n+c0,n≤Hpoly​(Y)≤n+c0.n\\leq\\mathrm{H}\_{\\mathrm{poly}}(X)\\leq n+c\_{0},\\qquad n\\leq\\mathrm{H}\_{\\mathrm{poly}}(Y)\\leq n+c\_{0}. |  |\
\
In particular, −c0≤Hpoly​(Y)−Hpoly​(X)≤c0-c\_{0}\\leq\\mathrm{H}\_{\\mathrm{poly}}(Y)-\\mathrm{H}\_{\\mathrm{poly}}(X)\\leq c\_{0}, so Hpoly​(Y)−Hpoly​(X)=O​(1)\\mathrm{H}\_{\\mathrm{poly}}(Y)-\\mathrm{H}\_{\\mathrm{poly}}(X)=O(1).\
\
##### Forward conditional term Hpoly​(Y∣X)\\mathrm{H}\_{\\mathrm{poly}}(Y\\mid X).\
\
There is a deterministic conditional sampler that on input xx outputs f​(x)f(x).\
For this sampler, P​(Y∣X)=1P(Y\\mid X)=1, hence log⁡(1/P​(Y∣X))=0\\log(1/P(Y\\mid X))=0.\
Since Hpoly​(Y∣X)\\mathrm{H}\_{\\mathrm{poly}}(Y\\mid X) is the expected log-loss of the MDL-optimal conditional sampler,\
we obtain\
\
|     |     |     |\
| --- | --- | --- |\
|  | Hpoly​(Y∣X)=O​(1).\\mathrm{H}\_{\\mathrm{poly}}(Y\\mid X)=O(1). |  |\
\
##### Hard conditional term Hpoly​(X∣Y)\\mathrm{H}\_{\\mathrm{poly}}(X\\mid Y).\
\
Let P⋆:=PX∣Y⋆P^{\\star}:=P^{\\star}\_{X\\mid Y} be the MDL-optimal conditional probabilistic model for X∣YX\\mid Y\
over the class of non-uniform PPT model, and define\
\
|     |     |     |\
| --- | --- | --- |\
|  | ϕ​(y):=Pru∼U∞⁡\[SamplePX∣y⋆​(u)=f−1​(y)\].\\phi(y)\\;:=\\;\\Pr\_{u\\sim U\_{\\infty}}\\left\[\\mathrm{Sample}\_{P^{\\star}\_{X\\mid y}}(u)=f^{-1}(y)\\right\]. |  |\
\
Because Y=f​(X)Y=f(X) and ff is a permutation, we have X=f−1​(Y)X=f^{-1}(Y), and thus\
\
|     |     |     |\
| --- | --- | --- |\
|  | P⋆​(X∣Y)=P⋆​(f−1​(Y)∣Y)=ϕ​(Y)a.s.P^{\\star}(X\\mid Y)=P^{\\star}(f^{-1}(Y)\\mid Y)=\\phi(Y)\\qquad\\text{a.s.} |  |\
\
Therefore\
\
|     |     |     |\
| --- | --- | --- |\
|  | Hpoly​(X∣Y)=𝔼​\[log⁡1P⋆​(X∣Y)\]=𝔼​\[log⁡1ϕ​(Y)\].\\mathrm{H}\_{\\mathrm{poly}}(X\\mid Y)=\\mathbb{E}\\Big\[\\log\\frac{1}{P^{\\star}(X\\mid Y)}\\Big\]=\\mathbb{E}\\Big\[\\log\\frac{1}{\\phi(Y)}\\Big\]. |  |\
\
By Jensen’s inequality for the convex function log⁡(1/t)\\log(1/t),\
\
|     |     |     |\
| --- | --- | --- |\
|  | 𝔼​\[log⁡1ϕ​(Y)\]≥log⁡1𝔼​\[ϕ​(Y)\].\\mathbb{E}\\Big\[\\log\\frac{1}{\\phi(Y)}\\Big\]\\;\\geq\\;\\log\\frac{1}{\\mathbb{E}\[\\phi(Y)\]}. |  |\
\
Now consider the inverter ℐ\\mathcal{I} that on input yy runs the sampler P⋆​(X∣Y)P^{\\star}(X\\mid Y)\
once and outputs the resulting xx. Since P⋆P^{\\star} is a non-uniform PPT sampler, ℐ\\mathcal{I}\
is a non-uniform PPT inverter. Moreover, its inversion success probability is exactly\
\
|     |     |     |\
| --- | --- | --- |\
|  | Pr⁡\[ℐ​(Y)=f−1​(Y)\]=𝔼​\[ϕ​(Y)\].\\Pr\[\\mathcal{I}(Y)=f^{-1}(Y)\]=\\mathbb{E}\[\\phi(Y)\]. |  |\
\
Equivalently (since Y=f​(X)Y=f(X)),\
\
|     |     |     |\
| --- | --- | --- |\
|  | PrX∼Un⁡\[ℐ​(f​(X))=X\]=𝔼​\[ϕ​(Y)\].\\Pr\_{X\\sim U\_{n}}\\big\[\\mathcal{I}(f(X))=X\\big\]=\\mathbb{E}\[\\phi(Y)\]. |  |\
\
By one-wayness, this success probability is negligible. In particular, for every constant\
c>0c>0 there exists NN such that for all n≥Nn\\geq N,\
\
|     |     |     |\
| --- | --- | --- |\
|  | 𝔼​\[ϕ​(Y)\]≤n−c.\\mathbb{E}\[\\phi(Y)\]\\leq n^{-c}. |  |\
\
Plugging into the Jensen bound yields, for all n≥Nn\\geq N,\
\
|     |     |     |\
| --- | --- | --- |\
|  | Hpoly​(X∣Y)≥log⁡1𝔼​\[ϕ​(Y)\]≥c​log⁡n.\\mathrm{H}\_{\\mathrm{poly}}(X\\mid Y)\\;\\geq\\;\\log\\frac{1}{\\mathbb{E}\[\\phi(Y)\]}\\;\\geq\\;c\\log n. |  |\
\
##### Combine.\
\
For n≥Nn\\geq N, we have\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | Hpoly​(X∣Y)+Hpoly​(Y)\\displaystyle\\mathrm{H}\_{\\mathrm{poly}}(X\\mid Y)+\\mathrm{H}\_{\\mathrm{poly}}(Y) | ≥c​log⁡n+Hpoly​(Y)\\displaystyle\\geq c\\log n+\\mathrm{H}\_{\\mathrm{poly}}(Y) |  | (36) |\
|  |  | ≥c​log⁡n+Hpoly​(X)−O​(1)\\displaystyle\\geq c\\log n+\\mathrm{H}\_{\\mathrm{poly}}(X)-O(1) |  | (37) |\
|  |  | =Hpoly​(Y∣X)+Hpoly​(X)+c​log⁡n−O​(1),\\displaystyle=\\mathrm{H}\_{\\mathrm{poly}}(Y\\mid X)+\\mathrm{H}\_{\\mathrm{poly}}(X)+c\\log n-O(1), |  | (38) |\
\
where we used Hpoly​(Y∣X)=O​(1)\\mathrm{H}\_{\\mathrm{poly}}(Y\\mid X)=O(1) and Hpoly​(Y)−Hpoly​(X)≥−c0\\mathrm{H}\_{\\mathrm{poly}}(Y)-\\mathrm{H}\_{\\mathrm{poly}}(X)\\geq-c\_{0}.\
\
\
###### Corollary 26\
\
Let ff be a one-way permutation and lef X=Unif​({0,1}n),Y=f​(X)X=\\mathrm{Unif}(\\{0,1\\}^{n}),Y=f(X). Define 𝒫\\mathcal{P} as a family of probabilistic generative model that allows for multiple factorizations of the data, ie P∈𝒫P\\in\\mathcal{P} it can make predictions P1→2​(X,Y)=P1​(X)​P2​(Y;X)P\_{1\\to 2}(X,Y)=P\_{1}(X)P\_{2}(Y;X) and P2→1​(X,Y)=P2​(Y)​P1​(X;Y)P\_{2\\to 1}(X,Y)=P\_{2}(Y)P\_{1}(X;Y) for the functions P1​(⋅),P1​(⋅;⋅)P\_{1}(\\cdot),P\_{1}(\\cdot\ ;\\cdot),P2​(⋅),P2​(⋅;⋅)P\_{2}(\\cdot),P\_{2}(\\cdot\ ;\\cdot) that are normalized probability distributions over the first variable.\
\
Suppose that PP fits the forward direction of ff (and the input uniform distributions)\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | 𝔼​\[−log⁡P1​(X)\]\\displaystyle\\mathbb{E}\[-\\log P\_{1}(X)\] | ≤n+ε\\displaystyle\\leq n+\\varepsilon |  |\
|  | 𝔼​\[−log⁡P2​(f​(X)∣X)\]\\displaystyle\\mathbb{E}\[-\\log P\_{2}(f(X)\\mid X)\] | ≤ε\\displaystyle\\leq\\varepsilon |  |\
\
then it must violate Bayes theorem P1→2=P2→1P\_{1\\to 2}=P\_{2\\to 1} by a margin growing with nn.\
\
Specifically, for any value of cc there exists NN such that for all n>Nn>N, there exists at least one x∈{0,1}nx\\in\\{0,1\\}^{n} such that\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | P1​(x)​P2​(f​(x);x)>nc​2−2​ε​P2​(f​(x))​P1​(x;f​(x))P\_{1}(x)P\_{2}(f(x);x)>n^{c}2^{-2\\varepsilon}P\_{2}(f(x))P\_{1}(x;f(x)) |  | (39) |\
\
Proof\
From [Theorem 25](https://arxiv.org/html/2601.03220v2#Thmtheorem25 "Theorem 25 (OWP induces entropy asymmetry) ‣ A.5 Information Content is not Independent of Factorization ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") which applies also for each PP, we have\
\
|     |     |     |\
| --- | --- | --- |\
|  | 𝔼​\[−log⁡P2​(X;Y)\]>c​log⁡n.\\mathbb{E}\\left\[-\\log P\_{2}(X;Y)\\right\]>c\\log n. |  |\
\
The minimim value of 𝔼​\[−log⁡P2​(f​(X))\]\\mathbb{E}\\left\[-\\log P\_{2}(f(X))\\right\] is nn since ff is a bijection. Assembling these components,\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | 𝔼​\[log⁡P1​(X)​P2​(f​(X);X)P2​(f​(X))​P1​(X;f​(X))\]>c​log⁡n−2​ε.\\mathbb{E}\\left\[\\log\\frac{P\_{1}(X)P\_{2}(f(X);X)}{P\_{2}(f(X))P\_{1}(X;f(X))}\\right\]>c\\log n-2\\varepsilon. |  | (40) |\
\
Since the inequality holds in expectation, it also must hold for at least one value of XX. Exponentiating provides the final result.\
\
\
### A.6 Problems with time-bounded sophistication\
\
Epiplexity can be seen as a time-bounded and distributional generalization of sophistication. A natural question is whether we can directly define a time-bounded version of sophistication for individual strings.\
We show below that a naive time-bounded generalization degenerates: it makes the “model” part essentially constant for _every_ string.\
\
##### Preliminaries.\
\
Fix a reference universal (prefix-free or plain) Turing machine UU.\
For a program pp and auxiliary input dd, we write U​(p,d)U(p,d) for the output of running pp on input dd.\
The length of a binary string pp is denoted \|p\|\|p\|.\
A program pp is _total_ if U​(p,d)U(p,d) halts for every input dd (i.e., pp computes a total function).\
\
We write K​(x)K(x) for Kolmogorov complexity (plain or prefix; the choice only changes values by O​(1)O(1)).\
For a time bound t​(⋅)t(\\cdot), the time-bounded Kolmogorov complexity is\
\
|     |     |     |\
| --- | --- | --- |\
|  | Kt​(x):=min⁡{\|q\|:U​(q)​ outputs ​x​ within ​t​(\|x\|)​ steps}.K^{t}(x)\\;:=\\;\\min\\bigl\\{\\,\|q\|\\;:\\;U(q)\\text{ outputs }x\\text{ within }t(\|x\|)\\text{ steps}\\,\\bigr\\}. |  |\
\
(Any standard time-constructible tt suffices for the discussion.)\
\
We adopt the definition of sophistication from Koppel ( [1988](https://arxiv.org/html/2601.03220v2#bib.bib56 "")) and Antunes et al. ( [2005](https://arxiv.org/html/2601.03220v2#bib.bib7 "")), phrased for finite strings as in later expositions.\
For a significance level c≥0c\\geq 0, the sophistication of xx is\
\
###### Definition 27 (Sophistication at significance cc)\
\
|     |     |     |\
| --- | --- | --- |\
|  | sophc​(x):=minp⁡{\|p\|:p​ is total and ​∃d​ such that ​U​(p,d)=x​ and ​\|p\|+\|d\|≤K​(x)+c}.\\mathrm{soph}\_{c}(x)\\;:=\\;\\min\_{p}\\Bigl\\{\\,\|p\|\\;:\\;p\\text{ is total and }\\exists d\\text{ such that }U(p,d)=x\\text{ and }\|p\|+\|d\|\\leq K(x)+c\\Bigr\\}. |  |\
\
Intuitively, (p,d)(p,d) is a near-optimal two-part description of xx.\
The requirement that pp be _total_ is crucial: it prevents taking pp to be a tiny universal interpreter and pushing all information into dd (since a universal interpreter is not total).\
One of the most intuitive attempts at “time-bounded sophistication” is to simply replace K​(x)K(x) by the time-bounded complexity Kt​(x)K^{t}(x) in Definition [27](https://arxiv.org/html/2601.03220v2#Thmtheorem27 "Definition 27 (Sophistication at significance 𝑐) ‣ Preliminaries. ‣ A.6 Problems with time-bounded sophistication ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
###### Definition 28 (Naive time-bounded sophistication)\
\
Fix a time bound t​(⋅)t(\\cdot) and significance level c≥0c\\geq 0. Define\
\
|     |     |     |\
| --- | --- | --- |\
|  | sophct​(x):=minp⁡{\|p\|:p​ is total and ​∃d​ such that ​U​(p,d)=x​ and ​\|p\|+\|d\|≤Kt​(x)+c}.\\mathrm{soph}^{t}\_{c}(x)\\;:=\\;\\min\_{p}\\Bigl\\{\\,\|p\|\\;:\\;p\\text{ is total and }\\exists d\\text{ such that }U(p,d)=x\\text{ and }\|p\|+\|d\|\\leq K^{t}(x)+c\\Bigr\\}. |  |\
\
The definition above _collapses_, essentially because time bounds make it easy to “totalize” a universal interpreter by adding a timeout.\
\
###### Lemma 29 (Naive time-bounded sophistication is O​(1)O(1))\
\
For every time bound t​(⋅)t(\\cdot) and every c≥0c\\geq 0, there exists a constant CtC\_{t} (depending only on tt and the choice of UU) such that for every string xx,\
\
|     |     |     |\
| --- | --- | --- |\
|  | sophct​(x)≤Ct.\\mathrm{soph}^{t}\_{c}(x)\\leq C\_{t}. |  |\
\
In particular, sophct​(x)\\mathrm{soph}^{t}\_{c}(x) does not meaningfully distinguish structured strings from random-looking strings.\
\
Proof \[sketch\]\
Fix tt.\
Let ptlp\_{\\mathrm{tl}} be a constant-size program that, on input dd, simulates U​(d)U(d) for at most t​(\|x\|)t(\|x\|) steps (or more generally for the same time budget used in the definition of Kt​(x)K^{t}(x)), and:\
(i) if the simulation halts within the budget, output the same result; otherwise\
(ii) output a fixed default string (say 0).\
By construction, ptlp\_{\\mathrm{tl}} is _total_ (it always halts, because it enforces a timeout).\
\
Now let d⋆d^{\\star} be a shortest program witnessing Kt​(x)K^{t}(x), i.e., \|d⋆\|=Kt​(x)\|d^{\\star}\|=K^{t}(x) and U​(d⋆)U(d^{\\star}) outputs xx within the allowed time.\
Then U​(ptl,d⋆)=xU(p\_{\\mathrm{tl}},d^{\\star})=x.\
Moreover,\
\
|     |     |     |\
| --- | --- | --- |\
|  | \|ptl\|+\|d⋆\|=\|ptl\|+Kt​(x)≤Kt​(x)+cfor all ​c≥\|ptl\|.\|p\_{\\mathrm{tl}}\|+\|d^{\\star}\|=\|p\_{\\mathrm{tl}}\|+K^{t}(x)\\leq K^{t}(x)+c\\quad\\text{for all }c\\geq\|p\_{\\mathrm{tl}}\|. |  |\
\
Thus ptlp\_{\\mathrm{tl}} is feasible in Definition [28](https://arxiv.org/html/2601.03220v2#Thmtheorem28 "Definition 28 (Naive time-bounded sophistication) ‣ Preliminaries. ‣ A.6 Problems with time-bounded sophistication ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), giving\
sophct​(x)≤\|ptl\|=Ct\\mathrm{soph}^{t}\_{c}(x)\\leq\|p\_{\\mathrm{tl}}\|=C\_{t} for all xx.\
\
\
In the original (unbounded-time) Definition [27](https://arxiv.org/html/2601.03220v2#Thmtheorem27 "Definition 27 (Sophistication at significance 𝑐) ‣ Preliminaries. ‣ A.6 Problems with time-bounded sophistication ‣ Appendix A Proofs ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), totality prevents a universal interpreter from being used as the “model” part, because such an interpreter cannot halt on inputs that encode non-halting computations.\
However, once we commit to a time bound in the _optimality criterion_ (i.e., we compare against Kt​(x)K^{t}(x)), the data part dd can be chosen to be a short program that is _guaranteed to halt quickly_.\
A constant-size _clocked interpreter_ ptlp\_{\\mathrm{tl}} is then total and suffices for every xx, pushing all of the description length into dd.\
This is precisely the sense in which the naive time-bounded generalization becomes degenerate.\
\
## Appendix B Measuring Epiplexity\
\
### B.1 Further details on estimating epiplexity\
\
Here we provide further details on measuring epiplexity.\
\
##### Evaluating code lengths and time bounds.\
\
As described in [Section˜4](https://arxiv.org/html/2601.03220v2#S4 "4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), evaluating the code length for the model boils down to tracking the training losses (prequential) or teacher-student KL (requential) at each step i:i:\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | \|Ppreq\|\\displaystyle\|\\mathrm{P}\_{\\mathrm{preq}}\| | ≈∑i=0M−1(log⁡1/Pi​(Zi)−log⁡1/PM​(Zi)),\\displaystyle\\,\\approx\\sum\_{i=0}^{M-1}\\quantity(\\log 1/P\_{i}(Z\_{i})-\\log 1/P\_{M}(Z\_{i})), |  | (41) |\
|  | \|Preq\|\\displaystyle\|\\mathrm{P}\_{\\mathrm{req}}\| | ≈∑i=0M−1KL​(Pit∥Pis).\\displaystyle\\,\\approx\\sum\_{i=0}^{M-1}\\mathrm{KL}(P^{\\mathrm{t}}\_{i}\\\|P^{\\mathrm{s}}\_{i}). |  | (42) |\
\
For prequential coding, we need to compute the loss of the final model summed over the entire training dataset, ∑i=0M−1log⁡1/PM​(Zi)\\sum\_{i=0}^{M-1}\\log 1/P\_{M}(Z\_{i}), which is time-consuming if done exactly. Since all of our experiments are in the one-epoch training regime without data repeat and training data ZiZ\_{i} are drawn i.i.d. (except for the ADO experiment [Section˜6.4](https://arxiv.org/html/2601.03220v2#S6.SS4 "6.4 Pre-Training Data Selection and Curriculum for Language Models ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), we make the assumption that the generalization gap is small and estimate ∑i=0M−1log⁡1/PM​(Zi)\\sum\_{i=0}^{M-1}\\log 1/P\_{M}(Z\_{i}) as M​log⁡1/PM​(ZM),M\\log 1/P\_{M}(Z\_{M}), where the latter is a rescaled loss for PMP\_{M} on unseen data ZM.Z\_{M}. The i.i.d. assumption breaks down for the ADO experiment [Section˜6.4](https://arxiv.org/html/2601.03220v2#S6.SS4 "6.4 Pre-Training Data Selection and Curriculum for Language Models ‣ 6 Epiplexity, Pre-Training, and OOD Generalization ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), where we instead compute ∑i=0M−1log⁡1/PM​(Zi)\\sum\_{i=0}^{M-1}\\log 1/P\_{M}(Z\_{i}) exactly.\
\
For requential coding, we need to evaluate the teacher-student KL, KL​(Pt∥Ps),\\mathrm{KL}(P^{\\mathrm{t}}\\\|P^{\\mathrm{s}}), at each training step. The KL divergence over sequences decomposes as a sum over token positions and is estimated as:\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | KL​(Pt∥Ps)\\displaystyle\\mathrm{KL}(P^{\\mathrm{t}}\\\|P^{\\mathrm{s}}) | =∑j=1L𝔼Z<j∼Pt​\[∑Zj∈𝒱Pt​(Zj\|Z<j)​log⁡Pt​(Zj\|Z<j)Ps​(Zj\|Z<j)\]\\displaystyle=\\sum\_{j=1}^{L}\\mathbb{E}\_{Z\_{<j}\\sim P^{\\mathrm{t}}}\\left\[\\sum\_{Z\_{j}\\in\\mathcal{V}}P^{\\mathrm{t}}(Z\_{j}\|Z\_{<j})\\log\\frac{P^{\\mathrm{t}}(Z\_{j}\|Z\_{<j})}{P^{\\mathrm{s}}(Z\_{j}\|Z\_{<j})}\\right\] |  | (43) |\
|  |  | ≈∑j=1L∑Zj′∈𝒱Pt​(Zj′\|Z<j)​log⁡Pt​(Zj′\|Z<j)Ps​(Zj′\|Z<j),\\displaystyle\\approx\\sum\_{j=1}^{L}\\sum\_{Z^{\\prime}\_{j}\\in\\mathcal{V}}P^{\\mathrm{t}}(Z^{\\prime}\_{j}\|Z\_{<j})\\log\\frac{P^{\\mathrm{t}}(Z^{\\prime}\_{j}\|Z\_{<j})}{P^{\\mathrm{s}}(Z^{\\prime}\_{j}\|Z\_{<j})}, |  | (44) |\
\
where Z∼PtZ\\sim P^{\\mathrm{t}} is a sample from the teacher, LL is the sequence length, and 𝒱\\mathcal{V} is the vocabulary. We evaluate this estimator using the sample ZZ generated by the teacher to train the student, along with their next-token-prediction logits {Pt​(Zj\|Z<j),Ps​(Zj\|Z<j)}j\\{P^{\\mathrm{t}}(Z\_{j}\|Z\_{<j}),P^{\\mathrm{s}}(Z\_{j}\|Z\_{<j})\\}\_{j} recorded on the generated sequence\
\
Finally, to estimate the expected entropy code length for the test data 𝔼​\[log⁡1/P​(X)\]\\mathbb{E}\[\\log 1/P(X)\] under the trained model P,P, we use an appropriately scaled empirical entropy code length of a heldout test set X^.\\hat{X}. Let KK and K^\\hat{K} denote the number of examples in each dataset. Then:\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | 𝔼​\[log⁡1/P​(X)\]\\displaystyle\\mathbb{E}\[\\log 1/P(X)\] | =𝔼​\[log⁡1∏iP​(Xi)\]\\displaystyle=\\mathbb{E}\\quantity\[\\log\\frac{1}{\\prod\_{i}P(X\_{i})}\] |  | (45) |\
|  |  | =∑i𝔼​\[log⁡1/P​(Xi)\]\\displaystyle=\\sum\_{i}\\mathbb{E}\[\\log 1/P(X\_{i})\] |  | (46) |\
|  |  | =K​𝔼​\[log⁡1/P​(X1)\]\\displaystyle=K\\mathbb{E}\[\\log 1/P(X\_{1})\] |  | (47) |\
|  |  | ≈KK^​∑i=1K^log⁡1/P​(X^i)\\displaystyle\\approx\\frac{K}{\\hat{K}}\\sum\_{i=1}^{\\hat{K}}\\log 1/P(\\hat{X}\_{i}) |  | (48) |\
\
where we assumed the datasets XX and X^\\hat{X} consist of i.i.d. draws from the same distribution. This estimator is simply a scaled version of the standard empirical test loss, and it converges to the true expectation as K^\\hat{K} becomes large. To speedup evaluation, we typically choose K^≪K,\\hat{K}\\ll K, but this choice does not affect our time-bound calculation: for both prequential and requential coding, the total decoding time of the two-part code for the test dataset XX is estimated as 6​N​D+2​N​𝒟6ND+2N\\mathcal{D} where NN is the number of parameters of the (student) model, DD is the number of (student) training tokens, and 𝒟\\mathcal{D} is the number of tokens in the test dataset. When evaluating conditional epiplexity ST​(Y\|X),\\mathrm{S}\_{T}(Y\|X), decoding time takes into account both the input (XX) and label (YY) tokens, but code length only needs to be computed for the label tokens (tokens contributing to the training loss).\
\
##### Finding Hyperparameters for Compute-Optimal Two-Part Code.\
\
To identify models that lead to compute-optimal two-part code, we need to optimize several key hyperparameters, including model size (NN), training tokens (DD), width-depth ratio, learning rate, etc. Through our early experiments, we found two interventions that reduce the model code length under requential coding: (1) distilling from an exponential moving average (EMA) of teacher checkpoints rather than instantaneous checkpoints, which reduces noise in the distillation signal, and (2) imposing a maximum KL threshold between teacher and student—when exceeded, the teacher is frozen while the student catches up, preventing divergence that would otherwise inflate the code length. The EMA time scale and the maximum KL threshold are additional hyperparameters for requential coding.\
\
In each experiment, we first identify a good learning rate for a small model size and use the Maximum Update Parameterization (Yang et al., [2022](https://arxiv.org/html/2601.03220v2#bib.bib107 "")) and CompleteP (Dey et al., [2025](https://arxiv.org/html/2601.03220v2#bib.bib26 "")) to transfer the found learning rate to larger models. We also optimize the EMA time scale and maximum KL threshold for the small model when using requential coding. We then train models of various depths and widths to simultaneously sweep over model size and width-depth ratios, for a total number of training tokens chosen to be larger than the test dataset size 𝒟,\\mathcal{D}, motivated by the observation that the optimal training tokens typically grows with the model size but do not exceed 𝒟\\mathcal{D} (see [Section˜B.4](https://arxiv.org/html/2601.03220v2#A2.SS4 "B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). To avoid separately training a model for intermediate training token budgets, we record an EMA of the iterates (for requential coding, this is done for the student) under a constant learning rate schedule, rather than using a decaying learning rate schedule, following Hägele et al. ( [2024](https://arxiv.org/html/2601.03220v2#bib.bib46 "")). Each training run traces a curve in the \|P\|+𝔼​\[1/log⁡P​(X)\]\|\\mathrm{P}\|+\\mathbb{E}\[1/\\log P(X)\] vs TT plane as more training tokens are seen. The Pareto frontier of all such curves yields the optimal hyperparameters (N,D,N,D, width, depth, etc.) as a function of the compute budget.\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x19.png)Figure 10: Estimating the Pareto frontier from a finite number of training runs. While the exact Pareto frontier is smooth and the optimal model size and training tokens increase smoothly with compute, the empirical frontier is jagged and includes many spurious points due to selecting over only a finite number of hyperparameter combinations. Replacing the empirical Pareto frontier with the lower convex hull and retaining only the median point (ordered by compute) belong to a single training run with a fixed model size results in a much more accurate estimate of the true Pareto frontier. The example training curves are generated using the scaling laws in Hoffmann et al. ( [2022](https://arxiv.org/html/2601.03220v2#bib.bib49 "")) and prequential coding. The exact frontier is found via root finding for [Equation˜56](https://arxiv.org/html/2601.03220v2#A2.E56 "In Solution. ‣ B.3 A Solvable Model Using Scaling Laws ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
##### Estimating the Pareto Frontier.\
\
Due to computational constraints, we can only sweep over a limited set of hyperparameter combinations, which makes the empirical Pareto frontier noisy and jagged; we therefore use the lower convex hull of the resulting curves as a smoother approximation to the true Pareto frontier, a strategy often used in the compute-optimal scaling law literature (Henighan et al., [2020](https://arxiv.org/html/2601.03220v2#bib.bib48 ""); McLeish et al., [2025](https://arxiv.org/html/2601.03220v2#bib.bib66 "")) to overcome similar issues. After applying this strategy, we still often observe that multiple checkpoints from a single training run appear on the Pareto frontier. This is an artifact of finite hyperparameter sweeps: we expect both the optimal training tokens DD and model size NN to vary smoothly with compute budget, precluding multiple values of DD at the same NN from lying on the true Pareto frontier. These spurious points cause noisy, oscillatory trends in the estimated epiplexity, as shown in [Figure˜10](https://arxiv.org/html/2601.03220v2#A2.F10 "In Finding Hyperparameters for Compute-Optimal Two-Part Code. ‣ B.1 Further details on estimating epiplexity ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). As a simple workaround, we retain only the median point (ordered by compute) per training run (which has a fixed model size) on the lower convex hull.\
\
##### Sources of errors.\
\
In addition to the artifacts produced by finite (N,D)(N,D) combinations, our estimated epiplexity may differ from the true value for a few reasons: 1) potential systematic errors introduced by using the lower convex hull and taking the median point, 2) using a fixed architecture (e.g., the transformer) and learning algorithm (e.g., requential training with Adam) rather than considering all possible programs, and 3) suboptimality of other hyperparameters, such as the learning rate, Adam (β1,β2),(\\beta\_{1},\\beta\_{2}), etc. In most cases, we believe these sources of errors only contribute sub-leading corrections to the estimated epiplexity that do not impact the result qualitatively. For example, they are unlikely to alter the ordering between datasets if the estimated epiplexity gap is already significant or there is a clear trend along some axis of variation (e.g., number of hidden bits in the induction experiment in [Section˜5.3.1](https://arxiv.org/html/2601.03220v2#S5.SS3.SSS1 "5.3.1 Induction ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"))\
\
### B.2 Prequential Coding Approximates Requential Coding with a Static Teacher\
\
In this section, we show that the prequential coding estimate in [Equation˜8](https://arxiv.org/html/2601.03220v2#S4.E8 "In 4.1 Approximating Model Description Length with Prequential Coding ‣ 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") can be viewed as an approximation to requential coding with a static teacher, providing an alternative justification for its use beyond the symmetry of information argument.\
\
Consider requential coding with a fixed teacher across all time steps, i.e., Pit=PtP^{\\mathrm{t}}\_{i}=P^{\\mathrm{t}} for all i∈{0,…,M−1}i\\in\\{0,\\ldots,M-1\\}. The requential code length becomes\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|Preq\|≈∑i=0M−1KL​(Pt∥Pis)=∑i=0M−1𝔼Pt​\[log⁡1Pis​(X)−log⁡1Pt​(X)\].\|\\mathrm{P}\_{\\mathrm{req}}\|\\approx\\sum\_{i=0}^{M-1}\\mathrm{KL}(P^{\\mathrm{t}}\\\|P^{\\mathrm{s}}\_{i})=\\sum\_{i=0}^{M-1}\\mathbb{E}\_{P^{\\mathrm{t}}}\\left\[\\log\\frac{1}{P^{\\mathrm{s}}\_{i}(X)}-\\log\\frac{1}{P^{\\mathrm{t}}(X)}\\right\]. |  | (49) |\
\
Now suppose the static teacher closely matches the true data distribution, i.e., Pt≈PX1P^{\\mathrm{t}}\\approx P\_{X\_{1}}(we use PX1P\_{X\_{1}} in order to refer to the distribution of a single example, not the dataset). Under this assumption, we can make three simplifying approximations:\
\
1. 1.\
\
\
The expectation under the teacher can be replaced by the expectation under the data distribution: 𝔼Pt​\[⋅\]≈𝔼PX1​\[⋅\]\\mathbb{E}\_{P^{\\mathrm{t}}}\[\\cdot\]\\approx\\mathbb{E}\_{P\_{X\_{1}}}\[\\cdot\].\
\
2. 2.\
\
\
Training the student on synthetic samples from PtP^{\\mathrm{t}} yields similar dynamics to training on real data samples from PX1P\_{X\_{1}}.\
\
3. 3.\
\
\
If the student converges to the teacher, then PMs≈PtP^{\\mathrm{s}}\_{M}\\approx P^{\\mathrm{t}}, allowing us to estimate the teacher’s loss 𝔼PX1​\[log⁡1/Pt​(X)\]\\mathbb{E}\_{P\_{X\_{1}}}\[\\log 1/P^{\\mathrm{t}}(X)\] by the final student’s loss 𝔼PX1​\[log⁡1/PMs​(X)\]\\mathbb{E}\_{P\_{X\_{1}}}\[\\log 1/P^{\\mathrm{s}}\_{M}(X)\].\
\
\
Applying these approximations, the requential code length with a static teacher becomes\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|Preq\|≈∑i=0M−1𝔼PX1​\[log⁡1Pis​(X)−log⁡1PMs​(X)\],\|\\mathrm{P}\_{\\mathrm{req}}\|\\,\\approx\\sum\_{i=0}^{M-1}\\mathbb{E}\_{P\_{X\_{1}}}\\left\[\\log\\frac{1}{P^{\\mathrm{s}}\_{i}(X)}-\\log\\frac{1}{P^{\\mathrm{s}}\_{M}(X)}\\right\], |  | (50) |\
\
which, when estimated empirically on real training data Z0,…,ZM−1∼PX1Z\_{0},\\ldots,Z\_{M-1}\\sim P\_{X\_{1}}, recovers precisely the prequential estimate from [Equation˜8](https://arxiv.org/html/2601.03220v2#S4.E8 "In 4.1 Approximating Model Description Length with Prequential Coding ‣ 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"):\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|Ppreq\|≈∑i=0M−1(log⁡1Pi​(Zi)−log⁡1PM​(Zi)).\|\\mathrm{P}\_{\\mathrm{preq}}\|\\,\\approx\\sum\_{i=0}^{M-1}\\left(\\log\\frac{1}{P\_{i}(Z\_{i})}-\\log\\frac{1}{P\_{M}(Z\_{i})}\\right). |  | (51) |\
\
This connection also lends some justification to treating 6​N​D6ND as the decoding time for the model in prequential coding, as it relates to a requential scheme that achieves this runtime.\
Since a static teacher is generally suboptimal compared to the time-varying teachers used in full requential coding, which can remain close to the student throughout training while still guiding it toward the target distribution, we expect the prequential estimate to be an overestimate of the requential code length. This is consistent with the empirical observations in [Figure˜2](https://arxiv.org/html/2601.03220v2#S4.F2 "In 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), where the prequential estimate is typically several times larger than the requential estimate.\
\
### B.3 A Solvable Model Using Scaling Laws\
\
In this section, we present a simplified analytical model from combining neural scaling laws with prequential coding to gain insight into how epiplexity and compute-optimal hyperparameters typically vary with compute and dataset size, along with their asymptotic behaviors.\
\
We adopt a standard scaling law for the loss as a function of model size NN and training tokens DD:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ℒ​(N,D)=E+(N0N)α+(D0D)β,\\displaystyle\\mathcal{L}(N,D)=E+\\quantity(\\frac{N\_{0}}{N})^{\\alpha}+\\quantity(\\frac{D\_{0}}{D})^{\\beta}, |  | (52) |\
\
where EE is the irreducible loss, N0N\_{0} and D0D\_{0} are scaling constants, and 0<α,β<10<\\alpha,\\beta<1 are the scaling exponents. The total compute for training and evaluating on 𝒟\\mathcal{D} test tokens is T=6​N​D+2​N​𝒟=2​N​(3​D+𝒟)T=6ND+2N\\mathcal{D}=2N(3D+\\mathcal{D}).\
\
To simplify the analysis, we work in natural units: n=N/N0n=N/N\_{0}, d=D/D0d=D/D\_{0}, δ=𝒟/D0\\delta=\\mathcal{D}/D\_{0}, and t=T/(2​N0​D0)t=T/(2N\_{0}D\_{0}). The loss becomes ℒ​(n,d)=E+n−α+d−β\\mathcal{L}(n,d)=E+n^{-\\alpha}+d^{-\\beta}, and the compute constraint simplifies to t=n​(3​d+δ)t=n(3d+\\delta).\
\
##### Two-part code length.\
\
The two-part code Ptot\\mathrm{P}\_{\\mathrm{tot}} consists of the model description and the data encoded using the model. The data code length on the test set is δ​D0⋅ℒ​(n,d)\\delta D\_{0}\\cdot\\mathcal{L}(n,d).\
\
For the model description length, we use the prequential estimate from [Equation˜8](https://arxiv.org/html/2601.03220v2#S4.E8 "In 4.1 Approximating Model Description Length with Prequential Coding ‣ 4 Measuring Epiplexity and Time-Bounded Entropy ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), which corresponds to the area under the loss curve above the final loss666We start the sum and integral at 11 to avoid the singularity at 0,0, which is an artifact of the scaling law as it typically only holds for large D.D.:\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | \|Ppreq\|\\displaystyle\|\\mathrm{P}\_{\\mathrm{preq}}\| | =∑i=1D\[(iD0)−β−(DD0)−β\]\\displaystyle\\,=\\sum\_{i=1}^{D}\\quantity\[\\quantity(\\frac{i}{D\_{0}})^{-\\beta}-\\quantity(\\frac{D}{D\_{0}})^{-\\beta}\] |  |\
|  |  | =∫1D\[(uD0)−β−(DD0)−β\]​𝑑u+O​(1),\\displaystyle=\\int\_{1}^{D}\\quantity\[\\quantity(\\frac{u}{D\_{0}})^{-\\beta}-\\quantity(\\frac{D}{D\_{0}})^{-\\beta}\]du+O(1), |  | (53) |\
\
where the O​(1)O(1) term remains bounded as D→∞D\\to\\infty. Evaluating the integral and dropping O​(1)O(1) terms, we obtain the expression valid for large DD:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|Ppreq\|=β1−β​D0​d1−β.\\displaystyle\|\\mathrm{P}\_{\\mathrm{preq}}\|\\,=\\frac{\\beta}{1-\\beta}D\_{0}\\,d^{1-\\beta}. |  | (54) |\
\
##### Optimality condition.\
\
Dropping the constant term δ​D0​E\\delta D\_{0}E from the two-part code length and dividing by D0D\_{0}, we seek to minimize\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | f​(n,d)=β1−β​d1−β+δ​(n−α+d−β)\\displaystyle f(n,d)=\\frac{\\beta}{1-\\beta}d^{1-\\beta}+\\delta(n^{-\\alpha}+d^{-\\beta}) |  | (55) |\
\
subject to t=n​(3​d+δ)t=n(3d+\\delta).\
\
##### Solution.\
\
Eliminating nn using the constraint n=t/(3​d+δ)n=t/(3d+\\delta), we obtain a one-dimensional optimization problem in dd. Setting the derivative to zero and simplifying, the optimal d⋆​(t)d^{\\star}(t) satisfies\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | β​d−β−1​(δ−d)=3​α​δ​t−α​(3​d+δ)α−1,\\displaystyle\\beta d^{-\\beta-1}(\\delta-d)=3\\alpha\\delta\\,t^{-\\alpha}(3d+\\delta)^{\\alpha-1}, |  | (56) |\
\
with the corresponding optimal model size given by\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | n⋆​(t)=t3​d⋆​(t)+δ.\\displaystyle n^{\\star}(t)=\\frac{t}{3d^{\\star}(t)+\\delta}. |  | (57) |\
\
While [Equation˜56](https://arxiv.org/html/2601.03220v2#A2.E56 "In Solution. ‣ B.3 A Solvable Model Using Scaling Laws ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") does not admit a simple closed-form solution in general, we can extract the asymptotic behavior in the large- and small-compute regimes.\
\
##### Large-compute regime (t→∞t\\to\\infty).\
\
As tt grows, the right-hand side of [Equation˜56](https://arxiv.org/html/2601.03220v2#A2.E56 "In Solution. ‣ B.3 A Solvable Model Using Scaling Laws ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") scales as t−α→0t^{-\\alpha}\\to 0. For the equation to remain balanced, we require δ−d→0\\delta-d\\to 0, i.e., d⋆​(t)→δd^{\\star}(t)\\to\\delta. The leading-order scaling is therefore:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | d⋆​(t)=δ−Θ​(t−α),n⋆​(t)∼t4​δ.\\displaystyle d^{\\star}(t)=\\delta-\\Theta(t^{-\\alpha}),\\qquad n^{\\star}(t)\\sim\\frac{t}{4\\delta}. |  | (58) |\
\
In this regime, the optimal training set size saturates at the test set size δ\\delta, while the model size grows linearly with compute. Correspondingly, the epiplexity saturates to\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | S∞​(X)=β1−β​D0​δ1−β=β1−β​D0β​𝒟1−β.\\displaystyle\\mathrm{S}\_{\\infty}(X)=\\frac{\\beta}{1-\\beta}D\_{0}\\,\\delta^{1-\\beta}=\\frac{\\beta}{1-\\beta}D\_{0}^{\\beta}\\mathcal{D}^{1-\\beta}. |  | (59) |\
\
For the entropy, we have (n⋆)−α→0(n^{\\star})^{-\\alpha}\\to 0 while (d⋆)−β→δ−β(d^{\\star})^{-\\beta}\\to\\delta^{-\\beta}, so\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | H∞​(X)=𝒟​(E+δ−β)=𝒟​E+D0β​𝒟1−β.\\displaystyle\\mathrm{H}\_{\\infty}(X)=\\mathcal{D}\\quantity(E+\\delta^{-\\beta})=\\mathcal{D}E+D\_{0}^{\\beta}\\mathcal{D}^{1-\\beta}. |  | (60) |\
\
The entropy approaches the irreducible entropy 𝒟​E\\mathcal{D}E plus a residual term from finite training data that scales sublinearly with the test set size, meaning that the achieved per-token loss is E+O​(𝒟−β).E+O(\\mathcal{D}^{-\\beta}).\
\
##### Small-compute regime (d⋆≪δd^{\\star}\\ll\\delta).\
\
When compute is limited such that d≪δd\\ll\\delta, we approximate δ−d≈δ\\delta-d\\approx\\delta and (3​d+δ)α−1≈δα−1(3d+\\delta)^{\\alpha-1}\\approx\\delta^{\\alpha-1}. Substituting into [Equation˜56](https://arxiv.org/html/2601.03220v2#A2.E56 "In Solution. ‣ B.3 A Solvable Model Using Scaling Laws ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") and solving for dd gives\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | d⋆​(t)=(β3​α)1β+1​tαβ+1​δ1−αβ+1.\\displaystyle d^{\\star}(t)=\\quantity(\\frac{\\beta}{3\\alpha})^{\\frac{1}{\\beta+1}}t^{\\frac{\\alpha}{\\beta+1}}\\delta^{\\frac{1-\\alpha}{\\beta+1}}. |  | (61) |\
\
Since 3​d⋆≪δ3d^{\\star}\\ll\\delta in this regime, the optimal model size is\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | n⋆​(t)≈tδ.\\displaystyle n^{\\star}(t)\\approx\\frac{t}{\\delta}. |  | (62) |\
\
Here, the model size is constrained by the need to evaluate on δ\\delta tokens, and the optimal training set size grows sublinearly with compute as d⋆∝tα/(β+1)d^{\\star}\\propto t^{\\alpha/(\\beta+1)}. The epiplexity in this regime scales as\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ST​(X)=β1−β​D0​(d⋆)1−β∝Tα​(1−β)β+1,\\displaystyle\\mathrm{S}\_{T}(X)=\\frac{\\beta}{1-\\beta}D\_{0}\\,(d^{\\star})^{1-\\beta}\\propto T^{\\frac{\\alpha(1-\\beta)}{\\beta+1}}, |  | (63) |\
\
growing sublinearly with compute.\
\
For the entropy, both the model and data contributions are significant. The model contribution scales as\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | 𝒟​(n⋆)−α=𝒟​(δt)α∝T−α,\\displaystyle\\mathcal{D}(n^{\\star})^{-\\alpha}=\\mathcal{D}\\quantity(\\frac{\\delta}{t})^{\\alpha}\\propto T^{-\\alpha}, |  | (64) |\
\
while the data contribution scales as\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | 𝒟​(d⋆)−β∝T−α​ββ+1.\\displaystyle\\mathcal{D}(d^{\\star})^{-\\beta}\\propto T^{-\\frac{\\alpha\\beta}{\\beta+1}}. |  | (65) |\
\
Since α​β/(β+1)<α\\alpha\\beta/(\\beta+1)<\\alpha, the data term decays more slowly and dominates for larger tt within this regime. The entropy above the irreducible level is thus\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | HT​(X)−𝒟​E∝T−α​ββ+1,\\displaystyle\\mathrm{H}\_{T}(X)-\\mathcal{D}E\\propto T^{-\\frac{\\alpha\\beta}{\\beta+1}}, |  | (66) |\
\
decaying as a power law with compute.\
\
For typical scaling exponents (e.g., α≈0.34\\alpha\\approx 0.34 and β≈0.28\\beta\\approx 0.28 from Hoffmann et al. ( [2022](https://arxiv.org/html/2601.03220v2#bib.bib49 ""))), the epiplexity grows as ST∝T0.19\\mathrm{S}\_{T}\\propto T^{0.19} and the entropy decays as HT−𝒟​E∝T−0.07\\mathrm{H}\_{T}-\\mathcal{D}E\\propto T^{-0.07} in the small-compute regime.\
\
### B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size\
\
In this section, we analyze how epiplexity and time-bounded entropy scale with compute budget and dataset size under natural assumptions about neural network training, without relying on specific functional forms for scaling laws. The goal is to provide some general intuitions for how these quantities are expected to vary as a function of the compute budget and dataset size.\
[Section˜B.3](https://arxiv.org/html/2601.03220v2#A2.SS3 "B.3 A Solvable Model Using Scaling Laws ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") explicitly demonstrates using scaling laws and prequential coding that (1) epiplexity grows with both compute and dataset size, and (2) for a fixed XX, epiplexity saturates to a finite value in the limit of infinite compute—specifically, to the amount of information acquired by an arbitrarily large model trained on a training set of the same size as the test set XX, while time-bounded entropy decays to the loss achievable by an infinitely large model on this training set. Here, we show that similar or weaker statements hold more generally, requiring only a few natural assumptions about the effect of increasing model size NN and training data size DD. These assumptions capture typically observed regularities in deep learning, such as the smoothly diminishing returns in scaling only model size while holding training set size fixed, but they may fail to capture rare exceptions like grokking and sudden improvement in performance above certain compute thresholds (as in [Section˜5.3.2](https://arxiv.org/html/2601.03220v2#S5.SS3.SSS2 "5.3.2 Emergent Phenomena ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")).\
\
Denote the code length for an NN-parameter model trained on DD tokens as \|P\|​(N,D),\|\\mathrm{P}\|(N,D), the per-token loss it achieves as ℒ​(N,D)\\mathcal{L}(N,D), the compute-optimal model size as N⋆​(T)N^{\\star}(T) and training data size as D⋆​(T),D^{\\star}(T), so that ST​(X)=\|P\|​(N⋆​(T),D⋆​(T))\\mathrm{S}\_{T}(X)=\|\\mathrm{P}\|\\quantity(N^{\\star}(T),D^{\\star}(T)) and HT​(X)=𝒟​ℒ​(N⋆​(T),D⋆​(T)).\\mathrm{H}\_{T}(X)=\\mathcal{D}\\,\\mathcal{L}\\quantity(N^{\\star}(T),D^{\\star}(T)). We establish the following results as we vary TT and 𝒟=\|X\|\\mathcal{D}=\|X\|, fixing the distribution of XiX\_{i} (only the dataset size changes):\
\
- •\
\
\
Monotonicity of N⋆​(T)N^{\\star}(T), D⋆​(T)D^{\\star}(T), ST​(X)\\mathrm{S}\_{T}(X), and HT​(X)\\mathrm{H}\_{T}(X) ( [Section˜B.4.1](https://arxiv.org/html/2601.03220v2#A2.SS4.SSS1 "B.4.1 Monotonicity of 𝑁^∗⁢(𝑇), 𝐷^∗⁢(𝑇), S_𝑇⁢(𝑋), and H_𝑇⁢(𝑋) ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")): Under natural assumptions on the effect of increasing NN and DD, the compute-optimal model size N⋆​(T)N^{\\star}(T) and training data size D⋆​(T)D^{\\star}(T) are both increasing in the compute budget TT. As a result, epiplexity typically grows with TT while time-bounded entropy typically decreases with TT.\
\
- •\
\
\
Monotonicity of S∞​(X)\\mathrm{S}\_{\\infty}(X) and H∞​(X)\\mathrm{H}\_{\\infty}(X) in 𝒟\\mathcal{D} ( [Section˜B.4.2](https://arxiv.org/html/2601.03220v2#A2.SS4.SSS2 "B.4.2 Monotonicity of S_∞⁢(𝑋) and H_∞⁢(𝑋) in 𝒟 ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")): In the infinite-compute limit, epiplexity S∞​(X)\\mathrm{S}\_{\\infty}(X) is nondecreasing in 𝒟=\|X\|\\mathcal{D}=\|X\|, while the per-token time-bounded entropy h∞​(X𝒟):=H∞​(X𝒟)/𝒟h\_{\\infty}(X\_{\\mathcal{D}}):=\\mathrm{H}\_{\\infty}(X\_{\\mathcal{D}})/\\mathcal{D} is nonincreasing in 𝒟\\mathcal{D}.\
\
- •\
\
\
D⋆​(T)D^{\\star}(T) generally approaches 𝒟\\mathcal{D} in prequential coding ( [Section˜B.4.3](https://arxiv.org/html/2601.03220v2#A2.SS4.SSS3 "B.4.3 𝐷^⋆⁢(𝑇) Generally Approaches 𝒟 in Prequential Coding ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")): For prequential coding, the compute-optimal training set size satisfies D⋆​(T)→𝒟D^{\\star}(T)\\to\\mathcal{D} as T→∞T\\to\\infty, where 𝒟\\mathcal{D} is the test set size, without assuming the scaling law form. Combined with monotonicity of D⋆​(T)D^{\\star}(T), this implies D⋆​(T)↑𝒟D^{\\star}(T)\\uparrow\\mathcal{D} from below.\
\
\
#### B.4.1 Monotonicity of N∗​(T)N^{\*}(T), D∗​(T)D^{\*}(T), ST​(X)\\mathrm{S}\_{T}(X), and HT​(X)\\mathrm{H}\_{T}(X)\
\
The following theorem shows that the compute-optimal model size and training data size are both monotonically increasing in the compute budget under natural assumptions.\
\
###### Theorem 30 (Monotone growth of compute-optimal NN and DD)\
\
Define the effective data D~=6​D+2​𝒟\\widetilde{D}=6D+2\\mathcal{D}, so that the compute constraint becomes T=N​D~T=N\\widetilde{D}. Let J​(N,D~)J(N,\\widetilde{D}) denote the two-part code length as a function of model size NN and effective data D~\\widetilde{D}, and assume JJ is twice continuously differentiable. Consider the constrained MDL problem\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | minN>0,D~≥2​𝒟⁡J​(N,D~)s.t.N​D~=T.\\displaystyle\\min\_{N>0,\\,\\widetilde{D}\\geq 2\\mathcal{D}}\\;J(N,\\widetilde{D})\\qquad\\text{s.t.}\\qquad N\\widetilde{D}=T. |  | (67) |\
\
Assume that for each TT in the regime of interest there is a unique interior optimizer (N⋆​(T),D~⋆​(T))(N^{\\star}(T),\\widetilde{D}^{\\star}(T)) with D~⋆​(T)>2​𝒟\\widetilde{D}^{\\star}(T)>2\\mathcal{D} and N⋆​(T)​D~⋆​(T)=TN^{\\star}(T)\\widetilde{D}^{\\star}(T)=T.\
\
Work in logarithmic coordinates μ:=log⁡N\\mu:=\\log N and ν:=log⁡D~\\nu:=\\log\\widetilde{D}, and by slight abuse of notation write J​(μ,ν)=J​(eμ,eν)J(\\mu,\\nu)=J(e^{\\mu},e^{\\nu}). Assume that for all such TT, the following conditions hold at the corresponding optimum (μ⋆​(T),ν⋆​(T))(\\mu^{\\star}(T),\\nu^{\\star}(T)):\
\
1. 1.\
\
\
Complementarity (larger models are more sample-efficient):\
\
\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ∂2J∂μ​∂ν≤0.\\displaystyle\\frac{\\partial^{2}J}{\\partial\\mu\\partial\\nu}\\leq 0. |  | (68) |\
\
2. 2.\
\
\
Diminishing returns in model size (in log coordinates):\
\
\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ∂2J∂μ2>0.\\displaystyle\\frac{\\partial^{2}J}{\\partial\\mu^{2}}>0. |  | (69) |\
\
3. 3.\
\
\
Diminishing returns in effective data (in log coordinates):\
\
\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ∂2J∂ν2>0.\\displaystyle\\frac{\\partial^{2}J}{\\partial\\nu^{2}}>0. |  | (70) |\
\
\
Then both compute-optimal choices are strictly increasing functions of TT:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | T2>T1⟹N⋆​(T2)>N⋆​(T1)andD~⋆​(T2)>D~⋆​(T1).\\displaystyle T\_{2}>T\_{1}\\quad\\Longrightarrow\\quad N^{\\star}(T\_{2})>N^{\\star}(T\_{1})\\quad\\text{and}\\quad\\widetilde{D}^{\\star}(T\_{2})>\\widetilde{D}^{\\star}(T\_{1}). |  | (71) |\
\
Proof\
Work in logarithmic coordinates\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | μ:=log⁡N,ν:=log⁡D~,τ:=log⁡T.\\displaystyle\\mu:=\\log N,\\qquad\\nu:=\\log\\widetilde{D},\\qquad\\tau:=\\log T. |  | (72) |\
\
The compute constraint N​D~=TN\\widetilde{D}=T becomes the affine constraint\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | μ+ν=τ⟺ν=τ−μ.\\displaystyle\\mu+\\nu=\\tau\\qquad\\Longleftrightarrow\\qquad\\nu=\\tau-\\mu. |  | (73) |\
\
By slight abuse of notation, write J​(μ,ν):=J​(eμ,eν)J(\\mu,\\nu):=J(e^{\\mu},e^{\\nu}) and denote its partial derivatives by Jμ,Jν,Jμ​μ,Jν​ν,Jμ​νJ\_{\\mu},J\_{\\nu},J\_{\\mu\\mu},J\_{\\nu\\nu},J\_{\\mu\\nu}, etc., all taken with respect to the log-coordinates (μ,ν)(\\mu,\\nu).\
\
Define the _restricted objective_ along the compute frontier by\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | f​(μ,τ):=J​(μ,τ−μ).\\displaystyle f(\\mu,\\tau):=J(\\mu,\\tau-\\mu). |  | (74) |\
\
For each τ\\tau in the regime of interest, let μ⋆​(τ)\\mu^{\\star}(\\tau) denote the unique interior minimizer of f​(⋅,τ)f(\\cdot,\\tau), and set ν⋆​(τ):=τ−μ⋆​(τ)\\nu^{\\star}(\\tau):=\\tau-\\mu^{\\star}(\\tau).\
\
Holding τ\\tau fixed and differentiating ff with respect to μ\\mu gives\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | fμ​(μ,τ)\\displaystyle f\_{\\mu}(\\mu,\\tau) | =∂∂μ​J​(μ,τ−μ)\\displaystyle=\\frac{\\partial}{\\partial\\mu}J(\\mu,\\tau-\\mu) |  |\
|  |  | =Jμ​(μ,ν)+Jν​(μ,ν)​∂∂μ​(τ−μ)\\displaystyle=J\_{\\mu}(\\mu,\\nu)+J\_{\\nu}(\\mu,\\nu)\\frac{\\partial}{\\partial\\mu}(\\tau-\\mu) |  |\
|  |  | =Jμ​(μ,ν)−Jν​(μ,ν),\\displaystyle=J\_{\\mu}(\\mu,\\nu)-J\_{\\nu}(\\mu,\\nu), |  | (75) |\
\
where ν=τ−μ\\nu=\\tau-\\mu. The optimality condition for μ⋆​(τ)\\mu^{\\star}(\\tau) is therefore\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | fμ​(μ⋆​(τ),τ)=0⟺Jμ​(μ⋆​(τ),ν⋆​(τ))=Jν​(μ⋆​(τ),ν⋆​(τ)).\\displaystyle f\_{\\mu}(\\mu^{\\star}(\\tau),\\tau)=0\\qquad\\Longleftrightarrow\\qquad J\_{\\mu}(\\mu^{\\star}(\\tau),\\nu^{\\star}(\\tau))=J\_{\\nu}(\\mu^{\\star}(\\tau),\\nu^{\\star}(\\tau)). |  | (76) |\
\
Differentiating the identity fμ​(μ⋆​(τ),τ)=0f\_{\\mu}(\\mu^{\\star}(\\tau),\\tau)=0 with respect to τ\\tau yields\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | 0=dd​τ​fμ​(μ⋆​(τ),τ)=fμ​μ​(μ⋆​(τ),τ)​d​μ⋆d​τ+fμ​τ​(μ⋆​(τ),τ).\\displaystyle 0=\\frac{d}{d\\tau}f\_{\\mu}(\\mu^{\\star}(\\tau),\\tau)=f\_{\\mu\\mu}(\\mu^{\\star}(\\tau),\\tau)\\,\\frac{d\\mu^{\\star}}{d\\tau}+f\_{\\mu\\tau}(\\mu^{\\star}(\\tau),\\tau). |  | (77) |\
\
Assuming fμ​μ​(μ⋆​(τ),τ)≠0f\_{\\mu\\mu}(\\mu^{\\star}(\\tau),\\tau)\\neq 0 (verified below), we obtain\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | d​μ⋆d​τ=−fμ​τfμ​μevaluated at ​(μ,τ)=(μ⋆​(τ),τ).\\displaystyle\\frac{d\\mu^{\\star}}{d\\tau}=-\\frac{f\_{\\mu\\tau}}{f\_{\\mu\\mu}}\\quad\\text{evaluated at }(\\mu,\\tau)=(\\mu^{\\star}(\\tau),\\tau). |  | (78) |\
\
We now express fμ​τf\_{\\mu\\tau} and fμ​μf\_{\\mu\\mu} in terms of second partial derivatives of JJ. From ( [75](https://arxiv.org/html/2601.03220v2#A2.E75 "Equation 75 ‣ B.4.1 Monotonicity of 𝑁^∗⁢(𝑇), 𝐷^∗⁢(𝑇), S_𝑇⁢(𝑋), and H_𝑇⁢(𝑋) ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) and the chain rule, using ∂τ(τ−μ)=1\\partial\_{\\tau}(\\tau-\\mu)=1,\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | fμ​τ​(μ,τ)\\displaystyle f\_{\\mu\\tau}(\\mu,\\tau) | =∂∂τ​(Jμ​(μ,ν)−Jν​(μ,ν))\\displaystyle=\\frac{\\partial}{\\partial\\tau}\\quantity(J\_{\\mu}(\\mu,\\nu)-J\_{\\nu}(\\mu,\\nu)) |  |\
|  |  | =Jμ​ν​(μ,ν)​∂ν∂τ−Jν​ν​(μ,ν)​∂ν∂τ\\displaystyle=J\_{\\mu\\nu}(\\mu,\\nu)\\frac{\\partial\\nu}{\\partial\\tau}-J\_{\\nu\\nu}(\\mu,\\nu)\\frac{\\partial\\nu}{\\partial\\tau} |  |\
|  |  | =Jμ​ν​(μ,ν)−Jν​ν​(μ,ν),\\displaystyle=J\_{\\mu\\nu}(\\mu,\\nu)-J\_{\\nu\\nu}(\\mu,\\nu), |  | (79) |\
\
with ν=τ−μ\\nu=\\tau-\\mu. Similarly, differentiating ( [75](https://arxiv.org/html/2601.03220v2#A2.E75 "Equation 75 ‣ B.4.1 Monotonicity of 𝑁^∗⁢(𝑇), 𝐷^∗⁢(𝑇), S_𝑇⁢(𝑋), and H_𝑇⁢(𝑋) ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) with respect to μ\\mu while holding τ\\tau fixed, and using ∂μ(τ−μ)=−1\\partial\_{\\mu}(\\tau-\\mu)=-1 together with symmetry Jν​μ=Jμ​νJ\_{\\nu\\mu}=J\_{\\mu\\nu}, yields\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | fμ​μ​(μ,τ)\\displaystyle f\_{\\mu\\mu}(\\mu,\\tau) | =∂∂μ​(Jμ​(μ,ν)−Jν​(μ,ν))\\displaystyle=\\frac{\\partial}{\\partial\\mu}\\quantity(J\_{\\mu}(\\mu,\\nu)-J\_{\\nu}(\\mu,\\nu)) |  |\
|  |  | =(Jμ​μ​(μ,ν)+Jμ​ν​(μ,ν)​∂ν∂μ)−(Jν​μ​(μ,ν)+Jν​ν​(μ,ν)​∂ν∂μ)\\displaystyle=\\quantity(J\_{\\mu\\mu}(\\mu,\\nu)+J\_{\\mu\\nu}(\\mu,\\nu)\\frac{\\partial\\nu}{\\partial\\mu})-\\quantity(J\_{\\nu\\mu}(\\mu,\\nu)+J\_{\\nu\\nu}(\\mu,\\nu)\\frac{\\partial\\nu}{\\partial\\mu}) |  |\
|  |  | =(Jμ​μ−Jμ​ν)−(Jμ​ν−Jν​ν)\\displaystyle=(J\_{\\mu\\mu}-J\_{\\mu\\nu})-(J\_{\\mu\\nu}-J\_{\\nu\\nu}) |  |\
|  |  | =Jμ​μ​(μ,ν)+Jν​ν​(μ,ν)−2​Jμ​ν​(μ,ν).\\displaystyle=J\_{\\mu\\mu}(\\mu,\\nu)+J\_{\\nu\\nu}(\\mu,\\nu)-2J\_{\\mu\\nu}(\\mu,\\nu). |  | (80) |\
\
Substituting ( [79](https://arxiv.org/html/2601.03220v2#A2.E79 "Equation 79 ‣ B.4.1 Monotonicity of 𝑁^∗⁢(𝑇), 𝐷^∗⁢(𝑇), S_𝑇⁢(𝑋), and H_𝑇⁢(𝑋) ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"))–( [80](https://arxiv.org/html/2601.03220v2#A2.E80 "Equation 80 ‣ B.4.1 Monotonicity of 𝑁^∗⁢(𝑇), 𝐷^∗⁢(𝑇), S_𝑇⁢(𝑋), and H_𝑇⁢(𝑋) ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) into ( [78](https://arxiv.org/html/2601.03220v2#A2.E78 "Equation 78 ‣ B.4.1 Monotonicity of 𝑁^∗⁢(𝑇), 𝐷^∗⁢(𝑇), S_𝑇⁢(𝑋), and H_𝑇⁢(𝑋) ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) gives\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | d​μ⋆d​τ=−Jμ​ν−Jν​νJμ​μ+Jν​ν−2​Jμ​ν=Jν​ν−Jμ​νJμ​μ+Jν​ν−2​Jμ​ν,\\displaystyle\\frac{d\\mu^{\\star}}{d\\tau}=-\\frac{J\_{\\mu\\nu}-J\_{\\nu\\nu}}{J\_{\\mu\\mu}+J\_{\\nu\\nu}-2J\_{\\mu\\nu}}=\\frac{J\_{\\nu\\nu}-J\_{\\mu\\nu}}{J\_{\\mu\\mu}+J\_{\\nu\\nu}-2J\_{\\mu\\nu}}, |  | (81) |\
\
with all second partial derivatives of JJ evaluated at (μ,ν)=(μ⋆​(τ),ν⋆​(τ))(\\mu,\\nu)=(\\mu^{\\star}(\\tau),\\nu^{\\star}(\\tau)).\
\
By the assumptions Jν​ν>0J\_{\\nu\\nu}>0 and Jμ​ν≤0J\_{\\mu\\nu}\\leq 0 at the optimum, the numerator in ( [81](https://arxiv.org/html/2601.03220v2#A2.E81 "Equation 81 ‣ B.4.1 Monotonicity of 𝑁^∗⁢(𝑇), 𝐷^∗⁢(𝑇), S_𝑇⁢(𝑋), and H_𝑇⁢(𝑋) ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) satisfies Jν​ν−Jμ​ν>0J\_{\\nu\\nu}-J\_{\\mu\\nu}>0. By the assumptions Jμ​μ>0J\_{\\mu\\mu}>0, Jν​ν>0J\_{\\nu\\nu}>0, and Jμ​ν≤0J\_{\\mu\\nu}\\leq 0, the denominator satisfies Jμ​μ+Jν​ν−2​Jμ​ν>0J\_{\\mu\\mu}+J\_{\\nu\\nu}-2J\_{\\mu\\nu}>0. Hence\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | d​μ⋆d​τ>0.\\displaystyle\\frac{d\\mu^{\\star}}{d\\tau}>0. |  | (82) |\
\
Since ν⋆​(τ)=τ−μ⋆​(τ)\\nu^{\\star}(\\tau)=\\tau-\\mu^{\\star}(\\tau), we also have\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | d​ν⋆d​τ=1−d​μ⋆d​τ=Jμ​μ−Jμ​νJμ​μ+Jν​ν−2​Jμ​ν>0,\\displaystyle\\frac{d\\nu^{\\star}}{d\\tau}=1-\\frac{d\\mu^{\\star}}{d\\tau}=\\frac{J\_{\\mu\\mu}-J\_{\\mu\\nu}}{J\_{\\mu\\mu}+J\_{\\nu\\nu}-2J\_{\\mu\\nu}}>0, |  | (83) |\
\
where positivity follows from Jμ​μ>0J\_{\\mu\\mu}>0 and Jμ​ν≤0J\_{\\mu\\nu}\\leq 0 together with the same positive denominator.\
\
Finally, N⋆​(T)=exp⁡(μ⋆​(log⁡T))N^{\\star}(T)=\\exp(\\mu^{\\star}(\\log T)) and D~⋆​(T)=exp⁡(ν⋆​(log⁡T))\\widetilde{D}^{\\star}(T)=\\exp(\\nu^{\\star}(\\log T)), so d​μ⋆/d​τ>0d\\mu^{\\star}/d\\tau>0 and d​ν⋆/d​τ>0d\\nu^{\\star}/d\\tau>0 imply that both N⋆​(T)N^{\\star}(T) and D~⋆​(T)\\widetilde{D}^{\\star}(T) are strictly increasing functions of TT.\
\
\
##### Empirical plausibility of the assumptions.\
\
The three conditions in [Theorem˜30](https://arxiv.org/html/2601.03220v2#Thmtheorem30 "Theorem 30 (Monotone growth of compute-optimal 𝑁 and 𝐷) ‣ B.4.1 Monotonicity of 𝑁^∗⁢(𝑇), 𝐷^∗⁢(𝑇), S_𝑇⁢(𝑋), and H_𝑇⁢(𝑋) ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") reflect well-documented empirical phenomena in deep learning. The complementarity condition ∂2J/∂μ​∂ν≤0\\partial^{2}J/\\partial\\mu\\partial\\nu\\leq 0 captures the observation that larger models are more sample-efficient: increasing model size leads to faster learning (Kaplan et al., [2020](https://arxiv.org/html/2601.03220v2#bib.bib53 ""); Yang et al., [2022](https://arxiv.org/html/2601.03220v2#bib.bib107 "")), which leads to a faster decrease in both the model description length and data code length (final loss), and thus ∂J/∂ν\\partial J/\\partial\\nu should decrease with μ\\mu. The diminishing returns conditions ∂2J/∂μ2>0\\partial^{2}J/\\partial\\mu^{2}>0 and ∂2J/∂ν2>0\\partial^{2}J/\\partial\\nu^{2}>0 simply state that there is diminishing return in successive doubling of the model size or training data size, holding the other quantity fixed.\
\
##### Asymptotic growth of ST\\mathrm{S}\_{T} and monotone decay of HT\\mathrm{H}\_{T}.\
\
The monotone growth of the compute-optimal N⋆​(T)N^{\\star}(T) and D⋆​(T)D^{\\star}(T) does not by itself imply that ST​(X):=\|P\|​(N⋆​(T),D⋆​(T))\\mathrm{S}\_{T}(X):=\|\\mathrm{P}\|\\quantity(N^{\\star}(T),D^{\\star}(T)) is monotone for all TT. Intuitively, while we expect the model description length \|P\|​(N,D)\|\\mathrm{P}\|(N,D) to grow with DD, it need not increase with NN: larger models can be more sample-efficient, which may reduce the effective complexity of the learned predictor under some coding schemes. However, one should still expect ST​(X)\\mathrm{S}\_{T}(X) to grow with TT, at least asymptotically, if we assume (1) the compute-optimal model size diverges while the optimal training horizon converges, as in the scaling-law model of [Section˜B.3](https://arxiv.org/html/2601.03220v2#A2.SS3 "B.3 A Solvable Model Using Scaling Laws ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), and (2) the existence of infinite-model-size limits of the training dynamics.\
\
That is, assume that along the compute-optimal path,\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | N⋆​(T)→∞andD⋆​(T)→D∞<∞as ​T→∞.\\displaystyle N^{\\star}(T)\\to\\infty\\qquad\\text{and}\\qquad D^{\\star}(T)\\to D\_{\\infty}<\\infty\\qquad\\text{as }T\\to\\infty. |  | (84) |\
\
Assume moreover that for bounded training horizons, the description length admits a well-defined infinite-model-size limit: there exists a function \|P\|∞​(D)\|\\mathrm{P}\|\_{\\infty}(D) such that for each fixed DD,\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|P\|​(N,D)→\|P\|∞​(D)as ​N→∞.\\displaystyle\|\\mathrm{P}\|(N,D)\\to\|\\mathrm{P}\|\_{\\infty}(D)\\qquad\\text{as }N\\to\\infty. |  | (85) |\
\
This assumption is motivated by the existence of infinite-width and depth limits of neural networks under appropriate parameterizations (Yang and Littwin, [2023](https://arxiv.org/html/2601.03220v2#bib.bib106 ""); Dey et al., [2025](https://arxiv.org/html/2601.03220v2#bib.bib26 "")), where scalar quantities such as loss and teacher–student KL divergence that determine \|P\|​(N,D)\|\\mathrm{P}\|(N,D) admit stable large-model limits for bounded training durations. Under these conditions, any non-monotonic dependence of \|P\|\|\\mathrm{P}\| on NN is a finite-model effect; once N⋆​(T)N^{\\star}(T) is large enough, \|P\|​(N⋆​(T),D⋆​(T))\|\\mathrm{P}\|\\quantity(N^{\\star}(T),D^{\\star}(T)) is well-approximated by the limiting curve \|P\|∞​(D⋆​(T))\|\\mathrm{P}\|\_{\\infty}\\quantity(D^{\\star}(T)). Since D⋆​(T)D^{\\star}(T) is monotone increasing and convergent under our earlier assumptions, the large-TT behavior of ST​(X)\\mathrm{S}\_{T}(X) is therefore governed primarily by the behavior of D⋆​(T)D^{\\star}(T) alone, which we have shown is increasing with TT, so one expects ST​(X)\\mathrm{S}\_{T}(X) to increase at large TT as \|P\|∞​(D)\|\\mathrm{P}\|\_{\\infty}(D) should increase with D.D.\
\
For the entropy term HT​(X):=𝒟​ℒ​(N⋆​(T),D⋆​(T))\\mathrm{H}\_{T}(X):=\\mathcal{D}\\,\\mathcal{L}\\quantity(N^{\\star}(T),D^{\\star}(T)), the conclusion is simpler and does not require taking N→∞N\\to\\infty. Assume only that the loss ℒ​(N,D)\\mathcal{L}(N,D) is nonincreasing in both NN and DD (more data and parameters cannot make the loss worse). Since N⋆​(T)N^{\\star}(T) and D⋆​(T)D^{\\star}(T) are increasing in TT, we have\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | T2>T1⟹ℒ​(N⋆​(T2),D⋆​(T2))≤ℒ​(N⋆​(T1),D⋆​(T1)),\\displaystyle T\_{2}>T\_{1}\\quad\\Longrightarrow\\quad\\mathcal{L}\\quantity(N^{\\star}(T\_{2}),D^{\\star}(T\_{2}))\\leq\\mathcal{L}\\quantity(N^{\\star}(T\_{1}),D^{\\star}(T\_{1})), |  | (86) |\
\
and therefore HT​(X)\\mathrm{H}\_{T}(X) is nonincreasing in TT. In particular, whenever HT​(X)\\mathrm{H}\_{T}(X) has a finite large-compute limit H∞​(X)\\mathrm{H}\_{\\infty}(X), it approaches this limit from above.\
\
#### B.4.2 Monotonicity of S∞​(X)\\mathrm{S}\_{\\infty}(X) and H∞​(X)\\mathrm{H}\_{\\infty}(X) in 𝒟\\mathcal{D}\
\
We now show that epiplexity and time-bounded entropy (after appropriate normalization) in the infinite-compute limit are monotonic in the test set size 𝒟=\|X\|\\mathcal{D}=\|X\|, regardless of the coding scheme.\
\
Fix a dataset X𝒟X\_{\\mathcal{D}} of length 𝒟\\mathcal{D} tokens. For a two-part code of the form\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | J​(N,D;𝒟)=\|P\|​(N,D)+𝒟​ℒ​(N,D),\\displaystyle J(N,D;\\mathcal{D})=\|\\mathrm{P}\|(N,D)+\\mathcal{D}\\,\\mathcal{L}(N,D), |  | (87) |\
\
let (NT⋆​(𝒟),DT⋆​(𝒟))(N^{\\star}\_{T}(\\mathcal{D}),D^{\\star}\_{T}(\\mathcal{D})) denote the compute-optimal choices. We write\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | ST​(X𝒟)\\displaystyle\\mathrm{S}\_{T}(X\_{\\mathcal{D}}) | :=\|P\|​(NT⋆​(𝒟),DT⋆​(𝒟)),\\displaystyle:=\|\\mathrm{P}\|\\quantity(N^{\\star}\_{T}(\\mathcal{D}),D^{\\star}\_{T}(\\mathcal{D})), |  | (88) |\
|  | HT​(X𝒟)\\displaystyle\\mathrm{H}\_{T}(X\_{\\mathcal{D}}) | :=𝒟​ℒ​(NT⋆​(𝒟),DT⋆​(𝒟)),\\displaystyle:=\\mathcal{D}\\,\\mathcal{L}\\quantity(N^{\\star}\_{T}(\\mathcal{D}),D^{\\star}\_{T}(\\mathcal{D})), |  | (89) |\
|  | hT​(𝒟)\\displaystyle h\_{T}(\\mathcal{D}) | :=HT​(X𝒟)𝒟=ℒ​(NT⋆​(𝒟),DT⋆​(𝒟)).\\displaystyle:=\\frac{H\_{T}(X\_{\\mathcal{D}})}{\\mathcal{D}}=\\mathcal{L}\\quantity(N^{\\star}\_{T}(\\mathcal{D}),D^{\\star}\_{T}(\\mathcal{D})). |  | (90) |\
\
In the infinite-compute limit T→∞T\\to\\infty, the compute constraint becomes irrelevant, so the limiting quantities coincide with the optimum of the unconstrained problem\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | (N∞⋆​(𝒟),D∞⋆​(𝒟))=arg⁡minN>0,D≥0⁡\|P\|​(N,D)+𝒟​ℒ​(N,D).\\displaystyle(N\_{\\infty}^{\\star}(\\mathcal{D}),D\_{\\infty}^{\\star}(\\mathcal{D}))=\\arg\\min\_{N>0,\\,D\\geq 0}\\;\|\\mathrm{P}\|(N,D)+\\mathcal{D}\\,\\mathcal{L}(N,D). |  | (91) |\
\
Thus\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | S∞​(X𝒟)=\|P\|​(N∞⋆,D∞⋆),h∞​(X𝒟)=ℒ​(N∞⋆,D∞⋆).\\displaystyle S\_{\\infty}(X\_{\\mathcal{D}})=\|\\mathrm{P}\|(N\_{\\infty}^{\\star},D\_{\\infty}^{\\star}),\\qquad h\_{\\infty}(X\_{\\mathcal{D}})=\\mathcal{L}(N\_{\\infty}^{\\star},D\_{\\infty}^{\\star}). |  | (92) |\
\
We claim that S∞​(X𝒟)\\mathrm{S}\_{\\infty}(X\_{\\mathcal{D}}) is nondecreasing in 𝒟\\mathcal{D}, and h∞​(X𝒟)h\_{\\infty}(X\_{\\mathcal{D}}) is nonincreasing in 𝒟\\mathcal{D}, assuming that for each 𝒟>0\\mathcal{D}>0 the unconstrained problem ( [91](https://arxiv.org/html/2601.03220v2#A2.E91 "Equation 91 ‣ B.4.2 Monotonicity of S_∞⁢(𝑋) and H_∞⁢(𝑋) in 𝒟 ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) admits at least one minimizer.\
\
To see this, fix 𝒟2>𝒟1\\mathcal{D}\_{2}>\\mathcal{D}\_{1} and let (Ni,Di)(N\_{i},D\_{i}) be minimizers of ( [91](https://arxiv.org/html/2601.03220v2#A2.E91 "Equation 91 ‣ B.4.2 Monotonicity of S_∞⁢(𝑋) and H_∞⁢(𝑋) in 𝒟 ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) at 𝒟=𝒟i\\mathcal{D}=\\mathcal{D}\_{i}. Write Pi:=\|P\|​(Ni,Di)P\_{i}:=\|\\mathrm{P}\|(N\_{i},D\_{i}) and Li:=ℒ​(Ni,Di)L\_{i}:=\\mathcal{L}(N\_{i},D\_{i}). Optimality of (N2,D2)(N\_{2},D\_{2}) at 𝒟2\\mathcal{D}\_{2} implies\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | P2+𝒟2​L2≤P1+𝒟2​L1.\\displaystyle P\_{2}+\\mathcal{D}\_{2}L\_{2}\\leq P\_{1}+\\mathcal{D}\_{2}L\_{1}. |  | (93) |\
\
Optimality of (N1,D1)(N\_{1},D\_{1}) at 𝒟1\\mathcal{D}\_{1} implies\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | P1+𝒟1​L1≤P2+𝒟1​L2.\\displaystyle P\_{1}+\\mathcal{D}\_{1}L\_{1}\\leq P\_{2}+\\mathcal{D}\_{1}L\_{2}. |  | (94) |\
\
Adding ( [93](https://arxiv.org/html/2601.03220v2#A2.E93 "Equation 93 ‣ B.4.2 Monotonicity of S_∞⁢(𝑋) and H_∞⁢(𝑋) in 𝒟 ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) and ( [94](https://arxiv.org/html/2601.03220v2#A2.E94 "Equation 94 ‣ B.4.2 Monotonicity of S_∞⁢(𝑋) and H_∞⁢(𝑋) in 𝒟 ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) gives\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | (P2+𝒟2​L2)+(P1+𝒟1​L1)\\displaystyle(P\_{2}+\\mathcal{D}\_{2}L\_{2})+(P\_{1}+\\mathcal{D}\_{1}L\_{1}) | ≤(P1+𝒟2​L1)+(P2+𝒟1​L2)\\displaystyle\\leq(P\_{1}+\\mathcal{D}\_{2}L\_{1})+(P\_{2}+\\mathcal{D}\_{1}L\_{2}) |  |\
|  | 𝒟2​L2+𝒟1​L1\\displaystyle\\mathcal{D}\_{2}L\_{2}+\\mathcal{D}\_{1}L\_{1} | ≤𝒟2​L1+𝒟1​L2\\displaystyle\\leq\\mathcal{D}\_{2}L\_{1}+\\mathcal{D}\_{1}L\_{2} |  |\
|  | (𝒟2−𝒟1)​(L2−L1)\\displaystyle(\\mathcal{D}\_{2}-\\mathcal{D}\_{1})(L\_{2}-L\_{1}) | ≤0,\\displaystyle\\leq 0, |  | (95) |\
\
hence L2≤L1L\_{2}\\leq L\_{1} since 𝒟2>𝒟1\\mathcal{D}\_{2}>\\mathcal{D}\_{1}, i.e., the achieved loss h∞​(X𝒟)h\_{\\infty}(X\_{\\mathcal{D}}) is nonincreasing in 𝒟\\mathcal{D}. Substituting L2≤L1L\_{2}\\leq L\_{1} back into ( [94](https://arxiv.org/html/2601.03220v2#A2.E94 "Equation 94 ‣ B.4.2 Monotonicity of S_∞⁢(𝑋) and H_∞⁢(𝑋) in 𝒟 ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")) yields P2≥P1P\_{2}\\geq P\_{1}, i.e., S∞​(X𝒟)\\mathrm{S}\_{\\infty}(X\_{\\mathcal{D}}) is nondecreasing in 𝒟\\mathcal{D}.\
\
#### B.4.3 D⋆​(T)D^{\\star}(T) Generally Approaches 𝒟\\mathcal{D} in Prequential Coding\
\
We now show that the compute-optimal training set size for prequential coding generically saturates at D=𝒟D=\\mathcal{D} as T→∞T\\to\\infty, without assuming specific scaling laws.\
\
In continuous time, the prequential model description length is the area above the final loss:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | \|Ppreq​(N,D)\|:=∫0D(ℒ​(N,u)−ℒ​(N,D))​𝑑u.\\displaystyle\|\\mathrm{P}\_{\\mathrm{preq}}(N,D)\|\\,:=\\int\_{0}^{D}\\quantity(\\mathcal{L}(N,u)-\\mathcal{L}(N,D))\\,du. |  | (96) |\
\
The corresponding two-part code length for a test set of size 𝒟\\mathcal{D} is\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | Jpreq​(N,D;𝒟)\\displaystyle J\_{\\mathrm{preq}}(N,D;\\mathcal{D}) | =\|Ppreq​(N,D)\|+𝒟​ℒ​(N,D)\\displaystyle=\|\\mathrm{P}\_{\\mathrm{preq}}(N,D)\|\\,+\\mathcal{D}\\,\\mathcal{L}(N,D) |  |\
|  |  | =∫0Dℒ​(N,u)​𝑑u+(𝒟−D)​ℒ​(N,D).\\displaystyle=\\int\_{0}^{D}\\mathcal{L}(N,u)\\,du+(\\mathcal{D}-D)\\,\\mathcal{L}(N,D). |  | (97) |\
\
We express NN in terms of DD for fixed TT using the constraint 6​N​D+2​N​𝒟=T6ND+2N\\mathcal{D}=T:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | NT​(D)=T6​D+2​𝒟.\\displaystyle N\_{T}(D)=\\frac{T}{6D+2\\mathcal{D}}. |  | (98) |\
\
##### Large-compute limit.\
\
Assume: (i) ℒ​(N,D)\\mathcal{L}(N,D) is nonincreasing in NN and admits a pointwise infinite-model-size limit ℒ∞​(D):=limN→∞ℒ​(N,D)\\mathcal{L}\_{\\infty}(D):=\\lim\_{N\\to\\infty}\\mathcal{L}(N,D);777This limit provably exists under μ\\muP, but is a reasonable assumption in general as it simply asserts diminishing returns in scaling model size without increasing data. (ii) ℒ∞\\mathcal{L}\_{\\infty} is continuously differentiable and strictly decreasing, i.e., ℒ∞′​(D)<0\\mathcal{L}\_{\\infty}^{\\prime}(D)<0. Along the compute frontier ( [98](https://arxiv.org/html/2601.03220v2#A2.E98 "Equation 98 ‣ B.4.3 𝐷^⋆⁢(𝑇) Generally Approaches 𝒟 in Prequential Coding ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")), for any fixed DD we have NT​(D)→∞N\_{T}(D)\\to\\infty as T→∞T\\to\\infty, hence\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | Jpreq​(NT​(D),D;𝒟)→J∞​(D):=∫0Dℒ∞​(u)​𝑑u+(𝒟−D)​ℒ∞​(D).\\displaystyle J\_{\\mathrm{preq}}(N\_{T}(D),D;\\mathcal{D})\\to J\_{\\infty}(D):=\\int\_{0}^{D}\\mathcal{L}\_{\\infty}(u)\\,du+(\\mathcal{D}-D)\\,\\mathcal{L}\_{\\infty}(D). |  | (99) |\
\
Differentiating gives\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | J∞′​(D)=(𝒟−D)​ℒ∞′​(D).\\displaystyle J\_{\\infty}^{\\prime}(D)=(\\mathcal{D}-D)\\,\\mathcal{L}\_{\\infty}^{\\prime}(D). |  | (100) |\
\
Since ℒ∞′​(D)<0\\mathcal{L}\_{\\infty}^{\\prime}(D)<0, we have J∞′​(D)<0J\_{\\infty}^{\\prime}(D)<0 for D<𝒟D<\\mathcal{D} and J∞′​(D)>0J\_{\\infty}^{\\prime}(D)>0 for D>𝒟D>\\mathcal{D}. Thus J∞J\_{\\infty} is uniquely minimized at D=𝒟D=\\mathcal{D}, implying\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | D⋆​(T)→𝒟as ​T→∞.\\displaystyle D^{\\star}(T)\\to\\mathcal{D}\\qquad\\text{as }T\\to\\infty. |  | (101) |\
\
##### Approach from below and linear growth of N⋆​(T)N^{\\star}(T).\
\
By [Theorem˜30](https://arxiv.org/html/2601.03220v2#Thmtheorem30 "Theorem 30 (Monotone growth of compute-optimal 𝑁 and 𝐷) ‣ B.4.1 Monotonicity of 𝑁^∗⁢(𝑇), 𝐷^∗⁢(𝑇), S_𝑇⁢(𝑋), and H_𝑇⁢(𝑋) ‣ B.4 How Epiplexity and Time-Bounded Entropy Scale with Compute and Dataset Size ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), under the complementarity and diminishing-returns assumptions, the compute-optimal training set size D⋆​(T)D^{\\star}(T) is strictly increasing in TT. Combined with the convergence D⋆​(T)→𝒟D^{\\star}(T)\\to\\mathcal{D}, this yields D⋆​(T)↑𝒟D^{\\star}(T)\\uparrow\\mathcal{D}, i.e., D⋆​(T)D^{\\star}(T) approaches 𝒟\\mathcal{D} from below. Finally, since N⋆​(T)=NT​(D⋆​(T))N^{\\star}(T)=N\_{T}(D^{\\star}(T)),\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | N⋆​(T)=T6​D⋆​(T)+2​𝒟∼T8​𝒟,\\displaystyle N^{\\star}(T)=\\frac{T}{6D^{\\star}(T)+2\\mathcal{D}}\\sim\\frac{T}{8\\mathcal{D}}, |  | (102) |\
\
so the compute-optimal model size grows linearly with TT in the large-compute regime.\
\
## Appendix C Experiment Details\
\
Unless otherwise stated, we use the GPT-2 (Radford et al., [2019](https://arxiv.org/html/2601.03220v2#bib.bib78 "")) transformer architecture trained with Adam optimizer. In experiments where we vary the model size, we tune the base learning rate on a small model and transfer it to larger models using using μ\\muP (Yang et al., [2022](https://arxiv.org/html/2601.03220v2#bib.bib107 "")) and CompleteP (Dey et al., [2025](https://arxiv.org/html/2601.03220v2#bib.bib26 "")). In μ\\muP, the per-layer learning rate is base learning rate divided by the input dimension, so our reported base learning rate is larger than typical learning rates used for Adam. The hyperparameters presented below are shared between the teacher and the student for requential coding (width, depth, learning rate, EMA time scale, etc.). As described in [Section˜B.1](https://arxiv.org/html/2601.03220v2#A2.SS1 "B.1 Further details on estimating epiplexity ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), the EMA for the teacher is used only for producing the distillation target and does not alter the raw teacher training dynamics, while the EMA for the student model does alter its training dynamics and is used to replace a decaying learning rate schedule.\
\
### C.1 ECA\
\
In [Figure˜3](https://arxiv.org/html/2601.03220v2#S5.F3 "In 5.1 Paradox 1: Information Cannot be Created by Deterministic Transformations ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), we train the transformer to predict YY given XX where XX is the initial state with a state size of 64 cells and YY is obtained by evolving XX for 48 steps. We apply a burnin period of 1000 steps for sampling the initial state XX to eliminate the less uninteresting transient dynamics from random initialization. That is XX is obtained by evolving the ECA on ZZ for 1000 steps where ZZ is a uniform random initial state. For each rule, we train models with width (embedding dimension) ∈{16,32,64,128,256,512}\\in\\{16,32,64,128,256,512\\} and depth (number of transformer blocks) ∈{1,2,4,6,9}\\in\\{1,2,4,6,9\\}. We train both teacher and student using batches of 1536 sequences (each an (X,Y)(X,Y) pair), a base learning rate of 0.03 with 100 warmup steps, and an EMA time scale of 50 steps (half-life divided by ln⁡(2)\\ln(2)). We did not set a max teacher-student KL as the student smoothly trackes the teacher throughout training. The epiplexity and time-bounded entropy is estimated for a test set of size 𝒟=100\\mathcal{D}=100M tokens (counting YY only).\
\
### C.2 Easy induction\
\
For this task, we use a sequence length of n=512n=512 (as described in [Section˜5.3.1](https://arxiv.org/html/2601.03220v2#S5.SS3.SSS1 "5.3.1 Induction ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")). The model has 3 layers and a width of 128, and is trained with a learning rate of 0.03 and a batch size of 384 sequences for 3000 steps with 15 warmup steps and an EMA time scale of 50 steps. We found further increasing the model size led to negligible improvement in the loss, and [Figure˜5](https://arxiv.org/html/2601.03220v2#S5.F5 "In 5.3.1 Induction ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") shows that the model has nearly converged by the end of training to the theoretical minimum loss, so there is no need to further increase the training data. As a result, we expect the epiplexity ST​(X)\\mathrm{S}\_{T}(X) to stabilize as TT and 𝒟=\|X\|\\mathcal{D}=\|X\| increases (in the relevant regime where TT is still much less than what is required for implementing the brute-force solution that enumerates all possible combinations of hidden entries in the transition matrix), and our estimated epiplexity approximates this stabilized value.\
\
### C.3 Hard induction\
\
We modify the ECA experiment in [Section˜C.1](https://arxiv.org/html/2601.03220v2#A3.SS1 "C.1 ECA ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") to remove the first h∈{0,1,…,5}h\\in\\{0,1,\\ldots,5\\} bits in XX when fed to the model as input. We use a state size of 32, batch size of 1536 sequences, learning of 0.03, EMA time scale of 100 steps. We set the max KL threshold between the teacher and student as 0.03 (nats per token). To construct a forward function that is hard to invert, we use rule 30 iterated for 4 steps. We train models with 3 layers and width 256 for 20000. Further increasing model size or training data led to no improvement in the loss. As [Figure˜5](https://arxiv.org/html/2601.03220v2#S5.F5 "In 5.3.1 Induction ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") shows, the models converge by the end of training (the loss curves shown are for the student models, but the teacher models also converge) to the theoretical minimum values. Therefore, like the case for [Section˜C.2](https://arxiv.org/html/2601.03220v2#A3.SS2 "C.2 Easy induction ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), we expect the epiplexity ST​(X)\\mathrm{S}\_{T}(X) to stabilize as TT and 𝒟=\|X\|\\mathcal{D}=\|X\| increases, at least in the relevant regime where TT is still much less than what is required for implementing the brute-force solution that enumerates all possible combinations of hidden bits, and our estimated epiplexity approximates this stabilized value.\
\
### C.4 Chess\
\
We train models of varying sizes from 1M to 160M parameters with depth between 33 and 2424 layers. The base learning rate is set to 22 and the batch size is 256, with a sequence length of 512. We set the EMA time scale to 50 steps and max KL to 0.1 nats per token. We use character-level tokenization. The teacher models are trained for 5B tokens in total, and the student models are trained for slightly more due to hitting the max KL threshold during training. The test set size is set to 55B tokens.\
\
##### Pre-Training Data.\
\
We use the Lichess dataset available on Hugging Face at [https://huggingface.co/datasets/Lichess/standard-chess-games](https://huggingface.co/datasets/Lichess/standard-chess-games "") as pre-training data, formatted as either "<board>\|<moves>" or "<moves>\|<board>", where moves are in algebraic chess notation and board is the final board state in FEN notation. We use a slightly more concise version of the algebraic notation to further compress the move sequence. An example input where the board appears last is:\
\
```\
e4,e5;Nf3,Nc6;Bb5,a6;Ba4,Nf6;O-O,Be7;Re1,b5;Bb3,d6;c3,O-O;h3,Nb8;d4,Nbd7;\
|r1bq1rk1/2pnbppp/p2p1n2/1p2p3/3PP3/1BP2N1P/PP3PP1/RNBQR1K1 w - - 0 10\
```\
\
For downstream evaluation, we evaluate performance on the following two datasets after fine-tuning on 5050k examples for a 10M-parameter model with depth 24. We report accuracy under greedy decoding at zero temperature.\
\
##### Chess Puzzles.\
\
We use puzzles from the Lichess puzzle database available at [https://huggingface.co/datasets/EleutherAI/lichess-puzzles](https://huggingface.co/datasets/EleutherAI/lichess-puzzles ""), filtering for puzzles with difficulty rating above 2000. The task is to predict the correct move sequence given the game context. Puzzles are formatted as move sequences where the model must predict the next optimal move, following (Burns et al., [2023](https://arxiv.org/html/2601.03220v2#bib.bib17 "")), with only the target moves included in the loss computation via masking. This tests the model’s ability to recognize tactical patterns and calculate forced sequences.\
\
##### Centipawn Evaluation.\
\
We evaluate position understanding using the Lichess chess position evaluations dataset at [https://huggingface.co/datasets/Lichess/chess-position-evaluations](https://huggingface.co/datasets/Lichess/chess-position-evaluations ""), where models classify positions into 9 evaluation buckets based on Stockfish centipawn (cp) scores: class 0 (≤−800\\leq-800cp), class 1 (−800-800 to −400-400cp), class 2 (−400-400 to −200-200cp), class 3 (−200-200 to −50-50cp), class 4 (−50-50 to +50+50cp), class 5 (+50+50 to +200+200cp), class 6 (+200+200 to +400+400cp), class 7 (+400+400 to +800+800cp), and class 8 (≥+800\\geq+800cp). Examples are formatted as "<board>\|<class>" where the model predicts the evaluation class, with mate positions assigned to the extreme classes (0 or 8). Loss during fine-tuning is computed only for predicting the class.\
\
### C.5 OpenWebText\
\
We use the OpenWebText dataset at [https://huggingface.co/datasets/Skylion007/openwebtext](https://huggingface.co/datasets/Skylion007/openwebtext ""), keeping only documents containing only 96 common alphanumeric symbols, and apply character-level tokenization. The setup is otherwise identical to the chess experiment ( [Section˜C.4](https://arxiv.org/html/2601.03220v2#A3.SS4 "C.4 Chess ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")).\
\
### C.6 CIFAR-5M\
\
We use the CIFAR-5M dataset at [https://github.com/preetum/cifar5m](https://github.com/preetum/cifar5m ""). We convert the 32×32×332\\times 32\\times 3 images to greyscale and flatten to a 1D sequence of 1024 in raster-scan order. The vocabulary is the set of pixel intensities {0,…,255}\\{0,\\ldots,255\\}. The setup is otherwise identical to the chess experiment ( [Section˜C.4](https://arxiv.org/html/2601.03220v2#A3.SS4 "C.4 Chess ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence")).\
\
### C.7 Prequential vs Requential Comparison\
\
##### ECA.\
\
The ECA experiment include rules {0,32,4,15,22,30,41,54,106,110},\\{0,32,4,15,22,30,41,54,106,110\\}, covering all 4 classes. We train models with width ∈{16,32,64,128}\\in\\{16,32,64,128\\} and depth ∈{1,2,3}\\in\\{1,2,3\\} up to 10000 steps. We use a base learning rate of 0.03 and batch size of 384. Other hyperparameters are identical to [Section˜C.1](https://arxiv.org/html/2601.03220v2#A3.SS1 "C.1 ECA ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). We set 𝒟=250\\mathcal{D}=250M tokens. For each rule, we report the maximum epiplexity over the resulting compute range.\
\
##### Induction.\
\
Both the easy and hard induction results directly come from the experiments in [Section˜5.3.1](https://arxiv.org/html/2601.03220v2#S5.SS3.SSS1 "5.3.1 Induction ‣ 5.3 Paradox 3: Likelihood Modeling is Merely Distribution Matching ‣ 5 Three Apparent Paradoxes of Information ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). As explained in [Section˜C.2](https://arxiv.org/html/2601.03220v2#A3.SS2 "C.2 Easy induction ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") and [Section˜C.3](https://arxiv.org/html/2601.03220v2#A3.SS3 "C.3 Hard induction ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), the compute budget TT and test set size 𝒟\\mathcal{D} need not be precisely specified for these two tasks as the epiplexity stabilizes as TT and 𝒟\\mathcal{D} increase due to the convergent training dynamics.\
\
##### Natural data.\
\
We report the estimated epiplexity on each dataset at the maximum tested compute budget as described in [Section˜C.4](https://arxiv.org/html/2601.03220v2#A3.SS4 "C.4 Chess ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), [Section˜C.5](https://arxiv.org/html/2601.03220v2#A3.SS5 "C.5 OpenWebText ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"), and [Section˜C.6](https://arxiv.org/html/2601.03220v2#A3.SS6 "C.6 CIFAR-5M ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
\
### C.8 ECA Emergence\
\
We modify the setup in [Section˜C.1](https://arxiv.org/html/2601.03220v2#A3.SS1 "C.1 ECA ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") to include models that predict intermediate states and the final state rather than the final state directly. Let X(0)X^{(0)} denote the initial ECA state, and X(s)X^{(s)} denote it evolved for ss steps. For an ℓ\\ell-loop model, we train the model to predict (X(Δ),X(2​Δ),…,X(t))(X^{(\\Delta)},X^{(2\\Delta)},\\ldots,X^{(t)}) instead of X(t)X^{(t)} only, where Δ=t/ℓ.\\Delta=t/\\ell. Its marginal probability on the final state is lower-bounded by its joint probability on the ground truth trajectory:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | P​(X(t))=∑X′⁣(Δ),…,X′⁣(t−Δ)P​(X′⁣(Δ),…,X′⁣(t−Δ),X(t))P(X^{(t)})=\\sum\_{X^{\\prime(\\Delta)},\\ldots,X^{\\prime(t-\\Delta)}}P\\!\\big(X^{\\prime(\\Delta)},\\ldots,X^{\\prime(t-\\Delta)},X^{(t)}\\big) |  | (103) |\
\
So we upper-bound its NLL as\
\
|     |     |     |     |     |\
| --- | --- | --- | --- | --- |\
|  | log⁡1P​(X(t))\\displaystyle\\log\\frac{1}{P(X^{(t)})} | ≤log⁡1P​(X(Δ),…,X(t))\\displaystyle\\leq\\log\\frac{1}{P\\!\\big(X^{(\\Delta)},\\ldots,X^{(t)}\\big)} |  |\
|  |  | =∑k=1ℓlog⁡1P​(X(k​Δ)∣X((k−1)​Δ),…,X(Δ)),\\displaystyle=\\sum\_{k=1}^{\\ell}\\log\\frac{1}{P\\!\\big(X^{(k\\Delta)}\\mid X^{((k-1)\\Delta)},\\ldots,X^{(\\Delta)}\\big)}, |  | (104) |\
\
We account for the intermediate tokens when computing the time bound and the code length (they contribute to the model code length as well as the data entropy code length).\
In the experiment, we set the ECA steps to t=64.t=64. We train models with width {16,32,64,128},\\{16,32,64,128\\}, depth ∈{1,2,4,8,16,32},\\in\\{1,2,4,8,16,32\\}, and number of loops ℓ∈{1,2,4,8,16}.\\ell\\in\\{1,2,4,8,16\\}. We found ℓ∈{2,4,8}\\ell\\in\\{2,4,8\\} has no advantage over the non-looped model (ℓ=1\\ell=1) in terms of the two-part code, only ℓ=16\\ell=16 does. We therefore refer to ℓ=1\\ell=1 as non-looped and ℓ=16\\ell=16 as looped. The fact that a small ℓ>1\\ell>1 is not helpful is likely because the overhead of encoding and generating intermediate states exceeds the savings from only slightly simplifying each prediction step, as the per-step prediction horizon is still significant. We train all models with a base learning rate of 0.06, batch size of 147456 tokens, warmup of 100 steps, and EMA time scale of 50 steps. We did not set a max teacher-student KL. The test set size is set to 𝒟=100\\mathcal{D}=100M final state tokens.\
\
### C.9 Scaling Laws\
\
We estimate epiplexity and time-bounded entropy using the expressions derived in [Section˜B.3](https://arxiv.org/html/2601.03220v2#A2.SS3 "B.3 A Solvable Model Using Scaling Laws ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") for prequential coding using existing scaling laws for ℒ​(N,D)\\mathcal{L}(N,D). We solve for the optimal training tokens D⋆​(T)D^{\\star}(T) as a function of compute using root finding for [Equation˜56](https://arxiv.org/html/2601.03220v2#A2.E56 "In Solution. ‣ B.3 A Solvable Model Using Scaling Laws ‣ Appendix B Measuring Epiplexity ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence"). For language, we use the Chinchilla scaling laws from Hoffmann et al. ( [2022](https://arxiv.org/html/2601.03220v2#bib.bib49 "")), which were fit to total parameter counts. For all other modalities (images and video), we use the scaling laws from Henighan et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib48 "")), which follow the methodology of Kaplan et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib53 "")) and report non-embedding parameter counts. We correct these to use total parameters following Pearce and Song ( [2024](https://arxiv.org/html/2601.03220v2#bib.bib75 "")), as described below.\
\
##### Correcting for embedding parameters.\
\
The scaling laws in Kaplan et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib53 "")) and Henighan et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib48 "")) are reported in terms of non-embedding parameters N\EN\_{\\backslash E} and non-embedding compute C\EC\_{\\backslash E}, excluding embedding and unembedding parameters. As shown by Pearce and Song ( [2024](https://arxiv.org/html/2601.03220v2#bib.bib75 "")), this choice—combined with smaller model scales—accounts for much of the discrepancy between the Kaplan and Chinchilla scaling laws. Following their approach, we relate total parameters NN to non-embedding parameters via\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | N=N\E+ω​N\E1/3,ω=(V+Lctx)​(A12)1/3,\\displaystyle N=N\_{\\backslash E}+\\omega N\_{\\backslash E}^{1/3},\\qquad\\omega=(V+L\_{\\mathrm{ctx}})\\quantity(\\frac{A}{12})^{1/3}, |  | (105) |\
\
where VV is the vocabulary size, LctxL\_{\\mathrm{ctx}} is the context length, and AA is the aspect ratio (width/depth)\\mathrm{width}/\\mathrm{depth}). We use A=5A=5 as Henighan et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib48 "")) showed the optimal aspect ratio is around this value for non-language datasets. We generate points (C\E,N\E,L)(C\_{\\backslash E},N\_{\\backslash E},L) from the original scaling laws, convert to (C,N,ℒ)(C,N,\\mathcal{L}) using this relation (with total compute as C=C\E⋅N/N\EC=C\_{\\backslash E}\\cdot N/N\_{\\backslash E}), and refit the power-law exponents and the irreducible loss.\
\
##### Parameterization conversion.\
\
The scaling laws in Henighan et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib48 "")) are reported in compute-centric form, expressing the optimal loss L⋆​(C)=(C/C0)−γ+EL^{\\star}(C)=(C/C\_{0})^{-\\gamma}+E and optimal model size N⋆​(C)=(C/C^)δN^{\\star}(C)=(C/\\hat{C})^{\\delta} as functions of compute budget CC. We convert these to the (N,D)(N,D) parameterization used in this work:\
\
|     |     |     |     |\
| --- | --- | --- | --- |\
|  | ℒ​(N,D)=(NN0)−α+(DD0)−β+E,\\displaystyle\\mathcal{L}(N,D)=\\quantity(\\frac{N}{N\_{0}})^{-\\alpha}+\\quantity(\\frac{D}{D\_{0}})^{-\\beta}+E, |  | (106) |\
\
where the exponents transform as α=γ/δ\\alpha=\\gamma/\\delta and β=γ/(1−δ)\\beta=\\gamma/(1-\\delta), and the token scale is given by D0=C^6​N0α/β​(β/α)−1/βD\_{0}=\\frac{\\hat{C}}{6}N\_{0}^{\\alpha/\\beta}(\\beta/\\alpha)^{-1/\\beta}.\
\
##### Corrected parameters.\
\
[Table˜1](https://arxiv.org/html/2601.03220v2#A3.T1 "In Corrected parameters. ‣ C.9 Scaling Laws ‣ Appendix C Experiment Details ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence") presents the corrected scaling law parameters used in our final calculations.\
\
Table 1: Final scaling law parameters used. Image and video domains from Henighan et al. ( [2020](https://arxiv.org/html/2601.03220v2#bib.bib48 "")) are corrected for embedding parameters using aspect ratio A=5A=5 following (Pearce and Song, [2024](https://arxiv.org/html/2601.03220v2#bib.bib75 "")); Chinchilla (language) from Hoffmann et al. ( [2022](https://arxiv.org/html/2601.03220v2#bib.bib49 "")) was originally fit to total parameter counts and requires no correction. D0D\_{0} is measured in tokens and EE is measured in nats.\
\
| Domain | α\\alpha | β\\beta | N0N\_{0} | D0D\_{0} | EE |\
| --- | --- | --- | --- | --- | --- |\
| Image 8×\\times8 | 0.331 | 0.566 | 8.0×1018.0\\times 10^{1} | 2.66×1062.66\\times 10^{6} | 3.14 |\
| Image 16×\\times16 | 0.307 | 0.820 | 2.8×1022.8\\times 10^{2} | 8.94×1078.94\\times 10^{7} | 2.68 |\
| Image 32×\\times32 | 0.258 | 0.399 | 6.3×1016.3\\times 10^{1} | 1.95×1061.95\\times 10^{6} | 2.30 |\
| Image VQ 16×\\times16 | 0.322 | 0.441 | 2.7×1042.7\\times 10^{4} | 4.44×1074.44\\times 10^{7} | 4.23 |\
| Image VQ 32×\\times32 | 0.287 | 0.560 | 1.9×1041.9\\times 10^{4} | 1.63×1081.63\\times 10^{8} | 3.32 |\
| Video VQ 163 | 0.428 | 0.718 | 3.7×1043.7\\times 10^{4} | 1.79×1081.79\\times 10^{8} | 1.15 |\
| Language (Chinchilla) | 0.339 | 0.285 | 4.91×1074.91\\times 10^{7} | 1.49×1091.49\\times 10^{9} | 1.69 |\
\
## Appendix D RASP-L for Elementary Cellular Automata\
\
Below we provide RASP-L code (Zhou et al., [2023](https://arxiv.org/html/2601.03220v2#bib.bib111 "")) demonstrating how the evolution rule of an ECA can be implemented, providing evidence that the solution can be expressed within an autoregressive transformer model.\
\
Listing 1: RASPL implementation of a cellular automaton evolution step\
\
[⬇](data:text/plain;base64,ZnJvbSBucF9yYXNwIGltcG9ydCAqCgpkZWYgaW50MmJpdHMoeCwgYml0cz04KTogIyByZXR1cm5zIExTQiBmaXJzdAogICAgIiIiIEhlbHBlciBmdW5jdGlvbiB0byBnZW5lcmF0ZSBmaXhlZCBiaXRzdHJpbmcgcmVwcmVzZW50aW5nIGEgbnVtYmVyLgogICAgTm90IFJBU1AtTCwgY2FuIGJlIGFzc3VtZWQgY29uc3RhbnQuIiIiCiAgICBiaXRzX3N0ciA9IGJpbih4KVsyOl0uemZpbGwoYml0cykKICAgIHJldHVybiBucC5hcnJheShsaXN0KG1hcChpbnQsYml0c19zdHJbOjotMV0pKSxkdHlwZT1ucC51aW50OCkKCnNlcCA9IC0xCnNlcDIgPSAtMgpkZWYgZXZvbHZlX2NhKHgsIHJ1bGUpOgogICAgIiIiIEZ1bmN0aW9uIHRvIGF1dG9yZWdyZXNzaXZlbHkgb3V0cHV0IHByb2R1Y2UgdGhlIG91dHB1dCBvZiBvbmUgc3RlcCBvZiB0aGUgRUNBIHJ1bGUuIFByb2JsZW0gZW5jb2RlZCBhcyB4PSAtLWlucHV0IHN0YXRlLS0sc2VwLHNlcDIsLS1vdXRwdXQgc3RhdGUtLS4KICAgIFJ1bGU6IGludCAoc3BlY2lmeWluZyB0aGUgRUNBKSIiIgogICAgbG9va3VwID0gaW50MmJpdHMocnVsZSwgOCkKICAgIGluX2lucHV0ID0gMSAtIGhhc19zZWVuKHgsIGZ1bGwoeCwgc2VwKSkKICAgIGluX2lucHV0MiA9IDEgLSBoYXNfc2Vlbih4LCBmdWxsKHgsIHNlcDIpKQogICAgd2lkdGggPSBjdW1zdW0oaW5faW5wdXQpICAjIG9ubHkgdmFsaWQgYWZ0ZXIgc2VwCiAgICBpZHggPSBpbmRpY2VzKHgpCiAgICBjaXJjX3ggPSB3aGVyZShpbl9pbnB1dCwgeCwgaW5kZXhfc2VsZWN0KHgsIGlkeCAtIHdpZHRoKSkKICAgIHByZXYgPSBzaGlmdF9yaWdodCh4LCAxKQogICAgY3ByZXYgPSB3aGVyZShpbl9pbnB1dDIsIHByZXYsIGluZGV4X3NlbGVjdChwcmV2LCBpZHggLSB3aWR0aCkpCiAgICBwcmV2MiA9IHNoaWZ0X3JpZ2h0KHgsIDIpCiAgICBuYmhkID0gKHByZXYyIDw8IDIpICsgKGNwcmV2IDw8IDEpICsgY2lyY194CiAgICBzaGlmdGVkX25leHRzdGF0ZSA9IGxvb2t1cFtuYmhkXQogICAgdG9fc2VsZWN0X2lkeCA9IGlkeCAtIHdpZHRoCiAgICB0b19zZWxlY3RfaWR4ID0gd2hlcmUodG9fc2VsZWN0X2lkeCA8IDMsIGlkeCwgdG9fc2VsZWN0X2lkeCkKICAgIG91dHN0YXRlID0gaW5kZXhfc2VsZWN0KHNoaWZ0ZWRfbmV4dHN0YXRlLCB0b19zZWxlY3RfaWR4KQogICAgcmV0dXJuIG91dHN0YXRl)\
\
fromnp\_raspimport\*\
\
defint2bits(x,bits=8):#returnsLSBfirst\
\
"""Helperfunctiontogeneratefixedbitstringrepresentinganumber.\
\
NotRASP-L,canbeassumedconstant."""\
\
bits\_str=bin(x)\[2:\].zfill(bits)\
\
returnnp.array(list(map(int,bits\_str\[::-1\])),dtype=np.uint8)\
\
sep=-1\
\
sep2=-2\
\
defevolve\_ca(x,rule):\
\
"""FunctiontoautoregressivelyoutputproducetheoutputofonestepoftheECArule.Problemencodedasx=--inputstate--,sep,sep2,--outputstate--.\
\
Rule:int(specifyingtheECA)"""\
\
lookup=int2bits(rule,8)\
\
in\_input=1-has\_seen(x,full(x,sep))\
\
in\_input2=1-has\_seen(x,full(x,sep2))\
\
width=cumsum(in\_input)#onlyvalidaftersep\
\
idx=indices(x)\
\
circ\_x=where(in\_input,x,index\_select(x,idx-width))\
\
prev=shift\_right(x,1)\
\
cprev=where(in\_input2,prev,index\_select(prev,idx-width))\
\
prev2=shift\_right(x,2)\
\
nbhd=(prev2<<2)+(cprev<<1)+circ\_x\
\
shifted\_nextstate=lookup\[nbhd\]\
\
to\_select\_idx=idx-width\
\
to\_select\_idx=where(to\_select\_idx<3,idx,to\_select\_idx)\
\
outstate=index\_select(shifted\_nextstate,to\_select\_idx)\
\
returnoutstate\
\
## Appendix E Cellular Automata and Game of Life\
\
Elementary cellular automata\
Elementary cellular automata (ECA) (Wolfram and Gad-el Hak, [2003](https://arxiv.org/html/2601.03220v2#bib.bib104 "")) are one-dimensional cellular automata defined on a finite or infinite line of cells, each in one of two states: 0 or 1. The system evolves in discrete time steps according to local rules: a cell’s next state depends only on its current state and those of its two immediate neighbors, yielding 23=82^{3}=8 possible neighborhood configurations. Since each configuration can map to either 0 or 1, there are 28=2562^{8}=256 possible rules, conventionally numbered 0–255 using Wolfram’s notation, where the rule number’s binary representation specifies the output for each neighborhood. Despite their simplicity, ECAs exhibit diverse behaviors ranging from trivial (e.g., Rule 0) to complex and chaotic (e.g., Rule 30), with Rule 54 proven to be Turing-complete. These systems serve as minimal models for studying emergence, computation, and the relationship between local rules and global behavior.\
\
Conways Game of Life\
Conway’s Game of Life (Gardner, [1970](https://arxiv.org/html/2601.03220v2#bib.bib35 "")) is a cellular automaton defined on an infinite two-dimensional grid of cells, each in one of two states: alive (1) or dead (0). The system evolves in discrete time steps according to deterministic local rules: a cell’s next state depends only on its current state and those of its eight neighbors. Specifically, a live cell survives if it has exactly 2 or 3 live neighbors (otherwise it dies), while a dead cell becomes alive if it has exactly 3 live neighbors (otherwise it remains dead). Despite the simplicity of these rules, the Game of Life exhibits remarkably complex emergent behavior, including stable structures (blocks), periodic oscillators (blinkers), mobile patterns (gliders), and structures that generate infinite streams of gliders (glider guns). The system also happens to be Turing-complete, with a specific initial configuration specifying the program, it is capable of universal computation.\
\
## Appendix F Emergence\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x20.png)(a)\
\
![Refer to caption](https://arxiv.org/html/2601.03220v2/x21.png)(b)\
\
Figure 11: LLMs can learn the invariant measure of chaotic systems despite unpredictable trajectories.\
(a) Chaotic systems like the Lorenz equations display sensitive dependence on initial conditions. Tiny perturbations to the initial conditions (orange) diverge exponentially, making long-term predictions impossible when simulating with limited computation and precision on a computer.\
(b) 30003000 sampled points from the distribution modeled by the LLM (left) and from the invariant measure of the Lorenz system (right). Color denotes kernel density estimation of each density.\
\
Lorenz System and Chaotic Dynamics\
For the Lorenz system, a canonical example of a chaotic ODE, we can observe a different kind of emergence (Type-0 in Carroll and Parola ( [2024](https://arxiv.org/html/2601.03220v2#bib.bib18 ""))). There exists a canonical invariant measure in dynamical systems (under some regularity conditions) known as the SRB measure(Metzger, [2000](https://arxiv.org/html/2601.03220v2#bib.bib69 "")). States evolved for a long time in the Lorenz system will converge this measure. As the Lorenz system is chaotic, tiny perturbations are exponentially amplified through time at a rate related to the largest Lyapunov exponent λ1≈0.9\\lambda\_{1}\\approx 0.9. There is a precise sense in which entropy is created in this system at a rate of λ1​log2⁡(e)\\lambda\_{1}\\log\_{2}(e) bits per second, formalized through Pesin’s theorem (Pesin, [1977](https://arxiv.org/html/2601.03220v2#bib.bib77 "")), despite the fact that it is a purely deterministic process. Intuitively one can see this picture when simulating the system using fixed precision numbers, and seeing log2⁡(e)\\log\_{2}(e) bits of that description replaced with unpredictable random content after every Lyapunov time 1/λ11/\\lambda\_{1}. On the one hand randomness is produced, but it is not uniformly random. Rather, there is a stationary measure in the shape of a butterfly, and an observer who has lost track of all previous bits due to chaos can still learn the shape of the butterfly. Moreover, the shape of the stationary measure is not immediately obvious from the ODE, it is emergent and cannot easily be understood without intensive numerical simulation of the system (hence why most of chaos theory was developed after computers).\
\
To demonstrate this interplay, we train a language model to predict the first B=10B=10 bits of the future state Φt​(X)\\Phi\_{t}(X) from an initial state sampled uniformly from the box X∼U​\[−20,20\]3+20​\[0,0,1\]X\\sim U\[-20,20\]^{3}+20\[0,0,1\] quantized to BB bits, in comparison to directly modeling Φt​(X)\\Phi\_{t}(X). For both we set the time tt to be 3030 Lyapunov times into the future, t=30/λ1t=30/\\lambda\_{1}. The resulting model has a nearly identical loss and estimated epiplexity in the two settings. Despite being unable to distinguish the initial conditions, the LLM learns the invariant (SRB) measure to a reasonable approximation as shown in [Figure 11](https://arxiv.org/html/2601.03220v2#A6.F11 "Figure 11 ‣ Appendix F Emergence ‣ From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence").\
With very limited compute the stationary measure is not predictable apriori from the dynamics, but with more compute it is merely a consequence. The epiplexity of the attractor for limited compute may be larger than a description of the dynamics ST​(Φt​(X))>ST​(Φ,t)\\mathrm{S}\_{T}(\\Phi\_{t}(X))>\\mathrm{S}\_{T}(\\Phi,t).\
\
Chess: AlphaZero and Minimax\
A qualitatively different kind of example can be had by considering the models produced by AlphaZero (Silver et al., [2018](https://arxiv.org/html/2601.03220v2#bib.bib90 "")) and the theoretically optimal minimax solution for these two player zero sum perfect information games (von Neumann, [1928](https://arxiv.org/html/2601.03220v2#bib.bib99 ""); Shannon, [1950](https://arxiv.org/html/2601.03220v2#bib.bib88 "")). The minimax strategy can be implemented by a short program, and with sufficient compute (exponential in the size of the board (Fraenkel and Lichtenstein, [1981](https://arxiv.org/html/2601.03220v2#bib.bib33 ""))) the optimal strategy can be found. On the other hand the CNN policy and value network produced by AlphaZero contain 1010s of millions of parameters. Given that the rules of chess can be encoded in just a few hundred bytes, and the algorithm used to train the model can be simply described and also implemented by a short program, one may wonder _where does this information come from?_ With the other examples of emergent phenomena in mind, we can make sense of this information being produced by the computational process of the AlphaZero system. In contrast, with unbounded compute, the best strategy contains little information.\
\
To summarize, due to the existence of emergent phenomena, even systems that have simple generating processes or simple descriptions can lead to large amounts of structural information to be learned by computationally constrained observers.\
\
## Appendix G Induction is Not Specific to Autoregressive Factorization\
\
One might get the impression that key constraint that leads to this induction phenomenon is the autoregressive factorization, as it is intuitive to see how such a model needs to perform induction in-context to achieve minimum loss. However, we argue this phenomenon takes place with other classes of generative models trained as long as they are trained with Maximum Likelihood Estimation (MLE) or its approximations.\
\
In MLE, a generative model allowing explicit likelihood evaluation is trained to maximize the likelihood of the data. Computing the likelihood can be significantly more computationally challenging than sampling from the distribution P.P. This distinction is particularly clear in the examples we gave where the ground-truth PP is a mixture distribution represented by a latent variable model with the CA initial state or Markov chain transition matrix acting as the latent variable ZZ. Given access to PX\|ZP\_{X\|Z} (equivalent to some easy to implement forward function FF), sampling is easy as long as PZP\_{Z} is a simple, but computing PX​(x)P\_{X}(x) for some input xx requires evaluating an intractable integral PX​(x)=∫PX\|Z​(x\|z)​PZ​(z)​𝑑zP\_{X}(x)=\\int P\_{X\|Z}(x\|z)P\_{Z}(z)\\,dz due to the high-dimensionality of Z.Z. As such, a model given a limited compute-budget is forced to learn a cheaper but more sophisticated algorithm for computing PX​(x),P\_{X}(x), often involving approximating the inverse PZ\|XP\_{Z\|X} either explicitly as done in expectation–maximization-type algorithms and Variational Autoencoders (Kingma et al., [2013](https://arxiv.org/html/2601.03220v2#bib.bib54 "")), or implicitly as we illustrated for the autoregressive transformer.\
\
## Appendix H Minimum Description Legnth\
\
Intuitively, L​(H)L(H) can be interpreted as the structural information, and −log⁡P​(x∣H)-\\log P(x\\mid H) can be understood as the remaining random information that cannot be predicted by the best model in ℋ\\mathcal{H}.\
A main problem with the crude two-part code is that it does not prescribe how one should design the code for HH (i.e., a procedure for describing HH within ℋ\\mathcal{H}).\
The description of a particular HH can be short under one code but very large under another, which could require additional knowledge to resolve.\
To circumvent this issue, one can use a more refined one-part code that describes the data with the entire model class ℋ\\mathcal{H} rather than any single model HH. One of the most important one-part codes is the normalized maximum likelihood code.\
\
###### Definition 31 (Normalized maximum likelhood code (Grünwald, [2007](https://arxiv.org/html/2601.03220v2\#bib.bib43 "")))\
\
The NML distribution PℋNML:{0,1}n×d→\[0,1\]P^{\\mathrm{NML}}\_{\\mathcal{H}}:\\{0,1\\}^{n\\times d}\\rightarrow\[0,1\] of a probablistic model class ℋ\\mathcal{H} is:\
\
|     |     |     |\
| --- | --- | --- |\
|  | PℋNML​(x)=P​(x∣H^​(x))∑y∈{0,1}n×dP​(y∣H^​(y)),P^{\\mathrm{NML}}\_{\\mathcal{H}}(x)=\\frac{P(x\\mid\\widehat{H}(x))}{\\sum\_{y\\in\\{0,1\\}^{n\\times d}}P(y\\mid\\widehat{H}(y))}, |  |\
\
where H^​(x)=arg​maxH∈ℋ⁡P​(x∣H)\\widehat{H}(x)=\\operatorname\*{arg\\,max}\_{H\\in\\mathcal{H}}P(x\\mid H) is the maximum likelihood estimator for xx.\
\
Crucially, notice that the NML code only depends on ℋ\\mathcal{H} rather than any particular H∈ℋH\\in\\mathcal{H}, so we do not have to design a particular code for HH.\
Unfortunately, the NML code requires integrating over the maximum likelihood estimator for all possible data, which is intractable for most practical models such as deep neural networks.\
We can instead use a more tractable variant of one-part code based on sequential prediction called prequential coding.\
\
###### Definition 32 (Prequential code (Grünwald, [2007](https://arxiv.org/html/2601.03220v2\#bib.bib43 "")))\
\
The prequential distribution PℋPREQ:{0,1}n×d→\[0,1\]P^{\\mathrm{PREQ}}\_{\\mathcal{H}}:\\{0,1\\}^{n\\times d}\\rightarrow\[0,1\] of a probabilistic model class ℋ\\mathcal{H} is:\
\
|     |     |     |\
| --- | --- | --- |\
|  | PℋPREQ​(x)=∏k=1nP​(xk∣H^​(x1:k)),P^{\\mathrm{PREQ}}\_{\\mathcal{H}}(x)=\\prod\_{k=1}^{n}P(x\_{k}\\mid\\widehat{H}(x\_{1:k})), |  |\
\
where H^​(x1:k)=arg​maxH∈ℋ⁡P​(x1:k∣H)\\widehat{H}(x\_{1:k})=\\operatorname\*{arg\\,max}\_{H\\in\\mathcal{H}}P(x\_{1:k}\\mid H) is the MLE for the first kk elements of xx.\
\
This definition above uses the MLE for updating H^\\widehat{H} but there are in fact no constraints on how the update is performed.\
We may use any update method of our choice to produce the next model in the sequence, so long as it only depends on the previous data.\
This means that we can naturally adapt it for deep learning, where we use stochastic gradient descent to update the model sequentially.\
\
A code cannot be optimal simultaneously for all possible data xx unless it has knowledge of the particular xx. Therefore, it is useful to characterize how close a given code is to the optimal model, which can be formalized via the notion of _regret_.\
\
###### Definition 33 (Regret (Grünwald, [2007](https://arxiv.org/html/2601.03220v2\#bib.bib43 "")))\
\
The regret of a code QQ relative to ℋ\\mathcal{H} for xx is the additional number of bits needed to encode xx using QQ compared to the best model in hindsight,\
\
|     |     |     |\
| --- | --- | --- |\
|  | 𝖱𝖾𝗀​(Q,ℋ,x)=−log⁡Q​(x)−minH∈ℋ⁡{−log⁡P​(x∣H)}.\\mathsf{Reg}(Q,\\mathcal{H},x)=-\\log Q(x)-\\min\_{H\\in\\mathcal{H}}\\{-\\log P(x\\mid H)\\}. |  |\
\
Under this notion of penalty, the NML is optimal in the sense that it achieves the minimax regret.\
The regret provides a way to compare different codes.\
Consider the two-part regret of the crude two-part code P2​P​(⋅)P^{\\mathrm{2P}}(\\cdot) with minimizer H⋆H^{\\star} and associated predictive distribution P(⋅∣H⋆)P(\\cdot\\mid H^{\\star}),\
\
|     |     |     |\
| --- | --- | --- |\
|  | 𝖱𝖾𝗀​(P2​P,ℋ,x)=L​(H⋆)+log⁡1P​(x∣H⋆)−log⁡1P​(x∣H^).\\mathsf{Reg}(P^{\\mathrm{2P}},\\mathcal{H},x)=L(H^{\\star})+\\log\\frac{1}{P(x\\mid H^{\\star})}-\\log\\frac{1}{P(x\\mid\\widehat{H})}. |  |\
\
This means that for a two-part code, the regret is an upper bound on the description length of the model.\
For sufficiently large nn, the last two terms become close to each other and 𝖱𝖾𝗀​(P2​P,ℋ,x)≈L​(H⋆)\\mathsf{Reg}(P^{\\mathrm{2P}},\\mathcal{H},x)\\approx L(H^{\\star}).\
In the case of NML, the regret is the minimax regret that 𝖱𝖾𝗀​(PℋNML,ℋ,x)=log​∑y∈{0,1}nP​(y∣H^​(y))\\mathsf{Reg}(P^{\\mathrm{NML}}\_{\\mathcal{H}},\\mathcal{H},x)=\\log\\sum\_{y\\in\\{0,1\\}^{n}}P(y\\mid\\widehat{H}(y)).\
This quantity is independent of xx, which is also called _parametric complexity_ of ℋ\\mathcal{H}, because it measures how expressive the entire _model class_ is by counting the total amount of possible data sequences the model class can model well.