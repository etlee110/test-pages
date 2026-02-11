You are an AI System Architect. I am building a "A Personal Website" project that uses a Terminal-based Copilot to orchestrate a data pipeline.

In the website, I want to build a system that wakes up, fetches real-time arXiv paper feed  using the arXiv API and fetches the most recent papers in the field of Aritificial Intelligence, generates a summary report of the latest papers, and deploys a live dashboard to GitHub Pages—all without writing manual code. Use the deploy from a branch feature. 

You need to design a comprehensive plan for this project, including:

Only generate the agents in .github/agents/ directory, skills in .github/skills/ directory, and prompts in .github/prompts/ directory. No additional code.
Design the agents and their interactions for the data pipeline.
Design the skills required for each agent to perform their tasks effectively.
Design the prompts that will guide the agents in executing their tasks.
Design general instrunctions for coding style and specific instructions for html
Add requirement to follow the format for copilot CLI: e.g., agent in the file name .agent.md, with the yaml front matter specifying the agent type, model, and tools used. Refer to official documentation in https://code.visualstudio.com/docs/copilot/customization/custom-agents

Ask me which github account and repository I want to deploy when planning