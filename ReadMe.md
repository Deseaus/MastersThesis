# Computer-Assisted Translation at the Service of Translators: A Unified Methodology

### Abstract

This thesis identifies shortcomings with how Computer-Assisted Translation (CAT) tools are developed. Their final use as an aid to translators is often not fully considered and left to others to evaluate. A unified methodology is proposed which allows a CAT tool to be evaluated intrinsically and extrinsically using methods that show the tool’s effect on the whole translation process. Special emphasis is placed on prototyping as a resource-effective way to create tools and gain critical feedback before a full implementation. To evaluate the methodology’s usefulness, StyleCheck is developed and evaluated using it. StyleCheck is a tool implemented in Grammatical Framework. It detects when a style guide rule is applied and gives a hint to the translator when it isn’t. The use of methods developed in Translation Process Research generates a wealth of data that gives detailed insights into how a tool performs. Results show StyleCheck is effective at getting a style guide to be applied, more than translating from scratch or post-editing, although more work on the user interface is required. The methodology is proven to be good at coming up with CAT tool improvements, quickly protoyping them and evaluating them.

### Repository structure

* `results/` contains the result data and Jupyter notebooks where it is analysed.
* `paper/` contains the Latex source for the thesis.
* `server/` contains the code for the web app where the experiments were carried out.
* `StyleCheck/` contains the GF grammar for StyleCheck.
