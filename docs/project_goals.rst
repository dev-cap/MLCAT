What does MLCAT plan to accomplish?
===============================================

This project aims to cover some of the most prevalent issues and topics in social networking. It can be used to identify the community structure in a mailing list, track the community of experts on channels, form different types of graphs for making predictive models, assign weights based on the activeness or response times for each user amongst various other activities.

===========================
Overall Research Objectives
===========================

The objective of this research is to answer the following questions:

1. How does a typical mailing list subscriber communicate with other subscribers?
2. What are the invariant characteristics of a discussion thread on the mailing list?
3. What are the suitable graph models (simple, weighted - directed, hypergraph) for the discussion threads and subscriber communication?
4. In light of answers to above questions, what kind of updates can be done to mailing list filters in order to remove spam messages for subscribers.
5. How can we model the **temporal behaviour of the authors** in the mailing list?

Further research objectives:

1. Formulation of a proper algorithm for the **identification of popular authors** in a given mailing list.
2. **Degree distribution** of the nodes and authors in the mailing list.
3. **Mean path length analysis**
4. **Community detection**: Identification of the various communities of authors in the mailing list and assigning proper labels for these communities.
5. Stability and growth of an egocentric neighbourhood.
6. Identification of a pattern that leads to changes in marked observers across generations in a thread.
 
We shall use Linux Kernel Mailing List (LKML) as the base case to form suitable hypothesis. After the hypotheses are formulated, we shall validate the hypotheses on other open mailing lists. This research can be divided into data collection, the analysis of threads and the author-centric analysis.

============================
A List of Research Questions
============================

1. Why do mailing list subscribers put people in to CC, BCC instead of To?
2. What is the Dunbar number (Refer: `Dunbar's_number <https://en.wikipedia.org/wiki/Dunbar's_number>`_) on LKML?
3. What are the primary labels for each of the subscribers of the LKML?
4. Is there a correlation between the number of authors and the length of a thread (either in time or the number of messages)?
5. Each user can be thought of as a peer or a server. Servers arrive or depart with a high churn rate. A peer posts a question (ticket) and waits for service while the ticket is serviced by a server or sometimes self-serviced. If this is the case, what is the churn rate or diurnal activity and the message arrival and servicing characterization?
6. Is there a correlation between the number of marked people in a node and the height of node? Does this relationship depend on the length of the entire thread? 