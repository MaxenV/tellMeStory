FROM ollama/ollama:0.5.7

ARG LLM_MODEL 
ENV LLM_MODEL ${LLM_MODEL}

EXPOSE 11434
RUN nohup bash -c "ollama serve &" && sleep 5 && ollama pull ${LLM_MODEL}
