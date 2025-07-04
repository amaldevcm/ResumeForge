document.getElementById("generate").addEventListener("click", async () => {
  const jobDescription = document.getElementById("jobDescription").value.trim();
  const fileReader = new FileReader()
  const resumeUrl = './Amal_Resume.pdf';
  const resume = fileReader.readAsText(resumeUrl);
  console.log(resume)

  if (!jobDescription) {
    alert("Please paste a job description.");
    return;
  }

  document.getElementById("result").textContent = "Generating...";
  document.getElementById("download").disabled = true;  // lock download while working
  try {
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer <Your api key>"
      },
      body: JSON.stringify({
        model: "llama3-70b-8192",
        messages: [
          {
            role: "system",
            content: `
            You are a professional technical recruiter and career optimization expert. Your task is to:

1. Modify the provided resume **only where relevant** to make it better tailored to the job description (JD).
2. Maintain the **overall structure, tone, and format** of the original resume.
3. Ensure the result is **ATS-friendly**, with clear headings, bullet points, and no graphics.
4. Include a **tailored cover letter** specific to the job description and resume.
5. Output only a valid JSON string using the structure below. Do not include any other text, comments, or formatting outside the JSON block.
---

## RULES FOR THE OUTPUT:

- Output must be valid JSON with no trailing commas, quotation mismatches, or formatting errors.
- Do not include any explanation, header, or markdown formatting — just the JSON.

---

### RULES FOR THE RESUME:

- **Preserve the original structure** (sections, order, formatting).
- Modify or rephrase **only skills, work experience bullets, or project descriptions** to better align with the job description.
- Never invent experiences. Do not add new companies, job titles, or roles.
- Insert **missing relevant keywords** from the JD naturally into existing bullet points where contextually appropriate.
- Maintain **concise and quantifiable language** (use metrics if present).
- Resume must be **ATS-compatible** (no tables, no columns, no images, no unusual fonts).


---

### RULES FOR THE COVER LETTER:

- Start with a personalized greeting, then a compelling hook.
- Reference the **specific job title and company name**.
- Briefly summarize relevant experience, aligning with the JD.
- Highlight how your background fits the company’s mission or product.
- Express enthusiasm, and include a clear call to action.
- Keep tone **professional but warm**, max one page.

---

    ### OUTPUT FORMAT:

    {
        "custom_resume": "<Rewritten resume content here>",
        "custom_CV": "<Cover letter content here>",
    }
---
`
          },
          {
            role: "user",
            content: jobDescription
          }, {
            role: "user",
            content: resume
          }
        ]
      })
    });

    const data = await response.json();
    const generated = data.choices[0].message.content;

    // preview in the <pre> block
    document.getElementById("result").textContent = generated;

    // enable download
    document.getElementById("download").disabled = false;
  } catch (error) {
    console.error(error);
    document.getElementById("result").textContent = "Error generating resume.";
    document.getElementById("download").disabled = true;
  }
});

// document.getElementById("download").addEventListener("click", () => {
//   const content = document.getElementById("result").textContent;
//   const blob = new Blob([content], { type: "text/plain" });
//   const url = URL.createObjectURL(blob);

//   const a = document.createElement("a");
//   a.href = url;
//   a.download = "custom_resume.pdf";
//   a.click();

//   URL.revokeObjectURL(url);
// });
