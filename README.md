# Arctic-AI
A locally run chatbot using Arctic texts for Retrieval Augmented Generation (RAG)

The app was copied from the excellent [pixelgami](https://github.com/pixegami) tutorial found here: https://github.com/pixegami/rag-tutorial-v2 . Some revisions were made to accomodate `langchain` updates and experiment with chunking and prompt engineering, a different embedding model was used ([nomic-embed-text](https://ollama.com/library/nomic-embed-text)), and a different LLM was used ([phi3:medium](https://ollama.com/library/phi3)). Deprecation warnings were silenced.

In the various branches, I have added data about Arctic Climate from various sources including SNAP's [Northern Climate Reports](https://northernclimatereports.org/).

### Setup:
- Download `ollama` from [here](https://ollama.com/download) and install on your machine.
- Pull the embedding model and LLM. This is approximately 9GB download.
```
ollama pull nomic-embed-text
ollama pull phi3:medium
```
- Start the `ollama` server
```
ollama serve
```
- Build a conda environment from the `requirements.txt`
```
conda create --name rag --file requirements.txt
```
- You might need to install more packages as you run the code.

### Build the `chroma` vector database
- Put your data files in the `/data` folder, and run `python populate_database.py`. 
- Data format can be PDF, Markdown, JSON, HTML, etc. Check out the different branches in this repo to see the changes required in `populate_database.py` when using different file types, and explore what the loading and chunking process looks like for the different file types in `explore_loading_<filetype>.ipynb` notebooks. The `main` branch uses PDFs. 

### Query the LLM
- Run `python query_data.py` plus a string query to ask a question. You will recieve a response, along with the full prompt to the LLM including the top 5 text chunks that make up the RAG component of the query, and a list of explicit references for each of those chunks. The references include the file name, the page number, and the chunk on that page. The prompt can be removed from the response by commenting out the `print(prompt)` line in `query_data.py`.

```
python query_data.py "How fast is the Arctic warming?"

Human: 
Answer the question based only on the following context:

termed Arctic Amplification. Recent studies have shown that, after accounting for natural variability, the 
Arctic is warming approximately three times faster than the global mean based on observational data 
and climate model simulations since 1980 (Sweeney et al. 2023; Zhou et al. 2024). There are many 
documented physical indicators of a warming Arctic. Recent decades have witnessed springtime snow 
cover declines on Arctic lands (see essay Terrestrial Snow Cover),  summer sea ice losses (see essay Sea 
Ice), and Greenland Ice Sheet mass loss (see essay Greenland Ice Sheet). Extreme events are also 
becoming more frequent (Overland 2024) and their character is changing over time (e.g., Arctic cold

---

extremes are warming at twice the rate as pan-Arctic annual temperatures since 1979; Polyakov et al. 
2024). The warming Arctic has palpable ecological impacts at various spatial scales, which have been

---

NOAA Technical Report OAR ARC ; 24-01 Arctic Report Card 2024 
2 
2024 Headlines 
The rapid pace and complexity of Arctic change demand new and strengthened 
Arctic adaptation and global reductions of fossil fuel pollution 
The Arctic continues to warm at a faster rate than the global average. The 2024 Arctic Report Card 
highlights record-breaking and near-record-breaking observations that demonstrate dramatic change, 
including Arctic tundra transformation from carbon sink to carbon source, declines of previously large 
inland caribou herds, and increasing winter precipitation. Observations also reveal regional differences 
that make local and regional experiences of environmental change highly variable for people, plants and

---

temperatures in the Arctic did not climb to record levels in 2024, yet a long-term warming trend is clear 
and most Arctic Ocean marginal seas were ~2-4°C (3.6-7.2°F) warmer in August 2024 than the 1991-
2020 baseline. One more example from the marine environment is overall high primary productivity, 
including sharp increases in some seas during the 2003-24 observational record. 
Framing the Arctic as in a “new regime” underscores that the region today is dramatically changed from 
even a decade or two ago, yet it must not imply that the Arctic climate has stabilized under human-
caused warming. Projections of climate change for the next several decades are clear: change will 
continue. Every year the Arctic Report Card includes observations that bring sometimes surprising and

---

animals. Adaptation is increasingly necessary and Indigenous Knowledge and community-led research 
programs are essential to understand and respond to rapid Arctic changes. 
Headlines 
In the air 
• Arctic annual surface air temperatures ranked second warmest since 1900.
• Autumn 2023 and summer 2024 were especially warm across the Arctic with temperatures 
ranking 2nd and 3rd warmest, respectively.
• An early August 2024 heatwave set all-time record daily temperatures in several northern 
Alaska and Canada communities.
• The last nine years are the nine warmest on record in the Arctic.
• Summer 2024 across the Arctic was the wettest on record.
• Arctic precipitation has shown an increasing trend from 1950 through 2024, with the most 
pronounced
 increases occurring in winter.

---

Answer the question based on the above context: How fast is the Arctic warming?

Response: The Arctic is warming approximately three times faster than the global mean since 1980, as per observational data and climate model simulations.
Sources: ['data/ArcticReportCard_full_report2024.pdf:9:3', 'data/ArcticReportCard_full_report2024.pdf:9:4', 'data/ArcticReportCard_full_report2024.pdf:3:0', 'data/ArcticReportCard_full_report2024.pdf:6:1', 'data/ArcticReportCard_full_report2024.pdf:3:1']
```

### Test the output

- Run `pytest test_rag.py -W ignore::DeprecationWarning` to run the unit tests. 
- These tests consist of a sample question and expected output. We actually use the LLM again to compare the application's response to our expected output, since the wording might not be exactly the same. This has potential uses for complex answers that are not explicit numerical values.
- The tests also include a negative and positive version of each unit test. This is to ensure that the LLM is not being too generous in comparing the responses.