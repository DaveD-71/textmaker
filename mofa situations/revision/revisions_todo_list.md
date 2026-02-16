# Revisions To-Do List

Source: `mofa situations/checks/revisions_checklist.txt`

|ID|Role|Area|Severity|Action Item|Action Taken (Who / When / Notes)|
|---|---|---|---|---|---|
|H01|Human|Roleplay 1 Translation|Minor|English mentions "consulate" but also says the visitor arrived at the "embassy"; Japanese uses "embassy" only, so the institution type is inconsistent.||
|H01|AI|Roleplay 1 Model vs Task|Minor|Model gives bathroom directions but does not provide any additional information, which the prompt allows for.||
|H02|AI|Roleplay 1 Model vs Task|Minor|Model uses "tomorrow" instead of the specified arrival on Saturday.||
|H02|AI|Writing Task Model vs Task|Minor|Model does not explicitly mention the recent phone conversation.||
|H03|AI|Roleplay 1 Model vs Task|Major|Model makes a reservation but never mentions the visitor’s seafood allergy.||
|H04|Human|Roleplay 1 Translation|Minor|Japanese omits the location (New York consulate) present in English.||
|H05|Human|Purpose Objectives Translation|Minor|English is slightly awkward: "incorrect statement amount"; meaning still clear.||
|H06|Human|Roleplay 1 Translation|Minor|Japanese has a typo ("伝えてださい" missing く), but meaning is clear.||
|H06|AI|Roleplay 1 Model vs Task|Major|Colleague asks where the office is; model does not provide directions.||
|H08|Human|Roleplay 1 Translation|Minor|Japanese omits "from Japan" and "on business" details.||
|H08|AI|Roleplay 1 Model vs Task|Minor|Prompt asks about her free time; model shifts to asking what the visitor can do on the weekend.||
|G01|AI|Roleplay 1 Model vs Task|Major|Prompt says boss returns the day after tomorrow; model says he returns tomorrow.||
|G01|AI|Writing Task Model vs Task|Minor|Model does not state when the call was received.||
|G03|AI|Writing Task Model vs Task|Minor|Model does not include a specific event name.||
|G05|Human|Purpose Objectives Translation|Minor|Japanese adds an extra parenthetical elaboration not present in English; scope slightly expanded.||
|G05|AI|Writing Task Model vs Task|Minor|Model provides a route but no alternative route as requested.||
|G07|AI|Roleplay 1 Model vs Task|Minor|Model does not really discuss options; it decides to call the visitor and reschedule.||
|G08|AI|Roleplay 1 Model vs Task|Minor|Model does not ask about plans for next year.||
|F03|Human|Roleplay 1 Translation|Minor|Japanese adds "by phone or in writing"; English specifies only calling.||
|F05|AI|Roleplay 1 Model vs Task|Minor|Model does not explicitly mention submitting additional visa documents beyond the form (aside from passport).||
|F06|Human|Roleplay 1 Translation|Minor|Japanese omits the location (Sydney embassy) present in English.||
|F08|Human|Purpose Objectives Translation|Major|English line appears truncated (ends with "sol"), so content is incomplete vs Japanese.||
|F08|AI|Writing Task Model vs Task|Minor|Model does not briefly outline the options discussed during the meeting.||
|E01|Human|Roleplay 2 Translation|Minor|Japanese adds "next year" (来年) while English does not specify the year.||
|E07|Human|Roleplay 1 Translation|Minor|Japanese adds that Candidate 1 has a strong interest in Japan; not stated in English.||
|E07|Human|Roleplay 2 Translation|Minor|Japanese adds that the second candidate loves Japanese anime; English says fan of Japanese culture only.||
|D02|Human|Purpose Objectives Translation|Minor|Japanese "事件性の高い問題" suggests more serious incidents than English "incidental issues".||
|D02|Human|Writing Task Translation|Minor|Japanese adds that the meeting is scheduled for "tomorrow morning" (明朝), which is not specified in English.||
|D02|AI|Roleplay 1 Model vs Task|Minor|Model does not ask about required procedures.||
|D03|Human|Purpose Objectives Translation|Major|English line appears truncated (ends with "by c"), so content is incomplete vs Japanese.||
|D03|Human|Writing Task Translation|Minor|Japanese omits the specific location ("New York’s airport") and generalizes to "arrival airport."||
|D03|AI|Roleplay 1 Model vs Task|Minor|Model does not describe the missing suitcase’s color/size/features.||
|D04|AI|Roleplay 1 Model vs Task|Major|Model does not secure a reduced-cost business seat; it resolves via points instead.||
|D04|Human|Instruction Verbosity|Minor|Roleplay 1 and Roleplay 2 prompts are each 100 words with weak purpose/objective alignment (0.093, 0.091).||
|D06|AI|Writing Task Model vs Task|Minor|Model gives reasons but no concrete evidence as requested.||
|D07|AI|Writing Task Model vs Task|Minor|Model does not explicitly request written confirmation of the agreed-upon solution.||
|D08|Human|Roleplay 2 Translation|Major|Japanese line is truncated and missing the end of the prompt (taxi cost detail).||
|D08|Human|Writing Task Translation|Major|Japanese line is truncated and missing the end of the prompt.||
|D08|Human|Instruction Verbosity|Minor|Roleplay 1 (149 words) and Roleplay 2 (120 words) have very weak purpose/objective alignment (0.014, 0.026).||
|D10|AI|Roleplay 1 Model vs Task|Major|Prompt requires reaffirming your hotel choice; model accepts counterpart’s choice instead.||
|C01|AI|Roleplay 1 Model vs Task|Major|Prompt specifies key events on Day 2; model places the meeting and dinner on the arrival day.||
|C01|AI|Writing Task Model Format|Minor|Email-style model is missing a subject line.||
|C03|Human|Purpose Objectives Translation|Major|English line appears truncated (ends with "taking i"), so content is incomplete vs Japanese.||
|C04|Human|Roleplay 1 Translation|Major|Japanese line is truncated and missing the final sentence about wanting to use the hotel again.||
|C05|Human|Roleplay 1 Translation|Major|Japanese line is truncated and missing the remainder of the prompt.||
|C05|Human|Roleplay 2 Translation|Major|Japanese line is truncated and missing the remainder of the prompt.||
|C05|Human|Instruction Verbosity|Minor|Roleplay 1 (101 words) and Roleplay 2 (107 words) have weak purpose/objective alignment (0.042, 0.043).||
|C06|Human|Instruction Verbosity|Minor|Roleplay 1 (122 words) and Roleplay 2 (117 words) have weak purpose/objective alignment (0.019, 0.067).||
|C07|AI|Roleplay 1 Model vs Task|Minor|Model does not ask directly about fit with office colleagues.||
|C08|AI|Roleplay 1 Model vs Task|Minor|Model does not clearly assert that the product was undamaged when shipped or push for a resolution.||
|C08|Human|Instruction Verbosity|Minor|Roleplay 1 prompt is 113 words with weak purpose/objective alignment (0.043).||
|C09|Human|Instruction Verbosity|Minor|Roleplay 2 prompt is 105 words with very weak purpose/objective alignment (0.000).||
