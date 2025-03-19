Latex2Katex

Use this code to convert the contents of 'latex.txt' from Latex code to Katex code to be added to Gradescope solutions sections.

Requirements:
latex.txt - The text file which you will paste your latex code which you want to convert. It cannot currently fix \begin{align} ... \end{align} which are typically issues, but the goal is to have it work towards that.

Optional:
math.sty - If you include this file it can convert \newcommands{}{} back to the original format which Katex should understand. This file should be in the following format:
Each newcomand should be on a new line. Some examples:
\newcommand{\jv}{\mathbf{j}}
\newcommand{\kv}{\mathbf{k}}
\newcommand{\lv}{\mathbf{l}}
\newcommand{\mv}{\mathbf{m}}
If you do not have this file, it will just replace the common issues.