
# Why the Logic Evaluation Engine (LEE) Matters

*Symbolic Inference. Structural Transparency. Academic Usability.*

---

The Logic Evaluation Engine (LEE) is an open-source platform for symbolic inference, traceable evaluation, and structural modeling of logical expressions. It provides a compositional language and compact runtime for evaluating lambda applications, variable substitution, modal expressions, and memory-state logic, all with a focus on clarity, transparency, and pedagogical value.

LEE is not a theorem prover, SAT solver, or logic toy. It is a working core engine designed to visualize symbolic reasoning steps in a format accessible to both students and researchers. The engine enables detailed inspection of substitution chains, application order, state-dependent inference, and memory-layer logic across complex expressions. These evaluation steps are rendered in structural phases that capture interruption, memory carryover, and substitutional success or failure.

---

## Who It’s For

- *Philosophy of Logic / Philosophy of Language*: Explore intensionality, substitution, self-reference, and trace structure in formal reasoning.
- *CS and AI Research*: Use as a base for symbolic reasoning overlays, transparency tools for inference, or XAI integration.
- *Cognitive Science*: Visualize reasoning sequences, belief modeling, or structural inference in compact, inspectable form.
- *Educators*: Teach symbolic logic using walkable, trace-based output and compact, human-readable syntax.

---

## What It Enables

- **Trace-based Substitution Evaluation**: LEE supports symbolic tracing of lambda application and substitution, with memory-aware inference steps that produce clear, stepwise JSON and visual output.
- **Visual Exports for Teaching and Debugging**: The engine produces SVG/PNG diagrams and structured JSON manifests for every evaluation.
- **Composable Expression Syntax**: Expressions use a defined, symbolic syntax (EX, SUB, MEM, LAM, APP, EEX) to allow both formal rigor and user creativity.
- **Phase-sensitive Logic Evaluation**: Each inference step is assigned a structural phase (e.g., active, obstructed, retained, or deferred), allowing inspection of logic collapse and trace retention.
- **Open-Source Extensibility**: Designed in Python with a clean modular core, LEE is easy to fork, extend, or integrate into educational or experimental environments.

---

## What’s Next

LEE is actively maintained and now seeking:

- Collaborators or testers in philosophy, logic, AI, and cognitive modeling.
- University departments interested in using it for advanced coursework.
- Funding to support feature buildout (quantifiers, fixed-point logic, structured proof export).

---

## Explore the Project

GitHub: [github.com/KILGORETROUT111/logic-evaluation-engine](https://github.com/KILGORETROUT111/logic-evaluation-engine)  
Contact: dianoetic@tuta.com  
CC: kilgoretrout@berkeley.edu  
License: GNU GPLv3
