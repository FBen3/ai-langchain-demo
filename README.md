Proposed plan
  1. Write the loop by hand: about 30 lines of plain Python against Ollama, no LangChain.
  2. Rebuild it with LangChain’s `create_agent`, to see exactly what disappeared.
  3. Turn on LangSmith tracing and look at the run, compared with Langfuse.
  4. Open the hood with LangGraph: a tiny graph with state, and a human-approval pause.
  5. Deep Agents, which is honestly only about 10 lines once 1–4 make sense.
  6. A quick conceptual tour of Engine and Fleet.
