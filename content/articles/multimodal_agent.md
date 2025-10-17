Title: Exploring Multi-Modal AI Agents: My Journey with the GAIA Benchmark
Date: 2025-08-12 13:49
Category: ai
Tags: ai
Slug: exploring-multi-modal-ai-agents
Authors: me
Summary: Building a multi-modal AI agent that performs well on the GAIA benchmark.
PreviewImage: images/blog/gaia.png

As artificial intelligence evolves, the potential for agents to tackle complex, real-world tasks autonomously is becoming increasingly tangible. In this post, I reflect on my experience with the [AI Agent course on Hugging Face](https://huggingface.co/learn/agents-course/en/unit0/introduction) and the process of building an agent for the GAIA benchmark—a challenge that highlights both the promise and the limitations of current AI systems.

## The Hugging Face AI Agent Course and the Challenge

The Hugging Face AI Agent course provided a foundation for understanding how to build, train, and deploy AI agents. The final assignment was to develop an agent capable of achieving at least 30% success rate on 20 level 1 questions from the GAIA benchmark.

After completing the course, I continued to experiment and improve the agent, eventually reaching a **54.55% success rate on the entire validation set** across all difficulty levels—including the challenging Level 3 questions. These results, while encouraging, also reveal the stochastic nature of the agent: sometimes it succeeds, sometimes it fails on the same task, reflecting the probabilistic decision-making inherent in current AI models.

## What is the GAIA Benchmark?

The General AI Assistant (GAIA) benchmark is a comprehensive evaluation framework designed to test AI agents' abilities across a wide range of tasks and modalities. What makes GAIA particularly challenging is its focus on:

1. **Multi-modal Understanding**: Questions involve processing different types of data including text, images, audio, video, and structured data.
2. **Progressive Difficulty Levels**:  
   - **Level 1**: Basic information extraction and simple reasoning
   - **Level 2**: More complex reasoning and understanding
   - **Level 3**: Advanced reasoning requiring multiple steps and cross-modal understanding

The benchmark evaluates exact match accuracy, making it particularly unforgiving - an agent's answer must precisely match the expected response to be considered correct.

## The Architecture of My Agent

My agent is built on a ReAct (Reasoning + Acting) architecture, which allows it to break down complex problems into manageable steps through a cycle of thought, action, and observation.

### Core Components

1. **Base Model**: The agent leverages OpenAI's o3 model for its reasoning capabilities.
2. **Tool Integration**: One of the agent's key strengths is its rich toolset that allows it to process various data types.
3. **Structured Response Format**: The agent follows a strict protocol for reasoning and answering questions, ensuring clarity and precision.

### The Agent's Toolbox

What makes my agent particularly powerful is the comprehensive set of tools that I built:

**Media Processing Tools**:

- `analyze_audio`: Extracts and analyzes content from audio files
- `analyze_image`: Describes and extracts information from images
- `get_video_transcript`: Transcribes and analyzes video content

**Data Processing Tools**:

- `load_file_or_url`: Loads and parses files of various formats
- `unzip`: Extracts content from compressed files
- `calculator`: Performs mathematical calculations
- `convert_unit`: Handles unit conversions
- `run_python`: Executes Python code for complex calculations

**Web Interaction Tools**:

- `web_search_tool`: Searches the web for information
- Browser tools (`get_browser_tools`): Allow the agent to navigate and extract information from websites
- `semantic_tools`: Process and understand semantic content

**Specialized Tools**:

- `chess`: Analyzes chess positions and suggests moves

This diverse toolset allows the agent to tackle a wide variety of questions, from simple text-based queries to complex multi-modal challenges.

## Implementation Details

The agent follows a structured ReAct (Reasoning + Acting) protocol:

1. It first receives a question and any associated files.
2. It breaks down the problem using a "Thought" process.
3. It selects and uses appropriate tools with "Action".
4. It processes the tool output through "Observation".
5. This cycle repeats until the agent has enough information to provide a final answer.

A critical aspect of my implementation was ensuring that the agent adheres to strict answer formatting rules, as the GAIA benchmark evaluates exact matches:

- For numerical answers: plain digits without commas or units
- For string answers: concise responses without articles
- For lists: properly formatted comma-separated elements

## Results and Performance

The agent achieved solid results across all difficulty levels:

| Difficulty Level | Success Rate |
|------------------|--------------|
| Level 1          | 64.2%        |
| Level 2          | 53.5%        |
| Level 3          | 38.5%        |
| **Overall**      | **54.55%**   |

> **Note:** Running the agent on the training (validation) questions cost around $20 in API usage. Running it on the actual test set would cost significantly more, so it's important to consider the financial aspect when scaling up experiments.

## Challenges, Lessons, and Future Directions

Building this agent for the GAIA benchmark has been a valuable learning experience, revealing both the strengths and limitations of current AI systems. Some of the main challenges included:

You can find the full code and project details here: [ai-agent-gaia on GitHub](https://github.com/tartieret/ai-agent-gaia)

---

Ultimately, while the agent can autonomously tackle a wide range of tasks—sometimes with impressive results—its performance is not deterministic. The same question may yield different outcomes on different runs, underscoring both the strengths and the current limitations of AI reasoning. As AI agents continue to develop, their ability to operate autonomously and adapt to new challenges will only grow. However, it’s important to recognize that success is not guaranteed, and results can vary due to the stochastic nature of these systems. Structured reasoning, careful tool integration, and robust answer formatting remain essential for progress in this field.

One of the most important lessons is just how critical tools are to an agent's capabilities. While the underlying language model provides reasoning and generalization, it is the tools—whether for file parsing, web search, or even chess—that truly expand what the agent can accomplish. Adding new tools (like a chess engine) can dramatically improve the agent's reach, but it also increases the context the agent must manage. This can sometimes lead to the agent selecting the wrong tool for a given task, especially as the toolbox grows.

This observation suggests that, in the future, we may see agents that are more specialized, with a limited set of tools tailored to their domain. Specialization can help reduce context size and improve tool selection accuracy. While I haven't yet experimented with a swarm of agents—each focused on a specific set of tasks or tools—that would be a logical next step for scaling up capabilities while maintaining efficiency.

Ultimately, while the agent can autonomously tackle a wide range of tasks—sometimes with impressive results—its performance is not deterministic. The same question may yield different outcomes on different runs, underscoring both the strengths and the current limitations of AI reasoning. As AI agents continue to develop, their ability to operate autonomously and adapt to new challenges will only grow. However, it’s important to recognize that success is not guaranteed, and results can vary due to the stochastic nature of these systems. Structured reasoning, careful tool integration, and robust answer formatting remain essential for progress in this field.
