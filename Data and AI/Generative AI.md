MCP Model Context Protocol

- Provides AI ability to perform actions and access real time data
- Standardized interface for AI agents to connect to your existing data via APIs, querying databases, or performing computations. MCP servers expose [tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#tool) that can be invoked by models.

RAG gives AI knowledge, MCP gives AI capabilities. They're complementary, not competing approaches.

Use RAG When:
You need to search large knowledge bases
Information is relatively static (documentation, policies, historical data)
You want semantic similarity matching
Context fits in the prompt window

Use MCP When:
You need real-time/live data
AI needs to take actions and do stuff
Information requires authentication/permissions
Data is too large for prompt injection
You need interactive workflows
Practical Examples


Agentic AI Security
https://martinfowler.com/articles/agentic-ai-security.html

AI Enabled cyber attacks
https://www.anthropic.com/news/disrupting-AI-espionage

MCP Poisoning
https://research.checkpoint.com/2025/cursor-vulnerability-mcpoison/

https://blog.checkpoint.com/research/cursor-ide-persistent-code-execution-via-mcp-trust-bypass/

Securing AI Agents with a Standalone MCP Server
https://docs.paloaltonetworks.com/ai-runtime-security/release-notes/features-introduced/ai-runtime-security-api-intercept?otp=concept-p11_21z_wgc#concept-p11_21z_wgc
prompt injection detection, 
sensitive data detection, 
URL categorization - URLs related to entertainment, social networking, file sharing, shopping, gambling, or education may each belong to distinct categories

AI agents for offensive security testing
https://blog.checkpoint.com/executive-insights/hexstrike-ai-when-llms-meet-zero-day-exploitation/

Understanding MCP security
https://kiro.dev/docs/mcp/security/#understanding-mcp-security

Github MCP server
https://github.blog/ai-and-ml/generative-ai/a-practical-guide-on-how-to-use-the-github-mcp-server/

LLM Guardrails
https://medium.com/deloitte-artificial-intelligence-data-tech-blog/nemo-guardrails-a-comprehensive-guide-on-how-to-get-started-with-nemo-guardrails-695b0fb5fc4f
