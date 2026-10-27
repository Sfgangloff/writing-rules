# Structure of a paper

## Title and abstract

- The title states the thesis or the question plainly.
- **The abstract has no precise numbers and no technical details** (sizes, architecture names, internal test names). Its order is: the general question or motivation, how it is studied concretely, and the kind of results obtained.
- **Lead with the most interesting finding.** Controls and validation experiments come after it, as confirmation.
- Add a connecting sentence wherever the abstract jumps between two topics.
- A key term the reader cannot know gets at least a compressed definition.
- Check the venue's length limit.
- Read it as a first-time reader: is it understandable, and is it interesting?

## Introduction

- The introduction contains compressed versions of the ideas developed in the body, without large overlap. Detailed explanations belong in the body.
- Mention the key design choices (where the architecture comes from, why the setting was chosen), so that a skimming reviewer sees they are not arbitrary.
- Emphasize the interesting results over methodological details.
- **Contributions list:** an overview of each contribution, without technical enumeration and without internal names introduced later.
- **Roadmap:** keep each description short and concrete. Check that every section is listed and that each description matches the section's content.

## Sections

- Open each section by stating what it does overall, then describe its subsections. Check that the announced number of parts is right.
- Open with the purpose ("In this section we test the hypothesis that..."), not with what was left unexplained.
- In a section that develops a thesis, recall at the beginning of each subsection which part of the claim it develops.
- Avoid a long undivided part followed by two subsections, and avoid sections with a single subsection.
- Section titles describe the content specifically, and sibling titles share a tone.
- Paragraph headings are full phrases ("Why we chose 6×6 grids", not "Why 6×6.").
- Place definitions before the material that uses them, and state the problem before the solution. Do not give away the punchline in a preview paragraph.

## Related work and alternative views

- Explain what prior work does. Do not differentiate aggressively from work that the reader already knows is different.
- Do not present prior work as what we should have done, or as having already done our study at a larger scale. Do not diminish our own contribution in the comparison.
- Do not blame named individuals or a field for something too recent to blame anyone for.
- Keep paragraph lengths balanced, and trim to the essential.

## Results

- Before commenting on a table or figure, say which experiment it reports, in the text and in the caption.
- Reference every table and figure in the text, and place the sentence that introduces a figure before the figure. A table reports; it does not "test" anything.
- Lead with the most surprising and least technical result. Do not present obvious results as findings.
- If a claim from the literature or from intuition is refuted, say so, so that the negative result keeps its value.
- Justify sample sizes and the other choices a reviewer will question.

## Limitations and conclusion

- Limitations stay high level.
- Unfinished experiments are TODOs, not limitations.
- Keep acknowledgements, AI usage statements and similar sections in the format the venue requires.

## Appendices

- **Each appendix covers one topic and is self-contained.** Restate the context and the result it expands on, with references to the sections, so that the reader does not have to re-read the main text ("In Section 4.2 we stated that ... We expand on this result here.").
- Be pedagogical: there is space to explain basics for readers who do not know the material. For a technical appendix, explain the issue again, then give a concrete example, then do the computation.
- Prefer one subsection with a paragraph per item to many tiny subsections.
- Cite every appendix from the main text. Remove sentences that become orphans when text moves to an appendix.
- With a single appendix, call it "the appendix", not "Appendix A".

## Page limits

To reach a page limit: remove repetition, trim what is superficial, compress formulations, and move expository material that is not needed to follow the paper into coherent appendices. Do not touch the results unless asked. Never lose information when compressing.
