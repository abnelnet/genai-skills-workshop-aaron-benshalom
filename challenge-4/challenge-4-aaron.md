# Challenge Four — Agents with AI Applications (bonus)

Build the **Aurora Bay Agent**: a Conversational Agent in Google **AI Applications**, grounded on a
Data Store of the Aurora Bay documents. Built in the console

## Steps (console)
1. Console -> **AI Applications**.
2. Create a **Conversational Agent** app named **`Aurora Bay Agent`** in **us-central1**.
3. Open the **Default Playbook** and paste the **Goal** and **Instructions** below.
4. Create a **Data Store** on **`gs://labs.roitraining.com/aurora-bay-faqs`** (the 50 `faq-*.txt`
   docs — unstructured text) and attach it to the playbook.
5. **Test**: ask covered questions (mayor, library hours, industries) and confirm answers come from
   the data store; ask something out of scope and confirm it declines instead of guessing.

## Playbook — Goal (paste verbatim)
```
Help citizens of Aurora Bay, Alaska get accurate answers to frequently asked questions about the
town and its services, using only the connected Aurora Bay FAQ data store.
```

## Playbook — Instructions (paste verbatim)
```
- Greet the user briefly and ask how you can help with Aurora Bay services.
- Answer questions using ONLY information retrieved from the Aurora Bay FAQ data store.
- If the data store does not contain the answer, say you don't have that information and suggest
  contacting the Aurora Bay Town Hall. Do not guess or invent facts.
- Keep answers concise and factual. Quote specifics (hours, locations, names) when available.
- Stay on the topic of Aurora Bay town information; politely decline unrelated requests.
```

## Notes
- The data store ingests the unstructured `.txt` FAQs; the `.csv` in the same folder is the
  structured source used in Challenge 2.
- Grounding is the graded behavior: confirm it answers from the data and declines gracefully when
  the answer isn't present.
